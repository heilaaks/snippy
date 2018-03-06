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

"""test_api_delete_solutions: Test DELETE solutions API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiDeleteSolution(object):
    """Test DELETE solutions API."""

    @pytest.mark.usefixtures('server', 'snippy', 'default-solutions', 'kafka')
    def test_api_delete_solution_001(self, snippy, mocker):
        """Delete solution with DELETE."""

        ## Brief: Call DELETE /snippy/api/v1/solutions with digest parameter
        ##        that matches one solution that is deleted.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        result_headers = {}
        snippy.run_server()
        assert len(Database.get_contents()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(  ## apiflow
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='digest=eeef5ca3ec9cd36')
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('server', 'snippy', 'default-solutions', 'kafka')
    def test_api_delete_solution_002(self, snippy, mocker):
        """Delete solution with digest."""

        ## Brief: Call DELETE /snippy/api/v1/solutions/f3fd167c64b6f97e that
        ##        matches one solution that is deleted.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        result_headers = {}
        snippy.run_server()
        assert len(Database.get_solutions()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(  ## apiflow
            path='/snippy/api/v1/solutions/eeef5ca3ec9cd36',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('server', 'snippy', 'default-solutions', 'kafka', 'caller')
    def test_api_delete_solution_003(self, snippy):
        """Delete solution with digest."""

        ## Brief: Try to DELETE solution with resource location that does
        ##        not exist.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '362'
        }
        result_json = {
            'meta': Solution.get_http_metadata(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest beefbeef'
            }]
        }
        snippy.run_server()
        assert len(Database.get_solutions()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(  ## apiflow
            path='/snippy/api/v1/solutions/beefbeef',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_solutions()) == 3

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
