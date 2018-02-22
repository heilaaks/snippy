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
import pytest

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiUpdateSolution(object):
    """Test PUT /solutions/{digest] API."""

    @pytest.mark.usefixtures('server', 'snippy', 'beats', 'beats-utc')
    def test_api_update_solution_001(self, snippy, mocker):
        """Update one solution with PUT."""

        ## Brief: Call PUT /snippy/api/v1/solutions to update existing
        ##        solution. In this case when fields like UTC and filename
        ##        are not provided, the empty fields override the content
        ##        because it was updated with PUT. TODO: This is not working
        ##        correctly because fields not defined in update keep their
        ##        original values. A PATCH should behave like in this case.
        content_read = {'2cd0e794244a07f': Solution.DEFAULTS[Solution.NGINX]}
        content_send = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2972'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/solutions/2cd0e794244a07f8'
            },
            'data': {
                'type': 'solutions',
                'id': '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d',
                'attributes': copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])
            }
        }
        # TODO: These fields should be empty because these are not defined
        #       in PUT. The PUT will override the whole content with new
        #       values and if fields are not there, default must be applied.
        result_json['data']['attributes']['filename'] = Const.EMPTY
        result_json['data']['attributes']['created'] = Solution.BEATS_CREATED
        result_json['data']['attributes']['updated'] = Solution.BEATS_CREATED
        result_json['data']['attributes']['digest'] = '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d'
        snippy.run_server()
        result = testing.TestClient(snippy.server.api).simulate_put(  ## apiflow
            path='/snippy/api/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_solutions()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('server', 'snippy', 'caller', 'beats', 'beats-utc')
    def test_api_update_solution_002(self, snippy, mocker):
        """Update one solution with PUT."""

        ## Brief: Try to call PUT /snippy/api/v1/solutions to update solution
        ##        with digest that cannot be found.
        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        content_send = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '369'
        }
        result_json = {
            'meta': Solution.get_http_metadata(),
            'errors': [{
                'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest 101010101010101'
            }]
        }
        snippy.run_server()
        result = testing.TestClient(snippy.server.api).simulate_put(  ## apiflow
            path='/snippy/api/v1/solutions/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_solutions()) == 1
        Content.verified(mocker, snippy, content_read)

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_update_solution_errors(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Try to update solution with malformed queries."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Try to call PUT /snippy/api/v1/solutions to update solution with
        ##        malformed JSON request.
        snippy = Solution.add_one(Solution.BEATS)
        solution = {'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])}
        headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '2707'}
        headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '2708'}
        body = {'meta': Solution.get_http_metadata(),
                'errors': [{'status': '400', 'statusString': '400 Bad Request', 'module': 'snippy.testing.testing:123',
                            'title': 'not compared because of hash structure in random order inside the string'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/solutions/a96accc25dd23ac0',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(solution))
        assert result.headers == headers_p2 or result.headers == headers_p3
        assert Solution.error_body(result.json) == Solution.error_body(body)
        assert result.status == falcon.HTTP_400
        assert len(Database.get_solutions()) == 1
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call PUT /snippy/api/v1/solutions to update solution with
        ##        client generated resource ID. In this case the ID looks like a
        ##        valid message digest.
        snippy = Solution.add_one(Solution.BEATS)
        solution = {'data': {'type': 'snippet',
                             'id': '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d',
                             'attributes': {'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                                            'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                                            'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                                            'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                                            'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])}}}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '382'}
        body = {'meta': Solution.get_http_metadata(),
                'errors': [{'status': '403', 'statusString': '403 Forbidden', 'module': 'snippy.testing.testing:123',
                            'title': 'client generated resource id is not supported, remove member data.id'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/solutions/a96accc25dd23ac0',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(solution))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_403
        assert len(Database.get_solutions()) == 1
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call PUT /snippy/api/v1/solutions to update solution with
        ##        client generated resource ID. In this case the ID is empty string.
        snippy = Solution.add_one(Solution.BEATS)
        solution = {'data': {'type': 'snippet',
                             'id': '',
                             'attributes': {'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                                            'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                                            'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                                            'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                                            'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])}}}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '382'}
        body = {'meta': Solution.get_http_metadata(),
                'errors': [{'status': '403', 'statusString': '403 Forbidden', 'module': 'snippy.testing.testing:123',
                            'title': 'client generated resource id is not supported, remove member data.id'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/solutions/a96accc25dd23ac0',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(solution))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_403
        assert len(Database.get_solutions()) == 1
        snippy.release()
        snippy = None
        Database.delete_storage()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
