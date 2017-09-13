#!/usr/bin/env python3

"""test_sqlite3_db_insert_snippet_basic.py: Test inserting snippet into the sqlite3 database."""

import unittest
import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestSqlite3DbInsertSnippetBasic(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Testing inserting new snippets with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_with_all_parameters(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet with tags, brief or links is stored."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'

        obj = Sqlite3Db().init()
        references = Snippet().get_references(0)
        obj.insert_snippet(references[0][CONTENT:TESTING], references[0][DIGEST], references[0][METADATA])
        Snippet().compare_db((Database().select_all_snippets())[0], references[0])
        assert len(Database().select_all_snippets()) == 1
        obj.disconnect()

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_multiple_links(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet can be added with multiple links."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'

        obj = Sqlite3Db().init()
        references = Snippet().get_references(1)
        obj.insert_snippet(references[0][CONTENT:TESTING], references[0][DIGEST], references[0][METADATA])
        Snippet().compare_db((Database().select_all_snippets())[0], references[0])
        assert len(Database().select_all_snippets()) == 1
        obj.disconnect()
