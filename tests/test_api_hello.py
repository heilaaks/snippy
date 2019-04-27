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

"""test_api_hello: Test /hello API endpoints and OPTIONS method."""

from falcon import testing
import falcon
import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.snip import Snippy
from tests.lib.content import Content

pytest.importorskip('gunicorn')


class TestApiHello(object):  # pylint: disable=too-many-public-methods
    """Test /hello API endpoint and OPTIONS method."""

    @staticmethod
    def test_api_hello_api_001(server):
        """Test server hello response.

        Send GET /api/snippy/rest to get the server hello response.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '202'
        }
        expect_body = {'meta': Content.get_api_meta()}
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy/rest')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    def test_api_hello_api_002(server):
        """Test server hello response.

        Send GET /api/snippy/rest/hello to get server hello response.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '202'
        }
        expect_body = {'meta': Content.get_api_meta()}
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy/rest/hello')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    def test_api_hello_api_003(server):
        """Test server hello response.

        Try to send GET / to get server hello response. The server must not
        respond from the root. All API routes start from the base path. This
        avoids possible conflicts when running Snippy with other servers.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json',
            'content-length': '0'
        }
        result = testing.TestClient(server.server.api).simulate_get('/')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_004():
        """Test server hello response.

        Send GET /api/snippy to get server hello response. In this case the
        server base path is changed from default and it is set in correct
        format.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path-rest', '/api/snippy/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_005():
        """Test server hello response.

        Send GET /api/snippy to get server hello response. In this case server
        base path configuration is incorrect. The server base path must contain
        trailing slash which is missing from this test. The configuration must
        be updated automatically and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path-rest', '/api/snippy'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_006():
        """Test server hello response.

        Send GET /api/snippy to get server hello response. In this case server
        base path configuration is incorrect. The server base path must contain
        leading slash which is missing from this test. The configuration must
        be updated and the API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path-rest', 'api/snippy/'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_007():
        """Test server hello response.

        Send GET /api/snippy/ to get server hello response. In this case the
        server base path configuration is incorrect. The server base path must
        contain leading and trailing slashes which are missing from this test.
        In this case the configuration must be updated automatically and the
        API call must work.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path-rest', 'api/snippy'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_008():
        """Test server hello response.

        Send GET /api/snippy/rest/' to get server hello response. In this case
        the server base path is incorrect because it contains two slashes. This
        configuration error results the default base path configuration.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path-rest', '/api//snippy'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy/rest')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_009(caplog):
        """Test server hello response.

        Send GET /api/snippy/rest to get server hello response. In this case
        the server host is changed from the default with command line option.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8081', '--debug'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy/rest')
        assert 'server_host=localhost:8081' in caplog.text
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_010(server):
        """Test HTTP OPTIONS with server hello response.

        Send OPTIONS /api/snippyrest to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_011(server):
        """Test HTTP OPTIONS with server hello response.

        Send OPTIONS /snippets to get allowed methods.
        """

        expect_headers = {
            'allow': 'DELETE,GET,OPTIONS,POST',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest/snippets')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_012(server):
        """Test HTTP OPTIONS with /snippets/{id}.

        Send OPTIONS /snippets/{id} to get allowed methods.
        """

        expect_headers = {
            'allow': 'DELETE,GET,OPTIONS,PATCH,POST,PUT',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest/snippets/123456')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_013(server):
        """Test HTTP OPTIONS with /snippets/{id}/{attribute}.

        Send OPTIONS /snippets/{id}/{field} to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest/snippets/123456/brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_014(server):
        """Test HTTP OPTIONS with /groups API endpoint.

        Send OPTIONS /groups/{groups} to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest/groups/docker')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_015(server):
        """Test HTTP OPTIONS with /tags API endpoint.

        Send OPTIONS /tags/{tag] to get allowed methods.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest/tags/docker')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_016(server):
        """Test HTTP OPTIONS with /groups API endpoint.

        Send OPTIONS /groups to get allowed methods for keywords API. Note
        that this does not call the groups API but keywords API. The reason is
        that the route /groups does not have the parameter and in this case id
        does not lead to /groups but to /{keywords} API.
        """

        expect_headers = {
            'allow': 'GET,OPTIONS',
            'content-length': '0',
            'content-type': 'application/vnd.api+json'
        }
        result = testing.TestClient(server.server.api).simulate_options('/api/snippy/rest/groups')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        assert not result.text

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_017(caplog, osenviron):
        """Test server configuration.

        Send GET /api/snippy/rest/v2 to get server hello response. In this
        case the server variables are changed with environment variables.
        """

        osenviron.setenv('SNIPPY_SERVER_BASE_PATH_REST', '/api/snippy/rest/v2')
        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        osenviron.setenv('SNIPPY_SERVER_MINIFY_JSON', 'True')
        osenviron.setenv('SNIPPY_STORAGE_TYPE', 'misconfig')  # Must be mapped to default.
        osenviron.setenv('SNIPPY_LOG_MSG_MAX', 'misconfig')  # Must be mapped to default.
        osenviron.setenv('SNIPPY_LOG_JSON', '1')  # Must be mapped to True.
        osenviron.setenv('SNIPPY_Q', 'True')  # Must be mapped to True.
        osenviron.setenv('SNIPPY_PROFILE', 'False')
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '202'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--debug'])
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy/rest/v2')
        assert 'server_base_path_rest=/api/snippy/rest/v2' in caplog.text
        assert 'server_host=127.0.0.1:8081' in caplog.text
        assert 'server_minify_json=True' in caplog.text
        assert 'storage_type=sqlite' in caplog.text
        assert 'log_json=True' in caplog.text       # Debug log settings are twice and both parsing must be correct.
        assert 'json logs: True' in caplog.text     # Debug log settings are twice and both parsing must be correct.
        assert 'log_msg_max=80' in caplog.text      # Debug log settings are twice and both parsing must be correct.
        assert 'log msg max: 80' in caplog.text     # Debug log settings are twice and both parsing must be correct.
        assert 'quiet=True' in caplog.text          # Debug log settings are twice and both parsing must be correct.
        assert 'quiet: True' in caplog.text         # Debug log settings are twice and both parsing must be correct.
        assert 'profiler=False' in caplog.text
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('mock-server')
    def test_api_hello_api_018(caplog, osenviron):
        """Test server configuration.

        Send GET /api/snippy/rest/v3 to get server hello response. In this
        case the server options are configured with environment variables
        and command line options. The command line option has higher
        precedence and they must be used.
        """

        osenviron.setenv('SNIPPY_SERVER_BASE_PATH_REST', '/api/snippy/rest/v2')
        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        osenviron.setenv('SNIPPY_SERVER_MINIFY_JSON', 'False')
        osenviron.setenv('SNIPPY_LOG_MSG_MAX', '100')
        osenviron.setenv('SNIPPY_LOG_JSON', '0')  # Must be mapped to False.
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '202'
        }
        expect_body = {'meta': Content.get_api_meta()}
        server = Snippy(['snippy', '--server-host', 'localhost:8080', '--server-base-path-rest', '/api/snippy/rest/v3', '--server-minify-json', '--log-msg-max', '20', '--debug'])  # noqa pylint: disable=line-too-long
        server.run()
        result = testing.TestClient(server.server.api).simulate_get('/api/snippy/rest/v3')
        assert 'server_base_path_rest=/api/snippy/rest/v3' in caplog.text
        assert 'server_host=localhost:8080' in caplog.text
        assert 'server_minify_json=True' in caplog.text
        assert 'storage_type=sqlite' in caplog.text
        assert 'log_msg_max=20' in caplog.text      # Debug log settings are twice and both parsing must be correct.
        assert 'log msg max: 20' in caplog.text     # Debug log settings are twice and both parsing must be correct.
        assert 'log_json=False' in caplog.text      # Debug log settings are twice and both parsing must be correct.
        assert 'json logs: False' in caplog.text    # Debug log settings are twice and both parsing must be correct.
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        server.release()
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'mock-server')
    def test_api_hello_api_019(snippy, osenviron, capsys):
        """Test search operation with server configuration.

        When server is run in a Docker container, it must accept command
        line operations without starting the server. In a Docker container,
        the ``server-host`` setting is always set via environment variable.
        """

        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'redis', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
