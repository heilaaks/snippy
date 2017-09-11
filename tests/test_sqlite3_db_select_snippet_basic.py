#!/usr/bin/env python3

"""test_sqlite3_db_select_snippet_basic.py: Test selecting snippets from the sqlite3 database."""

import mock
from snippy.config import Constants as Const
from snippy.config import Config
from snippy.storage.database import Sqlite3Db

class TestSqlite3DbSelectSnippetBasic(object): # pylint: disable=too-few-public-methods
    """Testing selecting of snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_select_keyword_matching_column_links(self, mock_get_storage_schema, mock_is_storage_in_memory, mock_is_search_all):
        """Test that snippet can be selected with regexp keywords. In this
        case only the last keyword matches to links column."""

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        mock_is_search_all.return_value = True
        snippet = ('docker rm $(docker ps -a -q)',
                   'Remove all docker containers',
                   'moby',
                   ['container', 'cleanup', 'docker'],
                   ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'])
        digest = 'da106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'
        metadata = 'metadata'
        keywords = ['moby', 'delete', 'askubuntu']
        db_rows = [(snippet[Const.SNIPPET_CONTENT], snippet[Const.SNIPPET_BRIEF], snippet[Const.SNIPPET_GROUP],
                    'container,cleanup,docker', snippet[Const.SNIPPET_LINKS][0], digest, metadata, 1)]
        obj = Sqlite3Db().init()
        obj.insert_snippet(snippet, digest, metadata)
        assert obj.select_snippets(keywords) == db_rows
        obj.disconnect()
