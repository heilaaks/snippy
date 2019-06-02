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

"""test_api_update_snippet: Test PUT /snippets API endpoint."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.content import Request
from tests.lib.content import Storage
from tests.lib.snippet import Snippet

pytest.importorskip('gunicorn')


# pylint: disable=unsupported-assignment-operation, unsubscriptable-object
class TestApiUpdateSnippet(object):
    """Test PUT /snippets API endpoint."""

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-exited-utc')
    def test_api_update_snippet_001(server):
        """Update one snippet with PUT request.

        Send PUT /snippets/{id} to update existing resource with specified
        digest. See 'updating content attributes' for the attribute list that
        can be changed by user.
        """

        storage = {
            'data': [
                Storage.exited
            ]
        }
        storage['data'][0]['created'] = Content.FORCED_TIME
        storage['data'][0]['updated'] = Content.EXITED_TIME
        storage['data'][0]['uuid'] = Snippet.FORCED_UUID
        storage['data'][0]['digest'] = Snippet.EXITED_DIGEST
        request_body = {
            'data': {
                'type': 'snippet',
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
            'content-length': '999'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_update_snippet_002(server):
        """Update one snippet with PUT request.

        Send PUT /snippets/{id} to update existing resource with specified
        digest. Only partial set of attributes that can be modified is sent
        in request.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': Snippet.REMOVE['data'],
                'brief': '',
                'description': '',
                'name': '',
                'groups': Snippet.REMOVE['groups'],
                'tags': (),
                'links': Snippet.REMOVE['links'],
                'source': '',
                'versions': (),
                'filename': '',
                'created': Content.FORCED_TIME,
                'updated': Content.REMOVE_TIME,
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': 'e56c2183edcc3a67cab99e6064439495a8af8a1d0b78bc538acd6079c841f27f'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': storage['data'][0]['data'],
                    'groups': storage['data'][0]['groups'],
                    'links': storage['data'][0]['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '700'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_update_snippet_003(server):
        """Update one snippet with PUT request.

        Send PUT /snippets/{id} to update existing resource with specified
        digest. The PUT request contains only the mandatory data attribute.
        All other attributes must be set to their default values.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': Snippet.REMOVE['data'],
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'source': '',
                'versions': (),
                'filename': '',
                'created': Content.FORCED_TIME,
                'updated': Content.REMOVE_TIME,
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': '26128ea95707a3a2623bb2613a17f50e29a5ab5232b8ba7ca7f1c96cb1ea5c58'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Snippet.REMOVE['data'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '643'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'caller')
    def test_api_update_snippet_004(server):
        """Try to update snippet with malformed request.

        Try to send PUT /snippets/{id} to update resource with digest that
        is not found.
        """

        storage = {
            'data': [
                Storage.forced
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Request.remove['data'],
                    'brief': Request.remove['brief'],
                    'groups': Request.remove['groups'],
                    'tags': Request.remove['tags'],
                    'links': Request.remove['links']
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
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: 101010101010101'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/snippets/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'caller')
    def test_api_update_snippet_005(server):
        """Try to update snippet with malformed request.

        Try to send PUT /snippets/{id} to update snippet with malformed
        JSON request.
        """

        storage = {
            'data': [
                Storage.forced
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Request.remove['data']),
            'brief': Request.remove['brief'],
            'groups': Request.remove['groups'],
            'tags': Const.DELIMITER_TAGS.join(Request.remove['tags']),
            'links': Const.DELIMITER_LINKS.join(Request.remove['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1328'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1371'}
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
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-netcat-utc')
    def test_api_update_snippet_006(server):
        """Updated snippet and verify created and updated timestamps.

        Send PUT /snippets/{id} to update existing resource with specified
        digest. This test verifies that the created timestamp does not change
        and the updated timestamp changes when the content is updated.
        """

        storage = {
            'data': [
                Storage.netcat
            ]
        }
        storage['data'][0]['created'] = Content.FORCED_TIME
        storage['data'][0]['updated'] = Content.NETCAT_TIME
        storage['data'][0]['uuid'] = Snippet.FORCED_UUID
        storage['data'][0]['digest'] = Snippet.NETCAT_DIGEST
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': storage['data'][0]['data'],
                    'brief': storage['data'][0]['brief'],
                    'groups': storage['data'][0]['groups'],
                    'tags': storage['data'][0]['tags'],
                    'links': storage['data'][0]['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '762'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        expect_body['data']['attributes']['updated'] = Content.NETCAT_TIME
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_update_snippet_007(server):
        """Update one snippet with PATCH request.

        Send PATCH /snippets/{id} to update existing resource with specified
        digest. The PATCH request contains only mandatory the data attribute.
        All other attributes must be returned with their previous stored values.
        """

        storage = {
            'data': [
                Storage.forced
            ]
        }
        storage['data'][0]['data'] = Snippet.REMOVE['data']
        storage['data'][0]['created'] = Content.FORCED_TIME
        storage['data'][0]['updated'] = Content.REMOVE_TIME
        storage['data'][0]['uuid'] = Snippet.FORCED_UUID
        storage['data'][0]['digest'] = 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Snippet.REMOVE['data']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '886'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
