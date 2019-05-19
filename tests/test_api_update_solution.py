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
from tests.lib.content import Content
from tests.lib.content import Request
from tests.lib.content import Storage
from tests.lib.solution import Solution

pytest.importorskip('gunicorn')


# pylint: disable=unsupported-assignment-operation, unsubscriptable-object
class TestApiUpdateSolution(object):
    """Test PUT /solutions/{digest} API."""

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-kafka-utc')
    def test_api_update_solution_001(server):
        """Update one solution with PUT request.

        Send PUT /solutions/{id} to update existing resource with specified
        digest. See 'updating content attributes' for the attribute list that
        can be changed by client.
        """

        storage = {
            'data': [
                Storage.dkafka
            ]
        }
        storage['data'][0]['filename'] = ''
        storage['data'][0]['created'] = Content.BEATS_TIME
        storage['data'][0]['updated'] = Content.KAFKA_TIME
        storage['data'][0]['uuid'] = Solution.BEATS_UUID
        storage['data'][0]['digest'] = '0a2b29d2fde6b900375d68be93ac6142c5adafb27fb5d6294fab465090d82504'
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
            'content-length': '4383'
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_update_solution_002(server):
        """Update one solution with PUT request.

        Send PUT /solutions/{id} to update existing resource. The PUT request
        contains only the mandatory data attribute. All other attributes must
        be set to their default values.
        """

        storage = {
            'data': [{
                'category': 'solution',
                'data': Request.dnginx['data'],
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
                'digest': 'd2b737f5be315e098941245b7415b6ef751aef2712daf5a6329366057ec26edc'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': storage['data'][0]['data'],
                }
            }
        }

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2627'
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_003(server):
        """Update one solution with PUT request.

        Try to send PUT /solutions/{id} to update resource with ``id`` in
        URI that is not found.
        """

        storage = {
            'data': [
                Storage.ebeats
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Request.dnginx['data'],
                    'brief': Request.dnginx['brief'],
                    'groups': Request.dnginx['groups'],
                    'tags': Request.dnginx['tags'],
                    'links': Request.dnginx['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '377'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: 101010101010101'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/solutions/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_004(server):
        """Try to update solution with malformed request.

        Try to send PUT /solutions/{id} to update resource with malformed
        JSON request.
        """

        storage = {
            'data': [
                Storage.ebeats
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Request.dnginx['data']),
            'brief': Request.dnginx['brief'],
            'groups': Request.dnginx['groups'],
            'tags': Const.DELIMITER_TAGS.join(Request.dnginx['tags']),
            'links': Const.DELIMITER_LINKS.join(Request.dnginx['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '5090'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '4975'}
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
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_005(server):
        """Try to update solution with malformed request.

        Try to send PUT /solutions/{id} to update resource with a client
        generated resource ID. In this case the ID looks like a valid message
        digest.
        """

        storage = {
            'data': [
                Solution.BEATS
            ]
        }
        request_body = {
            'data': {
                'type': 'solution',
                'id': '59c5861b51701c2f52abad1a7965e4503875b2668a4df12f6c3386ef9d535970',
                'attributes': {
                    'data': Request.dnginx['data'],
                    'brief': Request.dnginx['brief'],
                    'groups': Request.dnginx['groups'],
                    'tags': Request.dnginx['tags'],
                    'links': Request.dnginx['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '387'
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
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_006(server):
        """Try to update solution with malformed request.

        Try to send PUT /solutions/{id} to update solution with a client
        generated resource ID. In this case the ID is empty string.
        """

        storage = {
            'data': [
                Storage.ebeats
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'id': '',
                'attributes': {
                    'data': Request.dnginx['data'],
                    'brief': Request.dnginx['brief'],
                    'groups': Request.dnginx['groups'],
                    'tags': Request.dnginx['tags'],
                    'links': Request.dnginx['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '387'
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
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'update-kafka-utc')
    def test_api_update_solution_007(server):
        """Update one solution with PATCH request.

        Send PATCH /solutions/{id} to update existing resource with digest.
        The PATCH request contains only the mandatory data attribute. All other
        attributes that can be updated must be returned with their previous
        values.
        """

        storage = {
            'data': [
                Storage.ebeats
            ]
        }
        storage['data'][0]['data'] = Solution.KAFKA['data']
        storage['data'][0]['created'] = Content.BEATS_TIME
        storage['data'][0]['updated'] = Content.KAFKA_TIME
        storage['data'][0]['uuid'] = Solution.BEATS_UUID
        storage['data'][0]['digest'] = 'd8271fa72ab79e877fd977ae66019b1afc86826a93530b28c3756077a8ace067'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Request.dkafka['data'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4254'
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
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_008(server):
        """Update one solution with PUT request.

        Try to update solution ``uuid`` attribute by sending PUT /solutions.
        This must not work because the ``uuid`` cannot be changed by client.
        """

        storage = {
            'data': [
                Storage.ebeats
            ]
        }
        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': storage['data'][0]['data'],
                    'uuid': '11111111-1111-1111-1111-111111111111'
                }
            }
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '3813'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '3905'}
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
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
