#!/usr/bin/env python3

"""test_sqlite3_db_delete_snippet_basic.py: Test deleting snippets from the sqlite3 database."""

import unittest
import mock
from snippy.config import Constants as Const
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper

class TestSqlite3DbDeleteSnippetBasic(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Testing deleting snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_delete_snippet_with_short_digest(self, mock_get_storage_schema, mock_is_storage_in_memory, mock_is_search_all):
        """Two snippes are added and one of them is deleted leaving only one snippet
        after the test. Deleting is made with short version from snippet digest"""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        mock_is_search_all.return_value = True
        snippet1 = Sqlite3DbHelper.SNIPPET1
        digest1 = Sqlite3DbHelper.DIGEST1
        snippet2 = Sqlite3DbHelper.SNIPPET2
        digest2 = Sqlite3DbHelper.DIGEST2
        metadata = 'metadata'
        keywords = ['help', 'docker']
        db_rows = [(snippet1[Const.SNIPPET_CONTENT], snippet1[Const.SNIPPET_BRIEF], snippet1[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet1[Const.SNIPPET_LINKS][0], digest1, metadata, 1),
                   (snippet2[Const.SNIPPET_CONTENT], snippet2[Const.SNIPPET_BRIEF], snippet2[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet2[Const.SNIPPET_LINKS][0], digest2, metadata, 2)]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet1, digest1, metadata)
        obj.insert_snippet(snippet2, digest2, metadata)
        snippet_db = obj.select_snippets(keywords)
        self.assertEqual(snippet_db[0][Const.SNIPPET_CONTENT], db_rows[0][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[0][Const.SNIPPET_BRIEF], db_rows[0][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[0][Const.SNIPPET_GROUP], db_rows[0][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[0][Const.SNIPPET_TAGS], db_rows[0][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[0][Const.SNIPPET_LINKS], db_rows[0][Const.SNIPPET_LINKS])
        self.assertEqual(snippet_db[1][Const.SNIPPET_CONTENT], db_rows[1][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[1][Const.SNIPPET_BRIEF], db_rows[1][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[1][Const.SNIPPET_GROUP], db_rows[1][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[1][Const.SNIPPET_TAGS], db_rows[1][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[1][Const.SNIPPET_LINKS], db_rows[1][Const.SNIPPET_LINKS])
        obj.delete_snippet('da217a911ec37e9a')
        snippet_db = obj.select_snippets(keywords)
        self.assertEqual(snippet_db[0][Const.SNIPPET_CONTENT], db_rows[1][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[0][Const.SNIPPET_BRIEF], db_rows[1][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[0][Const.SNIPPET_GROUP], db_rows[1][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[0][Const.SNIPPET_TAGS], db_rows[1][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[0][Const.SNIPPET_LINKS], db_rows[1][Const.SNIPPET_LINKS])
        obj.disconnect()

    @mock.patch.object(Config, 'is_search_all')
    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_delete_snippet_long_digest(self, mock_get_storage_schema, mock_is_storage_in_memory, mock_is_search_all):
        """Delete one of the snippets with long digest."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        mock_is_search_all.return_value = True
        snippet1 = Sqlite3DbHelper.SNIPPET1
        digest1 = Sqlite3DbHelper.DIGEST1
        snippet2 = Sqlite3DbHelper.SNIPPET2
        digest2 = Sqlite3DbHelper.DIGEST2
        metadata = 'metadata'
        keywords = ['help', 'docker']
        db_rows = [(snippet1[Const.SNIPPET_CONTENT], snippet1[Const.SNIPPET_BRIEF], snippet1[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet1[Const.SNIPPET_LINKS][0], digest1, metadata, 1),
                   (snippet2[Const.SNIPPET_CONTENT], snippet2[Const.SNIPPET_BRIEF], snippet2[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet2[Const.SNIPPET_LINKS][0], digest2, metadata, 2)]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet1, digest1, metadata)
        obj.insert_snippet(snippet2, digest2, metadata)
        snippet_db = obj.select_snippets(keywords)
        self.assertEqual(snippet_db[0][Const.SNIPPET_CONTENT], db_rows[0][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[0][Const.SNIPPET_BRIEF], db_rows[0][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[0][Const.SNIPPET_GROUP], db_rows[0][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[0][Const.SNIPPET_TAGS], db_rows[0][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[0][Const.SNIPPET_LINKS], db_rows[0][Const.SNIPPET_LINKS])
        self.assertEqual(snippet_db[1][Const.SNIPPET_CONTENT], db_rows[1][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[1][Const.SNIPPET_BRIEF], db_rows[1][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[1][Const.SNIPPET_GROUP], db_rows[1][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[1][Const.SNIPPET_TAGS], db_rows[1][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[1][Const.SNIPPET_LINKS], db_rows[1][Const.SNIPPET_LINKS])
        obj.delete_snippet('aa106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c')
        snippet_db = obj.select_snippets(keywords)
        self.assertEqual(snippet_db[0][Const.SNIPPET_CONTENT], db_rows[0][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[0][Const.SNIPPET_BRIEF], db_rows[0][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[0][Const.SNIPPET_GROUP], db_rows[0][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[0][Const.SNIPPET_TAGS], db_rows[0][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[0][Const.SNIPPET_LINKS], db_rows[0][Const.SNIPPET_LINKS])
        obj.disconnect()
