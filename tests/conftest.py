#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

import pytest

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

# Snippet importing and get_utc_time():
#
#   1) Create empty content.
#   2) Comparing content against template calls implicitly empty content creation in Parser.
#   3) Comparing content against template calls implicitly empty content creation in Storage.
#
# Snippet creation and get_utc_time():
#
#   1) Creating empty content.
#
# Solution creation and get_utc_time():
#
#   1) Creating empty content.
#   2) Comparing against content template (create empty).
#   3) Comparing against content template (make timestamp).
#
# Snippet or solution exporting and get_utc_time():
#
#   1) Creating metadata with export timestamp.

# Snippets
REMOVE_CREATED = '2017-10-14 19:56:31'
FORCED_CREATED = '2017-10-14 19:56:31'
EXITED_CREATED = '2017-10-20 07:08:45'
NETCAT_CREATED = '2017-10-20 07:08:45'
CREATE_REMOVE = (REMOVE_CREATED,)*1
CREATE_FORCED = (FORCED_CREATED,)*1
CREATE_EXITED = (EXITED_CREATED,)*1
CREATE_NETCAT = (NETCAT_CREATED,)*1
IMPORT_REMOVE = (REMOVE_CREATED,)*3
IMPORT_FORCED = (FORCED_CREATED,)*3
IMPORT_EXITED = (EXITED_CREATED,)*3
IMPORT_NETCAT = (NETCAT_CREATED,)*3

# Solutions
BEATS_CREATED = '2017-10-20 11:11:19'
NGINX_CREATED = '2017-10-20 06:16:27'
KAFKA_CREATED = '2017-10-20 06:16:27'
CREATE_BEATS = (BEATS_CREATED,)*3
CREATE_NGINX = (NGINX_CREATED,)*3
CREATE_KAFKA = (KAFKA_CREATED,)*3
IMPORT_BEATS = (BEATS_CREATED,)*5
IMPORT_NGINX = (NGINX_CREATED,)*5
IMPORT_KAFKA = (KAFKA_CREATED,)*5

IMPORT_DEFAULT_SNIPPETS = (IMPORT_REMOVE + IMPORT_FORCED)
IMPORT_DEFAULT_SOLUTIONS = (IMPORT_BEATS + IMPORT_NGINX)

@pytest.fixture(scope='function', name='snippy')
def mocked_snippy(mocker, request):
    """Create mocked instance from snippy."""

    snippy = create_snippy(mocker)
    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_storage()
    request.addfinalizer(fin)

    return snippy

@pytest.fixture(scope='function', name='server')
def server(mocker):
    """Run mocked server for testing purposes."""

    mocker.patch('snippy.server.server.SnippyServer')

## Snippets

@pytest.fixture(scope='function', name='default-snippets')
def import_default_snippets(mocker, snippy):
    """Import default snippets for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
    import_content(snippy, mocker, contents, IMPORT_DEFAULT_SNIPPETS)

@pytest.fixture(scope='function', name='exited')
def import_exited_snippet(mocker, snippy):
    """Import 'exited' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.EXITED]]
    import_content(snippy, mocker, contents, IMPORT_EXITED)

@pytest.fixture(scope='function', name='remove')
def import_remove_snippet(mocker, snippy):
    """Import 'remove' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE]]
    import_content(snippy, mocker, contents, IMPORT_REMOVE)

@pytest.fixture(scope='function', name='forced')
def import_forced_snippet(mocker, snippy):
    """Import 'forced' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.FORCED]]
    import_content(snippy, mocker, contents, IMPORT_FORCED)

@pytest.fixture(scope='function', name='netcat')
def import_netcat_snippet(mocker, snippy):
    """Import 'netcat' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.NETCAT]]
    import_content(snippy, mocker, contents, IMPORT_NETCAT)

@pytest.fixture(scope='function', name='remove-utc')
def create_remove_snippet_time_mock(mocker):
    """Mock timestamps to create 'remove' snippet."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_REMOVE)

## Solutions

@pytest.fixture(scope='function', name='default-solutions')
def import_default_solutions(mocker, snippy):
    """Import default soutions for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.NGINX]]
    import_content(snippy, mocker, contents, IMPORT_DEFAULT_SOLUTIONS)

@pytest.fixture(scope='function', name='beats')
def import_beats_solution(mocker, snippy):
    """Import 'beats' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.BEATS]]
    import_content(snippy, mocker, contents, IMPORT_BEATS)

@pytest.fixture(scope='function', name='kafka')
def import_kafka_solution(mocker, snippy):
    """Import 'kafka' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.KAFKA]]
    import_content(snippy, mocker, contents, IMPORT_KAFKA)

@pytest.fixture(scope='function', name='beats-utc')
def create_beats_solution_time_mock(mocker):
    """Mock timestamps to create 'beats' solution."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_BEATS)

@pytest.fixture(scope='function', name='kafka-utc')
def create_kafka_solution_time_mock(mocker):
    """Mock timestamps to create 'kafka' solution."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_KAFKA)

@pytest.fixture(scope='function', name='beats-kafka-utc')
def create_beats_kafka_solution_time_mock(mocker):
    """Mock timestamps to create 'beats' and 'kafka' solutions."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_BEATS + CREATE_KAFKA)

## Helpers

def create_snippy(mocker):
    """Create snippy with mocks."""

    mocker.patch.object(Config, '_storage_file', return_value=Database.get_storage())
    mocker.patch('snippy.migrate.migrate.os.path.isfile', return_value=True)
    snippy = Snippy()

    return snippy

def import_content(snippy, mocker, contents, timestamps):
    """Import requested content."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=timestamps)
    start = len(Database.get_contents()) + 1
    for idx, content in enumerate(contents, start=start):
        mocked_open = mocker.mock_open(read_data=Snippet.get_template(content))
        mocker.patch('snippy.migrate.migrate.open', mocked_open, create=True)
        cause = snippy.run_cli(['snippy', 'import', '-f', 'content.txt'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_contents()) == idx
