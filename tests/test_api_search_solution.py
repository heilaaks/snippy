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

"""test_api_search_solution.py: Test GET /snippy/api/solutions API."""

import sys

import mock
import falcon
from falcon import testing

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.metadata import __version__
from snippy.metadata import __homepage__
from snippy.snip import Snippy
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiSearchSolution(object):
    """Test GET /snippy/api/solutions API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_solutions_with_sall(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search solution from all fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/solutions and search keywords from all fields. The
        ##        search query matches to two solutions and both of them are returned. The
        ##        search is sorted based on one field. The search result limit defined in
        ##        the search query is not exceeded.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '5056'}
        body = {'data': [{'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.BEATS]},
                         {'type': 'solutions', 'id': '2', 'attributes': Solution.DEFAULTS[Solution.NGINX]}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=nginx%2CElastic&limit=20&sort=brief')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/solutions and search keywords from all fields. The
        ##        search query matches to three solutions but limit defined in search query
        ##        results only two of them sorted by the brief field. The sorting must be
        ##        applied before limit is applied. The search is case insensitive and the
        ##        search keywords are stored with initial letters capitalized when the search
        ##        keys are all small letters. The search keywords must still match.
        mock_get_utc_time.side_effect = (Solution.UTC1,)*3 + (Solution.UTC2,)*6 + (None,) # [REF_UTC]
        snippy = Solution.add_defaults(Snippy())
        Solution.add_one(snippy, Solution.KAFKA)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '5056'}
        body = {'data': [{'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.BEATS]},
                         {'type': 'solutions', 'id': '2', 'attributes': Solution.DEFAULTS[Solution.NGINX]}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=debug%2Ctesting&limit=2&sort=brief')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Call GET /snippy/api/v1/solutions and search keywords from all fields. The
        ##        search query matches to two solutions but only one of them is returned because
        ##        the limit parameter was set to one. In this case the sort is descending and
        ##        the last match must be returned. The resulting fields are limited to brief
        ##        and category.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '112'}
        body = {'data': [{'type': 'solutions',
                          'id': '1',
                          'attributes': {field: Solution.DEFAULTS[Solution.NGINX][field] for field in ['brief', 'category']}}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=debug&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/solutions and search keywords from all fields but
        ##        return only two fields. This syntax that separates the sorted fields causes
        ##        the parameter to be processed in string context which must handle multiple
        ##        fields.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '112'}
        body = {'data': [{'type': 'solutions',
                          'id': '1',
                          'attributes': {field: Solution.DEFAULTS[Solution.NGINX][field] for field in ['brief', 'category']}}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=debug&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/solutions and search keywords from all fields. The
        ##        search query matches to three solutions but limit defined in search query
        ##        results only two of them sorted by the utc field in descending order and
        ##        then based on brief field in descending order.
        mock_get_utc_time.side_effect = (Solution.UTC1,)*3 + (Solution.UTC2,)*6 + (None,)  # [REF_UTC]
        snippy = Solution.add_defaults(Snippy())
        Solution.add_one(snippy, Solution.KAFKA)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '7266'}
        body = {'data': [{'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.KAFKA]},
                         {'type': 'solutions', 'id': '2', 'attributes': Solution.DEFAULTS[Solution.NGINX]}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=-utc,-brief')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Call GET /snippy/api/v1/solutions and search keywords from all fields sorted
        ##        with two fields. This syntax that separates the sorted fields causes the
        ##        parameter to be processed in string context which must handle multiple fields.
        mock_get_utc_time.side_effect = (Solution.UTC1,)*3 + (Solution.UTC2,)*6 + (None,)  # [REF_UTC]
        snippy = Solution.add_defaults(Snippy())
        Solution.add_one(snippy, Solution.KAFKA)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '7266'}
        body = {'data': [{'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.KAFKA]},
                         {'type': 'solutions', 'id': '2', 'attributes': Solution.DEFAULTS[Solution.NGINX]}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=-utc%2C-brief')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Try to call GET /snippy/api/v1/solutions with sort parameter set to field
        ##        name that is not existing. The sort must fall to default sorting.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '263'}
        body = {'meta': Solution.get_http_metadata(),
                'errors': [{'status': '400', 'statusString': '400 Bad Request', 'module': 'snippy.testing.testing:123',
                            'title': 'sort option validation failed for non existent field=notexisting'}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_400
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/solutions to return only defined fields. In this case
        ##        the fields are defined by setting the 'fields' parameter multiple times.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '112'}
        body = {'data': [{'type': 'solutions',
                          'id': '1',
                          'attributes': {field: Solution.DEFAULTS[Solution.NGINX][field] for field in ['brief', 'category']}}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=debug&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/solutions with search keywords that do not result any
        ##        results.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '12'}
        body = {'data': []}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_solutions_with_stag(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search solution from tag fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/solutions with search tag keywords that do not result
        ##        any matches.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '12'}
        body = {'data': []}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_solutions_with_sgrp(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search solution from group fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/solutions with search group keywords that do not
        ##        result any matches.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '12'}
        body = {'data': []}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_solutions_with_digest(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search solution with digets."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/solutions/{digest} to get explicit solution based on
        ##        digest. In this case the solution is found.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '2350'}
        body = {'links': {'self': 'http://falconframework.org/snippy/api/v1/solutions/a96accc25dd23ac0'},
                'data': {'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.BEATS]}}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions/a96accc25dd23ac0',  ## apiflow
                                                                    headers={'accept': 'application/json'})
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call GET /snippy/api/v1/solutions/{digest} with digest that cannot be
        ##        found.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '103'}
        body = {'links': {'self': 'http://falconframework.org/snippy/api/v1/solutions/101010101010101'}, 'data': None}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions/101010101010101',  ## apiflow
                                                                    headers={'accept': 'application/json'})
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_solutions_without_parameters(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search solution without search parameters."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/solutions without defining search parameters. In this
        ##        case all content should be returned based on filtering parameters.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '5056'}
        body = {'data': [{'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.BEATS]},
                         {'type': 'solutions', 'id': '2', 'attributes': Solution.DEFAULTS[Solution.NGINX]}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='limit=20&sort=brief')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/solutions without defining search parameters. In this
        ##        case only one solution must be returned because the limit is set to one. Also
        ##        the sorting based on brief field causes the last solution to be returned.
        snippy = Solution.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '2804'}
        body = {'data': [{'type': 'solutions', 'id': '1', 'attributes': Solution.DEFAULTS[Solution.NGINX]}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/solutions',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='limit=1&sort=-brief')
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
