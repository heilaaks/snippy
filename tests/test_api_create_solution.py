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

"""test_api_create_solution: Test POST /solutions API."""

import json

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiCreateSolution(object):
    """Test POST solutions collection API."""

    @pytest.mark.usefixtures('beats-utc')
    def test_api_create_solution_001(self, server, mocker):
        """Create one solution from API."""

        ## Brief: Call POST /snippy/api/v1/solutions to create new solution.
        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        content_send = {
            'data': [{
                'type': 'snippet',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2363'}
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(  ## apiflow
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_solutions()) == 1
        Content.verified(mocker, server, content_read)

    @pytest.mark.usefixtures('beats-utc', 'kafka-utc')
    def test_api_create_solutions_002(self, server, mocker):
        """Create multiple solutions from API."""

        ## Brief: Call POST /snippy/api/v1/solutions in list context to create
        ##        new solutions.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            'eeef5ca': Solution.DEFAULTS[Solution.KAFKA]
        }
        content_send = {
            'data': [{
                'type': 'snippet', 'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'snippet', 'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6926'
        }
        result_json = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solutions',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(  ## apiflow
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, server, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
