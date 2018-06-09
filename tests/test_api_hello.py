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
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiHello(object):
    """Test hello API."""

    def test_api_hello_api_001(self, server):
        """Test hello API in /snippy/api/app/v1/.

        Call GET /snippy/api/app/v1/ to get hello!
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    def test_api_hello_api_002(self, server):
        """Test hello API in /snippy/api/hello.

        Call GET /snippy/api/app/v1/hello to get hello!
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/hello')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_003(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api/hello to get hello! In this case the server base
        path is changed from default and it is set in correct format.
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', '/snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_004(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api/hello to get hello! In this case the server base
        path configuration is incorrect. The server base path must contain
        trailing slash which is missing from this test. The configuration
        must be updated and the API call must work.
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', '/snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_005(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api/hello to get hello! In this case the server base
        path configuration is incorrect. The server base path must contain
        leading slash which is missing from this test. The configuration must
        be updated and the API call must work.
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', 'snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_006(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api/hello to get hello! In this case the server base
        path configuration is incorrect. The server base path must contain
        leading and trailing slashes which are missing from this test. The
        configuration must be updated and the API call must work.
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', 'snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_007(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api/hello to get hello! In this case the server base
        path configuration is incorrect because it contains two slashes. In
        this case this misconfiguration results default base path.
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', '/snippy//api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_008(self, caplog):
        """Test hello API with modified server ip and port configuration.

        Call GET /snippy/api/hello to get hello! In this case the server base
        path is changed from default and it is set in correct format.
        """

        result_header = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        result_json = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--ip', 'localhost', '--port', '8081', '-vv'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/')
        assert result.headers == result_header
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert 'configured option server ip: localhost :and port: 8081' in caplog.text
        server.release()
        Database.delete_storage()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_009(self, server):
        """Test hello API with OPTIONS.

        Call GET /snippy/api/hello to get hello API allowed methods.
        """

        result_header = {
            'allow': 'GET',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/')
        assert result.headers == result_header
        assert not result.text
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_010(self, server):
        """Test snippets API with OPTIONS.

        Call GET /v1/snippets to get allowed methods.
        """

        result_header = {
            'allow': 'DELETE,GET,POST',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/snippets')
        assert result.headers == result_header
        assert not result.text
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_011(self, server):
        """Test snippets digest API with OPTIONS.

        Call GET /v1/snippets/digest to get allowed methods.
        """

        result_header = {
            'allow': 'DELETE,GET,PATCH,POST,PUT',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/snippets/123456')
        assert result.headers == result_header
        assert not result.text
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_012(self, server):
        """Test snippets field API with OPTIONS.

        Call GET /v1/snippets/<digest>/<field> to get allowed methods.
        """

        result_header = {
            'allow': 'GET',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/snippets/123456/brief')
        assert result.headers == result_header
        assert not result.text
        assert result.status == falcon.HTTP_200

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
