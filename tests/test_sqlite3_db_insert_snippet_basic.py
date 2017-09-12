#!/usr/bin/env python3

"""test_sqlite3_db_insert_snippet_basic.py: Test inserting snippet into the sqlite3 database."""

import unittest
import mock
from snippy.config import Constants as Const
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper

class TestSqlite3DbInsertSnippetBasic(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Testing inserting new snippets with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_with_all_parameters(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet with tags, brief or links is stored."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = ('docker rm $(docker ps -a -q)',
                   'Remove all docker containers',
                   'docker',
                   ['container', 'cleanup', 'docker'],
                   ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'])
        digest = 'da106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'
        metadata = 'metadata'
        db_rows = [(snippet[Const.SNIPPET_CONTENT], snippet[Const.SNIPPET_BRIEF], snippet[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet[Const.SNIPPET_LINKS][0], digest, metadata, 1)]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet, digest, metadata)
        snippet_db = Sqlite3DbHelper().select_all_snippets()
        self.assertEqual(snippet_db[0][Const.SNIPPET_CONTENT], db_rows[0][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[0][Const.SNIPPET_BRIEF], db_rows[0][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[0][Const.SNIPPET_GROUP], db_rows[0][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[0][Const.SNIPPET_TAGS], db_rows[0][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[0][Const.SNIPPET_LINKS], db_rows[0][Const.SNIPPET_LINKS])
        obj.disconnect()

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_multiple_links(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet can be added with multiple links."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = ('docker rm $(docker ps -a -q)',
                   'Remove all docker containers',
                   'docker',
                   ['container', 'cleanup', 'docker'],
                   ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                    'https://www.faked.com/tutorials/how-to-remove-docker-images-containers-and-volumes'])
        digest = 'da106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'
        metadata = 'metadata'
        db_rows = [(snippet[Const.SNIPPET_CONTENT], snippet[Const.SNIPPET_BRIEF], snippet[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet[Const.SNIPPET_LINKS][0] + Const.DELIMITER_LINKS +
                    snippet[Const.SNIPPET_LINKS][1], digest, metadata, 1)]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet, digest, metadata)
        snippet_db = Sqlite3DbHelper().select_all_snippets()
        self.assertEqual(snippet_db[0][Const.SNIPPET_CONTENT], db_rows[0][Const.SNIPPET_CONTENT])
        self.assertEqual(snippet_db[0][Const.SNIPPET_BRIEF], db_rows[0][Const.SNIPPET_BRIEF])
        self.assertEqual(snippet_db[0][Const.SNIPPET_GROUP], db_rows[0][Const.SNIPPET_GROUP])
        self.assertEqual(snippet_db[0][Const.SNIPPET_TAGS], db_rows[0][Const.SNIPPET_TAGS])
        self.assertEqual(snippet_db[0][Const.SNIPPET_LINKS], db_rows[0][Const.SNIPPET_LINKS])
        obj.disconnect()
