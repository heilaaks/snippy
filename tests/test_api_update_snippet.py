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

"""test_api_update_snippet: Test PUT /snippets API."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet

pytest.importorskip('gunicorn')


class TestApiUpdateSnippet(object):
    """Test PUT /snippets/{digest} API."""

    @pytest.mark.usefixtures('import-forced', 'update-exited-utc')
    def test_api_update_snippet_001(self, server):
        """Update one snippet with PUT request.

        Call PUT /v1/snippets/<digest> to update existing snippet with
        specified digest. See 'updating content attributes' for the attribute
        list that can be changed by user.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.DEFAULTS[Snippet.EXITED])
            ]
        }
        content['data'][0]['created'] = Content.FORCED_TIME
        content['data'][0]['updated'] = Content.EXITED_TIME
        content['data'][0]['digest'] = '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73'
        request_body = {
            'data': {
                'type': 'snippet',
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
            'content-length': '1007'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/49d6916b6711f13d'
            },
            'data': {
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_update_snippet_002(self, server):
        """Update one snippet with PUT request.

        Call PUT /v1/snippets/<digest> to update existing snippet with
        specified digest. Only partial set of attributes that can be modified
        is sent in request.
        """

        content = {
            'data': [{
                'data': Snippet.DEFAULTS[Snippet.REMOVE]['data'],
                'brief': '',
                'description': '',
                'groups': Snippet.DEFAULTS[Snippet.REMOVE]['groups'],
                'tags': (),
                'links': Snippet.DEFAULTS[Snippet.REMOVE]['links'],
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': '',
                'source': '',
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': Content.FORCED_TIME,
                'updated': Content.REMOVE_TIME,
                'digest': 'e56c2183edcc3a67cab99e6064439495a8af8a1d0b78bc538acd6079c841f27f'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': content['data'][0]['data'],
                    'groups': content['data'][0]['groups'],
                    'links': Const.DELIMITER_LINKS.join(content['data'][0]['links'],)
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '708'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/e56c2183edcc3a67'
            },
            'data': {
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_update_snippet_003(self, server):
        """Update one snippet with PUT request.

        Call PUT /v1/snippets/<digest> to update existing snippet with
        specified digest. The PUT request contains only the mandatory data
        attribute. All other attributes must be set to their default values.
        """

        content = {
            'data': [{
                'data': Snippet.DEFAULTS[Snippet.REMOVE]['data'],
                'brief': '',
                'description': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': '',
                'source': '',
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': Content.FORCED_TIME,
                'updated': Content.REMOVE_TIME,
                'digest': '26128ea95707a3a2623bb2613a17f50e29a5ab5232b8ba7ca7f1c96cb1ea5c58'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '651'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/26128ea95707a3a2'
            },
            'data': {
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'caller')
    def test_api_update_snippet_004(self, server):
        """Try to update snippet with malformed request.

        Try to call PUT /v1/snippets/<digest> to update snippet with digest
        that cannot be found.
        """

        content = {
            'data': [
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                    'groups': Snippet.DEFAULTS[Snippet.REMOVE]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '370'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest: 101010101010101'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/snippets/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'caller')
    def test_api_update_snippet_005(self, server):
        """Try to update snippet with malformed request.

        Try to call PUT /v1/snippets/<digest> to update new snippet with
        malformed JSON request.
        """

        content = {
            'data': [
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
            'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
            'groups': Snippet.DEFAULTS[Snippet.REMOVE]['groups'],
            'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
            'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '877'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '879'}
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
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers_p3 or result.headers == expect_headers_p2
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-netcat-utc')
    def test_api_update_snippet_006(self, server):
        """Updated snippet and verify created and updated timestamps.

        Call PUT /v1/snippets/<digest> to update existing snippet with
        specified digest. This test verifies that the created timestamp does
        not change and the updated timestamp changes when the content is
        updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.DEFAULTS[Snippet.NETCAT])
            ]
        }
        content['data'][0]['created'] = Content.FORCED_TIME
        content['data'][0]['updated'] = Content.NETCAT_TIME
        content['data'][0]['digest'] = 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(content['data'][0]['data']),
                    'brief': content['data'][0]['brief'],
                    'groups': content['data'][0]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(content['data'][0]['tags']),
                    'links': Const.DELIMITER_LINKS.join(content['data'][0]['links'])
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '770'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/f3fd167c64b6f97e'
            },
            'data': {
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        expect_body['data']['attributes']['updated'] = Content.NETCAT_TIME
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_update_snippet_007(self, server):
        """Update one snippet with PATCH request.

        Call PATCH /v1/snippets/<digest> to update existing snippet with
        specified digest. The PATCH request contains only mandatory the data
        attribute. All other attributes must be returned with their previous
        stored values.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.DEFAULTS[Snippet.FORCED])
            ]
        }
        content['data'][0]['data'] = Snippet.DEFAULTS[Snippet.REMOVE]['data']
        content['data'][0]['created'] = Content.FORCED_TIME
        content['data'][0]['updated'] = Content.REMOVE_TIME
        content['data'][0]['digest'] = 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '894'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/a9e137c08aee0985'
            },
            'data': {
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
