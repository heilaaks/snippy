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

"""test_api_update_solution.py: Test PUT /solutions API."""

import copy
import json

import mock
import falcon
from falcon import testing

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.metadata import __homepage__
from snippy.metadata import __version__
from snippy.snip import Snippy
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiUpdateSolution(object):
    """Test PUT /solutions/{digest] API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_update_solution_from_api(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Update solution from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call PUT /snippy/api/v1/solutions to update existing solution. In this
        #         case when fields like UTC and filename are not provided, the empty fields
        #         override the content because it was updated with PUT.
        snippy = Solution.add_one(Solution.BEATS)
        solution = {'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])}
        compare_content = {'2cd0e794244a07f': Solution.DEFAULTS[Solution.NGINX]}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '2871'}
        body = {'links': {'self': 'http://falconframework.org/snippy/api/v1/solutions/2cd0e794244a07f8'},
                'data': {'type': 'solutions', 'id': '1', 'attributes': copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])}}
        body['data']['attributes']['filename'] = Const.EMPTY
        body['data']['attributes']['utc'] = Solution.UTC1
        body['data']['attributes']['digest'] = '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d'
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/solutions/a96accc25dd23ac0',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(solution))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_solutions()) == 1
        Solution.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call PUT /snippy/api/v1/solutions to update solution with digest that
        ##        cannot be found.
        snippy = Solution.add_one(Solution.BEATS)
        solution = {'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '252'}
        body = {'meta': Solution.get_http_metadata(),
                'errors': [{'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                            'title': 'cannot find content with message digest 101010101010101'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/solutions/101010101010101',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(solution))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_solutions()) == 1
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
