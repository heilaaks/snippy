#!/usr/bin/env python3

"""test_sqlite3_db_select_snippet_basic.py: Test selecting snippets from the sqlite3 database."""

import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db

class TestSqlite3DbSelectSnippetBasic(object): # pylint: disable=too-few-public-methods
    """Testing selecting of snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_select_with_one_keyword_matching_column_links(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet can be selected with regexp keywords. In this
        case only the last keyword matches to links column."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        category = 'docker'
        tags = ['container', 'cleanup', 'docker']
        links = ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container']
        metadata = 'metadata'
        keywords = ['moby', 'delete', 'askubuntu']
        rows = [(1, content, brief, category, 'container,cleanup,docker', links[0], metadata)]
        obj = Sqlite3Db()
        obj.init()
        obj.insert_snippet(content, brief, category, tags, links, metadata)
        assert obj.select_snippets(keywords) == rows
        obj.disconnect()
