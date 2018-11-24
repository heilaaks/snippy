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

"""test_api_create_field: Test POST fields API."""

import json

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference

pytest.importorskip('gunicorn')


class TestApiCreateField(object):
    """Test POST fields API."""

    @pytest.mark.usefixtures('caller')
    def test_api_create_field_001(self, server):
        """Try to create keyword fields from API.

        Try to call not supported POST operation for /v1/keywords.
        """

        content = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG]
            ]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: POST'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_field_002(self, server):
        """Try to create keyword fields from API.

        Try to call not supported POST operation for /v1/keywords that
        is overridden as PUT.
        """

        request_body = {}
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: POST'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_field_003(self, server):
        """Try to create keyword fields from API.

        Try to call not supported POST operation for /v1/keywords that
        is overridden as PATCH.
        """

        request_body = {}
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: POST'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_field_004(self, server):
        """Try to create keyword fields from API.

        Try to call not supported POST operation for /v1/keywords that
        is overridden as DELETE.
        """

        request_body = {}
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: POST'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_field_005(self, server):
        """Try to create groups fields from API.

        Try to call not supported POST operation for /v1/groups.
        """

        content = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG]
            ]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: POST'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/groups/docs',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_field_006(self, server):
        """Try to create tags fields from API.

        Try to call not supported POST operation for /v1/tags.
        """

        content = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG]
            ]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: POST'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/tags/python,docs',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
