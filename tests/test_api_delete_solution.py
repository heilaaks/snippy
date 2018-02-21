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

"""test_api_delete_solutions: Test DELETE /solutions API."""

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


class TestApiDeleteSolution(object):
    """Test DELETE /solutions API."""

    @pytest.mark.usefixtures('server', 'snippy', 'default-solutions', 'kafka')
    def test_api_delete_snippet_001(self, snippy, mocker):
        """Delete solution with DELETE."""

        ## Brief: Call DELETE /snippy/api/v1/solutions with digest parameter
        ##        that matches one solution that is deleted.
        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
                        Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]}
        result_headers = {}
        snippy.run_server()
        assert len(Database.get_solutions()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(  ## apiflow
            path='/snippy/api/v1/solutions',
            headers={'accept': 'application/json'},
            query_string='digest=eeef5ca3ec9cd36')
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_delete_solution_with_digest(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Delete solution with digest."""

        mock_isfile.return_value = True
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call DELETE /snippy/api/v1/solutions/f3fd167c64b6f97e that
        ##        matches one solution that is deleted.
        mock_get_utc_time.side_effect = (Solution.CREATE_BEATS_DEF +
                                         Solution.CREATE_NGINX_DEF +
                                         Solution.CREATE_KAFKA_DEF +
                                         Solution.TEST_PYTHON2)
        snippy = Solution.add_defaults()
        Solution.add_one(Solution.KAFKA, snippy)
        headers = {}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        assert len(Database.get_solutions()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/snippy/api/v1/solutions/eeef5ca3ec9cd36',  ## apiflow
                                                                       headers={'accept': 'application/json'})
        assert result.headers == headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_solutions()) == 2
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to DELETE solution with resource location that does
        ##        not exist.
        mock_get_utc_time.side_effect = (Solution.CREATE_BEATS_DEF +
                                         Solution.CREATE_NGINX_DEF +
                                         Solution.CREATE_KAFKA_DEF +
                                         Solution.TEST_PYTHON2)
        snippy = Solution.add_defaults()
        Solution.add_one(Solution.KAFKA, snippy)
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '362'}
        body = {'meta': Solution.get_http_metadata(),
                'errors': [{'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                            'title': 'cannot find content with message digest beefbeef'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        assert len(Database.get_solutions()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/snippy/api/v1/solutions/beefbeef',  ## apiflow
                                                                       headers={'accept': 'application/json'})
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_solutions()) == 3
        snippy.release()
        snippy = None
        Database.delete_storage()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
