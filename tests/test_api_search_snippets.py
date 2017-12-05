#!/usr/bin/env python3

"""test_api_search_snippets.py: Test get /snippets API."""

import sys
import unittest
import json
import mock
import pytest
import falcon
from falcon import testing
from snippy.snip import Snippy
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiSearchSnippet(unittest.TestCase):
    """Test get /snippets API."""

    @pytest.mark.skip(reason='Sorting and comparing JSON does not yet work')
    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_api_search_snippets_with_sall(self, mock_get_db_location, mock_get_utc_time, mock_isfile, _):
        """Search snippet from all fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Get /api/snippets and search keywords from all columns. The search query
        ##        matches to two snippets and both of them are returned.
        snippy = Snippet.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '969'}
        body = json.dumps([Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]])
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/api/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == headers
        assert json.dumps(result.json) == body
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
