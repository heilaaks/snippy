#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_api_search_snippet: Test GET /snippets API endpoint."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.content import Storage
from tests.testlib.snippet import Snippet

pytest.importorskip('gunicorn')


# pylint: disable=unsubscriptable-object
class TestApiSearchSnippet(object):  # pylint: disable=too-many-public-methods
    """Test GET /snippets API."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_001(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all fields. The search
        query matches to two snippets and both of them are returned. The
        search is sorted based on one field. The limit defined in the search
        query is not exceeded.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1489'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_002(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all fields. The search
        query matches to four snippets but limit defined in search query
        results only two of them sorted by the brief field. The sorting must
        be applied before limit is applied.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1624'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_003(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all fields. The search
        query matches to two snippets but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting fields
        are limited only to brief and category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '218'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': {field: Storage.forced[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_004(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all fields but return
        only two fields. This syntax that separates the sorted fields causes
        the parameter to be processed in string context which must handle
        multiple fields.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '218'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': {field: Storage.forced[field] for field in ['brief', 'category']}
            }]
        }

        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_005(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all fields. The search
        query matches to four snippets but limit defined in search query
        results only two of them sorted by the utc field in descending order.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1592'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.NETCAT_UUID,
                'attributes': Storage.netcat
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created,-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_006(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all fields sorted with
        two fields. This syntax that separates the sorted fields causes the
        parameter to be processed in string context which must handle multiple
        fields.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1592'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.NETCAT_UUID,
                'attributes': Storage.netcat
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created%2C-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_007(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets with sort parameter set to field name
        that does not exist. In this case sorting must fall to default
        sorting.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '382'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'sort option validation failed for non existent field=notexisting'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_008(server):
        """Search snippets with GET.

        Send GET /v1/snippets to return only defined fields. In this case the
        fields are defined by setting the 'fields' parameter multiple times.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '218'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': {field: Storage.forced[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_009(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets with search keywords that do not result
        any matches.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_010(server):
        """Search snippets with GET from tag fields.

        Try to send GET /v1/snippets with search tag keywords that do not
        result any matches.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_011(server):
        """Search snippet from groups fields.

        Try to send GET /v1/snippets with search groups keywords that do not
        result any matches.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_012(server):
        """Search snippet with digets.

        Send GET /v1/snippets/{id} to read a snippet based on digest. In this
        case the snippet is found. In this case the URI path contains 15 digit
        digest. The returned self link must be the 16 digit link.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '854'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.REMOVE_UUID
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52a02b6',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_013(server):
        """Search snippet with digets.

        Try to send GET /v1/snippets/{id} with a digest that is not found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '392'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content identity: 101010101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/101010101010101',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_014(server):
        """Search snippet without search parameters.

        Send GET /v1/snippets without defining search parameters. In this
        case all content should be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1489'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_015(server):
        """Search snippet without search parameters.

        Send GET /v1/snippets without defining search parameters. In this
        case only one snippet must be returned because the limit is set to
        one. Also the sorting based on brief field causes the last snippet
        to be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '813'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.parametrize('server', [['--server-host', 'localhost:8080', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_016(server):
        """Search snippets with GET.

        Send GET /v1/snippets and search keywords from all attributes. The
        search query matches to two snippets and both of them are returned.
        The response JSON is sent as pretty printed.

        TODO: The groups refactoring changed the lenght from 2196 to 2278.
              Why so much? Is there a problem in the result JSON?
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2643'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_001(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset is
        zero and limit is bigger that the amount of search results so that
        all results fit into one response. Because all results fit into the
        same response, there is no need for next and prev links and those
        must not be set.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3357'
        }
        expect_body = {
            'meta': {
                'count': 4,
                'limit': 10,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }, {
                'type': 'snippet',
                'id': Snippet.NETCAT_UUID,
                'attributes': Storage.netcat
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=10&offset=0&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=10&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=10&offset=0&sall=docker%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=0&limit=10&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_002(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset is
        zero and limit is smaller that the amount of search results so that
        all results do not fit into one response. Because this is the first
        page, the prev link must not be set.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2076'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=0&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_003(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset is
        non zero and second page is requested. The requested second page is
        the last page. Because of this, there next link must not be set.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1908'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 2,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }, {
                'type': 'snippet',
                'id': Snippet.NETCAT_UUID,
                'attributes': Storage.netcat
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=2&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_004(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset is
        non zero and second page is requested. The requested second page is
        not the last page. In this case the last page has as many hits that
        will fit into one page (even last page). All pagination links must
        be set.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1511'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 1,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=1&offset=1&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=1&offset=0&sall=docker%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/api/snippy/rest/snippets?limit=1&offset=2&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/api/snippy/rest/snippets?limit=1&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=1&offset=3&sall=docker%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=1&limit=1&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_005(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset is
        non zero and second page is requested. The requested second page is
        not the last page. In this case the last page has less items than
        will fit to last page (uneven last page). Also the first page is
        not even and must be correctly set to zero. All pagination links must
        be set.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2255'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 1,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=1&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=1&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_006(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset is
        non zero and the last page is requested. Because original request
        was not started with  offset zero, the first and prev pages are not
        having offset based on limit. In here the offset is also exactly
        the same as total amount of hits.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1164'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 2,
                'offset': 3,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.NETCAT_UUID,
                'attributes': Storage.netcat
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=1&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=3&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'import-umount')
    def test_api_search_snippet_paginate_007(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied. The offset and
        limit are set so that the last page contains less hits than the limit
        and the requested page is not the last or the second last page.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2112'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 5
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }],
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cumount%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=2&sall=docker%2Cumount%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=0&sall=docker%2Cumount%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/api/snippy/rest/snippets?limit=2&offset=4&sall=docker%2Cumount%2Cnmap&sort=brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cumount%2Cnmap&offset=0&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_008(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets with pagination offset that is the same
        as the amount of snippets stored into the database.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=4&limit=2&sort=brief')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_009(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets with pagination offset that is one bigger
        than the maximum amount of hits.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '337'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=10&limit=10&sort=brief')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_010(server):
        """Search snippets with GET.

        Send GET /v1/snippets so that pagination is applied with limit zero.
        This is a special case that returns the metadata but the data list
        is empty.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '71'
        }
        expect_body = {
            'meta': {
                'count': 0,
                'limit': 0,
                'offset': 0,
                'total': 4
            },
            'data': [],
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=0&limit=0&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_011(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets with negative offset.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '361'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search offset is not a positive integer: -4'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=-4&limit=2&sort=brief')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_012(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets with negative offset and limit.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '517'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search result limit is not a positive integer: -2'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search offset is not a positive integer: -4'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=-4&limit=-2&sort=brief')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_013(server):
        """Search snippets with GET.

        Try to send GET /v1/snippets when offset and limit are not numbers.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '530'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search result limit is not a positive integer: 0xdeadbeef'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search offset is not a positive integer: ABCDEFG'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=ABCDEFG&limit=0xdeadbeef&sort=brief')
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_001(server):
        """Get specific snippet field.

        Send GET /v1/snippets/{id}/data for existing snippet.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '267'
        }
        expect_body = {
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': {
                    'data': Storage.remove['data']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/11cd5827-b6ef-4067-b5ac-3ceac07dde9f/data'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52a02b63/data',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_002(server):
        """Get specific snippet field.

        Send GET /v1/snippets/{id}/brief for existing snippet. In this case
        the URI digest is only 10 octets. The returned link must contain 16
        octet digest in the link.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '262'
        }
        expect_body = {
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': {
                    'brief': Storage.remove['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/11cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_003(server):
        """Get specific snippet field.

        Send GET /v1/snippets/{id}/groups for existing snippet.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '231'
        }
        expect_body = {
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': {
                    'groups': Storage.remove['groups']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/11cd5827-b6ef-4067-b5ac-3ceac07dde9f/groups'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52/groups',
            headers={'accept': 'application/vnd.api+json'})
        print(result.json)
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_004(server):
        """Get specific snippet field.

        Send GET /v1/snippets/{id}/tags for existing snippet.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '272'
        }
        expect_body = {
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': {
                    'tags': Storage.remove['tags']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/11cd5827-b6ef-4067-b5ac-3ceac07dde9f/tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_005(server):
        """Get specific snippet field.

        Send GET /v1/snippets/{id}/links for existing snippet.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '279'
        }
        expect_body = {
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': {
                    'links': Storage.remove['links']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/11cd5827-b6ef-4067-b5ac-3ceac07dde9f/links'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52/links',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_field_006(server):
        """Get specific snippet field.

        Try to send GET /v1/snippets/{id}/notexist for existing snippet. In
        this case the field name does not exist.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '357'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'resource field does not exist: notexist'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/54e41e9b52/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_field_007(server):
        """Get specific snippet field.

        Try to send GET /v1/snippets/0101010101/brief for non existing
        snippet with valid field.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '387'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content identity: 0101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/0101010101/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_008(server):
        """Get specific snippet field.

        Send GET /v1/snippets/{id}/brief for existing snippet. In this case
        the URI id is full length UUID that must be found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '251'
        }
        expect_body = {
            'data': {
                'type': 'snippet',
                'id': Storage.forced['uuid'],
                'attributes': {
                    'brief': Storage.forced['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/12cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/12cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_field_009(server):
        """Get specific snippet field.

        Try to send GET /v1/snippets/{id} for existing snippet with short form
        from UUID. The short form must not be accepted and no results must be
        returned. The UUID is intended to be used as fully matching identity.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '413'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content identity: 116cd5827-b6ef-4067-b5ac-3ceac07dde9 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets/116cd5827-b6ef-4067-b5ac-3ceac07dde9',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_pytest_fixtures(server):
        """Test pytest fixtures with pytest specific mocking.

        Send GET /v1/snippets and search keywords from all fields. The search
        query matches to two snippets and both of them are returned. The
        search is sorted based on one field. The limit defined in the search
        query is not exceeded.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1489'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': Storage.forced
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('import-remove', 'import-forced', 'import-exited', 'import-netcat')
    def test_pytest_fixtures2(server):
        """Test pytest fixtures with pytest specific mocking.

        Send GET /v1/snippets and search keywords from all fields. The search
        query matches to four snippets but limit defined in search query
        results only two of them sorted by the brief field. The sorting must
        be applied before limit is applied.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1624'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_UUID,
                'attributes': Storage.remove
            }, {
                'type': 'snippet',
                'id': Snippet.EXITED_UUID,
                'attributes': Storage.exited
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
