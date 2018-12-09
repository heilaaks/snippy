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

"""test_ut_sqlitedb: Test Sqlitedb() class."""

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet import Snippet
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestUtSqlitedb(object):
    """Test Sqlitedb() class."""

    def test_sqlitedb_insert_001(self, sqlitedb, cause):
        """Test SqliteDb basic insert.

        Insert one Snippet resource into the database.
        """

        collection = Content.get_collection(Snippet.REMOVE)
        sqlitedb.insert(collection)
        cause.assert_called_once_with('201 Created', 'content created')
        assert collection == Database.get_snippets()
        assert len(Database.get_snippets()) == 1

    def test_sqlitedb_insert_002(self, sqlitedb, cause):
        """Test SqliteDb basic insert.

        Insert four Snippet resources into the database. This verifies with
        multiple items in tag and link lists.
        """

        collection = Content.get_collection(Snippet.REMOVE)
        collection.migrate(Content.get_collection(Snippet.FORCED))
        collection.migrate(Content.get_collection(Snippet.EXITED))
        collection.migrate(Content.get_collection(Snippet.NETCAT))
        sqlitedb.insert(collection)
        cause.assert_called_once_with('201 Created', 'content created')
        assert collection == Database.get_snippets()
        assert len(Database.get_snippets()) == 4

    def test_sqlitedb_select_001(self, sqlitedb, cause):
        """Test SqliteDb basic select.

        Select content with regexp stored into sqlite. In this case the last
        keyword matches to links column.
        """

        collection = Content.get_collection(Snippet.FORCED)
        collection.migrate(Content.get_collection(Snippet.EXITED))
        collection.migrate(Content.get_collection(Snippet.NETCAT))
        sqlitedb.insert(collection)
        collection = sqlitedb.select(scat=(Const.SNIPPET,), sall=('foo', 'bar', 'digitalocean'))
        cause.assert_called_once_with('201 Created', 'content created')
        assert collection == Content.get_collection(Snippet.FORCED)

    def test_sqlitedb_delete_002(self, sqlitedb, cause, mocker):
        """Test SqliteDb basic delete.

        Delete one row from database with short digest.
        """

        collection = Content.get_collection(Snippet.REMOVE)
        collection.migrate(Content.get_collection(Snippet.FORCED))
        sqlitedb.insert(collection)
        sqlitedb.delete('53908d68425c61dc')
        results = []
        results.append(mocker.call('201 Created', 'content created'))
        results.append(mocker.call('204 No Content', 'content deleted successfully'))
        cause.assert_has_calls(results)
        assert Database.get_snippets() == Content.get_collection(Snippet.REMOVE)
        assert len(Database.get_snippets()) == 1

    def test_sqlitedb_delete_001(self, sqlitedb, cause, mocker):
        """Test SqliteDb basic delete.

        Delete one row from database with long digest.
        """

        collection = Content.get_collection(Snippet.REMOVE)
        collection.migrate(Content.get_collection(Snippet.FORCED))
        sqlitedb.insert(collection)
        sqlitedb.delete('53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5')
        results = []
        results.append(mocker.call('201 Created', 'content created'))
        results.append(mocker.call('204 No Content', 'content deleted successfully'))
        cause.assert_has_calls(results)
        assert Database.get_snippets() == Content.get_collection(Snippet.REMOVE)
        assert len(Database.get_snippets()) == 1
