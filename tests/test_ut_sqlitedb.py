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

from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestUtSqlitedb(object):
    """Test Sqlitedb() class."""

    def test_sqlitedb_intesert002(self, sqlitedb):
        """Test SqliteDb basic insert.

        Insert one Snippet resource into the database.
        """

        collection = Snippet.get_collection(snippet=Snippet.REMOVE)
        sqlitedb.insert(collection)
        assert collection == Database.get_snippets()
        assert Database.get_snippets().size() == 1

    def test_sqlitedb_insert_002(self, sqlitedb):
        """Test SqliteDb basic insert.

        Insert four Snippet resources into the database.
        """

        collection = Snippet.get_collection(snippet=Snippet.REMOVE)
        collection.migrate(Snippet.get_collection(snippet=Snippet.FORCED))
        collection.migrate(Snippet.get_collection(snippet=Snippet.EXITED))
        collection.migrate(Snippet.get_collection(snippet=Snippet.NETCAT))
        sqlitedb.insert(collection)
        assert collection == Database.get_snippets()
        assert Database.get_snippets().size() == 4
