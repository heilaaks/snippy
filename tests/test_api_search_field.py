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

"""test_api_search_field: Test GET /resource attribute API."""

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content
from tests.lib.content import Storage
from tests.lib.snippet import Snippet
from tests.lib.solution import Solution
from tests.lib.reference import Reference

pytest.importorskip('gunicorn')


class TestApiSearchField(object):  # pylint: disable=too-many-public-methods
    """Test GET resource attribute API."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_001(server):
        """Get specific content based on ``groups`` attribute.

        Send GET /groups/docker to get all content from the docker group.
        In this case the query matches to three out of four contents.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6163'
        }
        expect_body = {
            'meta': {
                'count': 3,
                'limit': 20,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_UUID,
                'attributes': Storage.dkafka
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_002(server):
        """Get specific content based on ``groups`` attribute.

        Call GET /groups/docker,python to get content from the docker and
        python groups with search all keywords and content limit applied.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5321'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.PYTEST_UUID,
                'attributes': Storage.pytest
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_UUID,
                'attributes': Storage.dkafka
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_003(server):
        """Get specific content based on ``groups`` attribute.

        Call GET /groups/docker,python to get content from the docker and
        python groups with search all keywords and limit applied. In this case
        the search is limited only to snippet and solution categories and the
        search hit from references should not be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4744'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'solution',
                'id': Solution.KAFKA_UUID,
                'attributes': Storage.dkafka
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief&scat=snippet,solution')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_004(server):
        """Get specific content based on ``groups`` attribute.

        Try to call GET /groups/docker,python and limit search to content
        categories defined in plural form. This must not work because only
        singular formas for search category ``scat`` is supported.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '547'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': "search categories: ('snippets', 'solutions') :are not a subset of: ('snippet', 'solution', 'reference')"
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief&scat=snippets,solutions')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_005(server):
        """Try to get specific content based on ``groups`` attribute.

        Try to call GET /groups/missing with a group that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_006(server):
        """Try to get specific content based on ``groups`` attribute.

        Try to call GET /missing/docker with a field name that is not
        found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json',
            'content-length': '0'
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/missing/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_007(server):
        """Get specific content based on ``groups`` attribute.

        Call GET /groups/docker to get all content from the docker group.
        In this case the search query parameter uuid is defined to match
        multiple contents and category is limited to snippets only. This is
        a different situation because the uuid is used as a search parameter,
        not part of the URI. In case URI, a non unique identity like uuid or
        digest must return error. But matching multiple contents with unique
        identity is possible in case of a parameter.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1489'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/docker',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=snippet&uuid=1')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_008(server):
        """Get specific content based on ``groups`` attribute.

        Try to call GET /groups/docker to get all content from the docker
        group. In this case one of the scat search keywords defining the
        category is not correct and error must be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '559'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': "search categories: ('reference', 'snippet', 'solutions') :are not a subset of: ('snippet', 'solution', 'reference')"
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups/docker',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=snippet,solutions,reference&uuid=1')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_001(server):
        """Get specific content based on ``tags`` attribute.

        Call GET /tags/moby to get all content with a moby tag.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6163'
        }
        expect_body = {
            'meta': {
                'count': 3,
                'limit': 20,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_UUID,
                'attributes': Storage.dkafka
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/tags/moby',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_002(server):
        """Get specific content based on ``tags`` attribute.

        Call GET /tags/volume,python to get all content with a volume or
        python tag.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '647'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'reference',
                'id': Reference.PYTEST_UUID,
                'attributes': Storage.pytest
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/tags/volume,python',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_tags_003(server):
        """Try to get specific content based on ``tags`` attribute.

        Try to call GET /tags/missing with a tag that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/tags/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
