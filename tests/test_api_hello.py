#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""test_api_hello.py: Test hello API."""

import sys
import unittest
import json
import mock

import falcon
from falcon import testing

from snippy.config.config import Config
from snippy.metadata import __version__
from snippy.snip import Snippy
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiHello(unittest.TestCase):
    """Test hello API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, '_storage_file')
    def test_api_hello_root(self, mock_get_db_location, mock_isfile, _):
        """Test hello API in /snippy."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy to get hello!
        header = {'content-type': 'application/json; charset=UTF-8', 'content-length': '25'}
        body = {'snippy': __version__}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy')   ## apiflow
        assert result.headers == header
        assert result.json == json.dumps(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, '_storage_file')
    def test_api_hello_api(self, mock_get_db_location, mock_isfile, _):
        """Test hello API in /snippy/api/hello."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/hello to get hello!
        header = {'content-type': 'application/json; charset=UTF-8', 'content-length': '25'}
        body = {'snippy': __version__}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/hello')   ## apiflow
        assert result.headers == header
        assert result.json == json.dumps(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, '_storage_file')
    def test_api_hello_v1(self, mock_get_db_location, mock_isfile, _):
        """Test hello API in /snippy/api/v1/hello."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/hello to get hello!
        header = {'content-type': 'application/json; charset=UTF-8', 'content-length': '25'}
        body = {'snippy': __version__}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/v1/hello')   ## apiflow
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
