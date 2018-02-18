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
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


REMOVE_CREATED = '2017-10-14 19:56:31'
FORCED_CREATED = '2017-10-14 19:56:31'
EXITED_CREATED = '2017-10-20 07:08:45'
NETCAT_CREATED = '2017-10-20 07:08:45'
CREATE_REMOVE = (REMOVE_CREATED,)*4
CREATE_FORCED = (FORCED_CREATED,)*4
CREATE_EXITED = (EXITED_CREATED,)*4
CREATE_NETCAT = (NETCAT_CREATED,)*4

BEATS_CREATED = '2017-10-20 11:11:19'
NGINX_CREATED = '2017-10-20 06:16:27'
KAFKA_CREATED = '2017-10-20 06:16:27'
CREATE_BEATS = (BEATS_CREATED,)*3
CREATE_NGINX = (NGINX_CREATED,)*3
CREATE_KAFKA = (KAFKA_CREATED,)*3

TEST_PYTHON2 = (None,)
ADD_DEFAULTS = (CREATE_REMOVE + CREATE_FORCED + TEST_PYTHON2)

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

@pytest.fixture(scope='function', name='defaults')
def add_default_snippets(mocker, snippy):
    """Add default snippets for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
    add_content(snippy, mocker, contents, ADD_DEFAULTS)

@pytest.fixture(scope='function', name='exited')
def add_exited_snippet(mocker, snippy):
    """Add 'exited' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.EXITED]]
    add_content(snippy, mocker, contents, CREATE_EXITED)

@pytest.fixture(scope='function', name='remove')
def add_remove_snippet(mocker, snippy):
    """Add 'remove' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE]]
    add_content(snippy, mocker, contents, CREATE_REMOVE)

@pytest.fixture(scope='function', name='remove_utc')
def add_remove_snippet_time_mock(mocker):
    """Add 'remove' snippet timestamp mock."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_REMOVE)

@pytest.fixture(scope='function', name='forced')
def add_forced_snippet(mocker, snippy):
    """Add 'forced' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.FORCED]]
    add_content(snippy, mocker, contents, CREATE_FORCED)

@pytest.fixture(scope='function', name='netcat')
def add_netcat_snippet(mocker, snippy):
    """Add 'netcat' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.NETCAT]]
    add_content(snippy, mocker, contents, CREATE_NETCAT)

## Solutions

@pytest.fixture(scope='function', name='beats_utc')
def add_beats_solution_time_mock(mocker):
    """Add 'beats' solution timestamp mock."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_BEATS)

## Helpers

def create_snippy(mocker):
    """Create snippy with mocks."""

    mocker.patch.object(Config, '_storage_file', return_value=Database.get_storage())
    mocker.patch('snippy.migrate.migrate.os.path.isfile', return_value=True)
    snippy = Snippy()

    return snippy

def add_content(snippy, mocker, contents, timestamps):
    """Add requested content."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=timestamps)
    start = len(Database.get_contents()) + 1
    for idx, content in enumerate(contents, start=start):
        mocked_open = mocker.mock_open(read_data=Snippet.get_template(content))
        mocker.patch('snippy.migrate.migrate.open', mocked_open, create=True)
        cause = snippy.run_cli(['snippy', 'import', '-f', 'content.txt'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_contents()) == idx
