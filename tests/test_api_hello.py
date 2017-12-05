#!/usr/bin/env python3

"""test_api_hello.py: Test hello API."""

import sys
import unittest
import json
import mock
import falcon
from falcon import testing
from snippy.snip import Snippy
from snippy.version import __version__
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiHello(unittest.TestCase):
    """Test hello API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_api_hello(self, mock_get_db_location, mock_isfile, _):
        """Test hello API."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        header = {'content-type': 'application/json; charset=UTF-8', 'content-length': '25'}
        body = {'snippy': __version__}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/api/hello')
        assert result.headers == header
        assert result.json == json.dumps(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
