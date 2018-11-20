#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""test_api_create_solution: Test POST /solutions API."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution

pytest.importorskip('gunicorn')


class TestApiCreateSolution(object):
    """Test POST solutions collection API."""

    @pytest.mark.usefixtures('create-beats-utc')
    def test_api_create_solution_001(self, server):
        """Create one solution from API.

        Call POST /v1/solutions to create new solution.
        """

        content = Solution.DEFAULTS[Solution.BEATS]
        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2455'}
        expect_json = {
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': content
            }]
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('create-beats-utc', 'create-kafka-utc')
    def test_api_create_solution_002(self, server):
        """Create multiple solutions from API.

        Call POST /v1/solutions in list context to create new solutions.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7155'
        }
        expect_json = {
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_DIGEST,
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        expect_storage = {
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.KAFKA]
            ]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_create_solution_003(self, server):
        """Update solution with POST that maps to PUT.

        Call POST /v1/solutions/<digest> to update existing solution with the
        X-HTTP-Method-Override header that overrides the operation as PUT. In
        this case the created timestamp must remain in initial value and the
        updated timestamp must be updated to reflect the update time.

        Because the method is PUT, it overrides fields that are not defined
        with default values. The filename field is set to empty value because
        of this.
        """

        content = Content.deepcopy(Solution.DEFAULTS[Solution.NGINX])
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'description': Solution.DEFAULTS[Solution.NGINX]['description'],
                    'groups': Solution.DEFAULTS[Solution.NGINX]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3080'
        }
        expect_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/59c5861b51701c2f'
            },
            'data': {
                'type': 'solution',
                'id': '59c5861b51701c2f52abad1a7965e4503875b2668a4df12f6c3386ef9d535970',
                'attributes': content
            }
        }
        expect_json['data']['attributes']['filename'] = ''
        expect_json['data']['attributes']['created'] = Content.BEATS_TIME
        expect_json['data']['attributes']['updated'] = Content.NGINX_TIME
        expect_json['data']['attributes']['digest'] = '59c5861b51701c2f52abad1a7965e4503875b2668a4df12f6c3386ef9d535970'
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_create_solution_004(self, server):
        """Update solution with POST that maps to PATCH.

        Call POST /v1/solutions/db712a82662d6932 to update existing solution
        with X-HTTP-Method-Override header that overrides the operation as
        PATCH.
        """

        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                }
            }
        }
        content = {
            'data': Solution.DEFAULTS[Solution.NGINX]['data'],
            'brief': Solution.DEFAULTS[Solution.BEATS]['brief'],
            'description': Solution.DEFAULTS[Solution.BEATS]['description'],
            'groups': Solution.DEFAULTS[Solution.BEATS]['groups'],
            'tags': Solution.DEFAULTS[Solution.BEATS]['tags'],
            'links': Solution.DEFAULTS[Solution.BEATS]['links'],
            'category': Solution.DEFAULTS[Solution.BEATS]['category'],
            'name': Solution.DEFAULTS[Solution.BEATS]['name'],
            'filename': Solution.DEFAULTS[Solution.BEATS]['filename'],
            'versions': Solution.DEFAULTS[Solution.BEATS]['versions'],
            'source': Solution.DEFAULTS[Solution.BEATS]['source'],
            'uuid': Solution.DEFAULTS[Solution.BEATS]['uuid'],
            'created': Content.BEATS_TIME,
            'updated': Content.BEATS_TIME,
            'digest': '02533ef592b8d26c557e1e365b3cc1bd9f54ca5599a5cb5aaf44a54cb7d6a310'
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3150'
        }
        expect_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/02533ef592b8d26c'
            },
            'data': {
                'type': 'solution',
                'id': '02533ef592b8d26c557e1e365b3cc1bd9f54ca5599a5cb5aaf44a54cb7d6a310',
                'attributes': content
            }
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_create_solution_005(self, server):
        """Update solution with POST that maps to DELETE.

        Call POST /v1/solutions with X-HTTP-Method-Override header to delete
        solution. In this case the resource exists and the content is deleted.
        """

        expect_headers = {}
        expect_storage = {
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.NGINX]
            ]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/fffeaf31e98e68a',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_006(self, server):
        """Try to create solution with resource id.

        Try to call POST /v1/solutions/<digest> to create new solution with
        resource ID in URL. The POST method is not overriden with custom
        X-HTTP-Method-Override header.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '398'
        }
        expect_json = {
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
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_007(self, server):
        """Try to create solution with malformed JSON request.

        Try to call POST /v1/solutions to create new solution with malformed
        JSON request. In this case the top level json object is incorrect
        because it contains only an empty list.
        """

        request_body = {
            'data': [{}]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '804'
        }
        expect_json = {
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
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-beats-utc', 'caller')
    def test_api_create_solution_008(self, server):
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
            'content-length': '737'
        }
        expect_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data is empty'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data is empty'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data was missing'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_solution_009(self, server):
        """Create one solution from API.

        Call POST /v1/solutions to create new content. In this case every
        attribute has additional leading and trailing whitespaces. Trimming
        must be done all fields with the exception of data field. In case of
        data field, there must be only one newline at the end of solution and
        the extra white spaces must be left as is.

        Tags and links must be sorted after parsing.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': {
                    'data': ['     first row   ', '   second row  ', '', '', ''],
                    'brief': ' short brief  ',
                    'description': ' long description  ',
                    'groups': ['    python   ',],
                    'tags': ['  bspaces   ', '  atabs    '],
                    'links': ['  blink1  ', '    alink2   '],
                    'name': '  short name   ',
                    'filename': '  shortfilename.yaml   ',
                    'versions': '  short versions   ',
                    'source': '  short source link   '
                }
            }]
        }
        content = {
            'data': ['     first row   ', '   second row  ', ''],
            'brief': 'short brief',
            'description': 'long description',
            'groups': ['python'],
            'tags': ['atabs', 'bspaces'],
            'links': ['alink2', 'blink1'],
            'category': 'solution',
            'name': 'short name',
            'filename': 'shortfilename.yaml',
            'versions': 'short versions',
            'source': 'short source link',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.REGEXP_TIME,
            'updated': Content.REGEXP_TIME,
            'digest': '13c08502972d72e0e9b355313bc3b14eddac5c7a80b34ca2b7f401ad57048c61'
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '677'}
        expect_json = {
            'data': [{
                'type': 'solution',
                'id': '13c08502972d72e0e9b355313bc3b14eddac5c7a80b34ca2b7f401ad57048c61',
                'attributes': content
            }]
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
