# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""conftest: Fixtures for pytest."""

from __future__ import print_function

import copy
import json
import re
import time
import traceback
import uuid
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

import docker
import mock
import pytest
import yaml

try:
    import http.client as httplib
except ImportError:
    import httplib

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.config.source.editor import Editor
from snippy.logger import Logger as SnippyLogger
from snippy.storage.database import Database as SnippyDb
from snippy.snip import Snippy
from tests.lib.helper import Helper
from tests.lib.reference import Reference
from tests.lib.snippet import Snippet
from tests.lib.solution import Solution
from tests.lib.todo import Todo
from tests.lib.database import Database

# Calls to Config.utcnow()
# =======================
#
# Content creation:
#
#   1) Create collection from given input.
#
# Content updating:
#
#   1) Create collection from given input.
#   2) Update 'updated' timestamp.
#
# Content importing from file:
#
#   1) Create collection from given input. Same timestamp
#      is used for all created resources.
#
# Content importing (=update) based on digest:
#
#   1) Create collection from given input.
#   2) Update 'updated' timestamp.
#
# Content editing:
#
#   1) Create resource from configured content.
#
# Content exporting:
#
#   1) Creating metadata with export timestamp.

# Content
EXPORT_TIME = Helper.EXPORT_TIME
IMPORT_TIME = Helper.IMPORT_TIME

# Snippets
IMPORT_SNIPPETS = Snippet.DEFAULT_TIME
REMOVE_CREATED = Snippet.REMOVE_CREATED
FORCED_CREATED = Snippet.FORCED_CREATED
EXITED_CREATED = Snippet.EXITED_CREATED
NETCAT_CREATED = Snippet.NETCAT_CREATED
UMOUNT_CREATED = Snippet.UMOUNT_CREATED
INTERP_CREATED = Snippet.INTERP_CREATED
CREATE_REMOVE = (REMOVE_CREATED,)*1
CREATE_FORCED = (FORCED_CREATED,)*1
CREATE_EXITED = (EXITED_CREATED,)*1
CREATE_NETCAT = (NETCAT_CREATED,)*1
CREATE_UMOUNT = (UMOUNT_CREATED,)*1
CREATE_INTERP = (INTERP_CREATED,)*1
IMPORT_REMOVE = (REMOVE_CREATED,)*1
IMPORT_FORCED = (FORCED_CREATED,)*1
IMPORT_EXITED = (EXITED_CREATED,)*1
IMPORT_NETCAT = (NETCAT_CREATED,)*1
IMPORT_UMOUNT = (UMOUNT_CREATED,)*1
IMPORT_INTERP = (INTERP_CREATED,)*1
UPDATE_REMOVE = (REMOVE_CREATED,)*2
UPDATE_FORCED = (FORCED_CREATED,)*2
UPDATE_EXITED = (EXITED_CREATED,)*2
UPDATE_NETCAT = (NETCAT_CREATED,)*2
EDITED_REMOVE = (REMOVE_CREATED,)*1

# Solutions
IMPORT_SOLUTIONS = Solution.DEFAULT_TIME
BEATS_CREATED = Solution.BEATS_CREATED
NGINX_CREATED = Solution.NGINX_CREATED
KAFKA_CREATED = Solution.KAFKA_CREATED
KAFKA_MKDN_CREATED = Solution.KAFKA_MKDN_CREATED
KAFKA_MKDN_UPDATED = Solution.KAFKA_MKDN_UPDATED
CREATE_BEATS = (BEATS_CREATED,)*1
CREATE_NGINX = (NGINX_CREATED,)*1
CREATE_KAFKA = (KAFKA_CREATED,)*1
CREATE_KAFKA_MKDN = (KAFKA_MKDN_CREATED,)*1
IMPORT_BEATS = (BEATS_CREATED,)*1
IMPORT_NGINX = (NGINX_CREATED,)*1
IMPORT_KAFKA = (KAFKA_CREATED,)*1
IMPORT_KAFKA_MKDN = (KAFKA_MKDN_CREATED,)*1
EDITED_BEATS = (BEATS_CREATED,)*1
UPDATE_BEATS = (BEATS_CREATED,)*2
UPDATE_NGINX = (NGINX_CREATED,)*2
UPDATE_KAFKA = (KAFKA_CREATED,)*2
UPDATE_KAFKA_MKDN = (KAFKA_MKDN_UPDATED,)*2

# References
IMPORT_REFERENCES = Reference.DEFAULT_TIME
GITLOG_CREATED = Reference.GITLOG_CREATED
REGEXP_CREATED = Reference.REGEXP_CREATED
PYTEST_CREATED = Reference.PYTEST_CREATED
CREATE_GITLOG = (GITLOG_CREATED,)*1
CREATE_REGEXP = (REGEXP_CREATED,)*1
CREATE_PYTEST = (PYTEST_CREATED,)*1
IMPORT_GITLOG = (GITLOG_CREATED,)*1
IMPORT_REGEXP = (REGEXP_CREATED,)*1
IMPORT_PYTEST = (PYTEST_CREATED,)*1
EDITED_GITLOG = (GITLOG_CREATED,)*1
UPDATE_GITLOG = (GITLOG_CREATED,)*2
UPDATE_REGEXP = (REGEXP_CREATED,)*2
UPDATE_PYTEST = (PYTEST_CREATED,)*2

# Todos
CREATE_DEFMKD = (Todo.DEFMKD_CREATED,)*1
CREATE_DEPLOY = (Todo.DEPLOY_CREATED,)*1
UPDATE_DEPLOY = (Todo.DEPLOY_CREATED,)*2

# Templates
EXPORT_TEMPLATE = Helper.EXPORT_TEMPLATE

IMPORT_DEFAULT_SNIPPETS = ((REMOVE_CREATED,) + (FORCED_CREATED,))
IMPORT_DEFAULT_SOLUTIONS = ((BEATS_CREATED,) + (NGINX_CREATED,))
IMPORT_DEFAULT_REFERENCES = ((GITLOG_CREATED,) + (REGEXP_CREATED,))

# Originals
JSON_LOAD = json.load

# pylint: disable=too-many-lines

# Pytest hooks.
def pytest_addoption(parser):
    """Pytest hook to add command line options.

    This hook allows defining additional options for Snippy testing.

    Args:
        parser (obj): Pytest Parser() object.
    """

    parser.addoption(
        '--snippy-db',
        action='store',
        default=Database.DB_SQLITE,
        help='Test with database: {' + Database.DB_SQLITE + ' (default), ' + Database.DB_POSTGRESQL + ', ' + Database.DB_COCKROACHDB + '}'
    )

    parser.addoption(
        '--snippy-logs',
        action='store_true',
        default=False,
        help='Add full log level.'
    )

def pytest_sessionstart(session):
    """Pytest hook called when session is started.

    This hook is called before the Pytest report header hook is called
    and after the Pytest command line arguments have been parsed.

    Args:
        session (obj): Pytest Session() object.
    """

    database = session.config.getoption("--snippy-db")
    Database.set_database(database)
    Database.delete_all_contents()

def pytest_report_header(config):  # pylint: disable=unused-argument
    """Pytest hook to set report header.

    Args:
        config (obj): Pytest Config() object.
    """

    return 'database: {}{}{}'.format(Helper.COLOR_OK, Database.get_database(), Helper.COLOR_END)

# Snippy
@pytest.fixture(scope='function', name='snippy')
def mocked_snippy(mocker, request):
    """Create mocked instance from snippy."""

    params = []

    # If there are no command line arguments, it causes unnecessary help
    # text that pollutes test case debug prints. In order to prevent this,
    # the quiet parameter is used. This parameter is dynamic and therefore
    # it affects only in the first run. If a test cases runs additional
    # commands for the same Snippy object, the initial value for the quiet
    # option does not affect anymore.
    if hasattr(request, 'param'):
        params = request.param
    else:
        params.append('-q')
    params.insert(0, 'snippy')  # Add the tool name here to args list.

    # Mock predicatable UUIDs.
    _mock_uuids(mocker)

    database = request.config.getoption("--snippy-db")
    snippy = _create_snippy(mocker, request, params, database)
    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_all_contents()
        Database.delete_storage()
    request.addfinalizer(fin)

    return snippy

@pytest.fixture(scope='function', name='snippy_perf')
def mocked_snippy_perf(mocker, request):
    """Create mocked instance from snippy for performance testing.

    The uuid mock must not be used for performance testing because
    mocking all the UUIDs needed for variable length run is not
    feasible.

    The --help option must be included in order to initialize the
    Snippy object with correct database. The --help option makes
    the command line options valid which allows running the storage
    specific options successfully.
    """

    database = request.config.getoption("--snippy-db")
    snippy = _create_snippy(mocker, request, ['--help'], database)
    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_all_contents()
        Database.delete_storage()
    request.addfinalizer(fin)

    return snippy

@pytest.fixture(scope='function', name='server')
def server(mocker, request):
    """Run mocked server for testing purposes."""

    params = []
    if hasattr(request, 'param'):
        params = request.param
    else:
        params.extend(['server', '--server-host', 'localhost:8080', '--server-minify-json', '-q'])
    params.insert(0, 'snippy')  # Add the tool name args list as a first parameter.

    # Mock predicatable UUIDs.
    _mock_uuids(mocker)

    # Mock server so that real Snippy server is not started.
    mocker.patch('snippy.server.server.SnippyServer')
    database = request.config.getoption("--snippy-db")
    snippy = _create_snippy(mocker, request, params, database)
    snippy.run()

    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_all_contents()
        Database.delete_storage()
    request.addfinalizer(fin)

    return snippy

@pytest.fixture(scope='function', name='server_db')
def server_db(mocker, request):
    """Run mocked server and database for testing purposes."""

    params = []
    if hasattr(request, 'param'):
        params = request.param
    else:
        params.extend(['server', '--server-host', 'localhost:8080', '--server-minify-json', '-q'])
    params.insert(0, 'snippy')  # Add the tool name args list as a first parameter.

    # Mock predicatable UUIDs.
    _mock_uuids(mocker)

    # Mock server so that real Snippy server is not started.
    with mock.patch('snippy.server.server.SnippyServer'):
        database = request.config.getoption("--snippy-db")
        if database in (Database.DB_SQLITE, Database.DB_IN_MEMORY):
            patched = 'snippy.storage.database.sqlite3.connect'
        else:
            patched = 'snippy.storage.database.psycopg2.connect'

        with mock.patch(patched, create=True) as mock_db_connect:
            snippy = _create_snippy(mocker, request, params, database)
            snippy.run()

    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_storage()
    request.addfinalizer(fin)

    return (snippy, mock_db_connect)

@pytest.fixture(scope='function', name='process')
def server_process(request):
    """Run real server for testing purposes.

    This will deadlock if there are too many logs in stdout [1]. Because of
    this, it is not possible to use the ``--snippy-logs`` option here.

    [1] https://stackoverflow.com/q/375427
    """

    params = [
        'python',
        './runner',
        'server',
        '--server-host',
        '127.0.0.1:0',
        '--storage-type',
        'in-memory'
    ]
    if hasattr(request, 'param'):
        params = params + request.param

    # Clear the real database and run the real server.
    call(['make', 'clean-db'])
    process = Popen(params, stdout=PIPE, stderr=PIPE)
    http = _wait_process(process)
    def fin():
        """Clear the process at the end.

        Because test cases need to read proccess output from blocking stderr
        and stdout, the process may be already terminated in test case. There
        will be a ``No such process`` exception if process has been already
        terminated.
        """

        try:
            process.terminate()
            process.wait()
        except OSError:
            pass
    request.addfinalizer(fin)

    return (process, http)

def _wait_process(process):
    """Wait untill the server is up.

    The port where the server is running is read from the logs. This does not
    work if the queiet option ``-q`` was used. The reason to use a log print
    is to avoid using ``psutils`` package and operating system specific tests
    to find the port where a process is running.

    Note that reading the stdout removes the read logs. This means that the
    test case using a real process cannot the logs before and including the
    snippy server startup log 'snippy server running at ...'.

    Args:
        process (obj): Popen object for Snippy proces.
    """

    re_catch_server_port = re.compile(r'''
        .*snippy\sserver\srunning\sat[:]\s.*[:](?P<port>\d{4,5})  # Catch server port.
        ''', re.MULTILINE | re.VERBOSE)

    port = 0
    while True:
        process.stdout.flush()
        line = process.stdout.readline().decode('utf-8')
        match = re_catch_server_port.search(line)
        if match:
            port = match.group('port')
            break
        if not line:
            break

    result = 0
    conn = None
    while result != 200:
        try:
            conn = httplib.HTTPConnection('127.0.0.1', port=int(port))
            conn.request('GET', '/api/snippy/rest/hello')
            resp = conn.getresponse()
            result = resp.status
        except Exception:  # pylint: disable=broad-except
            conn.close()
            time.sleep(0.01)

    return conn

@pytest.fixture(scope='function', name='mock-server')
def server_mock(mocker):
    """Mock Snippy server for testing."""

    mocker.patch('snippy.server.server.SnippyServer')

@pytest.fixture(scope='function', name='used_database')
def used_database(request):
    """Get used database."""

    return request.config.getoption("--snippy-db")

@pytest.fixture(scope='function', name='docker')
def docker_server(request):
    """Control the server in docker."""

    try:
        client = docker.from_env()
    except docker.errors.APIError:
        print('docker test fixture create failed: {}'.format(traceback.format_exc()))

    def fin():
        """Clear the resources at the end."""

        try:
            for container in client.containers.list():
                if 'snippy' in str(container.image):
                    container.stop()
                    container.remove()
        except docker.errors.APIError:
            print('docker test fixture release failed: {}'.format(traceback.format_exc()))
    request.addfinalizer(fin)

    return client

@pytest.fixture(scope='function', name='healthcheck')
def mock_httplib(mocker):
    """Mock the healthcheck."""

    healthcheck = mocker.patch.object(httplib, 'HTTPConnection', return_value=MockHTTPConnection())

    return healthcheck

# Logging
@pytest.fixture(scope='function', name='logger')
def logger_wrapper(request):
    """Create logger."""

    # Previous test may have configured the logger and therefore
    # the logger must be always reset before test.
    SnippyLogger.reset()
    logger = SnippyLogger.get_logger('snippy.' + __name__)
    def fin():
        """Clear the resources at the end."""

        SnippyLogger.remove()
    request.addfinalizer(fin)

    return logger

# Database
@pytest.fixture(scope='function', name='database')
def database_mock(request, mocker):
    """Mock database for testing."""

    Config.init(['snippy', '-q'] + Database.get_cli_params())  # Prevent unnecessary CLI help output with quiet option.
    mocker.patch.object(Config, 'storage_file', Database.get_storage(), create=True)
    mocker.patch.object(Config, 'storage_schema', Database.get_schema(), create=True)

    database = SnippyDb()
    database.init()

    def fin():
        """Clear the resources at the end."""

        database.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()
    request.addfinalizer(fin)

    return database

# Cause
@pytest.fixture(scope='function', name='cause')
def cause_mock(mocker):
    """Mock cause for unit testing."""

    cause = mocker.patch.object(Cause, 'push')

    return cause

@pytest.fixture(scope='function', name='caller')
def caller_mock(mocker):
    """Mock _caller() used to mark code module and line in logs."""

    mocker.patch.object(Cause, '_caller', return_value='snippy.testing.testing:123')

## Content

@pytest.fixture(scope='function', name='import-content-utc')
def import_content_time_mock(mocker):
    """Mock timestamps to create generic content."""

    mocker.patch.object(Config, 'utcnow', side_effect=(IMPORT_TIME,))

## Snippets

@pytest.fixture(scope='function', name='default-snippets')
def import_default_snippets(mocker, snippy):
    """Import default snippets for testing purposes."""

    contents = [Snippet.REMOVE, Snippet.FORCED]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='default-snippets-utc')
def import_snippets_time_mock(mocker):
    """Mock timestamps to import default snippets."""

    mocker.patch.object(Config, 'utcnow', side_effect=(IMPORT_SNIPPETS,))

@pytest.fixture(scope='function', name='import-exited')
def import_exited_snippet(mocker, snippy):
    """Import 'exited' snippet for testing purposes."""

    contents = [Snippet.EXITED]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-remove')
def import_remove_snippet(mocker, snippy):
    """Import 'remove' snippet for testing purposes."""

    contents = [Snippet.REMOVE]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='create-remove-utc')
def create_remove_time_mock(mocker):
    """Mock timestamps to create 'remove' snippet."""

    mocker.patch.object(Config, 'utcnow', side_effect=CREATE_REMOVE)

@pytest.fixture(scope='function', name='update-remove-utc')
def update_remove_time_mock(mocker):
    """Mock timestamps to update 'remove' snippet."""

    mocker.patch.object(Config, 'utcnow', side_effect=UPDATE_REMOVE)

@pytest.fixture(scope='function', name='import-remove-utc')
def import_remove_time_mock(mocker):
    """Mock timestamps to import 'remove' snippet."""

    _add_utc_time(mocker, IMPORT_REMOVE)

@pytest.fixture(scope='function', name='edit-remove')
def edit_remove_snippet(mocker):
    """Edited 'remove' snippet."""

    template = _get_template(Snippet.REMOVE)
    mocker.patch.object(Editor, '_call_editor', return_value=template)
    mocker.patch.object(Config, 'utcnow', side_effect=EDITED_REMOVE)

@pytest.fixture(scope='function', name='edited_remove')
def edited_remove(mocker):
    """Mock edited remove snippet."""

    return _editor(mocker, EDITED_REMOVE)

@pytest.fixture(scope='function', name='import-forced')
def import_forced_snippet(mocker, snippy):
    """Import 'forced' snippet for testing purposes."""

    contents = [Snippet.FORCED]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='create-forced-utc')
def create_forced_time_mock(mocker):
    """Mock timestamps to create 'forced' snippet."""

    _add_utc_time(mocker, CREATE_FORCED)

@pytest.fixture(scope='function', name='update-forced-utc')
def update_forced_time_mock(mocker):
    """Mock timestamps to update 'forced' snippet."""

    _add_utc_time(mocker, UPDATE_FORCED)

@pytest.fixture(scope='function', name='update-three-forced-utc')
def update_forced_three_time_mock(mocker):
    """Mock timestamps to update 'forced' snippet three times."""

    updates = (
        ('2017-10-14T19:56:31.000001+00:00',)*2 +
        ('2017-11-14T19:56:31.000001+00:00',)*2 +
        ('2017-12-14T19:56:31.000001+00:00',)*2
    )
    _add_utc_time(mocker, updates)

@pytest.fixture(scope='function', name='import-forced-utc')
def import_forced_time_mock(mocker):
    """Mock timestamps to import 'forced' snippet."""

    _add_utc_time(mocker, IMPORT_FORCED)

@pytest.fixture(scope='function', name='create-exited-utc')
def create_exited_time_mock(mocker):
    """Mock timestamps to create 'exited' solution."""

    mocker.patch.object(Config, 'utcnow', side_effect=CREATE_EXITED)

@pytest.fixture(scope='function', name='update-exited-utc')
def update_exited_time_mock(mocker):
    """Mock timestamps to update 'exited' solution."""

    mocker.patch.object(Config, 'utcnow', side_effect=UPDATE_EXITED)

@pytest.fixture(scope='function', name='import-netcat')
def import_netcat_snippet(mocker, snippy):
    """Import 'netcat' snippet for testing purposes."""

    contents = [Snippet.NETCAT]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='netcat-utc')
def create_netcat_time_mock(mocker):
    """Mock timestamps to create 'netcat' snippet."""

    mocker.patch.object(Config, 'utcnow', side_effect=CREATE_NETCAT)

@pytest.fixture(scope='function', name='update-netcat-utc')
def update_netcat_time_mock(mocker):
    """Mock timestamps to update 'netcat' snippet."""

    mocker.patch.object(Config, 'utcnow', side_effect=UPDATE_NETCAT)

@pytest.fixture(scope='function', name='import-netcat-utc')
def import_netcat_time_mock(mocker):
    """Mock timestamps to import 'netcat' snippet."""

    _add_utc_time(mocker, IMPORT_NETCAT)

@pytest.fixture(scope='function', name='import-umount')
def import_umount_snippet(mocker, snippy):
    """Import 'umount' snippet for testing purposes."""

    contents = [Snippet.UMOUNT]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-interp')
def import_interp_snippet(mocker, snippy):
    """Import 'interp' snippet for testing purposes."""

    contents = [Snippet.INTERP]
    _import_resources(snippy, mocker, contents)

## Solutions

@pytest.fixture(scope='function', name='default-solutions')
def import_default_solutions(mocker, snippy):
    """Import default soutions for testing purposes."""

    contents = [Solution.BEATS, Solution.NGINX]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='default-solutions-utc')
def import_default_solutions_time(mocker):
    """Mock timestamps to import default solutions."""

    mocker.patch.object(Config, 'utcnow', side_effect=(IMPORT_SOLUTIONS,))

@pytest.fixture(scope='function', name='import-beats')
def import_beats_solution(mocker, snippy):
    """Import 'beats' solution for testing purposes."""

    contents = [Solution.BEATS]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-nginx')
def import_nginx_solution(mocker, snippy):
    """Import 'nginx' solution for testing purposes."""

    contents = [Solution.NGINX]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-kafka')
def import_kafka_solution(mocker, snippy):
    """Import 'kafka' solution for testing purposes."""

    contents = [Solution.KAFKA]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-kafka-mkdn')
def import_kafka_mkdn_solution(mocker, snippy):
    """Import 'kafka_mkdn' solution for testing purposes."""

    contents = [Solution.KAFKA_MKDN]
    _import_content_mkdn(snippy, mocker, contents, IMPORT_KAFKA_MKDN)

@pytest.fixture(scope='function', name='create-beats-utc')
def create_beats_time_mock(mocker):
    """Mock timestamps to create 'beats' solution."""

    _add_utc_time(mocker, CREATE_BEATS)

@pytest.fixture(scope='function', name='update-beats-utc')
def update_beats_time_mock(mocker):
    """Mock timestamps to update 'beats' solution."""

    _add_utc_time(mocker, UPDATE_BEATS)

@pytest.fixture(scope='function', name='import-beats-utc')
def import_beats_time_mock(mocker):
    """Mock timestamps to import 'beats' solution."""

    _add_utc_time(mocker, IMPORT_BEATS)

@pytest.fixture(scope='function', name='edit-beats')
def edit_beats_solution(mocker):
    """Edited 'beats' solution."""

    # Set another UUID to prevent collision with existing UUID.
    solution = copy.deepcopy(Solution.BEATS)
    solution['uuid'] = Database.UUID_EDIT
    template = _get_template(solution)
    mocker.patch.object(Editor, '_call_editor', return_value=template)
    _add_utc_time(mocker, EDITED_BEATS)

@pytest.fixture(scope='function', name='edited_beats')
def edited_beats(mocker):
    """Mock edited beats solution."""

    return _editor(mocker, EDITED_BEATS)

@pytest.fixture(scope='function', name='nginx-utc')
def create_nginx_time_mock(mocker):
    """Mock timestamps to create 'nginx' solution."""

    _add_utc_time(mocker, CREATE_NGINX)

@pytest.fixture(scope='function', name='update-nginx-utc')
def update_nginx_time_mock(mocker):
    """Mock timestamps to update 'nginx' solution."""

    _add_utc_time(mocker, UPDATE_NGINX)

@pytest.fixture(scope='function', name='import-nginx-utc')
def import_nginx_time_mock(mocker):
    """Mock timestamps to import 'nginx' solution."""

    _add_utc_time(mocker, IMPORT_NGINX)

@pytest.fixture(scope='function', name='create-kafka-utc')
def create_kafka_time_mock(mocker):
    """Mock timestamps to create 'kafka' solution."""

    _add_utc_time(mocker, CREATE_KAFKA)

@pytest.fixture(scope='function', name='import-kafka-utc')
def import_kafka_time_mock(mocker):
    """Mock timestamps to import 'kafka' solution."""

    _add_utc_time(mocker, IMPORT_KAFKA)

@pytest.fixture(scope='function', name='update-kafka-utc')
def update_kafka_time_mock(mocker):
    """Mock timestamps to update 'kafka' solution."""

    _add_utc_time(mocker, UPDATE_KAFKA)


@pytest.fixture(scope='function', name='update-three-kafka-utc')
def update_kafka_three_time_mock(mocker):
    """Mock timestamps to update 'kafka' solution."""

    updates = (
        ('2017-10-20T06:16:27.000001+00:00',)*2 +
        ('2017-11-20T06:16:27.000001+00:00',)*2 +
        ('2017-12-20T06:16:27.000001+00:00',)*2
    )
    _add_utc_time(mocker, updates)

@pytest.fixture(scope='function', name='update-kafka-mkdn-utc')
def update_kafka_mkdn_time_mock(mocker):
    """Mock timestamps to update 'kafka-mkdn' solution."""

    _add_utc_time(mocker, UPDATE_KAFKA_MKDN)

@pytest.fixture(scope='function', name='import-kafka-mkdn-utc')
def import_kafka_mkdn_time_mock(mocker):
    """Mock timestamps to import 'kafka_mkdn' solution."""

    _add_utc_time(mocker, IMPORT_KAFKA_MKDN)

@pytest.fixture(scope='function', name='create-kafka-mkdn-utc')
def create_kafka_mkdn_time_mock(mocker):
    """Mock timestamps to create 'kafka_mkdn' solution."""

    _add_utc_time(mocker, CREATE_KAFKA_MKDN)

## References

@pytest.fixture(scope='function', name='default-references')
def import_default_references(mocker, snippy):
    """Import default references for testing purposes."""

    contents = [Reference.GITLOG, Reference.REGEXP]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='default-references-utc')
def import_default_references_time(mocker):
    """Mock timestamps to create and import default references."""

    mocker.patch.object(Config, 'utcnow', side_effect=(IMPORT_REFERENCES,))

@pytest.fixture(scope='function', name='create-gitlog-utc')
def create_gitlog_time_mock(mocker):
    """Mock timestamps to create 'gitlog' reference."""

    _add_utc_time(mocker, CREATE_GITLOG)

@pytest.fixture(scope='function', name='import-gitlog')
def import_gitlog_reference(mocker, snippy):
    """Import 'gitlog' reference for testing purposes."""

    contents = [Reference.GITLOG]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-gitlog-utc')
def import_gitlog_time_mock(mocker):
    """Mock timestamps to import 'gitlog' reference."""

    _add_utc_time(mocker, IMPORT_GITLOG)

@pytest.fixture(scope='function', name='update-gitlog-utc')
def update_gitlog_time_mock(mocker):
    """Mock timestamps to update 'gitlog' reference."""

    _add_utc_time(mocker, UPDATE_GITLOG)

@pytest.fixture(scope='function', name='update-three-gitlog-utc')
def update_gitlog_three_time_mock(mocker):
    """Mock timestamps to update 'gitlog' reference."""

    updates = (
        ('2018-06-22T13:11:13.678729+00:00',)*2 +
        ('2018-07-22T13:11:13.678729+00:00',)*2 +
        ('2018-08-22T13:11:13.678729+00:00',)*2
    )
    _add_utc_time(mocker, updates)

@pytest.fixture(scope='function', name='edited_gitlog')
def edited_gitlog(mocker):
    """Mock edited 'gitlog' referece."""

    return _editor(mocker, EDITED_GITLOG)

@pytest.fixture(scope='function', name='create-regexp-utc')
def create_regexp_time_mock(mocker):
    """Mock timestamps to create 'regexp' reference."""

    _add_utc_time(mocker, CREATE_REGEXP)

@pytest.fixture(scope='function', name='import-regexp')
def import_regexp_reference(mocker, snippy):
    """Import 'regexp' reference for testing purposes."""

    contents = [Reference.REGEXP]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='import-regexp-utc')
def import_regexp_time_mock(mocker):
    """Mock timestamps to import 'regexp' reference."""

    _add_utc_time(mocker, IMPORT_REGEXP)

@pytest.fixture(scope='function', name='update-regexp-utc')
def update_regexp_time_mock(mocker):
    """Mock timestamps to update 'regexp' reference."""

    _add_utc_time(mocker, UPDATE_REGEXP)

@pytest.fixture(scope='function', name='create-pytest-utc')
def create_pytest_time_mock(mocker):
    """Mock timestamps to create 'pytest' reference."""

    _add_utc_time(mocker, CREATE_PYTEST)

@pytest.fixture(scope='function', name='update-pytest-utc')
def update_pytest_time_mock(mocker):
    """Mock timestamps to update to 'pytest' reference."""

    _add_utc_time(mocker, UPDATE_PYTEST)

@pytest.fixture(scope='function', name='import-pytest')
def import_gitlog_solution(mocker, snippy):
    """Import 'pytest' reference for testing purposes."""

    contents = [Reference.PYTEST]
    _import_resources(snippy, mocker, contents)

## Todos

@pytest.fixture(scope='function', name='create-defmkd-utc')
def create_defmkd_time_mock(mocker):
    """Mock timestamps to create 'defmkd' todo."""

    mocker.patch.object(Config, 'utcnow', side_effect=CREATE_DEFMKD)

@pytest.fixture(scope='function', name='import-deploy')
def import_deploy_todo(mocker, snippy):
    """Import 'deploy' todo for testing purposes."""

    contents = [Todo.DEPLOY]
    _import_resources(snippy, mocker, contents)

@pytest.fixture(scope='function', name='create-deploy-utc')
def create_deploy_time_mock(mocker):
    """Mock timestamps to create 'deploy' todo."""

    mocker.patch.object(Config, 'utcnow', side_effect=CREATE_DEPLOY)

@pytest.fixture(scope='function', name='update-deploy-utc')
def update_deploy_time_mock(mocker):
    """Mock timestamps to update 'deploy' todo."""

    mocker.patch.object(Config, 'utcnow', side_effect=UPDATE_DEPLOY)

## Templates

@pytest.fixture(scope='function', name='template-utc')
def export_template_time_mock(mocker):
    """Mock timestamps to export solution template."""

    mocker.patch.object(Config, 'utcnow', side_effect=(EXPORT_TEMPLATE,)*2)

## Content

@pytest.fixture(scope='function', name='export-time')
def export_time_mock(mocker):
    """Mock timestamps to export any content."""

    _add_utc_time(mocker, (EXPORT_TIME,))

@pytest.fixture(scope='function', name='export-time-all-categories')
def export_time_all_categories_mock(mocker):
    """Mock timestamps to export all categories content."""

    _add_utc_time(mocker, (EXPORT_TIME, EXPORT_TIME, EXPORT_TIME))

## Templates

@pytest.fixture(scope='function', name='edit-snippet-template')
def edit_snippet_template(mocker):
    """Edited default snippet template."""

    template = Const.NEWLINE.join(Snippet.TEMPLATE)
    mocker.patch.object(Editor, '_call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-solution-template')
def edit_solution_template(mocker):
    """Edited default solution template."""

    template = Const.NEWLINE.join(Solution.TEMPLATE_TEXT)
    mocker.patch.object(Editor, '_call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-reference-template')
def edit_reference_template(mocker):
    """Edited default reference template."""

    template = Const.NEWLINE.join(Reference.TEMPLATE)
    mocker.patch.object(Editor, '_call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-empty')
def edit_empty_template(mocker):
    """Edited empty template."""

    mocker.patch.object(Editor, '_call_editor', return_value=Const.EMPTY)

@pytest.fixture(scope='function', name='edit-unknown-solution-template')
def edit_unidentified_template(mocker):
    """Edited unidentified template."""

    template = (
        '################################################################################',
        '## description',
        '################################################################################',
        '',
        '################################################################################',
        '## solutions',
        '################################################################################',
        '',
        '################################################################################',
        '## configurations',
        '################################################################################',
        '',
        '################################################################################',
        '## whiteboard',
        '################################################################################',
        ''
    )
    mocker.patch.object(Editor, '_call_editor', return_value=template)

## uuid

@pytest.fixture(scope='function', name='uuid')
def uuid_generate(mocker):
    """Mock generating uuid."""

    _mock_uuids(mocker)

## yaml

@pytest.fixture(scope='function', name='yaml')
def mock_yaml(mocker):
    """Mock yaml load and dump methods."""

    mocker.patch.object(yaml, 'safe_dump')
    mocker.patch.object(yaml, 'safe_load')

## json

@pytest.fixture(scope='function', name='json')
def mock_json(mocker):
    """Mock json load and dump methods."""

    mocker.patch.object(json, 'dump')
    mocker.patch.object(json, 'load')

## os.path

@pytest.fixture(scope='function', name='isfile_true')
def isfile_mock_true(mocker):
    """Mock os.path.isfile."""

    mocker.patch('snippy.content.migrate.os.path.isfile', return_value=True)

@pytest.fixture(scope='function', name='exists_true')
def exists_mock_true(mocker):
    """Mock os.path.exists."""

    mocker.patch('snippy.content.migrate.os.path.exists', return_value=True)

@pytest.fixture(scope='function', name='exists_false')
def exists_mock_false(mocker):
    """Mock os.path.exists."""

    mocker.patch('snippy.content.migrate.os.path.exists', return_value=False)

## os.access

@pytest.fixture(scope='function', name='access_true')
def access_mock_true(mocker):
    """Mock os.access."""

    mocker.patch('snippy.content.migrate.os.access', return_value=True)

@pytest.fixture(scope='function', name='access_false')
def access_mock_false(mocker):
    """Mock os.access."""

    mocker.patch('snippy.content.migrate.os.access', return_value=False)

## os.environ

@pytest.fixture(scope='function', name='osenviron')
def mock_os_environ(monkeypatch):
    """Mock os.environe."""

    return monkeypatch

## editor

@pytest.fixture(scope='function', name='editor_data')
def editor_data(mocker):
    """Mock editor object to allow mocking data from default editor."""

    return mocker.patch.object(Editor, '_call_editor')

## devel

@pytest.fixture(scope='function', name='devel_file_list')
def devel_file_list(mocker):
    """Mock devel package file list for tests."""

    tests = [
        'test_ut_arguments_create.py',
        'test_wf_console_help.py',
        'test_wf_export_snippet.py'
    ]
    mocker.patch('snippy.devel.reference.pkg_resources.resource_isdir', return_value=True)
    mocker.patch('snippy.devel.reference.pkg_resources.resource_listdir', return_value=tests)

@pytest.fixture(scope='function', name='devel_file_data')
def devel_file_data(mocker):
    """Mock devel package file reading for tests.

    This must mock all needed file reads because it is not possible to mock
    the 'builtins.open' only from one module.
    """

    testcase = (
        '#!/usr/bin/env python3',
        '',
        '"""test_wf_import_snippet.py: Test workflows for importing snippets."""',
        '',
        'import re',
        'import sys',
        'import copy',
        'import json',
        'import yaml',
        'import mock',
        'import pkg_resources',
        'from snippy.snip import Snippy',
        'from snippy.config.config import Config',
        'from snippy.constants import Constants as Const',
        'from snippy.cause import Cause',
        'from tests.lib.snippet import Snippet',
        'from tests.lib.database import Database',
        '',
        '',
        'class TestWfImportSnippet(object):',
        '    """Test workflows for importing snippets."""',
        '',
        '    @mock.patch.object(json, \'load\')',
        '    @mock.patch.object(yaml, \'safe_load\')',
        '    @mock.patch.object(Config, \'_storage_file\')',
        '    @mock.patch(\'snippy.content.migrate.os.path.isfile\')',
        '    def test_import_all_snippets(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):',
        '        """Import all snippets."""',
        '',
        '        mock_isfile.return_value = True',
        '        mock_storage_file.return_value = Database.get_storage()',
        '        import_dict = {\'content\': [Snippet.REMOVE, Snippet.NETCAT]}',
        '        mock_yaml_load.return_value = import_dict',
        '        mock_json_load.return_value = import_dict',
        '        compare_content = {\'54e41e9b52a02b63\': import_dict[\'data\'][0],',
        '                           \'f3fd167c64b6f97e\': import_dict[\'data\'][1]}',
        '',
        '        ## Brief: Import all snippets. File name is not defined in commmand line. This should',
        '        ##        result tool internal default file name ./snippets.yaml being used by default.',
        '        with mock.patch(\'snippy.content.migrate.io.open\', file_content) as mock_file:',
        '            snippy = Snippy()',
        '            cause = snippy.run([\'snippy\', \'import\', \'--filter\', \'.*(\\$\\s.*)\'])  ## workflow',
        '            assert cause == Cause.ALL_OK',
        '            assert len(Database.get_collection()) == 2',
        '            mock_file.assert_called_once_with(\'./snippets.yaml\', \'r\')',
        '            Snippet.test_content(snippy, mock_file, compare_content)',
        '            snippy.release()',
        '            snippy = None',
        '            Database.delete_storage()'
    )
    mocked = mocker.patch('snippy.devel.reference.io.open')  # This mocks all 'io.open' calls.
    handle = mocked.return_value.__enter__.return_value
    reads = [
        Const.NEWLINE.join(testcase),
        Const.NEWLINE.join(testcase),
        'dummy read 1',
        'dummy read 2',
        'dummy read 3',
        'dummy read 4',
        'dummy read 5',
        'dummy read 6',
        'dummy read 7',
        'dummy read 8',
        'dummy read 9',
        Database.get_schema_data()]
    handle.read.side_effect = lambda: reads.pop(0)

@pytest.fixture(scope='function', name='devel_no_tests')
def devel_no_tests(mocker):
    """Mock tests package missing exception."""

    tests = [
        'test_ut_arguments_create.py',
        'test_wf_console_help.py',
        'test_wf_export_snippet.py'
    ]
    # The exception in Python 3.6 is ModuleNotFoundError but this is not
    # available in earlier Python versions. The used ImportError is a parent
    # class of ModuleNotFoundError and it works with older Python versions.
    mocker.patch('snippy.devel.reference.pkg_resources.resource_isdir', side_effect=[ImportError("No module named 'tests'"), mocker.DEFAULT])
    mocker.patch('snippy.devel.reference.pkg_resources.resource_listdir', return_value=tests)
    file_content = mocker.mock_open(read_data=Const.EMPTY)
    mocker.patch('snippy.devel.reference.io.open', file_content)

## Helpers

def _get_template(dictionary):
    """Transform dictionary to text template."""

    collection = Collection()
    collection.load_dict('2018-10-20T06:16:27.000001+00:00', {'data': [dictionary]})

    return collection.dump_text(Config.templates)

def _get_template_mkdn(dictionary):
    """Transform dictionary to Markdown template."""

    collection = Collection()
    collection.load_dict('2018-10-20T06:16:27.000001+00:00', {'data': [dictionary]})

    return collection.dump_mkdn(Config.templates)

def _create_snippy(mocker, request, params, database):
    """Create snippy with mocks.

    Args:
        params (list): Command line arguments to start the Snippy.
        database (str): Database used with the tests.

    Returns:
        obj: Snippy object.
    """

    if request.config.getoption("--snippy-logs"):
        params.append('--debug')

    # Mock only objects from the Snippy package. If system calls like os.open
    # are mocked from here, it will mock all the third party packages that are
    # imported when the Snippy object is created. System calls must be mocked
    # after the Snippy object is in a such state that it can accept test case
    # input.
    mocker.patch.object(Config, '_storage_file', return_value=Database.get_storage())
    if database == Database.DB_POSTGRESQL:
        params = params + Database.get_cli_params()

    snippy = Snippy(params)

    return snippy

def _import_resources(snippy, mocker, resources):
    """Import resource.

    There is no need to mock Config.utcnow() because the imported resources
    always contain the ``created`` and ``updated`` timestamps. These values
    will always override the system clock.

    The Config.utcnow() is mocked away just to avoid calling ``utcnow``. The
    intention is just to avoid unncessary system calls during tests.

    The json.load is used by the import operation. Because of this, optional
    json.load mock must be temporary removed.
    """

    mock_load = json.load
    json.load = JSON_LOAD
    timestamp = '2000-01-01T01:01:01.000001+00:00'
    with mock.patch('snippy.content.migrate.os.path.isfile', return_value=True):
        for resource in resources:
            infile = mocker.mock_open(read_data=json.dumps({'data': [resource]}))
            with mock.patch('snippy.content.migrate.io.open', infile):
                with mock.patch.object(Config, 'utcnow', side_effect=(timestamp,)*20):
                    cause = snippy.run(['snippy', 'import', '--file', 'resource.json'])
                    assert cause == Cause.ALL_OK
    json.load = mock_load

def _import_content_mkdn(snippy, mocker, contents, timestamps):
    """Import requested Markdown content."""

    mocker.patch.object(Config, 'utcnow', side_effect=timestamps)
    start = len(Database.get_collection()) + 1
    with mock.patch('snippy.content.migrate.os.path.isfile', return_value=True):
        for idx, content in enumerate(contents, start=start):
            file_content = mocker.mock_open(read_data=_get_template_mkdn(content))
            with mock.patch('snippy.content.migrate.io.open', file_content):
                cause = snippy.run(['snippy', 'import', '-f', 'content.mkdn'])
                assert cause == Cause.ALL_OK
                assert len(Database.get_collection()) == idx

def _add_utc_time(mocker, timestamps):
    """Add UTC time mock as side effect."""

    side_effects = ()
    try:
        side_effects = Config.utcnow.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'utcnow', side_effect=tuple(side_effects) + timestamps)

def _editor(mocker, timestamp):
    """Mock editor."""

    editor = mocker.patch.object(Editor, '_call_editor')
    _add_utc_time(mocker, timestamp*2)

    return editor

def _mock_uuids(mocker):
    """Mock UUIDS."""

    mocker.patch.object(uuid, 'uuid1', side_effect=Database.TEST_UUIDS)
    mocker.patch.object(uuid, 'uuid4', side_effect=Database.TEST_UUIDS)


class MockHTTPConnection(httplib.HTTPConnection):
    """Mock for the httplib."""

    def __init__(self, *args, **kwargs): # pylint: disable=super-init-not-called, unused-argument
        self.status = 0

    def request(self, *args, **kwargs):  # pylint: disable=arguments-differ, unused-argument
        """Mock for httplib.request method."""

        return

    def getresponse(self, *args, **kwargs):  # pylint: disable=arguments-differ, unused-argument
        """Mock for httplib.getresponse."""

        self.status = 200

        return self

    def close(self, *args, **kwargs):  # pylint: disable=arguments-differ, unused-argument
        """Mock for httplib.close."""

        return
