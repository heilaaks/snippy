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
        snippets = ['docker rm $(docker ps -a -q)', 'docker rmi $(docker images -f dangling=true -q)']
        briefs = ['Remove all docker containers', 'Remove all dangling image layers']
        category = 'docker'
        tags = [['container', 'cleanup', 'docker'], ['container', 'cleanup', 'docker']]
        links = ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.faked.com/tutorials/how-to-remove-docker-images-containers-and-volumes']
        metadata = 'metadata'
        keywords = ['help', 'docker']
        rows = [(1, snippets[0], briefs[0], category, 'container,cleanup,docker', links[0], metadata),
                (2, snippets[1], briefs[1], category, 'container,cleanup,docker', links[1], metadata)]
        obj = Sqlite3Db()
        obj.init()
        obj.insert_snippet(snippets[0], briefs[0], category, tags[0], [links[0]], metadata)
        obj.insert_snippet(snippets[1], briefs[1], category, tags[1], [links[1]], metadata)
        assert obj.select_snippets(keywords) == rows
        obj.delete_snippet(1)
        assert obj.select_snippets(keywords) == [(2, snippets[1], briefs[1], category, 'container,cleanup,docker', \
                                                     links[1], metadata)]
        obj.disconnect()
