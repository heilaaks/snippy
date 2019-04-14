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

"""test_api_create_solution: Test POST /solutions API."""

import json

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.solution import Solution

pytest.importorskip('gunicorn')


class TestApiCreateSolution(object):
    """Test POST solutions collection API."""

    @staticmethod
    @pytest.mark.usefixtures('create-beats-utc')
    def test_api_create_solution_001(server):
        """Create one solution from API.

        Send POST /v1/solutions to create new solution.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2429'}
        expect_body = {
            'data': [{
                'type': 'solution',
                'id': Content.UUID1,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('create-kafka-utc', 'create-beats-utc')
    def test_api_create_solution_002(server):
        """Create multiple solutions from API.

        Send POST /v1/solutions in list context to create new solutions.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.KAFKA),
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': content['data'][0]
            }, {
                'type': 'solution',
                'attributes': content['data'][1]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7103'
        }
        expect_body = {
            'data': [{
                'type': 'solution',
                'id': Content.UUID1,
                'attributes': content['data'][0]
            }, {
                'type': 'solution',
                'id': Content.UUID2,
                'attributes': content['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_create_solution_003(server):
        """Update solution with POST that maps to PUT.

        Send POST /v1/solutions/[id} to update existing solution with the
        X-HTTP-Method-Override header that overrides the operation as PUT. In
        this case the created timestamp must remain in initial value and the
        updated timestamp must be updated to reflect the update time.

        The UUID must not be changed when the resource is updated because it
        is immutable resource identity used in resource URI.

        Because the method is PUT, it overrides fields that are not defined
        with default values. The filename field is set to empty value because
        of this.
        """


        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['filename'] = ''
        content['data'][0]['created'] = Content.BEATS_TIME
        content['data'][0]['updated'] = Content.NGINX_TIME
        content['data'][0]['uuid'] = Solution.BEATS_UUID
        content['data'][0]['digest'] = '59c5861b51701c2f52abad1a7965e4503875b2668a4df12f6c3386ef9d535970'
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': content['data'][0]['data'],
                    'brief': content['data'][0]['brief'],
                    'description': content['data'][0]['description'],
                    'groups': content['data'][0]['groups'],
                    'tags': content['data'][0]['tags'],
                    'links': content['data'][0]['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3074'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/' + Solution.BEATS_UUID
            },
            'data': {
                'type': 'solution',
                'id': content['data'][0]['uuid'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_create_solution_004(server):
        """Update solution with POST that maps to PATCH.

        Send POST /v1/solutions/db712a82662d6932 to update existing solution
        with X-HTTP-Method-Override header that overrides the operation as
        PATCH.

        The UUID must not be changed when the resource is updated because it
        is immutable resource identity used in resource URI.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['data'] = Solution.NGINX['data']
        content['data'][0]['uuid'] = Solution.BEATS_UUID
        content['data'][0]['digest'] = '02533ef592b8d26c557e1e365b3cc1bd9f54ca5599a5cb5aaf44a54cb7d6a310'
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': content['data'][0]['data'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3144'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/' + Solution.BEATS_UUID
            },
            'data': {
                'type': 'solution',
                'id': content['data'][0]['uuid'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_create_solution_005(server):
        """Update solution with POST that maps to DELETE.

        Send POST /v1/solutions with X-HTTP-Method-Override header to delete
        solution. In this case the resource exists and the content is deleted.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/fffeaf31e98e68a',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_006(server):
        """Try to create solution with resource id.

        Try to send POST /v1/solutions/{id} to create a new solution with
        resource ID in URL. The POST method is not overriden with custom
        X-HTTP-Method-Override header.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '400'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot create resource with id, use x-http-method-override to override the request'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_007(server):
        """Try to create solution with malformed JSON request.

        Try to call POST /v1/solutions to create new solution with malformed
        JSON request. In this case the top level json object is incorrect
        because it contains only an empty list.
        """

        request_body = {
            'data': [{}]
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '845'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '870'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-beats-utc', 'caller')
    def test_api_create_solution_008(server):
        """Create one solution from API.

        Try to call POST /v1/solutions to create new solution with empty
        content data.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': {
                    'data': [],
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '514'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data is empty'
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'no content to be stored'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_solution_009(server):
        """Create one solution from API.

        Call POST /v1/solutions to create new content. In this case every
        attribute has additional leading and trailing whitespaces. Trimming
        must be done all fields with the exception of data field. In case of
        data field, there must be only one newline at the end of solution and
        the extra white spaces must be left as is.

        Tags and links must be sorted after parsing.
        """

        content = {
            'data': [{
                'category': 'solution',
                'data': ('     first row   ', '   second row  ', ''),
                'brief': 'short brief',
                'description': 'long description',
                'name': 'short name',
                'groups': ('python',),
                'tags': ('atabs', 'bspaces'),
                'links': ('alink2', 'blink1'),
                'source': 'short source link',
                'versions': ('versions==1.1-alpha',),
                'filename': 'shortfilename.yaml',
                'created': Content.REGEXP_TIME,
                'updated': Content.REGEXP_TIME,
                'uuid': Content.UUID1,
                'digest': '2fba73d95146c736a2717e18758fd1871ccb9aa68171614435365f5ad5075ba8'
            }]
        }
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': {
                    'data': ['     first row   ', '   second row  ', '', '', ''],
                    'brief': ' short brief  ',
                    'description': ' long description  ',
                    'name': '  short name   ',
                    'groups': ['    python   ',],
                    'tags': ['  bspaces   ', '  atabs    '],
                    'links': ['  blink1  ', '    alink2   '],
                    'source': '  short source link   ',
                    'versions': ['  versions==1.1-alpha   '],
                    'filename': '  shortfilename.yaml   '
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '658'}
        expect_body = {
            'data': [{
                'type': 'solution',
                'id': content['data'][0]['uuid'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
