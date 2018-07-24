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

"""test_api_search_field: Test GET /snippy/api/{field} API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiSearchField(object):  # pylint: disable=too-many-public-methods
    """Test GET /snippy/api/{field} API."""

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_group_001(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get all content from the docker group.
        In this case the query matches to three out of four contents.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6141'
        }
        result_json = {
            'meta': {
                'count': 3,
                'limit': 20,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }, {
                'type': 'solution',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/group/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_group_002(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get content from the docker and python
        groups with filters and limit applied.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5295'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            }, {
                'type': 'solution',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/group/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_group_003(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get content from the docker and python
        groups with filters and limit applied. In this case the search is
        limited only to snippet and solution categories and the search hit
        from references should not be returned.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4714'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'solution',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/group/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief&scat=snippet,solution')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_group_004(self, server):
        """Try to get specific content based on group field.

        Try to call GET /v1/group/missing with a group that is not found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/group/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_group_005(self, server):
        """Try to get specific content based on group field.

        Try to call GET /v1/missing/docker with a field name that is not
        found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json',
            'content-length': '0'
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/missing/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
