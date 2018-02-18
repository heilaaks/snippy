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

"""test_api_create_solution.py: Test POST /solutions API."""

import json

from falcon import testing
import falcon
import mock
import pytest

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.snip import Snippy
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiCreateSolution(object):
    """Test POST /solutions API."""

    @pytest.mark.usefixtures('server', 'snippy', 'beats_utc')
    def test_api_create_solution_001(self, snippy, mocker):
        """Create one solution from API."""

        ## Brief: Call POST /snippy/api/v1/solutions to create new solution.
        content_send = {
            'data': [{
                'type': 'snippet',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }]
        }
        content_read = {'a96accc25dd23ac': Solution.DEFAULTS[Solution.BEATS]}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2363'}
        result_body = {
            'data': [{
                'type': 'solutions',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }]
        }
        snippy.run_server()
        result = testing.TestClient(snippy.server.api).simulate_post(  ## apiflow
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_body)
        assert result.status == falcon.HTTP_201
        Content.verified(mocker, snippy, content_read)
        assert 0

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_create_solutions(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Create list of solutions from API."""


        mock_isfile.return_value = True
        mock_get_utc_time.side_effect = (Solution.CREATE_BEATS +
                                         Solution.CREATE_KAFKA +
                                         Solution.TEST_CONTENT*2 +
                                         Solution.TEST_PYTHON2)
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call POST /snippy/api/v1/solutions in list context to create
        ##        new solutions.
        solutions = {'data': [{'type': 'snippet', 'attributes': Solution.DEFAULTS[Solution.BEATS]},
                              {'type': 'snippet', 'attributes': Solution.DEFAULTS[Solution.KAFKA]}]}
        compare_content = {'a96accc25dd23ac': Solution.DEFAULTS[Solution.BEATS],
                           'eeef5ca': Solution.DEFAULTS[Solution.KAFKA]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '6926'}
        body = {'data': [{'type': 'solutions',
                          'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                          'attributes': Solution.DEFAULTS[Solution.BEATS]},
                         {'type': 'solutions',
                          'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                          'attributes': Solution.DEFAULTS[Solution.KAFKA]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/solutions',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(solutions))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_solutions()) == 2
        Solution.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
