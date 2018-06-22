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
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiDeleteSolution(object):
    """Test DELETE solutions API."""

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_delete_solution_001(self, server, mocker):
        """Delete solution with digest.

        Call DELETE /solutions/f3fd167c64b6f97e that matches one solution
        that is deleted.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        result_headers = {}
        assert Database.get_solutions().size() == 3
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/solutions/eeef5ca3ec9cd36',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_204
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, server, content_read)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka', 'caller')
    def test_api_delete_solution_002(self, server):
        """Try to delete solution.

        Try to DELETE solution with resource location that does not exist.
        """
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest: beefbeef'
            }]
        }
        assert Database.get_solutions().size() == 3
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/solutions/beefbeef',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert Database.get_solutions().size() == 3

    @pytest.mark.usefixtures('default-solutions', 'caller')
    def test_api_delete_solution_003(self, server, mocker):
        """Try to delete solution.

        Try to call DELETE /snippets without digest identifying delete
        reource.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot delete content without identified resource'
            }]
        }
        assert Database.get_collection().size() == 2
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, server, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
