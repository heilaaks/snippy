#!/usr/bin/env python3

"""test_api_delete_snippets.py: Test DELETE /snippets API."""

import sys
import unittest
import mock
import falcon
from falcon import testing
from snippy.snip import Snippy
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiDeleteSnippet(unittest.TestCase):
    """Test DELETE /snippets API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_api_search_snippets_with_sall(self, mock_get_db_location, mock_get_utc_time, mock_isfile, _):
        """Search snippet from all fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call DELETE /api/snippets with digest parameter that matches one snippet
        ##        that is deleted.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*4 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults(Snippy())
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/api/snippets',  ## apiflow
                                                                       headers={'accept': 'application/json'},
                                                                       query_string='digest=f3fd167c64b6f97e')
        assert result.headers == headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_snippets()) == 2
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call DELETE /api/snippets/f3fd167c64b6f97e that matches one snippet that
        ##        is deleted.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*4 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults(Snippy())
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/api/snippets/f3fd167c64b6f97e',  ## apiflow
                                                                       headers={'accept': 'application/json'})
        assert result.headers == headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_snippets()) == 2
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
