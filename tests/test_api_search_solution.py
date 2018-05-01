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

"""test_api_search_solution: Test GET /snippy/api/solutions API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

pytest.importorskip('gunicorn')


class TestApiSearchSolution(object):
    """Test GET /snippy/api/solutions API."""

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_001(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to two solutions and both of them are returned.
        The search is sorted based on one attribute. The search result limit
        defined in the search query is not exceeded.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5258'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions', 'kafka')
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

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5258'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug%2Ctesting&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_003(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to two solutions but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting
        attributes are limited to brief and category.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '175'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': {field: Solution.DEFAULTS[Solution.NGINX][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_004(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes but
        return only two fields. This syntax that separates the sorted fields
        causes the parameter to be processed in string context which must
        handle multiple attributes.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '175'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': {field: Solution.DEFAULTS[Solution.NGINX][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions', 'kafka')
    def test_api_search_solution_005(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to three solutions but limit defined in search
        query results only two of them sorted by the utc attribute in
        descending order and then based on brief attribute in descending
        order.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7468'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }, {
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created,-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions', 'kafka')
    def test_api_search_solution_006(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes sorted
        with two fields. This syntax that separates the sorted fields causes
        the parameter to be processed in string context which must handle
        multiple attributes.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7468'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }, {
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created%2C-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_007(self, server):
        """Search solution with GET.

        Try to call GET /v1/solutions with sort parameter set to attribute
        name that is not existing. The sort must fall to default sorting.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '380'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'sort option validation failed for non existent field=notexisting'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400


    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_008(self, server):
        """Search solution with GET.

        Call GET /v1/solutions to return only defined attributes. In this case
        the fields are defined by setting the 'fields' parameter multiple
        times.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '175'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': {field: Solution.DEFAULTS[Solution.NGINX][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=debug&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_009(self, server):
        """Search solution with GET.

        Try to call GET /v1/solutions with search keywords that do not result
        any results.
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
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_010(self, server):
        """Search solution from tag fields.

        Try to call GET /v1/solutions with search tag keywords that do not
        result any matches.
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
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_011(self, server):
        """Search solution from group fields.

        Try to call GET /v1/solutions with search group keywords that do not
        result any matches.
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
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_012(self, server):
        """Search solution with digets.

        Call GET /snippy/api/v1/solutions/{digest} to get explicit solution
        based on digest. In this case the solution is found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2451'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/solutions/a96accc25dd23ac0'
            },
            'data': {
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_search_solution_013(self, server):
        """Search solution with digets.

        Try to call GET /v1/solutions/{digest} with digest that cannot be
        found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '334'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resource'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions/101010101010101',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_014(self, server):
        """Search solution without search parameters.

        Call GET /v1/solutions without defining search parameters. In this
        case all content should be returned based on filtering parameters.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '5258'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_015(self, server):
        """Search solution without search parameters.

        Call GET /v1/solutions without defining search parameters.
        In this case only one solution must be returned because the
        limit is set to one. Also the sorting based on brief field
        causes the last solution to be returned.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2905'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.parametrize('server', [['--server', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-solutions')
    def test_api_search_solution_016(self, server):
        """Search solution with GET.

        Call GET /v1/solutions and search keywords from all attributes. The
        search query matches to two solutions and both of them are returned.
        The response JSON is sent as pretty printed.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '8198'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solutions',
                'id': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
