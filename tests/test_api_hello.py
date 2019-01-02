#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_api_hello: Test hello API and OPTIONS method."""

from falcon import testing
import falcon
import pytest

from snippy.snip import Snippy
from tests.testlib.content import Content

pytest.importorskip('gunicorn')


class TestApiHello(object):
    """Test hello API and OPTIONS method."""

    def test_api_hello_api_001(self, server):
        """Test hello API in /snippy/api/app/v1/.

        Call GET /snippy/api/app/v1 to get hello!
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    def test_api_hello_api_002(self, server):
        """Test hello API in /snippy/api/hello.

        Call GET /api/app/v1/hello to get hello!
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/hello')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_003(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path is
        changed from default and it is set in correct format.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', '/snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_004(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path
        configuration is incorrect. The server base path must contain trailing
        slash which is missing from this test. The configuration must be
        updated automatically and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', '/snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_005(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path
        configuration is incorrect. The server base path must contain leading
        slash which is missing from this test. The configuration must be
        updated and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', 'snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_006(self):
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path
        configuration is incorrect. The server base path must contain leading
        and trailing slashes which are missing from this test. In this case the
        configuration must be updated automatically and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', 'snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_007(self):
        """Test hello API with modified server base path configuration.

        Call GET /api/app/v1 to get hello! In this case the server base path is
        incorrect because it contains two slashes. This configuration error
        results the default base path configuration.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--base-path-app', '/snippy//api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_008(self, caplog):
        """Test hello API with modified server ip and port configuration.

        Call GET /api/app/v1 to get hello! In this case the server base path is
        changed from default and it is set in correct format.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '197'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server', '--server-ip', 'localhost', '--server-port', '8081', '-vv'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/')
        assert 'configured option server ip: localhost :and port: 8081' in caplog.text
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_009(self, server):
        """Test hello API with OPTIONS.

        Call OPTIONS /api/app/v1 to get allowed methods for the hello API.
        """

        expect_headers = {
            'allow': 'GET',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_010(self, server):
        """Test snippets API with OPTIONS.

        Call OPTIONS /v1/snippets to get allowed methods.
        """

        expect_headers = {
            'allow': 'DELETE,GET,OPTIONS,POST',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/snippets')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_011(self, server):
        """Test snippets digest API with OPTIONS.

        Call OPTIONS /v1/snippets/<digest> to get allowed methods.
        """

        expect_headers = {
            'allow': 'DELETE,GET,OPTIONS,PATCH,POST,PUT',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/snippets/123456')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_012(self, server):
        """Test snippets field API with OPTIONS.

        Call OPTIONS /v1/snippets/<digest>/<field> to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/snippets/123456/brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_013(self, server):
        """Test fields groups API with OPTIONS.

        Call OPTIONS /v1/groups/<groups> to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/groups/docker')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_014(self, server):
        """Test fields tags API with OPTIONS.

        Call OPTIONS /v1/tags/<tag> to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/tags/docker')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_015(self, server):
        """Test fields tags API with OPTIONS.

        Call OPTIONS /v1/digest/<digest> to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/digest/01010101')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_016(self, server):
        """Test fields uuid API with OPTIONS.

        Call OPTIONS /v1/uuid/<uuid> to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/uuid/27cd5827')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_017(self, server):
        """Test fields uuid API with OPTIONS.

        Call OPTIONS /v1/uuid/<uuid>/<field> to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_018(self, server):
        """Test fields keywords API with OPTIONS.

        Call OPTIONS /v1/groups to get allowed methods for keywords API. Note
        that this does not call the groups API but keywords API. The reason is
        that the route /groups does not have the parameter and in this case id
        does not lead to /groups but to /{keywords} API.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/snippy/api/app/v1/groups')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
