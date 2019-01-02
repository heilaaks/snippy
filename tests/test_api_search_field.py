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

"""test_api_search_field: Test GET /{field} API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.snippet import Snippet
from tests.testlib.solution import Solution
from tests.testlib.reference import Reference

pytest.importorskip('gunicorn')


class TestApiSearchField(object):  # pylint: disable=too-many-public-methods
    """Test GET /{field} API."""

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_keyword_001(self, server):
        """Get specific content based on given keywords.

        Call GET /v1/docs,python to get content from any category with
        docs or python keyword.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2150'
        }
        expect_body = {
            'meta': {
                'count': 3,
                'limit': 20,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.PYTEST
            }, {
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.REMOVE
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_DIGEST,
                'attributes': Snippet.FORCED
            }]

        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-references', 'default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_keyword_002(self, server):
        """Get specific content based on given keywords.

        Call GET /v1/doc to get content from references category with doc
        keyword.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '675'
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
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.PYTEST
            }]

        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/doc',
            headers={'accept': 'application/vnd.api+json'},
            query_string='limit=20&sort=brief&scat=reference')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_001(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get all content from the docker group.
        In this case the query matches to three out of four contents.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6247'
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
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.REMOVE
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_DIGEST,
                'attributes': Snippet.FORCED
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_DIGEST,
                'attributes': Solution.KAFKA
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_002(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker,python to get content from the docker and
        python groups with search all keywords and content limit applied.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5377'
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
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.PYTEST
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_DIGEST,
                'attributes': Solution.KAFKA
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_003(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker,python to get content from the docker and
        python groups with search all keywords and limit applied. In this case
        the search is limited only to snippet and solution categories and the
        search hit from references should not be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4772'
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
                'id': Solution.KAFKA_DIGEST,
                'attributes': Solution.KAFKA
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief&scat=snippet,solution')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_004(self, server):
        """Get specific content based on group field.

        Try to call GET /v1/groups/docker,python and limit the search to
        content categories defined in plural form. This should not work even
        though this works from the CLI. The reasoning being used is that this
        enforces strict format for the API and it allows more straightforward
        implementation. If the plural forms would be accepted, then question
        would be for example is the result JSON data.type also in plural form
        in this case?
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '546'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': "search categories: ['snippets', 'solutions'] : are not a subset of: ('snippet', 'solution', 'reference')"
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief&scat=snippets,solutions')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_005(self, server):
        """Try to get specific content based on group field.

        Try to call GET /v1/groups/missing with a group that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
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
            path='/snippy/api/app/v1/groups/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_006(self, server):
        """Try to get specific content based on group field.

        Try to call GET /v1/missing/docker with a field name that is not
        found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json',
            'content-length': '0'
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/missing/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_007(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get all content from the docker group.
        In this case the search query parameter uuid is defined to match
        multiple contents and category is limited to snippets only. This is
        a different situation because the uuid is used as a search parameter,
        not part of the URI. In case URI, a non unique identity like uuid or
        digest must return error. But matching multiple contents with unique
        identity is possible in case of a parameter.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1545'
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
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.REMOVE
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_DIGEST,
                'attributes': Snippet.FORCED
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=snippet&uuid=1')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_008(self, server):
        """Get specific content based on group field.

        Try to call GET /v1/groups/docker to get all content from the docker
        group. In this case one of the scat search keywords defining the
        category is not correct and error must be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '558'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': "search categories: ['snippet', 'solutions', 'reference'] : are not a subset of: ('snippet', 'solution', 'reference')"
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=snippet,solutions,reference&uuid=1')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_001(self, server):
        """Get specific content based on tags field.

        Call GET /v1/tags/moby to get all content with a moby tag.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6247'
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
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.REMOVE
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_DIGEST,
                'attributes': Snippet.FORCED
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_DIGEST,
                'attributes': Solution.KAFKA
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/tags/moby',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_002(self, server):
        """Get specific content based on tags field.

        Call GET /v1/tags/volume,python to get all content with a volume or
        python tag.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '675'
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
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.PYTEST
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/tags/volume,python',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_tags_003(self, server):
        """Try to get specific content based on tags field.

        Try to call GET /v1/tags/missing with a tag that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
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
            path='/snippy/api/app/v1/tags/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_digest_001(self, server):
        """Get specific content based on digest.

        Call GET /v1/digest/<digest> to get specific content based on digest.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '764'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.PYTEST
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/digest/1f9d9496005736ef'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/digest/1f9d949600573',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_digest_002(self, server):
        """Try to get specific content based on digest.

        Try to call GET /v1/digest/<digest> with a digest that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '381'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content digest: 01010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/digest/01010101',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_uuid_001(self, server):
        """Get specific content based on uuid.

        Call GET /v1/uuid/<uuid> to get specific content based on uuid. The
        self link must be with the full length UUID because it is assumed
        that since user requested with UUID, he/she wants to operate content
        with selected identity.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '782'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.PYTEST
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_002(self, server):
        """Get specific content based on uuid.

        Try to call GET /v1/uuid/<uuid> that is not unique and it could match
        to multiple contents.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '354'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'unique content uuid: 1 :was not found: 0'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/1',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_003(self, server):
        """Try to get specific content based on uuid.

        Try to call GET /v1/uuid/<uuid> with a uuid that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '361'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'unique content uuid: 01010101 :was not found: 0'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/01010101',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_uuid_004(self, server):
        """Get specific content field based on uuid.

        Call GET /v1/uuid/<uuid>/brief to get specific content field.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '272'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': {field: Reference.PYTEST[field] for field in ['brief']}
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_uuid_005(self, server):
        """Get specific content field based on uuid.

        Call GET /v1/uuid/<uuid>/brief,tags to get specific content fields.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '315'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': {field: Reference.PYTEST[field] for field in ['brief', 'tags']}
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief,tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief,tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_006(self, server):
        """Get specific content field based on uuid.

        Try to call GET /v1/uuid/<uuid>/brief to get specific content field
        with unknown uuid.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '407'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content uuid: 12345678-b6ef-4067-b5ac-3ceac07dde9f was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/12345678-b6ef-4067-b5ac-3ceac07dde9f/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_007(self, server):
        """Get specific content field based on uuid.

        Try to call GET /v1/uuid/<uuid>/brief to get specific content field.
        In this case the uuid 1 matches to multiple contents and specific
        field cannot be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '372'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content uuid: 1 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/1/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
