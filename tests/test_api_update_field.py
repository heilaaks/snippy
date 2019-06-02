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

"""test_api_update_field: Test PUT fields API endpoint."""

import json

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content
from tests.lib.content import Request

pytest.importorskip('gunicorn')


class TestApiCreateField(object):
    """Test PUT fields API."""

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_update_field_001(server):
        """Try to update ``groups`` from /groups API endpoint.

        Try to send PUT /groups that is not supported.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.gitlog
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '367'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: PUT'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/groups',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_update_field_002(server):
        """"Try to update ``groups`` from /groups API endpoint.

        Try to send PUT /groups/{id} that is not supported.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.gitlog
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json',
            'content-length': '0'
        }
        expect_body = None
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/groups/1',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_update_field_003(server):
        """Try to update ``tags`` from /tags API endpoint.

        Try to send not supported PUT /tags.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.gitlog
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '367'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '405',
                'statusString': '405 Method Not Allowed',
                'module': 'snippy.testing.testing:123',
                'title': 'fields api does not support method: PUT'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/tags',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_405
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
