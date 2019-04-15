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

"""test_api_update_solution: Test PUT /solutions API."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution import Solution

pytest.importorskip('gunicorn')


class TestApiUpdateSolution(object):
    """Test PUT /solutions/{digest} API."""

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-kafka-utc')
    def test_api_update_solution_001(server):
        """Update one solution with PUT request.

        Send PUT /v1/solutions/{id} to update existing resource with specified
        digest. See 'updating content attributes' for the attribute list that
        can be changed by client.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.KAFKA)
            ]
        }
        content['data'][0]['filename'] = ''
        content['data'][0]['created'] = Content.BEATS_TIME
        content['data'][0]['updated'] = Content.KAFKA_TIME
        content['data'][0]['uuid'] = Solution.BEATS_UUID
        content['data'][0]['digest'] = '04be0828cd51e173eb7f12620ad79ddab36721ccbd85c3cfbf5218a93e9b1a2e'
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
            'content-length': '4758'
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_update_solution_002(server):
        """Update one solution with PUT request.

        Send PUT /v1/solutions/{id} to update existing resource. The PUT
        request contains only the mandatory data attribute. All other
        attributes must be set to their default values.
        """

        content = {
            'data': [{
                'category': 'solution',
                'data': Solution.NGINX['data'],
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'source': '',
                'versions': (),
                'filename': '',
                'created': Content.BEATS_TIME,
                'updated': Content.NGINX_TIME,
                'uuid': Solution.BEATS_UUID,
                'digest': '6cd48521a898357f5f088c3cd5a8614c6291ef98733cd7e52ab2cdedb146a874'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': content['data'][0]['data'],
                }
            }
        }

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2941'
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_003(server):
        """Update one solution with PUT request.

        Try to send PUT /v1/solutions/{id} to update resource with digest that
        is not found.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Solution.NGINX['data'],
                    'brief': Solution.NGINX['brief'],
                    'groups': Solution.NGINX['groups'],
                    'tags': Solution.NGINX['tags'],
                    'links': Solution.NGINX['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '374'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: 101010101010101'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_004(server):
        """Try to update solution with malformed request.

        Try to send PUT /v1/solutions/{id} to update resource with malformed
        JSON request.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Solution.NGINX['data']),
            'brief': Solution.NGINX['brief'],
            'groups': Solution.NGINX['groups'],
            'tags': Const.DELIMITER_TAGS.join(Solution.NGINX['tags']),
            'links': Const.DELIMITER_LINKS.join(Solution.NGINX['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '5710'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '5568'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_005(server):
        """Try to update solution with malformed request.

        Try to send PUT /v1/solutions/{id} to update resource with a client
        generated resource ID. In this case the ID looks like a valid message
        digest.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        request_body = {
            'data': {
                'type': 'solution',
                'id': '59c5861b51701c2f52abad1a7965e4503875b2668a4df12f6c3386ef9d535970',
                'attributes': {
                    'data': Solution.NGINX['data'],
                    'brief': Solution.NGINX['brief'],
                    'groups': Solution.NGINX['groups'],
                    'tags': Solution.NGINX['tags'],
                    'links': Solution.NGINX['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '384'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '403',
                'statusString': '403 Forbidden',
                'module': 'snippy.testing.testing:123',
                'title': 'client generated resource id is not supported, remove member data.id'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_006(server):
        """Try to update solution with malformed request.

        Try to send PUT /v1/solutions/{id} to update solution with a client
        generated resource ID. In this case the ID is empty string.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'id': '',
                'attributes': {
                    'data': Solution.NGINX['data'],
                    'brief': Solution.NGINX['brief'],
                    'groups': Solution.NGINX['groups'],
                    'tags': Solution.NGINX['tags'],
                    'links': Solution.NGINX['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '384'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '403',
                'statusString': '403 Forbidden',
                'module': 'snippy.testing.testing:123',
                'title': 'client generated resource id is not supported, remove member data.id'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-kafka-utc')
    def test_api_update_solution_007(server):
        """Update one solution with PATCH request.

        Send PATCH /v1/solutions/{id} to update existing resource with digest.
        The PATCH request contains only the mandatory data attribute. All other
        attributes that can be updated must be returned with their previous
        values.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['data'] = Solution.KAFKA['data']
        content['data'][0]['created'] = Content.BEATS_TIME
        content['data'][0]['updated'] = Content.KAFKA_TIME
        content['data'][0]['uuid'] = Solution.BEATS_UUID
        content['data'][0]['digest'] = 'c7b25c6ee326b025c471caa32be285f8c4fc4138593d7cb31a7da63acc36043b'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Solution.KAFKA['data'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4629'
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
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_008(server):
        """Update one solution with PUT request.

        Try to update solution ``uuid`` attribute by sending PUT /v1/solutions.
        This must not work because the uuid cannot be changed by client.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': content['data'][0]['data'],
                    'uuid': '11111111-1111-1111-1111-111111111111'
                }
            }
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '4480'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '4584'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
