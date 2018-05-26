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

from snippy.cause import Cause
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
        """Delete snippet with short digest.

        Delete snippets with short version from digest.
        """

        sqlite = Sqlite3Db()
        sqlite.init()

        collection1 = Snippet.get_collection(snippet=Snippet.REMOVE)
        collection2 = Snippet.get_collection(snippet=Snippet.FORCED)
        keywords = ['foo', 'engine', 'digitalocean']
        sqlite.insert(collection1)
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        sqlite.insert(collection2)
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        collection1.migrate(collection2)
        assert collection1 == sqlite.select(Const.SNIPPET, sall=keywords)
        assert Database.get_snippets().size() == 2
        sqlite.delete('53908d68425c61dc')
        mock_cause_push.assert_called_once_with('204 No Content', 'content deleted successfully')
        mock_cause_push.reset_mock()
        assert collection2 == sqlite.select(Const.SNIPPET, sall=keywords)
        assert Database.get_snippets().size() == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    @mock.patch.object(Config, 'search_all_kws', ('foo', 'engine', 'digitalocean'))
    def test_delete_snippet_long_digest(self, mock_cause_push):
        """Delete snippet with long digest.

        Delete snippets with long version from digest.
        """

        sqlite = Sqlite3Db()
        sqlite.init()

        collection1 = Snippet.get_collection(snippet=Snippet.REMOVE)
        collection2 = Snippet.get_collection(snippet=Snippet.FORCED)
        keywords = ['foo', 'engine', 'digitalocean']
        sqlite.insert(collection1)
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        sqlite.insert(collection2)
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        collection1.migrate(collection2)
        assert collection1 == sqlite.select(Const.SNIPPET, sall=keywords)
        assert Database.get_snippets().size() == 2
        sqlite.delete('53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5')
        mock_cause_push.assert_called_once_with('204 No Content', 'content deleted successfully')
        mock_cause_push.reset_mock()
        assert collection2 == sqlite.select(Const.SNIPPET, sall=keywords)
        assert Database.get_snippets().size() == 1
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
