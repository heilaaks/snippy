#!/usr/bin/env python3

"""test_ut_sqlite3db_delete.py: Test deleting snippets from the sqlite3 database."""

import unittest
import mock
from snippy.config.constants import Constants as Const
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbDelete(unittest.TestCase):
    """Testing deleting snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    def test_delete_snippet_with_short_digest(self, mock_is_search_all):
        """Two snippes are added and one of them is deleted leaving only one snippet
        after the test. Deleting is made with short version from snippet digest"""

        mock_is_search_all.return_value = True

        content1 = Snippet.get_content(snippet=Snippet.REMOVE)
        content2 = Snippet.get_content(snippet=Snippet.FORCED)
        keywords = ['foo', 'engine', 'digitalocean']
        self.sqlite.insert_content(content1, content1.get_digest(), content1.get_metadata())
        self.sqlite.insert_content(content2, content2.get_digest(), content2.get_metadata())
        Snippet.compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        Snippet.compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[1], content2)
        assert len(Database.select_all_snippets()) == 2
        self.sqlite.delete_content('53908d68425c61dc')
        Snippet.compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        assert len(Database.select_all_snippets()) == 1
        self.sqlite.disconnect()

    @mock.patch.object(Config, 'is_search_all')
    def test_delete_snippet_long_digest(self, mock_is_search_all):
        """Delete one of the snippets with long digest."""

        mock_is_search_all.return_value = True

        content1 = Snippet.get_content(snippet=Snippet.REMOVE)
        content2 = Snippet.get_content(snippet=Snippet.FORCED)
        keywords = ['foo', 'engine', 'digitalocean']
        self.sqlite.insert_content(content1, content1.get_digest(), content1.get_metadata())
        self.sqlite.insert_content(content2, content2.get_digest(), content2.get_metadata())
        Snippet.compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        Snippet.compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[1], content2)
        assert len(Database.select_all_snippets()) == 2
        self.sqlite.delete_content('53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5')
        Snippet.compare_db(self, (self.sqlite.select_content(Const.SNIPPET, keywords))[0], content1)
        assert len(Database.select_all_snippets()) == 1
        self.sqlite.disconnect()

    # pylint: disable=duplicate-code
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch.object(Config, 'get_storage_schema')
    def setUp(self, mock_get_storage_schema, mock__get_db_location): # pylint: disable=arguments-differ
        """Setup each test."""

        mock_get_storage_schema.return_value = Database.get_schema()
        mock__get_db_location.return_value = Database.get_storage()

        self.sqlite = Sqlite3Db()
        self.sqlite.init()

    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        self.sqlite.disconnect()
        Database.delete_storage()
