# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

from tests.lib.content import Content
from tests.lib.content import Request
from tests.lib.content import Storage
from tests.lib.solution import Solution

pytest.importorskip('gunicorn')


# pylint: disable=unsupported-assignment-operation, unsubscriptable-object
class TestApiCreateSolution(object):
    """Test POST solutions collection API."""

    @staticmethod
    @pytest.mark.usefixtures('create-beats-utc')
    def test_api_create_solution_001(server):
        """Create one Solution resource.

        Send POST /solutions to create a new resource. Created resource
        is sent in the POST method resource ``data`` attribute as a list of
        objects. The HTTP response must send the created resource in the
        resource ``data`` attribute as list of objects.
        """

        storage = {
            'data': [
                Storage.ebeats
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Request.ebeats
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2109'}
        expect_body = {
            'data': [{
                'type': 'solution',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-kafka-utc', 'create-beats-utc')
    def test_api_create_solution_002(server):
        """Create two Solutions resources.

        Send POST /solutions to create a new reference. Created resource
        is sent in the POST method resource ``data`` attribute as object. The
        HTTP response must send the created resource in the resource ``data``
        attribute as list of objects.
        """

        storage = {
            'data': [
                Storage.dkafka,
                Storage.ebeats
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        storage['data'][1]['uuid'] = Content.UUID2
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Request.dkafka
            }, {
                'type': 'solution',
                'attributes': Request.ebeats
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6427'
        }
        expect_body = {
            'data': [{
                'type': 'solution',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }, {
                'type': 'solution',
                'id': Content.UUID2,
                'attributes': storage['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_create_solution_003(server):
        """Update Solution with POST that maps to PUT.

        Send POST /solutions/{id} to update existing resource with the
        ``X-HTTP-Method-Override`` header that overrides the operation as
        PUT. In this case the created timestamp must remain in initial
        value and the updated timestamp must be updated to reflect the
        update time.

        In this case the resource ``created`` attribute must remain in the
        initial value and the ``updated`` attribute must be set to reflect
        the update time.

        The ``uuid`` attribute must not be changed from it's initial value.

        Because the HTTP method is PUT, it overrides attributes that are
        not defined with default values. The ``filename`` attribute is set
        to empty value because of this.
        """


        storage = {
            'data': [
                Storage.dnginx
            ]
        }
        storage['data'][0]['filename'] = ''
        storage['data'][0]['updated'] = Content.NGINX_TIME
        storage['data'][0]['uuid'] = Solution.BEATS_UUID
        storage['data'][0]['digest'] = '6d102b92af89d6bd6cb65e8d2a6e486dcff2d0fed015ba6b6afde0c99e74b9bc'
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': storage['data'][0]['data'],
                    'brief': storage['data'][0]['brief'],
                    'description': storage['data'][0]['description'],
                    'groups': storage['data'][0]['groups'],
                    'tags': storage['data'][0]['tags'],
                    'links': storage['data'][0]['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2777'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/' + Solution.BEATS_UUID
            },
            'data': {
                'type': 'solution',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_create_solution_004(server):
        """Update solution with POST that maps to PATCH.

        Send POST /solutions/{id} to update existing solution with the
        ``X-HTTP-Method-Override`` header that overrides the operation as
        PATCH.

        The UUID must not be changed when the resource is updated because it
        is immutable resource identity used in resource URI.
        """

        storage = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        storage['data'][0]['data'] = Solution.NGINX['data']
        storage['data'][0]['uuid'] = Solution.BEATS_UUID
        storage['data'][0]['digest'] = '038441c764ac6c4386fcb5a3bdf9b0521e4c0c0535ff5b445d022a83b7419c9a'
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': storage['data'][0]['data'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2847'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/' + Solution.BEATS_UUID
            },
            'data': {
                'type': 'solution',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_create_solution_005(server):
        """Update solution with POST that maps to DELETE.

        Send POST /solutions with the ``X-HTTP-Method-Override`` header to delete
        solution. In this case the resource exists and the content is deleted.
        """

        storage = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions/ee3f2ab7c63d696',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_006(server):
        """Try to create solution with resource id.

        Try to send POST /solutions/{id} to create a new resource with
        resource ID in URL. The POST method is not overriden with custom
        ``X-HTTP-Method-Override`` header.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Request.dnginx
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '403'
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
            path='/api/snippy/rest/solutions/53908d68425c61dc',
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

        Try to send POST /solutions to create new solution with malformed
        JSON request. In this case the top level json object is incorrect
        because it contains only an empty list.
        """

        request_body = {
            'data': [{}]
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '848'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '873'}
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
            path='/api/snippy/rest/solutions',
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

        Try to send POST /solutions to create new a resource with an empty
        resource ``data`` attribute.
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
            'content-length': '367'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'mandatory attribute data for solution is empty'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions',
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

        Send POST /solutions to create a new resource. In this case every
        attribute has additional leading and trailing whitespaces. Trimming
        must be done all fields with the exception of data field. In case of
        data field, there must be only one newline at the end of solution and
        the extra white spaces must be left as is.

        The ``tags`` and ``links`` attributes must be sorted when stored.
        """

        storage = {
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
                'languages': ('python',),
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
                    'languages': ['  python   '],
                    'filename': '  shortfilename.yaml   '
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '683'}
        expect_body = {
            'data': [{
                'type': 'solution',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_010(server):
        """Try to create two solutions.

        Try to send POST /solutions to create two new resources. The second
        resource contains an empty mandatory attribute ``data``. The HTTP
        request must be rejected with an error.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Request.dnginx
            }, {
                'type': 'solution',
                'attributes':{
                    'data': []
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '367'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'mandatory attribute data for solution is empty'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
