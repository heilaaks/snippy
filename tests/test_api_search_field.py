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
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database
from tests.testlib.reference_helper import ReferenceHelper as Reference

pytest.importorskip('gunicorn')


class TestApiSearchField(object):  # pylint: disable=too-many-public-methods
    """Test GET /snippy/api/{field} API."""

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_001(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get all content from the docker group.
        In this case the query matches to three out of four contents.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6120'
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
                'id': '15d1688c970fa336ad6d0b8c705aff18f3d89b49c48e1d6160d77ddccd75f5a8',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_002(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker to get content from the docker and python
        groups with filters and limit applied.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5271'
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
                'id': '15d1688c970fa336ad6d0b8c705aff18f3d89b49c48e1d6160d77ddccd75f5a8',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_003(self, server):
        """Get specific content based on group field.

        Call GET /v1/groups/docker,python to get content from the docker and
        python groups with filters and limit applied. In this case the search
        is limited only to snippet and solution categories and the search hit
        from references should not be returned.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4687'
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
                'id': '15d1688c970fa336ad6d0b8c705aff18f3d89b49c48e1d6160d77ddccd75f5a8',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker,python',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=test&limit=20&sort=brief&scat=snippet,solution')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

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

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '546'
        }
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_005(self, server):
        """Try to get specific content based on group field.

        Try to call GET /v1/groups/missing with a group that is not found.
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
            path='/snippy/api/app/v1/groups/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_006(self, server):
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
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_404

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

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1503'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/groups/docker',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=snippet&uuid=1')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_groups_008(self, server):
        """Get specific content based on group field.

        Try to call GET /v1/groups/docker to get all content from the docker
        group. In this case one of the scat search keywords defining the
        category is not correct and error must be returned.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '558'
        }
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_001(self, server):
        """Get specific content based on tags field.

        Call GET /v1/tags/moby to get all content with a moby tag.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6120'
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
                'id': '15d1688c970fa336ad6d0b8c705aff18f3d89b49c48e1d6160d77ddccd75f5a8',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/tags/moby',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_002(self, server):
        """Get specific content based on tags field.

        Call GET /v1/tags/moby,python to get all content with a volume or
        python tag.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '654'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/tags/volume,python',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_tags_003(self, server):
        """Try to get specific content based on tags field.

        Try to call GET /v1/tags/missing with a tag that is not found.
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
            path='/snippy/api/app/v1/tags/missing',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_digest_001(self, server):
        """Get specific content based on digest.

        Call GET /v1/digest/1f9d949600573 to get specific content based on digest.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '743'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/digest/1f9d9496005736ef'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/digest/1f9d949600573',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_digest_002(self, server):
        """Try to get specific content based on digest.

        Try to call GET /v1/digest/01010101 with a digest that is not found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '381'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content uuid: 01010101 was not unique and matched to: 1 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/digest/01010101',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_uuid_001(self, server):
        """Get specific content based on uuid.

        Call GET /v1/uuid/1f9d949600573 to get specific content based on uuid.
        The self link must be with the full length UUID because it is assumed
        that since user requested with UUID, he/she wants to operate content
        with selected identity.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '761'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_002(self, server):
        """Get specific content based on uuid.

        Try to call GET /v1/uuid/1 that matches multiple contents.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '372'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content uuid: 1 was not unique and matched to: 3 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/1',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_003(self, server):
        """Try to get specific content based on uuid.

        Try to call GET /v1/uuid/01010101 with a uuid that is not found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '379'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content uuid: 01010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/01010101',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_uuid_004(self, server):
        """Get specific content field based on uuid.

        Call GET /v1/uuid/1f9d949600573/brief to get specific content field.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '272'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': {field: Reference.DEFAULTS[Reference.PYTEST][field] for field in ['brief']}
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_uuid_005(self, server):
        """Get specific content field based on uuid.

        Call GET /v1/uuid/1f9d949600573/brief,tags to get specific content
        fields.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '315'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': {field: Reference.DEFAULTS[Reference.PYTEST][field] for field in ['brief', 'tags']}
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief,tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/27cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief,tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_006(self, server):
        """Get specific content field based on uuid.

        Try to call GET /v1/uuid/12345678-b6ef-4067-b5ac-3ceac07dde9f/brief
        to get specific content field with unknown uuid.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '407'
        }
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest', 'caller')
    def test_api_search_uuid_007(self, server):
        """Get specific content field based on uuid.

        Try to call GET /v1/uuid/1/brief to get specific content field. In
        this case the uuid 1 matches to multiple contents and specific field
        cannot be returned. The 404 Not Found is used to simplify the error
        handling instead of using multiple causes. The error title describes
        the error in more detail.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '372'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content uuid: 1 was not unique and matched to: 3 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/uuid/1/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_keyword_001(self, server):
        """Get specific content based on given keywords.

        Call GET /v1/docs,python to get content from any category with
        docs or python keyword.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2087'
        }
        result_json = {
            'meta': {
                'count': 3,
                'limit': 20,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            }, {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]

        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/docs,python',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references', 'default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_keyword_002(self, server):
        """Get specific content based on given keywords.

        Call GET /v1/doc to get content from references category with doc
        keyword.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '654'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            }]

        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/doc',
            headers={'accept': 'application/vnd.api+json'},
            query_string='limit=20&sort=brief&scat=reference')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
