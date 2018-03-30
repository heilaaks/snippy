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

"""test_api_search_snippet: Test GET /snippy/api/snippets API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiSearchSnippet(object):
    """Test GET /snippy/api/snippets API."""

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_001(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from
        ##        all fields. The search query matches to two snippets and
        ##        both of them are returned. The search is sorted based on
        ##        one field. The limit defined in the search query is not
        ##        exceeded.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1275'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'netcat', 'exited')
    def test_api_search_snippet_002(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all
        ##        fields. The search query matches to four snippets but limit
        ##        defined in search query results only two of them sorted by
        ##        the brief field. The sorting must be applied before limit is
        ##        applied.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1411'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippets',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_003(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all
        ##        fields. The search query matches to two snippets but only one
        ##        of them is returned because the limit parameter was set to one.
        ##        In this case the sort is descending and the last match must be
        ##        returned. The resulting fields are limited only to brief and
        ##       category.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '188'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_004(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from
        ##        all fields but return only two fields. This syntax that
        ##        separates the sorted fields causes the parameter to be
        ##        processed in string context which must handle multiple
        ##        fields.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '188'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'netcat', 'exited')
    def test_api_search_snippet_005(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from
        ##        all fields. The search query matches to four snippets but
        ##        limit defined in search query results only two of them
        ##        sorted by the utc field in descending order.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1379'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }, {
                'type': 'snippets',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created,-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'netcat', 'exited')
    def test_api_search_snippet_006(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from
        ##        all fields sorted with two fields. This syntax that separates
        ##        the sorted fields causes the parameter to be processed in
        ##        string context which must handle multiple fields.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1379'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }, {
                'type': 'snippets',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created%2C-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_007(self, server):
        """Search snippets with GET."""

        ## Brief: Try to call GET /snippy/api/v1/snippets with sort parameter
        ##        set to field name that does not exist. In this case sorting
        ##        must fall to default sorting.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '380'}
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'sort option validation failed for non existent field=notexisting'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_008(self, server):
        """Search snippets with GET."""

        ## Brief: Call GET /snippy/api/v1/snippets to return only defined
        ##        fields. In this case the fields are defined by setting
        ##        the 'fields' parameter multiple times.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '188'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_009(self, server):
        """Search snippets with GET."""

        ## Brief: Try to call GET /snippy/api/v1/snippets with search keywords
        ##        that do not result any matches.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_010(self, server):
        """Search snippets with GET from tag fields."""

        ## Brief: Try to call GET /snippy/api/v1/snippets with search tag
        ##        keywords that do not result any matches.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_011(self, server):
        """Search snippet from group fields."""

        ## Brief: Call GET /snippy/api/v1/snippets with search group keywords
        ##        that do not result any matches.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_012(self, server):
        """Search snippet with digets."""

        ## Brief: Call GET /snippy/api/v1/snippets/{digest} to get explicit
        ##        snippet based on digest. In this case the snippet is found.
        ##        In this case the URI path contains 15 digit digest. The
        ##        returned self link must contain the default 16 digit digest.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '695'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/snippets/54e41e9b52a02b63'
            },
            'data': {
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets/54e41e9b52a02b6',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_013(self, server):
        """Search snippet with digets."""

        ## Brief: Try to call GET /snippy/api/v1/snippets/{digest} with digest
        ##        that cannot be found. In this case the JSON 'null' is
        ##        converted to Python None.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '334'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resource'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets/101010101010101',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_014(self, server):
        """Search snippet without search parameters."""

        ## Brief: Call GET /snippy/api/v1/snippets without defining search
        ##        parameters. In this case all content should be returned
        ##        based on filtering parameters.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1275'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_015(self, server):
        """Search snippet without search parameters."""

        ## Brief: Call GET /snippy/api/v1/snippets without defining search
        ##        parameters. In this case only one snippet must be returned
        ##        because the limit is set to one. Also the sorting based on
        ##        brief field causes the last snippet to be returned.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '677'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_pytest_fixtures(self, server):
        """Test pytest fixtures with pytest specific mocking."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all
        ##        fields. The search query matches to two snippets and both of
        ##        them are returned. The search is sorted based on one field.
        ##        The limit defined in the search query is not exceeded.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1275'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('remove', 'forced', 'exited', 'netcat')
    def test_pytest_fixtures2(self, server):
        """Test pytest fixtures with pytest specific mocking."""

        ## Brief: Call GET /snippy/api/v1/snippets and search keywords from all
        ##        fields. The search query matches to four snippets but limit
        ##        defined in search query results only two of them sorted by
        ##        the brief field. The sorting must be applied before limit is
        ##        applied.
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1411'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippets',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
