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

import falcon
from falcon import testing
import mock

from snippy.config.config import Config
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiHello(object):
    """Test hello API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, '_storage_file')
    def test_api_hello_root(self, mock_get_db_location, mock_isfile, _):
        """Test hello API in /snippy/api/v1/."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/ to get hello!
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/v1/')   ## apiflow
        print(result.json)
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
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

        ## Brief: Call GET /snippy/api/v1/hello to get hello!
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/v1/hello')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, '_storage_file')
    def test_api_hello_server_base_path(self, mock_get_db_location, mock_isfile, _):
        """Test hello API with modified server base path configuration."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the server
        ##        base path is changed from default and it is set in correct format.
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server', '--base-path', '/snippy/api/'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the server
        ##        base path configuration is incorrect. The server base path must
        ##        contain trailing slash which is missing from this test. The
        ##        configuration must be updated and the API call must work.
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server', '--base-path', '/snippy/api'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the server
        ##        base path configuration is incorrect. The server base path must
        ##        contain leading slash which is missing from this test. The
        ##        configuration must be updated and the API call must work.
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server', '--base-path', 'snippy/api/'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the server
        ##        base path configuration is incorrect. The server base path must
        ##        contain leading and trailing slashes which are missing from this
        ##        test. The configuration must be updated and the API call must work.
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server', '--base-path', 'snippy/api'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the server
        ##        base path configuration is incorrect because it contains two slashes.
        ##        In this case this misconfiguration results default base path.
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server', '--base-path', '/snippy//api'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/v1')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, '_storage_file')
    def test_api_hello_server_ip_port(self, mock_get_db_location, mock_isfile, _, caplog):
        """Test hello API with modified server ip and port configuration."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the server
        ##        base path is changed from default and it is set in correct format.
        header = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '197'}
        body = {'meta': Snippet.get_http_metadata()}
        snippy = Snippy(['snippy', '--server', '--ip', 'localhost', '--port', '8081', '-vv'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get('/snippy/api/v1/')   ## apiflow
        assert result.headers == header
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_200
        assert 'configured option server ip localhost and port 8081' in caplog.text
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
