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


class TestApiHello(object):  # pylint: disable=too-many-public-methods
    """Test hello API and OPTIONS method."""

    @staticmethod
    def test_api_hello_api_001(server):
        """Test hello API.

        Call GET /snippy/api/app/v1 to get Hello response.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '199'
        }
        expect_body = {'meta': Content.get_api_meta()}
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    def test_api_hello_api_002(server):
        """Test hello API.

        Call GET /api/app/v1/hello to get hello!
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '199'
        }
        expect_body = {'meta': Content.get_api_meta()}
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/hello')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_003():
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path is
        changed from default and it is set in correct format.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '243'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path', '/snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_004():
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path
        configuration is incorrect. The server base path must contain trailing
        slash which is missing from this test. The configuration must be
        updated automatically and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '243'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path', '/snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_005():
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path
        configuration is incorrect. The server base path must contain leading
        slash which is missing from this test. The configuration must be
        updated and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '243'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path', 'snippy/api/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_006():
        """Test hello API with modified server base path configuration.

        Call GET /snippy/api to get hello! In this case the server base path
        configuration is incorrect. The server base path must contain leading
        and trailing slashes which are missing from this test. In this case the
        configuration must be updated automatically and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '243'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path', 'snippy/api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_007():
        """Test hello API with modified server base path configuration.

        Call GET /api/app/v1 to get hello! In this case the server base path is
        incorrect because it contains two slashes. This configuration error
        results the default base path configuration.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '243'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path', '/snippy//api'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_008(caplog):
        """Test hello API with modified server IP and port configuration.

        Call GET /api/app/v1 to get hello! In this case the server host is
        changed from the default with command line option.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '243'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8081', '--debug'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/app/v1/')
        assert 'server_host=localhost:8081' in caplog.text
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_009(server):
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_010(server):
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_011(server):
        """Test snippets digest API with OPTIONS.

        Call OPTIONS /v1/snippets/{id} to get allowed methods.
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_012(server):
        """Test snippets field API with OPTIONS.

        Call OPTIONS /v1/snippets/{id}/{field} to get allowed methods.
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_013(server):
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_014(server):
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_015(server):
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

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_016(caplog, osenviron):
        """Test server startup with environment variable configuration.

        Call GET /api/app/v1 to get Hello response. In this case the server
        variables are changed with environment variables.
        """

        osenviron.setenv('SNIPPY_SERVER_BASE_PATH', '/snippy/api/v2')
        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        osenviron.setenv('SNIPPY_SERVER_MINIFY_JSON', 'True')
        osenviron.setenv('SNIPPY_STORAGE_TYPE', 'misconfig')  # Must be mapped to default.
        osenviron.setenv('SNIPPY_LOG_MSG_MAX', 'misconfig')  # Must be mapped to default.
        osenviron.setenv('SNIPPY_LOG_JSON', '1')  # Must be mapped to True.
        osenviron.setenv('SNIPPY_Q', 'T')  # Must be mapped to True.
        osenviron.setenv('SNIPPY_PROFILE', 'True')
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '199'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--debug'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/v2/')
        assert 'server_base_path=/snippy/api/v2' in caplog.text
        assert 'server_host=127.0.0.1:8081' in caplog.text
        assert 'server_minify_json=True' in caplog.text
        assert 'storage_type=sqlite' in caplog.text
        assert 'log_json=True' in caplog.text       # Debug log settings are twice and both parsing must be correct.
        assert 'json logs: True' in caplog.text     # Debug log settings are twice and both parsing must be correct.
        assert 'log_msg_max=80' in caplog.text      # Debug log settings are twice and both parsing must be correct.
        assert 'log msg max: 80' in caplog.text     # Debug log settings are twice and both parsing must be correct.
        assert 'quiet=True' in caplog.text          # Debug log settings are twice and both parsing must be correct.
        assert 'quiet: True' in caplog.text         # Debug log settings are twice and both parsing must be correct.
        assert 'profiler=True' in caplog.text
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_017(caplog, osenviron):
        """Test server startup with environment and command line config.

        Call GET /api/app/v1 to get Hello response. In this case the server
        options are configured with environment variables and command line
        options. The command line option has higher precedence and they must
        be used.
        """

        osenviron.setenv('SNIPPY_SERVER_BASE_PATH', '/snippy/api/v2')
        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        osenviron.setenv('SNIPPY_SERVER_MINIFY_JSON', 'False')
        osenviron.setenv('SNIPPY_LOG_MSG_MAX', '100')
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '199'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path', '/snippy/api/v3', '--server-minify-json', '--log-msg-max', '20', '--debug'])  # noqa pylint: disable=line-too-long
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/snippy/api/v3/')
        assert 'server_base_path=/snippy/api/v3' in caplog.text
        assert 'server_host=localhost:8080' in caplog.text
        assert 'server_minify_json=True' in caplog.text
        assert 'storage_type=sqlite' in caplog.text
        assert 'log_msg_max=20' in caplog.text      # Debug log settings are twice and both parsing must be correct.
        assert 'log msg max: 20' in caplog.text     # Debug log settings are twice and both parsing must be correct.
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
