#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

import json

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.config.source.editor import Editor
from snippy.snip import Snippy
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

# Calls to Config.utcnow()
# =======================
#
# Content creation:
#
#   1) Create resource from each configured content.
#
# Content updating:
#
#   1) Create resource from configured content.
#   2) Update 'updated' timestamp.
#
# Content importing from file:
#
#   1) Create resource from each configured content.
#
# Content importing (=update) based on digest:
#
#   1) Create resource from each configured content.
#   2) Update 'updated' timestamp.
#
# Content editing:
#
#   1) Create resource from configured content.
#
# Content exporting:
#
#   1) Creating metadata with export timestamp.

# Snippets
REMOVE_CREATED = '2017-10-14T19:56:31.000001+0000'
FORCED_CREATED = '2017-10-14T19:56:31.000001+0000'
EXITED_CREATED = '2017-10-20T07:08:45.000001+0000'
NETCAT_CREATED = '2017-10-20T07:08:45.000001+0000'
UMOUNT_CREATED = '2018-05-07T11:11:55.000001+0000'
CREATE_REMOVE = (REMOVE_CREATED,)*1
CREATE_FORCED = (FORCED_CREATED,)*1
CREATE_EXITED = (EXITED_CREATED,)*1
CREATE_NETCAT = (NETCAT_CREATED,)*1
CREATE_UMOUNT = (UMOUNT_CREATED,)*1
UPDATE_REMOVE = (REMOVE_CREATED,)*2
UPDATE_FORCED = (FORCED_CREATED,)*2
UPDATE_EXITED = (EXITED_CREATED,)*2
UPDATE_NETCAT = (NETCAT_CREATED,)*2
IMPORT_REMOVE = (REMOVE_CREATED,)*1
IMPORT_FORCED = (FORCED_CREATED,)*1
IMPORT_EXITED = (EXITED_CREATED,)*1
IMPORT_NETCAT = (NETCAT_CREATED,)*1
IMPORT_UMOUNT = (UMOUNT_CREATED,)*1
EDITED_REMOVE = (REMOVE_CREATED,)*1

# Solutions
BEATS_CREATED = '2017-10-20T11:11:19.000001+0000'
NGINX_CREATED = '2017-10-20T06:16:27.000001+0000'
KAFKA_CREATED = '2017-10-20T06:16:27.000001+0000'
CREATE_BEATS = (BEATS_CREATED,)*1
CREATE_NGINX = (NGINX_CREATED,)*1
CREATE_KAFKA = (KAFKA_CREATED,)*1
UPDATE_BEATS = (BEATS_CREATED,)*2
UPDATE_NGINX = (NGINX_CREATED,)*2
IMPORT_BEATS = (BEATS_CREATED,)*1
IMPORT_NGINX = (NGINX_CREATED,)*2
IMPORT_KAFKA = (KAFKA_CREATED,)*2
EDITED_BEATS = (BEATS_CREATED,)*1

# Templates
EXPORT_TEMPLATE = '2017-10-14T19:56:31.000001+0000'

# Export
EXPORT_TIME = '2018-02-02T02:02:02.000001+0000'

IMPORT_DEFAULT_SNIPPETS = ((REMOVE_CREATED,) + (FORCED_CREATED,))
IMPORT_DEFAULT_SOLUTIONS = ((BEATS_CREATED,) + (NGINX_CREATED,))
IMPORT_DEFAULT_REFERENCES = ((Content.GITLOG_TIME,) + (Content.REGEXP_TIME,))

# Snippy
@pytest.fixture(scope='function', name='snippy')
def mocked_snippy(mocker, request):
    """Create mocked instance from snippy."""

    params = []

    # If there are no parameters, the only parameter passed is the tool
    # name. This creates unnecessary help text that pollutes the debug
    # output. In order to prevent this, the quiet is set. The quiet
    # parameter is dynamic and therefore it does not affect if the test
    # cases decided for example run CLI without it to test tool output.
    if hasattr(request, 'param'):
        params = request.param
    else:
        params.append('-q')

    params.insert(0, 'snippy')  # Add the tool name here to args list.
    snippy = _create_snippy(mocker, params)
    def fin():
        """Clear the resources at the end."""

        snippy.release()
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
        params.extend(['--server', '--compact-json', '-q'])
    params.insert(0, 'snippy')  # Add the tool name args list as a first parameter.

    mocker.patch('snippy.server.server.SnippyServer')
    snippy = _create_snippy(mocker, params)
    snippy.run()

    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_storage()
    request.addfinalizer(fin)

    return snippy

@pytest.fixture(scope='function', name='mock-server')
def server_mock(mocker):
    """Mock Snippy server for testing purposes."""

    mocker.patch('snippy.server.server.SnippyServer')

# Logging
@pytest.fixture(scope='function', name='logger')
def logger_wrapper(request):
    """Create logger."""

    from snippy.logger import Logger

    # Previous test may have configured the logger and therefore
    # the logger must be always reset before test.
    Logger.reset()
    logger = Logger.get_logger('snippy.' + __name__)
    def fin():
        """Clear the resources at the end."""

        Logger.remove()
    request.addfinalizer(fin)

    return logger

@pytest.fixture(scope='function', name='caller')
def caller(mocker):
    """Mock _caller() used to mark code module and line in logs."""

    mocker.patch.object(Cause, '_caller', return_value='snippy.testing.testing:123')

## Snippets

@pytest.fixture(scope='function', name='default-snippets')
def import_default_snippets(mocker, snippy):
    """Import default snippets for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
    _import_content(snippy, mocker, contents, IMPORT_DEFAULT_SNIPPETS)

@pytest.fixture(scope='function', name='import-exited')
def import_exited_snippet(mocker, snippy):
    """Import 'exited' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.EXITED]]
    _import_content(snippy, mocker, contents, IMPORT_EXITED)

@pytest.fixture(scope='function', name='import-remove')
def import_remove_snippet(mocker, snippy):
    """Import 'remove' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE]]
    _import_content(snippy, mocker, contents, IMPORT_REMOVE)

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

    template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
    mocker.patch.object(Editor, 'call_editor', return_value=template)
    mocker.patch.object(Config, 'utcnow', side_effect=EDITED_REMOVE)

@pytest.fixture(scope='function', name='edited_remove')
def edited_remove(mocker):
    """Mock edited remove snippet."""

    return _editor(mocker, EDITED_REMOVE)

@pytest.fixture(scope='function', name='import-forced')
def import_forced_snippet(mocker, snippy):
    """Import 'forced' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.FORCED]]
    _import_content(snippy, mocker, contents, IMPORT_FORCED)

@pytest.fixture(scope='function', name='create-forced-utc')
def create_forced_time_mock(mocker):
    """Mock timestamps to create 'forced' snippet."""

    _add_utc_time(mocker, CREATE_FORCED)

@pytest.fixture(scope='function', name='update-forced-utc')
def update_forced_time_mock(mocker):
    """Mock timestamps to update 'forced' snippet."""

    _add_utc_time(mocker, UPDATE_FORCED)

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

    contents = [Snippet.DEFAULTS[Snippet.NETCAT]]
    _import_content(snippy, mocker, contents, IMPORT_NETCAT)

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

    contents = [Snippet.DEFAULTS[Snippet.UMOUNT]]
    _import_content(snippy, mocker, contents, IMPORT_UMOUNT)

## Solutions

@pytest.fixture(scope='function', name='default-solutions')
def import_default_solutions(mocker, snippy):
    """Import default soutions for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.NGINX]]
    _import_content(snippy, mocker, contents, IMPORT_DEFAULT_SOLUTIONS)

@pytest.fixture(scope='function', name='import-beats')
def import_beats_solution(mocker, snippy):
    """Import 'beats' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.BEATS]]
    _import_content(snippy, mocker, contents, IMPORT_BEATS)

@pytest.fixture(scope='function', name='import-nginx')
def import_nginx_solution(mocker, snippy):
    """Import 'nginx' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.NGINX]]
    _import_content(snippy, mocker, contents, IMPORT_NGINX)

@pytest.fixture(scope='function', name='import-kafka')
def import_kafka_solution(mocker, snippy):
    """Import 'kafka' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.KAFKA]]
    _import_content(snippy, mocker, contents, IMPORT_KAFKA)

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

    template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
    mocker.patch.object(Editor, 'call_editor', return_value=template)
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
    """Mock timestamps to create 'nginx' solution."""

    _add_utc_time(mocker, IMPORT_NGINX)

@pytest.fixture(scope='function', name='create-kafka-utc')
def create_kafka_time_mock(mocker):
    """Mock timestamps to create 'kafka' solution."""

    _add_utc_time(mocker, CREATE_KAFKA)

@pytest.fixture(scope='function', name='import-kafka-utc')
def import_kafka_time_mock(mocker):
    """Mock timestamps to create 'kafka' solution."""

    _add_utc_time(mocker, IMPORT_KAFKA)

## References
@pytest.fixture(scope='function', name='default-references')
def import_default_references(mocker, snippy):
    """Import default references for testing purposes."""

    contents = [Reference.DEFAULTS[Reference.GITLOG], Reference.DEFAULTS[Reference.REGEXP]]
    _import_content(snippy, mocker, contents, IMPORT_DEFAULT_REFERENCES)

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

## Templates

@pytest.fixture(scope='function', name='edit-snippet-template')
def edit_snippet_template(mocker):
    """Edited default snippet template."""

    template = Const.NEWLINE.join(Snippet.TEMPLATE)
    mocker.patch.object(Editor, 'call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-solution-template')
def edit_solution_template(mocker):
    """Edited default solution template."""

    template = Const.NEWLINE.join(Solution.TEMPLATE)
    mocker.patch.object(Editor, 'call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-reference-template')
def edit_reference_template(mocker):
    """Edited default reference template."""

    template = Const.NEWLINE.join(Reference.TEMPLATE)
    mocker.patch.object(Editor, 'call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-empty')
def edit_empty_template(mocker):
    """Edited empty template."""

    mocker.patch.object(Editor, 'call_editor', return_value=Const.EMPTY)

@pytest.fixture(scope='function', name='edit-unknown-template')
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
    mocker.patch.object(Editor, 'call_editor', return_value=template)

## Yaml

@pytest.fixture(scope='function', name='yaml_load')
def yaml_load(mocker):
    """Mock importing from yaml file."""

    mocker.patch.object(yaml, 'safe_load')
    mocker_open = mocker.patch('snippy.content.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

@pytest.fixture(scope='function', name='yaml_dump')
def yaml_dump(mocker):
    """Mock exporting to yaml file."""

    mocker.patch.object(yaml, 'safe_dump')
    mocker_open = mocker.patch('snippy.content.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

## Json

@pytest.fixture(scope='function', name='json_load')
def json_load(mocker):
    """Mock importing from json file."""

    mocker.patch.object(json, 'load')
    mocker_open = mocker.patch('snippy.content.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

@pytest.fixture(scope='function', name='json_dump')
def json_dump(mocker):
    """Mock exporting to json file."""

    mocker.patch.object(json, 'dump')
    mocker_open = mocker.patch('snippy.content.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

@pytest.fixture(scope='function', name='isfile_true')
def isfile_mock(mocker):
    """Mock os.path.isfile."""

    mocker.patch('snippy.content.migrate.os.path.isfile', return_value=True)

## Devel

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
    """Mock devel package file reading for tests."""

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
        'from tests.testlib.snippet_helper import SnippetHelper as Snippet',
        'from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database',
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
        '        import_dict = {\'content\': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.NETCAT]]}',
        '        mock_yaml_load.return_value = import_dict',
        '        mock_json_load.return_value = import_dict',
        '        compare_content = {\'54e41e9b52a02b63\': import_dict[\'data\'][0],',
        '                           \'f3fd167c64b6f97e\': import_dict[\'data\'][1]}',
        '',
        '        ## Brief: Import all snippets. File name is not defined in commmand line. This should',
        '        ##        result tool internal default file name ./snippets.yaml being used by default.',
        '        with mock.patch(\'snippy.content.migrate.open\', mock.mock_open(), create=True) as mock_file:',
        '            snippy = Snippy()',
        '            cause = snippy.run([\'snippy\', \'import\', \'--filter\', \'.*(\\$\\s.*)\'])  ## workflow',
        '            assert cause == Cause.ALL_OK',
        '            assert Database.get_collection().size() == 2',
        '            mock_file.assert_called_once_with(\'./snippets.yaml\', \'r\')',
        '            Snippet.test_content(snippy, mock_file, compare_content)',
        '            snippy.release()',
        '            snippy = None',
        '            Database.delete_storage()'
    )
    mocked_open = mocker.mock_open(read_data=Const.NEWLINE.join(testcase))
    mocker.patch('snippy.devel.reference.open', mocked_open, create=True)

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
    mocked_open = mocker.mock_open(read_data=Const.EMPTY)
    mocker.patch('snippy.devel.reference.open', mocked_open, create=True)

## Helpers

def _create_snippy(mocker, options):
    """Create snippy with mocks."""

    # Mock only objects from Snippy package. If system calls are mocked
    # here, it will mock all the third party packages that are imported
    # when the Snippy object is created. System calls like os.path.isfile
    # must be mocked after the Snippy object is in a such state that it
    # can accept test case input.
    mocker.patch.object(Config, '_storage_file', return_value=Database.get_storage())
    snippy = Snippy(options)

    return snippy

def _import_content(snippy, mocker, contents, timestamps):
    """Import requested content."""

    mocker.patch.object(Config, 'utcnow', side_effect=timestamps)
    start = Database.get_collection().size() + 1
    with mock.patch('snippy.content.migrate.os.path.isfile', return_value=True):
        for idx, content in enumerate(contents, start=start):
            mocked_open = mocker.mock_open(read_data=Snippet.get_template(content))
            mocker.patch('snippy.content.migrate.open', mocked_open, create=True)
            cause = snippy.run(['snippy', 'import', '-f', 'content.txt'])
            assert cause == Cause.ALL_OK
            assert Database.get_collection().size() == idx

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

    editor = mocker.patch.object(Editor, 'call_editor')
    _add_utc_time(mocker, timestamp*3)

    return editor
