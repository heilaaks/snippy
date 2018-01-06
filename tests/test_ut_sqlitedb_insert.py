#!/usr/bin/env python3

"""test_ut_sqlite3db_insert.py: Test inserting content into sqlite."""

import mock
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbInsert(object):
    """Testing inserting content into sqlite."""

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'db_schema_file', Database.get_schema())
    def test_insert_with_all_parameters(self, mock_cause_push):
        """Insert content into database."""

        sqlite = Sqlite3Db()
        sqlite.init()

        ## Brief: Insert content into database with all parameters.
        content = Snippet.get_content(snippet=Snippet.REMOVE)
        sqlite.insert_content(content, content.get_digest(), content.get_metadata())
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        Snippet.compare_db((Database.select_all_snippets())[0], content)
        assert len(Database.select_all_snippets()) == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'db_schema_file', Database.get_schema())
    def test_insert_multiple_links(self, mock_cause_push):
        """Insert content with multiple links."""

        sqlite = Sqlite3Db()
        sqlite.init()

        ## Brief: Insert content with multiple links.
        content = Snippet.get_content(snippet=Snippet.FORCED)
        sqlite.insert_content(content, content.get_digest(), content.get_metadata())
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        Snippet.compare_db((Database.select_all_snippets())[0], content)
        assert len(Database.select_all_snippets()) == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
