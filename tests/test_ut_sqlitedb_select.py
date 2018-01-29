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

"""test_ut_sqlite3db_select.py: Test selecting content from sqlite."""

import mock
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbSelect(object):
    """Testing selecting content from sqlite."""

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    @mock.patch.object(Config, 'search_all_kws', ('foo', 'bar', 'digitalocean'))
    def test_select_keyword_matching_links_column(self, mock_cause_push):
        """Test selecting content."""

        sqlite = Sqlite3Db()
        sqlite.init()

        ## Brief: Select content with regexp stored into sqlite. In this
        ##        case th last keyword matches to links column.
        content = Snippet.get_content(snippet=Snippet.FORCED)
        keywords = ['foo', 'bar', 'digitalocean']
        sqlite.insert_content(content, content.get_digest(), content.get_metadata())
        mock_cause_push.reset_mock()
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[0], content)
        assert len(sqlite.select_content(Const.SNIPPET, keywords)) == 1
        mock_cause_push.assert_not_called()
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
