#!/usr/bin/env python3

"""test_sqlite3_db_select_snippet_basic.py: Test selecting snippets from the sqlite3 database."""

import unittest
import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import
from tests.testlib.snippet_helper import SnippetHelper as Snippet


class TestSqlite3DbSelectSnippetBasic(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Testing selecting of snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_select_keyword_matching_links_column(self, mock_get_storage_schema, mock_is_storage_in_memory, mock_is_search_all):
        """Test that snippet can be selected with regexp keywords. In this
        case only the last keyword matches to links column."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        mock_is_search_all.return_value = True

        obj = Sqlite3Db().init()
        references = Snippet().get_references(1)
        keywords = ['foo', 'bar', 'digitalocean']
        obj.insert_snippet(references[0][CONTENT:TESTING], references[0][DIGEST], references[0][METADATA])
        Snippet().compare_db((obj.select_snippets(keywords))[0], references[0])
        assert len(obj.select_snippets(keywords)) == 1
        obj.disconnect()
