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

"""test_api_hello: Test hello API."""

from falcon import testing
import falcon
import pytest

from snippy.snip import Snippy
from tests.testlib.content import Content
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

pytest.importorskip('gunicorn')


class TestApiHello(object):
    """Test hello API."""

    def test_api_hello_api_001(self, server):
        """Test hello API in /snippy/api/v1/."""

        ## Brief: Call GET /snippy/api/v1/ to get hello!
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/v1/')  ## apiflow
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    def test_api_hello_api_002(self, server):
        """Test hello API in /snippy/api/hello."""

        ## Brief: Call GET /snippy/api/v1/hello to get hello!
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/v1/hello')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_003(self):
        """Test hello API with modified server base path configuration."""

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the
        ##        server base path is changed from default and it is set in
        ##        correct format.
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path', '/snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_004(self):
        """Test hello API with modified server base path configuration."""

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the
        ##        server base path configuration is incorrect. The server base
        ##        path must contain trailing slash which is missing from this
        ##        test. The configuration must be updated and the API call
        ##        must work.
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path', '/snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_005(self):
        """Test hello API with modified server base path configuration."""

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the
        ##        server base path configuration is incorrect. The server base
        ##        path must contain leading slash which is missing from this
        ##        test. The configuration must be updated and the API call
        ##        must work.
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path', 'snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_006(self):
        """Test hello API with modified server base path configuration."""

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the
        ##        server base path configuration is incorrect. The server base
        ##        path must contain leading and trailing slashes which are
        ##        missing from this test. The configuration must be updated
        ##        and the API call must work.
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path', 'snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_007(self):
        """Test hello API with modified server base path configuration."""

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the
        ##        server base path configuration is incorrect because it
        ##        contains two slashes. In this case this misconfiguration
        ##        results default base path.
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path', '/snippy//api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/v1')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_008(self, caplog):
        """Test hello API with modified server ip and port configuration."""

        ## Brief: Call GET /snippy/api/hello to get hello! In this case the
        ##        server base path is changed from default and it is set in
        ##        correct format.
        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--ip', 'localhost', '--port', '8081', '-vv'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/v1/')  ## apiflow
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert 'configured option server ip localhost and port 8081' in caplog.text
        server.release()
        Database.delete_storage()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
