#!/usr/bin/env python3

"""test_sqlite3_db_delete_snippet_basic.py: Test deleting snippets from the sqlite3 database."""

import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db

class TestSqlite3DbDeleteSnippetBasic(object): # pylint: disable=too-few-public-methods
    """Testing deleting snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_delete_snippet_with_index(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Two snippes are added and one of them is deleted leaving only
        one snippet after the test."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        snippet1 = {'content': 'docker rm $(docker ps -a -q)',
                    'brief': 'Remove all docker containers',
                    'category': 'docker',
                    'tags': ['container', 'cleanup', 'docker'],
                    'links': ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'],
                    'digest': 'da106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}
        snippet2 = {'content': 'docker rmi $(docker images -f dangling=true -q)',
                    'brief': 'Remove all dangling image layers',
                    'category': 'docker',
                    'tags': ['container', 'cleanup', 'docker'],
                    'links': ['https://www.faked.com/tutorials/how-to-remove-docker-images-containers-and-volumes'],
                    'digest': 'aa106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}
        metadata = 'metadata'
        keywords = ['help', 'docker']
        db_rows = [(1, snippet1['content'], snippet1['brief'], snippet1['category'], 'container,cleanup,docker',
                    snippet1['links'][0], metadata, snippet1['digest']),
                   (2, snippet2['content'], snippet2['brief'], snippet2['category'], 'container,cleanup,docker',
                    snippet2['links'][0], metadata, snippet2['digest'])]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet1, metadata)
        obj.insert_snippet(snippet2, metadata)
        assert obj.select_snippets(keywords) == db_rows
        obj.delete_snippet(1)
        assert obj.select_snippets(keywords) == [db_rows[1]]
        obj.disconnect()
