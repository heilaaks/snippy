#!/usr/bin/env python3

"""test_sqlite3_db_insert_snippet_basic.py: Test inserting snippet into the sqlite3 database."""

import unittest
import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestSqlite3DbInsertSnippetBasic(unittest.TestCase):
    """Testing inserting new snippets with basic tests."""

    def test_insert_with_all_parameters(self):
        """Test that snippet with tags, brief or links is stored."""

        references = Snippet().get_references(0)
        self.sqlite.insert_content(references[0][DATA:TESTING], references[0][DIGEST], references[0][METADATA])
        Snippet().compare_db(self, (Database.select_all_snippets())[0], references[0])
        assert len(Database.select_all_snippets()) == 1
        self.sqlite.disconnect()

    def test_insert_multiple_links(self):
        """Test that snippet can be added with multiple links."""

        references = Snippet().get_references(1)
        self.sqlite.insert_content(references[0][DATA:TESTING], references[0][DIGEST], references[0][METADATA])
        Snippet().compare_db(self, (Database.select_all_snippets())[0], references[0])
        assert len(Database.select_all_snippets()) == 1
        self.sqlite.disconnect()

    # pylint: disable=duplicate-code
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch.object(Config, 'get_storage_schema')
    def setUp(self, mock_get_storage_schema, mock__get_db_location): # pylint: disable=arguments-differ
        """Setup each test."""

        mock_get_storage_schema.return_value = Database.get_schema()
        mock__get_db_location.return_value = Database.get_storage()

        self.sqlite = Sqlite3Db().init()

    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        self.sqlite.disconnect()
        Database.delete_storage()
