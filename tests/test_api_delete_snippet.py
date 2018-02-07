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

"""test_api_delete_snippets.py: Test DELETE /snippets API."""

import mock
import falcon
from falcon import testing

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiDeleteSnippet(object):
    """Test DELETE /snippets API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_delete_snippet_with_digest(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Delete snippet with digest."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call DELETE /snippy/api/v1/snippets with digest parameter that matches
        ##        one snippet that is deleted.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*4 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults()
        Snippet.add_one(Snippet.NETCAT, snippy)
        headers = {}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/snippy/api/v1/snippets',  ## apiflow
                                                                       headers={'accept': 'application/json'},
                                                                       query_string='digest=f3fd167c64b6f97e')
        assert result.headers == headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_snippets()) == 2
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call DELETE /snippy/api/v1/snippets/f3fd167c64b6f97e that matches one
        ##        snippet that is deleted.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*4 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults()
        Snippet.add_one(Snippet.NETCAT, snippy)
        headers = {}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/snippy/api/v1/snippets/f3fd167c64b6f97e',  ## apiflow
                                                                       headers={'accept': 'application/json'})
        assert result.headers == headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_snippets()) == 2
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to DELETE snippet with resource location that does not exist.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*4 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults()
        Snippet.add_one(Snippet.NETCAT, snippy)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '362'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                            'title': 'cannot find content with message digest beefbeef'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(snippy.server.api).simulate_delete(path='/snippy/api/v1/snippets/beefbeef',  ## apiflow
                                                                       headers={'accept': 'application/json'})
        assert result.headers == headers
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 3
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
