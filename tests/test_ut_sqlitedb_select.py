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

"""test_ut_sqlitedb_select.py: Test selecting content from sqlite."""

import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.storage.sqlitedb import SqliteDb
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestUtSqlitedbSelect(object):
    """Testing selecting content from sqlite."""

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    @mock.patch.object(Config, 'search_all_kws', ('foo', 'bar', 'digitalocean'))
    def test_select_keyword_matching_links_column(self, mock_cause_push):
        """Test selecting content.

        Select content with regexp stored into sqlite. In this case th last
        keyword matches to links column.
        """

        sqlite = SqliteDb()
        sqlite.init()

        collection = Snippet.get_collection(snippet=Snippet.FORCED)
        keywords = ['foo', 'bar', 'digitalocean']
        sqlite.insert(collection)
        mock_cause_push.reset_mock()
        assert collection == sqlite.select(Const.SNIPPET, sall=keywords)
        assert Database.get_snippets().size() == 1
        mock_cause_push.assert_not_called()
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    @classmethod
    def setup_class(cls):
        """Setup the test class."""

        Config.init(None)

    @classmethod
    def teardown_class(cls):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
