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

"""test_api_delete_field: Test DELETE fields API."""

import json

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference

pytest.importorskip('gunicorn')


class TestApiDeleteField(object):
    """Test DELETE fields API."""

    @pytest.mark.usefixtures('caller')
    def test_api_delete_field_001(self, server):
        """Try to delete keyword fields from API.

        Try to call not supported DELETE operation for /v1/keywords.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '365'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: DELETE'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_delete_field_002(self, server):
        """Try to delete groups fields from API.

        Try to call not supported DELETE operation for /v1/groups.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '365'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: DELETE'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/groups/docs,python',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_delete_field_003(self, server):
        """Try to delete tags fields from API.

        Try to call not supported DELETE operation for /v1/tags.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '365'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: DELETE'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/tags/5',
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
