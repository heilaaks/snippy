#!/usr/bin/env python3

"""test_ut_sqlite3db_select.py: Test selecting snippets from the sqlite3 database."""

import unittest
import mock
from snippy.config import Constants as Const
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbSelect(unittest.TestCase):
    """Testing selecting of snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    def test_select_keyword_matching_links_column(self, mock_is_search_all):
        """Test that snippet can be selected with regexp keywords. In this
        case only the last keyword matches to links column."""

        mock_is_search_all.return_value = True

        initial = Snippet().get_references(1)
        keywords = ['foo', 'bar', 'digitalocean']
        self.sqlite.insert_content(initial, initial.get_digest(), initial.get_metadata())
        Snippet().compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[0], initial)
        assert len(self.sqlite.select_content(Const.SNIPPET, keywords)) == 1
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
