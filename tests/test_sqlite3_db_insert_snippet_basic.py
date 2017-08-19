#!/usr/bin/env python3

"""test_sqlite3_db_insert_snippet_basic.py: Test inserting snippet into the sqlite3 database."""

import mock
from snippy.config import Constants as Const
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper

class TestSqlite3DbInsertSnippetBasic(object): # pylint: disable=too-few-public-methods
    """Testing inserting new snippets with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_with_all_parameters(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet with tags, brief or links is stored."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ['container', 'cleanup', 'docker']
        links = ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container']
        metadata = 'metadata'
        rows = [(1, snippet, brief, 'container,cleanup,docker', links[0], metadata)]
        obj = Sqlite3Db()
        obj.init()
        obj.insert_snippet(snippet, brief, tags, links, metadata)
        assert Sqlite3DbHelper().select_all_snippets() == rows
        obj.disconnect()

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_multiple_links(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet can be added with multiple links."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ['container', 'cleanup', 'docker']
        links = ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes']
        metadata = 'metadata'
        rows = [(1, snippet, brief, 'container,cleanup,docker', links[0] + Const.DELIMITER_LINKS + links[1], metadata)]
        obj = Sqlite3Db()
        obj.init()
        obj.insert_snippet(snippet, brief, tags, links, metadata)
        assert Sqlite3DbHelper().select_all_snippets() == rows
        obj.disconnect()
