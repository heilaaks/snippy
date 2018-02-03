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

"""test_ut_sqlite3db_delete.py: Test deleting content from sqlite."""

import mock

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbDelete(object):
    """Testing deleting snippets from sqlite."""

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    @mock.patch.object(Config, 'search_all_kws', ('foo', 'engine', 'digitalocean'))
    def test_delete_snippet_short_digest(self, mock_cause_push):
        """Delete snippet with short digest."""

        sqlite = Sqlite3Db()
        sqlite.init()

        ## Brief: Delete snippets with short version from digest.
        content1 = Snippet.get_content(snippet=Snippet.REMOVE)
        content2 = Snippet.get_content(snippet=Snippet.FORCED)
        keywords = ['foo', 'engine', 'digitalocean']
        sqlite.insert_content(content1, content1.get_digest(), content1.get_metadata())
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        sqlite.insert_content(content2, content2.get_digest(), content2.get_metadata())
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[1], content2)
        assert len(Database.select_all_snippets()) == 2
        sqlite.delete_content('53908d68425c61dc')
        mock_cause_push.assert_called_once_with('204 No Content', 'content deleted successfully')
        mock_cause_push.reset_mock()
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        assert len(Database.select_all_snippets()) == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    @mock.patch.object(Config, 'search_all_kws', ('foo', 'engine', 'digitalocean'))
    def test_delete_snippet_long_digest(self, mock_cause_push):
        """Delete snippet with long digest."""

        sqlite = Sqlite3Db()
        sqlite.init()

        ## Brief: Delete snippets with long version from digest.
        content1 = Snippet.get_content(snippet=Snippet.REMOVE)
        content2 = Snippet.get_content(snippet=Snippet.FORCED)
        keywords = ['foo', 'engine', 'digitalocean']
        sqlite.insert_content(content1, content1.get_digest(), content1.get_metadata())
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        sqlite.insert_content(content2, content2.get_digest(), content2.get_metadata())
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[1], content2)
        assert len(Database.select_all_snippets()) == 2
        sqlite.delete_content('53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5')
        mock_cause_push.assert_called_once_with('204 No Content', 'content deleted successfully')
        mock_cause_push.reset_mock()
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        assert len(Database.select_all_snippets()) == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
