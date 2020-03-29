# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_api_search_solution: Test GET /solutions API endpoint."""

import json
import zlib

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content
from tests.lib.content import Storage
from tests.lib.solution import Solution

pytest.importorskip('gunicorn')

# pylint: disable=unsubscriptable-object
class TestApiSearchSolution(object):  # pylint: disable=too-many-public-methods
    """Test GET /solutions API endpoint."""

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_001(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes. The
        search query matches to two solutions and both of them are returned.
        The search is sorted based on one attribute. The search result limit
        defined in the search query is not exceeded.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4847'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            }, {
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_002(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes. The
        search query matches to three solutions but limit defined in search
        query results only two of them sorted by the brief attribute. The
        sorting must be applied before limit is applied. The search is case
        insensitive and the search keywords are stored with initial letters
        capitalized when the search keys are all small letters. The search
        keywords must still match.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4846'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            }, {
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug%2Ctesting&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_003(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes. The
        search query matches to two solutions but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting
        attributes are limited to brief and category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '205'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': {field: Storage.dnginx[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_004(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes but
        return only two fields. This syntax that separates the sorted fields
        causes the parameter to be processed in string context which must
        handle multiple attributes.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '205'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': {field: Storage.dnginx[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_005(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes. The
        search query matches to three solutions but limit defined in search
        query results only two of them sorted by the created attribute in
        descending order and then based on brief attribute also in descending
        order.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4846'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }, {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker,beats%2Cnmap&limit=2&sort=-created,-brief')
        assert result.headers == expect_headers
        assert result.status == falcon.HTTP_200
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_006(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes sorted
        with two fields. This syntax that separates the sorted fields causes
        the parameter to be processed in string context which must handle
        multiple attributes. In this case the search query matches only to
        two fields.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7065'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_UUID,
                'attributes': Storage.dkafka
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created%2C-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_007(server):
        """Search solution with GET.

        Try to send GET /solutions with sort parameter set to attribute
        name that is not existing. The sort must fall to default sorting.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '385'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'sort option validation failed for non existent field=notexisting'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_008(server):
        """Search solution with GET.

        Send GET /solutions to return only defined attributes. In this case
        the fields are defined by setting the 'fields' parameter multiple
        times.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '205'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': {field: Storage.dnginx[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_009(server):
        """Search solution with GET.

        Try to send GET /solutions with search keywords that do not result
        any results.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '340'
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
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_010(server):
        """Search solution from tag fields.

        Try to send GET /solutions with search tag keywords that do not
        result any matches.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '340'
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
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_011(server):
        """Search solution from group fields.

        Try to send GET /solutions with search group keywords that do not
        result any matches.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '340'
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
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_012(server):
        """Search solution with digets.

        Send GET /api/snippy/rest/solutions/{id} to get explicit solution
        based on digest. In this case the solution is found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2279'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/' + Solution.BEATS_UUID
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_013(server):
        """Search solution with digets.

        Try to send GET /solutions/{id} with digest that cannot be found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '395'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content identity: 101010101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/101010101010101',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_014(server):
        """Search solution without search parameters.

        Send GET /solutions without defining search parameters. In this
        case all content should be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '4847'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            }, {
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_015(server):
        """Search solution without search parameters.

        Send GET /solutions without defining search parameters. In this
        case only one solution must be returned because the limit is set to
        one. Also the sorting based on brief field causes the last solution
        to be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2747'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.parametrize('server', [['server', '--server-host', 'localhost:8080', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_016(server):
        """Search solution with GET.

        Send GET /solutions and search keywords from all attributes. The
        search query matches to two solutions and both of them are returned.
        The response JSON is sent as pretty printed.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7633'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            }, {
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_017(server):
        """Search solution with GET.

        Search solutions and accept gzip compressed response. Note that the
        response length cannot be checked because the compression efficiency
        can change between Python versions. because of this, the response
        lenght is tested only that it should be less than the uncompressed
        response.
        """

        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': Storage.ebeats
            }, {
                'type': 'solution',
                'id': Solution.NGINX_UUID,
                'attributes': Storage.dnginx
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'accept-encoding': 'gzip'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        result_body = zlib.decompress(result.content, 16+zlib.MAX_WBITS).decode("utf-8")
        assert result.status == falcon.HTTP_200
        assert result.headers['content-type'] == 'application/vnd.api+json; charset=UTF-8'
        assert result.headers['content-encoding'] == 'gzip'
        assert int(result.headers['content-length']) < len(result_body)
        Content.assert_restapi(json.loads(result_body), expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_paginate_001(server):
        """Search solution with GET.

        Send GET /solution so that pagination is applied with limit zero.
        This is a special case that returns the metadata but the data list
        is empty. This query uses search all keywords with regexp . (dot)
        which matches to all solutions. The non-zero offset does not affect
        to the total count of query result and it is just returned in the
        meta as it was provided.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '71'
        }
        expect_body = {
            'meta': {
                'count': 0,
                'limit': 0,
                'offset': 4,
                'total': 3
            },
            'data': [],
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=.&offset=4&limit=0&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_001(server):
        """Get specific solution field.

        Send GET /solutions/{id}/data for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1622'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': {
                    'data': Storage.ebeats['data']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/21cd5827-b6ef-4067-b5ac-3ceac07dde9f/data'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430/data',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_002(server):
        """Get specific solution field.

        Send GET /solutions/{id}/brief for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': {
                    'brief': Storage.ebeats['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/21cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_003(server):
        """Get specific solution field.

        Send GET /solutions/{id}/groups for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '232'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': {
                    'groups': Storage.ebeats['groups']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/21cd5827-b6ef-4067-b5ac-3ceac07dde9f/groups'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430/groups',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_004(server):
        """Get specific solution field.

        Send GET /solutions/{id}/tags for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '269'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': {
                    'tags': Storage.ebeats['tags']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/21cd5827-b6ef-4067-b5ac-3ceac07dde9f/tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_005(server):
        """Get specific solution field.

        Send GET /solutions/{id}/lnks for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '309'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_UUID,
                'attributes': {
                    'links': Storage.ebeats['links']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/solutions/21cd5827-b6ef-4067-b5ac-3ceac07dde9f/links'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430/links',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_field_006(server):
        """Get specific solution field.

        Try to send GET /solutions/{id}/notexist for existing solution. In
        this case the field name does not exist.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '360'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'resource field does not exist: notexist'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/4346ba4c79247430/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_field_007(server):
        """Get specific solution field.

        Try to send GET /snippets/{id}/notexist for non existing resource
        with invalid attribute.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '536'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'resource field does not exist: notexist'
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content identity: 0101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/solutions/0101010101/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
