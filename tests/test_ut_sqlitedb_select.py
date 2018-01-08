#!/usr/bin/env python3

"""test_ut_sqlite3db_select.py: Test selecting content from sqlite."""

import mock
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbSelect(object):
    """Testing selecting content from sqlite."""

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    @mock.patch.object(Config, 'is_search_all', return_value=True)
    def test_select_keyword_matching_links_column(self, _, mock_cause_push):
        """Test selecting content."""

        sqlite = Sqlite3Db()
        sqlite.init()

        ## Brief: Select content with regexp stored into sqlite. In this
        ##        case th last keyword matches to links column.
        content = Snippet.get_content(snippet=Snippet.FORCED)
        keywords = ['foo', 'bar', 'digitalocean']
        sqlite.insert_content(content, content.get_digest(), content.get_metadata())
        mock_cause_push.reset_mock()
        Snippet.compare_db((sqlite.select_content(Const.SNIPPET, keywords))[0], content)
        assert len(sqlite.select_content(Const.SNIPPET, keywords)) == 1
        mock_cause_push.assert_not_called()
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
