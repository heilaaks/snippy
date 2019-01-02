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

"""test_api_search_solution: Test GET /snippy/api/solutions API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.solution import Solution

pytest.importorskip('gunicorn')


class TestApiSearchSolution(object):  # pylint: disable=too-many-public-methods
    """Test GET /snippy/api/solutions API."""

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_001(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to two solutions and both of them are returned.
        The search is sorted based on one attribute. The search result limit
        defined in the search query is not exceeded.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5518'
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
                'id': Solution.BEATS_DIGEST,
                'attributes': Solution.BEATS
            }, {
                'type': 'solution',
                'id': Solution.NGINX_DIGEST,
                'attributes': Solution.NGINX
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_002(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to three solutions but limit defined in search
        query results only two of them sorted by the brief attribute. The
        sorting must be applied before limit is applied. The search is case
        insensitive and the search keywords are stored with initial letters
        capitalized when the search keys are all small letters. The search
        keywords must still match.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5517'
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
                'id': Solution.BEATS_DIGEST,
                'attributes': Solution.BEATS
            }, {
                'type': 'solution',
                'id': Solution.NGINX_DIGEST,
                'attributes': Solution.NGINX
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug%2Ctesting&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_003(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to two solutions but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting
        attributes are limited to brief and category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
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
                'id': Solution.NGINX_DIGEST,
                'attributes': {field: Solution.NGINX[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_004(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes but
        return only two fields. This syntax that separates the sorted fields
        causes the parameter to be processed in string context which must
        handle multiple attributes.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
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
                'id': Solution.NGINX_DIGEST,
                'attributes': {field: Solution.NGINX[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_005(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to three solutions but limit defined in search
        query results only two of them sorted by the created attribute in
        descending order and then based on brief attribute also in descending
        order.
        """

        content = {
            'data': [
                Solution.NGINX,
                Solution.BEATS
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5517'
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
                'id': Solution.NGINX_DIGEST,
                'attributes': content['data'][0]
            }, {
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': content['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker,beats%2Cnmap&limit=2&sort=-created,-brief')
        assert result.headers == expect_headers
        assert result.status == falcon.HTTP_200
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_006(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes sorted
        with two fields. This syntax that separates the sorted fields causes
        the parameter to be processed in string context which must handle
        multiple attributes. In this case the search query matches only to
        two fields.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7772'
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
                'id': Solution.NGINX_DIGEST,
                'attributes': Solution.NGINX
            }, {
                'type': 'solution',
                'id': Solution.KAFKA_DIGEST,
                'attributes': Solution.KAFKA
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created%2C-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_007(self, server):
        """Search solution with GET.

        Try to call GET /v1/solutions with sort parameter set to attribute
        name that is not existing. The sort must fall to default sorting.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '380'
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
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_008(self, server):
        """Search solution with GET.

        Call GET /v1/solutions to return only defined attributes. In this case
        the fields are defined by setting the 'fields' parameter multiple
        times.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
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
                'id': Solution.NGINX_DIGEST,
                'attributes': {field: Solution.NGINX[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_009(self, server):
        """Search solution with GET.

        Try to call GET /v1/solutions with search keywords that do not result
        any results.
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
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_010(self, server):
        """Search solution from tag fields.

        Try to call GET /v1/solutions with search tag keywords that do not
        result any matches.
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
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_011(self, server):
        """Search solution from group fields.

        Try to call GET /v1/solutions with search group keywords that do not
        result any matches.
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
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_012(self, server):
        """Search solution with digets.

        Call GET /snippy/api/app/v1/solutions/{digest} to get explicit solution
        based on digest. In this case the solution is found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2609'
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
                'id': Solution.BEATS_DIGEST,
                'attributes': Solution.BEATS
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/db712a82662d6932'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/db712a82662d6932',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_013(self, server):
        """Search solution with digets.

        Try to call GET /v1/solutions/{digest} with digest that cannot be
        found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '388'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content digest: 101010101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/101010101010101',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_014(self, server):
        """Search solution without search parameters.

        Call GET /v1/solutions without defining search parameters. In this
        case all content should be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5518'
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
                'id': Solution.BEATS_DIGEST,
                'attributes': Solution.BEATS
            }, {
                'type': 'solution',
                'id': Solution.NGINX_DIGEST,
                'attributes': Solution.NGINX
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_015(self, server):
        """Search solution without search parameters.

        Call GET /v1/solutions without defining search parameters. In this
        case only one solution must be returned because the limit is set to
        one. Also the sorting based on brief field causes the last solution
        to be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3070'
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
                'id': Solution.NGINX_DIGEST,
                'attributes': Solution.NGINX
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.parametrize('server', [['--server', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_016(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to two solutions and both of them are returned.
        The response JSON is sent as pretty printed.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '8632'
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
                'id': Solution.BEATS_DIGEST,
                'attributes': Solution.BEATS
            }, {
                'type': 'solution',
                'id': Solution.NGINX_DIGEST,
                'attributes': Solution.NGINX
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_search_solution_paginate_001(self, server):
        """Search solution with GET.

        Call GET /v1/solution so that pagination is applied with limit zero.
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
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=.&offset=4&limit=0&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_001(self, server):
        """Get specific solution field.

        Call GET /v1/solutions/<digest>/data for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1969'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': {
                    'data': Solution.BEATS['data']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/db712a82662d6932/data'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/db712a82662d6932/data',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_002(self, server):
        """Get specific solution field.

        Call GET /v1/solutions/<digest>/brief for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '256'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': {
                    'brief': Solution.BEATS['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/db712a82662d6932/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/db712a82662d6932/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_003(self, server):
        """Get specific solution field.

        Call GET /v1/solutions/<digest>/groups for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '242'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': {
                    'groups': Solution.BEATS['groups']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/db712a82662d6932/groups'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/db712a82662d6932/groups',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_004(self, server):
        """Get specific solution field.

        Call GET /v1/solutions/<digest>/tags for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '279'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': {
                    'tags': Solution.BEATS['tags']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/db712a82662d6932/tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/db712a82662d6932/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_field_005(self, server):
        """Get specific solution field.

        Call GET /v1/solutions/<digest>/lnks for existing solution.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '319'
        }
        expect_body = {
            'data': {
                'type': 'solution',
                'id': Solution.BEATS_DIGEST,
                'attributes': {
                    'links': Solution.BEATS['links']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/db712a82662d6932/links'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/db712a82662d6932/links',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_field_006(self, server):
        """Get specific solution field.

        Try to call GET /v1/solutions/<digest>/notexist for existing solution.
        In this case the field name does not exist.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '355'
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
            path='/snippy/api/app/v1/solutions/db712a82662d6932/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_field_007(self, server):
        """Get specific solution field.

        Try to call GET /v1/snippets/0101010101/notexist for non existing
        snippet with invalid field.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '529'
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
                'title': 'content digest: 0101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/solutions/0101010101/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
