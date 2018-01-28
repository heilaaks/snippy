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

"""test_api_update_snippet.py: Test PUT /snippets API."""

import json
import sys

import mock
import falcon
from falcon import testing

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.metadata import __homepage__
from snippy.metadata import __version__
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiUpdateSnippet(object):
    """Test PUT /snippets/{digest] API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_update_snippet_from_api(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Update snippet from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call PUT /snippy/api/v1/snippets to update existing snippet.
        snippy = Snippet.add_one(Snippy(), Snippet.FORCED)
        snippet = {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                   'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                   'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                   'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                   'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])}
        compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '594'}
        body = {'links': {'self': 'http://falconframework.org/snippy/api/v1/snippets/54e41e9b52a02b63'},
                'data': {'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]}}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/snippets/53908d68425c61dc',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(snippet))
        print(Database.print_contents())
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Snippet.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call PUT /snippy/api/v1/snippets to update snippet with digest that
        ##        cannot be found.
        snippy = Snippet.add_one(Snippy(), Snippet.FORCED)
        snippet = {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                   'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                   'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                   'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                   'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '252'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                            'title': 'cannot find content with message digest 101010101010101'}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/snippy/api/v1/snippets/101010101010101',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(snippet))
        print(result.json)
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 1
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
