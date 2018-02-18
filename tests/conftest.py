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


@pytest.fixture(scope='function', name='snippy')
def snippy_defaults(mocker):
    """Add default snippets for testing purposes."""

    mocker.patch.object(Config, '_storage_file', return_value=Database.get_storage())
    snippy = Snippy()
    mocker.patch('snippy.migrate.migrate.os.path.isfile', return_value=True)
    mocker.patch.object(Config, 'get_utc_time', side_effect=Snippet.ADD_DEFAULTS)

    contents = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
    for idx, content in enumerate(contents, start=1):
        mocked_open = mocker.mock_open(read_data=Snippet.get_template(content))
        mocker.patch('snippy.migrate.migrate.open', mocked_open, create=True)
        cause = snippy.run_cli(['snippy', 'import', '-f', 'one-snippet.txt'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == idx

    return snippy

@pytest.fixture(scope='function')
def server(mocker):
    """Run mocker server for testing purposes."""

    mocker.patch('snippy.server.server.SnippyServer')
