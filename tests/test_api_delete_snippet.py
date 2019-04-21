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

"""test_api_delete_snippets: Test DELETE /snippets API endpoint."""

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content
from tests.lib.content import Storage
from tests.lib.snippet import Snippet

pytest.importorskip('gunicorn')


class TestApiDeleteSnippet(object):
    """Test DELETE /snippets API endpoint."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_api_delete_snippet_001(server):
        """Delete snippet with digest.

        Send DELETE /snippets/{id} to delete one snippet. The ``id`` in URI
        that matches to one resource that is deleted.
        """

        content = {
            'data': [
                Storage.remove,
                Storage.forced
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/snippets/f3fd167c64b6f97e',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'caller')
    def test_api_delete_snippet_002(server):
        """Try to delete snippet.

        Try to send DELETE /snippet{id} with a ``id`` in URI that does not
        exist.
        """

        content = {
            'data': [
                Storage.remove,
                Storage.forced,
                Storage.netcat,
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '367'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: beefbeef'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/snippets/beefbeef',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_delete_snippet_003(server):
        """Try to delete snippet.

        Try to send DELETE /snippets without ``id`` in URI that identifies
        the delete resource.
        """

        content = {
            'data': [
                Storage.remove,
                Storage.forced
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '365'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot delete content without identified resource'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_delete_snippet_004(server):
        """Delete snippet with UUID.

        Send DELETE /snippets/{id} to delete one snippet. The ``id`` in
        URI matches to one resource that is deleted.
        """

        content = {
            'data': [
                Storage.remove
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/snippets/' + Snippet.FORCED_UUID,
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
