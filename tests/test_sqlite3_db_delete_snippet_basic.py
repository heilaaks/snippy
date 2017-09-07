#!/usr/bin/env python3

"""test_sqlite3_db_delete_snippet_basic.py: Test deleting snippets from the sqlite3 database."""

import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper

class TestSqlite3DbDeleteSnippetBasic(object): # pylint: disable=too-few-public-methods
    """Testing deleting snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_delete_snippet_with_short_digest(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Two snippes are added and one of them is deleted leaving only one snippet
        after the test. Deleting is made with short version from snippet digest"""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet1 = Sqlite3DbHelper.SNIPPET1
        snippet2 = Sqlite3DbHelper.SNIPPET2
        metadata = 'metadata'
        keywords = ['help', 'docker']
        db_rows = [(1, snippet1['content'], snippet1['brief'], snippet1['group'], 'container,cleanup,docker',
                    snippet1['links'][0], metadata, snippet1['digest']),
                   (2, snippet2['content'], snippet2['brief'], snippet2['group'], 'container,cleanup,docker',
                    snippet2['links'][0], metadata, snippet2['digest'])]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet1, metadata)
        obj.insert_snippet(snippet2, metadata)
        assert obj.select_snippets(keywords) == db_rows
        obj.delete_snippet('da217a911ec37e9a')
        assert obj.select_snippets(keywords) == [db_rows[1]]
        obj.disconnect()

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_delete_snippet_long_digest(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Delete one of the snippets with long digest."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet1 = Sqlite3DbHelper.SNIPPET1
        snippet2 = Sqlite3DbHelper.SNIPPET2
        metadata = 'metadata'
        keywords = ['help', 'docker']
        db_rows = [(1, snippet1['content'], snippet1['brief'], snippet1['group'], 'container,cleanup,docker',
                    snippet1['links'][0], metadata, snippet1['digest']),
                   (2, snippet2['content'], snippet2['brief'], snippet2['group'], 'container,cleanup,docker',
                    snippet2['links'][0], metadata, snippet2['digest'])]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet1, metadata)
        obj.insert_snippet(snippet2, metadata)
        assert obj.select_snippets(keywords) == db_rows
        obj.delete_snippet('aa106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c')
        assert obj.select_snippets(keywords) == [db_rows[0]]
        obj.disconnect()
