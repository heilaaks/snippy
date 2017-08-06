#!/usr/bin/env python3

"""test_sqlite3_db_select_snippet_basic.py: Test selecting snippets from the sqlite3 database."""

import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db

class TestSqlite3DbSelectSnippetBasic(object): # pylint: disable=too-few-public-methods
    """Testing selecting of snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_select_with_one_keyword_matching_column_link(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet can be selected with regexp keywords. In this
        case only the last keyword matches to link column."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['container', 'cleanup', 'docker']
        comment = 'Remove all docker containers'
        link = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
        metadata = 'metadata'
        keywords = ['moby', 'delete', 'askubuntu']
        rows = [(1, snippet, 'container,cleanup,docker', comment, link, metadata)]
        obj = Sqlite3Db()
        obj.init()
        obj.insert_snippet(snippet, tags, comment, link, metadata)
        assert obj.select_snippet(keywords) == rows
        obj.disconnect()
