#!/usr/bin/env python3

"""test_sqlite3_db_delete_snippet_basic.py: Test deleting snippets from the sqlite3 database."""

import unittest
import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestSqlite3DbDeleteSnippetBasic(unittest.TestCase):
    """Testing deleting snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    def test_delete_snippet_with_short_digest(self, mock_is_search_all):
        """Two snippes are added and one of them is deleted leaving only one snippet
        after the test. Deleting is made with short version from snippet digest"""

        mock_is_search_all.return_value = True

        references = Snippet().get_references(sliced='0:2')
        keywords = ['foo', 'engine', 'digitalocean']
        self.sqlite.insert_snippet(references[0][CONTENT:TESTING], references[0][DIGEST], references[0][METADATA])
        self.sqlite.insert_snippet(references[1][CONTENT:TESTING], references[1][DIGEST], references[1][METADATA])
        Snippet().compare_db((self.sqlite.select_snippets(keywords))[0], references[0])
        Snippet().compare_db((self.sqlite.select_snippets(keywords))[1], references[1])
        assert len(Database.select_all_snippets()) == 2
        self.sqlite.delete_snippet('6f9e21abdc2e4c53')
        Snippet().compare_db((self.sqlite.select_snippets(keywords))[0], references[0])
        assert len(Database.select_all_snippets()) == 1
        self.sqlite.disconnect()

    @mock.patch.object(Config, 'is_search_all')
    def test_delete_snippet_long_digest(self, mock_is_search_all):
        """Delete one of the snippets with long digest."""

        mock_is_search_all.return_value = True

        references = Snippet().get_references(sliced='0:2')
        keywords = ['foo', 'engine', 'digitalocean']
        self.sqlite.insert_snippet(references[0][CONTENT:TESTING], references[0][DIGEST], references[0][METADATA])
        self.sqlite.insert_snippet(references[1][CONTENT:TESTING], references[1][DIGEST], references[1][METADATA])
        Snippet().compare_db((self.sqlite.select_snippets(keywords))[0], references[0])
        Snippet().compare_db((self.sqlite.select_snippets(keywords))[1], references[1])
        assert len(Database.select_all_snippets()) == 2
        self.sqlite.delete_snippet('6f9e21abdc2e4c53d04d77eff024708086c0a583f1be3dd761774353e9d2b74f')
        Snippet().compare_db((self.sqlite.select_snippets(keywords))[0], references[0])
        assert len(Database.select_all_snippets()) == 1
        self.sqlite.disconnect()

    # pylint: disable=duplicate-code
    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def setUp(self, mock_get_storage_schema, mock_is_storage_in_memory): # pylint: disable=arguments-differ
        """Setup each test."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'

        self.sqlite = Sqlite3Db().init()

    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        self.sqlite.disconnect()
