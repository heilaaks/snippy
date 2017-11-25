#!/usr/bin/env python3

"""test_api_hello.py: Test hello API."""

import unittest
import mock
import pytest
from snippy.version import __version__
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
from tests.testlib.falcon_helper import FalconHelper as Api


class TestApiHello(unittest.TestCase):
    """Test hello API."""

    @pytest.mark.skip(reason='Experimental testing with Falcon')
    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_api_hello(self, mock_get_db_location, mock_isfile, _):
        """Test hello API."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        response = {'snippy': __version__}
        result = Api.client().simulate_get('/api/hello')
        assert result.json == response
