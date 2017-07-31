#!/usr/bin/env python3

"""test_sqlite3_db_snippet.py: Test snippet storage in sqlite3 database."""

import mock
from snippy.config import Config
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper

class TestSqlite3DbAddNewSnippet(object): # pylint: disable=too-few-public-methods
    """Testing storing new snippets."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_add_new_with_all_parameters(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet with tags, comment or links is stored."""

        from snippy.storage.database import Sqlite3Db

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['container', 'cleanup', 'docker']
        comment = 'Remove all docker containers'
        link = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
        metadata = 'metadata'
        rows = [(1, snippet, 'container,cleanup,docker', comment, link, metadata)]
        obj = Sqlite3Db()
        obj.init()
        obj.insert_snippet(snippet, tags, comment, link, metadata)
        assert Sqlite3DbHelper().select_all_snippets() == rows
        obj.disconnect()
