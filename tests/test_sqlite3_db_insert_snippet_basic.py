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
        snippet = {'content': 'docker rm $(docker ps -a -q)',
                   'brief': 'Remove all docker containers',
                   'category': 'docker',
                   'tags': ['container', 'cleanup', 'docker'],
                   'links': ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'],
                   'digest': 'da106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}
        metadata = 'metadata'
        db_rows = [(1, snippet['content'], snippet['brief'], snippet['category'], 'container,cleanup,docker',
                    snippet['links'][0], metadata, snippet['digest'])]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet, metadata)
        assert Sqlite3DbHelper().select_all_snippets() == db_rows
        obj.disconnect()

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_insert_multiple_links(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet can be added with multiple links."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet = {'content': 'docker rm $(docker ps -a -q)',
                   'brief': 'Remove all docker containers',
                   'category': 'docker',
                   'tags': ['container', 'cleanup', 'docker'],
                   'links': ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                             'https://www.faked.com/tutorials/how-to-remove-docker-images-containers-and-volumes'],
                   'digest': 'da106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}
        metadata = 'metadata'
        db_rows = [(1, snippet['content'], snippet['brief'], snippet['category'], 'container,cleanup,docker',
                    snippet['links'][0] + Const.DELIMITER_LINKS + snippet['links'][1], metadata, snippet['digest'])]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet, metadata)
        assert Sqlite3DbHelper().select_all_snippets() == db_rows
        obj.disconnect()
