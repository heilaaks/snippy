#!/usr/bin/env python3

"""test_api_search_snippets.py: Test GET /snippets API."""

import sys
import unittest
import mock
import falcon
from falcon import testing
from snippy.metadata import __version__
from snippy.metadata import __homepage__
from snippy.snip import Snippy
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiSearchSnippet(unittest.TestCase):
    """Test GET /snippets API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_api_search_snippets_with_sall(self, mock_get_db_location, mock_get_utc_time, mock_isfile, _):
        """Search snippet from all fields."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call GET /api/snippets and search keywords from all columns. The search
        ##        query matches to two snippets and both of them are returned. The search
        ##        is sorted based on one field. The limit defined in the search query is
        ##        not exceeded.
        snippy = Snippet.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '969'}
        body = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/api/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == headers
        print(result.json)
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /api/snippets and search keywords from all columns. The search
        ##        query matches to four snippets but limit defined in search query results
        ##        only two of them sorted by the brief column. The sorting must be applied
        ##        before limit is applied.

        # [REF_UTC]: Each content generates 4 calls to get UTC time. There are 4 contents
        #            that are inserted into database and 2 first contain the UTC1 timestamp
        #            and the last two the UTC2 timestamp. The None is required in Python 2.7
        #            which behaves differently than Python 3 which does not require additional
        #            parameter after the last one.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*8 + (None,)
        snippy = Snippet.add_defaults(Snippy())
        Snippet.add_one(snippy, Snippet.EXITED)
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1105'}
        body = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.EXITED]]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/api/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Call GET /api/snippets and search keywords from all columns. The search
        ##        query matches to two snippets but only one of them is returned because the
        ##        limit parameter was set to one. In this case the sort is descending and the
        ##        last match must be returned. The resulting fields are limited only to brief
        ##        and category.
        snippy = Snippet.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '68'}
        body = [{column: Snippet.DEFAULTS[Snippet.FORCED][column] for column in ['brief', 'category']}]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/api/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call GET /api/snippets and search keywords from all columns. The search
        ##        query matches to four snippets but limit defined in search query results
        ##        only two of them sorted by the utc column in descending order.
        mock_get_utc_time.side_effect = (Snippet.UTC1,)*8 + (Snippet.UTC2,)*8 + (None,)  # [REF_UTC]
        snippy = Snippet.add_defaults(Snippy())
        Snippet.add_one(snippy, Snippet.EXITED)
        Snippet.add_one(snippy, Snippet.NETCAT)
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '1073'}
        body = [Snippet.DEFAULTS[Snippet.NETCAT], Snippet.DEFAULTS[Snippet.EXITED]]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/api/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cnmap&limit=2&sort=-utc,-brief')
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        snippy.release()
        snippy = None
        Database.delete_storage()
        mock_get_utc_time.side_effect = None

        ## Brief: Try to call GET /api/snippets with sort parameter set the column name
        ##        that is not existing. The sort must fall to default sorting.
        snippy = Snippet.add_defaults(Snippy())
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '262'}
        body = {'metadata': Snippet.get_http_metadata(),
                'errors': [{'code': 400, 'status': '400 Bad Request', 'module': 'snippy.config.source.base:334',
                            'message': 'sort option validation failed for non existing field=notexisting'}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_get(path='/api/snippets',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.headers == headers
        assert Snippet.sorted_json(result.json) == Snippet.sorted_json(body)
        assert result.status == falcon.HTTP_400
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
