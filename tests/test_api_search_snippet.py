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

"""test_api_search_snippet.py: Test GET /snippy/api/snippets API."""

import mock
import falcon
from falcon import testing

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.metadata import __version__
from snippy.metadata import __homepage__
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiSearchSnippet(object):
    """Test GET /snippets API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_snippets_with_sall(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search snippet from all fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all fields. The
        ##        search query matches to two snippets and both of them are returned. The
        ##        search is sorted based on one field. The limit defined in the search query
        ##        is not exceeded.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1073'}
        body = {'data': [{'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                         {'type': 'snippets', 'id': '2', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all fields. The
        ##        search query matches to four snippets but limit defined in search query
        ##        results only two of them sorted by the brief field. The sorting must be
        ##        applied before limit is applied.

        # [REF_UTC]: Each content generates 1 or 4 (delete) calls to get UTC time. There are
        #            four contents that are inserted into database and 2 first contain the UTC1
        #            timestamp and the last two the UTC2 timestamp. The None is required in
        #            Python 2.7 which behaves differently than Python 3 which does not require
        #            additional parameter after the last one.
        #
        #            In some cases when there is a test for the content, it includes export
        #            operation that needs one call to UTC timestamp to run the export operation.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*2 + (Snippet.UTC2,)*2 + (None,)
        snippy = Snippet.add_defaults(None)
        Snippet.add_one(snippy, Snippet.EXITED)
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1209'}
        body = {'data': [{'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                         {'type': 'snippets', 'id': '2', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all fields. The
        ##        search query matches to two snippets but only one of them is returned because
        ##        the limit parameter was set to one. In this case the sort is descending and
        ##        the last match must be returned. The resulting fields are limited only to brief
        ##        and category.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '125'}
        body = {'data': [{'type': 'snippets',
                          'id': '1',
                          'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all fields but
        ##        return only two fields. This syntax that separates the sorted fields causes
        ##        the parameter to be processed in string context which must handle multiple
        ##        fields.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '125'}
        body = {'data': [{'type': 'snippets',
                          'id': '1',
                          'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all fields. The
        ##        search query matches to four snippets but limit defined in search query results
        ##        only two of them sorted by the utc field in descending order.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*2 + (Snippet.UTC2,)*2 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults(None)
        Snippet.add_one(snippy, Snippet.EXITED)
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1177'}
        body = {'data': [{'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.NETCAT]},
                         {'type': 'snippets', 'id': '2', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=-utc,-brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all fields sorted
        ##        with two fields. This syntax that separates the sorted fields causes the
        ##        parameter to be processed in string context which must handle multiple fields.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*2 + (Snippet.UTC2,)*2 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults(None)
        Snippet.add_one(snippy, Snippet.EXITED)
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1177'}
        body = {'data': [{'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.NETCAT]},
                         {'type': 'snippets', 'id': '2', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=-utc%2C-brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Try to call GET /snippy/api/v1/snippets with sort parameter set to field
        ##        name that does not exist. In this case sorting must fall to default sorting.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '263'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '400', 'statusString': '400 Bad Request', 'module': 'snippy.testing.testing:123',
                            'title': 'sort option validation failed for non existent field=notexisting'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.headers == headers
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_400
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/snippets to return only defined fields. In this case
        ##        the fields are defined by setting the 'fields' parameter multiple times.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '125'}
        body = {'data': [{'type': 'snippets',
                          'id': '1',
                          'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/snippets with search keywords that do not result any
        ##        matches.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '12'}
        body = {'data': []}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_snippets_with_stag(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search snippet from tag fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/snippets with search tag keywords that do not result
        ##        any matches.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '12'}
        body = {'data': []}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_snippets_with_sgrp(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search snippet from group fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/snippets with search group keywords that do not
        ##        result any matches.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '12'}
        body = {'data': []}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_snippets_with_digest(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search snippet with digets."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/snippets/{digest} to get explicit snippet based on
        ##        digest. In this case the snippet is found. In this case the URI path contains
        ##        15 digit digest. The returned self link must contain the default 16 digit
        #         digest.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '594'}
        body = {'links': {'self': 'http://falconframework.org/snippy/api/v1/snippets/54e41e9b52a02b63'},
                'data': {'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]}}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets/54e41e9b52a02b6',  ## apiflow
                                                                    headers={'accept': 'application/json'})
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call GET /snippy/api/v1/snippets/{digest} with digest that cannot be
        ##        found. In this case the JSON 'null' is converted to Python None.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '102'}
        body = {'links': {'self': 'http://falconframework.org/snippy/api/v1/snippets/101010101010101'}, 'data': None}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets/101010101010101',  ## apiflow
                                                                    headers={'accept': 'application/json'})
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_search_snippets_without_parameters(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Search snippet without search parameters."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /snippy/api/v1/snippets without defining search parameters. In this
        ##        case all content should be returned based on filtering parameters.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1073'}
        body = {'data': [{'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                         {'type': 'snippets', 'id': '2', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='limit=20&sort=brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /snippy/api/v1/snippets without defining search parameters. In this
        ##        case only one snippet must be returned because the limit is set to one. Also
        ##        the sorting based on brief field causes the last snippet to be returned.
        snippy = Snippet.add_defaults(None)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '576'}
        body = {'data': [{'type': 'snippets', 'id': '1', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/snippy/api/v1/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='limit=1&sort=-brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
