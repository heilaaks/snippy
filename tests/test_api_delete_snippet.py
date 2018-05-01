#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""test_api_delete_snippets: Test DELETE snippets API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

pytest.importorskip('gunicorn')


class TestApiDeleteSnippet(object):
    """Test DELETE snippets API."""

    @pytest.mark.usefixtures('default-snippets', 'netcat')
    def test_api_delete_snippet_001(self, server, mocker):
        """Delete snippet with digest.

        Call DELETE /v1/snippets/f3fd167c64b6f97e that matches one snippet
        that is deleted.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        result_headers = {}
        server.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/v1/snippets/f3fd167c64b6f97e',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, server, content_read)

    @pytest.mark.usefixtures('default-snippets', 'netcat', 'caller')
    def test_api_delete_snippet_002(self, server):
        """Try to delete snippet.

        Try to DELETE snippet with resource location that does not exist.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '362'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest beefbeef'
            }]
        }
        server.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/v1/snippets/beefbeef',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 3

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_delete_snippet_003(self, server, mocker):
        """Try to delete snippet.

        Try to call DELETE /snippets without digest identifying delete
        reource.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '364'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot delete snippets without identified resource'
            }]
        }
        server.run()
        assert len(Database.get_contents()) == 2
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, server, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
