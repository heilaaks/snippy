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

"""test_api_search_reference: Test GET /references API endpoint."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.content import Storage
from tests.testlib.reference import Reference

pytest.importorskip('gunicorn')


# pylint: disable=unsubscriptable-object
class TestApiSearchReference(object):  # pylint: disable=too-many-public-methods
    """Test GET /references API."""

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_001(server):
        """Search reference with GET.

        Send GET /v1/references and search keywords from all attributes. The
        search query matches to two references and both of them are returned.
        The search is sorted based on one attribute. The search result limit
        defined in the search query is not exceeded.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1278'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': Storage.gitlog
            }, {
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': Reference.REGEXP
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=commit%2Cregular&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_search_reference_002(server):
        """Search reference with GET.

        Send GET /v1/references and search keywords from all attributes. The
        search query matches to three references but limit defined in search
        query results only two of them sorted by the brief attribute. The
        sorting must be applied before limit is applied. The search is case
        insensitive and the search keywords are stored with initial letters
        capitalized when the search keys are all small letters. The search
        keywords must still match.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1216'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': Storage.gitlog
            }, {
                'type': 'reference',
                'id': Reference.PYTEST_UUID,
                'attributes': Reference.PYTEST
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=PYTHON%2Cgit&limit=2&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_003(server):
        """Search reference with GET.

        Send GET /v1/references and search keywords from all attributes. The
        search query matches to two references but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting
        attributes are limited to brief and category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '217'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': {field: Reference.REGEXP[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=howto&limit=1&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_004(server):
        """Search reference with GET.

        Send GET /v1/references and search keywords from all attributes but
        return only two fields. This syntax that separates the sorted fields
        causes the parameter to be processed in string context which must
        handle multiple attributes.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '217'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': {field: Reference.REGEXP[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=howto&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_005(server):
        """Search reference with GET.

        Send GET /v1/references to return only defined attributes. In this case
        the fields are defined by setting the 'fields' parameter multiple
        times.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '217'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': {field: Reference.REGEXP[field] for field in ['brief', 'category']}
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=howto&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_006(server):
        """Search reference with GET.

        Try to send GET /v1/references with search keywords that do not result
        any results.
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
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_007(server):
        """Search reference from tag fields.

        Try to send GET /v1/references with search tag keywords that do not
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
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_008(server):
        """Search reference with digets.

        Send GET /snippy/api/app/v1/references/{id} to get explicit reference
        based on digest. In this case the reference is found.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '753'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': Storage.gitlog
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/' + Reference.GITLOG_UUID
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c20',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_009(server):
        """Search reference with digets.

        Try to send GET /v1/references/{id} with digest that is not found.
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
            path='/snippy/api/app/v1/references/101010101010101',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_010(server):
        """Search reference without search parameters.

        Send GET /v1/references without defining search keywords. In this case
        all content should be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1278'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': Storage.gitlog
            }, {
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': Reference.REGEXP
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_011(server):
        """Search reference without search parameters.

        Send GET /v1/references without defining search parameters.
        In this case only one reference must be returned because the
        limit is set to one. Also the sorting based on brief field
        causes the last reference to be returned.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '707'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': Reference.REGEXP
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.parametrize('server', [['--server-host', 'localhost:8080', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_012(server):
        """Search reference with GET.

        Send GET /v1/references and search keywords from all attributes. The
        search query matches to two references and both of them are returned.
        The response JSON is sent as pretty printed.

        TODO: The groups refactoring changed the lenght from 2196 to 2278.
              Why so much? Is there a problem in the result JSON?

              This was checked (but what was it?) and this is a left over
              comment?
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2296'
        }
        expect_body = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': Storage.gitlog
            }, {
                'type': 'reference',
                'id': Reference.REGEXP_UUID,
                'attributes': Reference.REGEXP
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=python%2CGIT&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_search_reference_paginate_001(server):
        """Search reference with GET.

        Send GET /v1/reference so that pagination is applied with limit zero.
        This is a special case that returns the metadata but the data list
        is empty. This query uses sall parameter with regexp . (dot) which
        matches to all references. The non-zero offset does not affect to the
        total count of query result and it is just returned in the meta as it
        was provided.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '71'
        }
        expect_body = {
            'meta': {
                'count': 0,
                'limit': 0,
                'offset': 4,
                'total': 3
            },
            'data': [],
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=.&offset=4&limit=0&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_001(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/category for existing reference.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '242'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'category': Storage.gitlog['category']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/category'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/category',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_002(server):
        """Get resource attribute.

        Send GET /v1/references/́{id}/data for existing reference. In this
        case the digest is shorter than the default 16 octet digest.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '225'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'data': []
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/data'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c20/data',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_003(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/brief for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '255'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'brief': Storage.gitlog['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_004(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/description for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '239'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'description': Storage.gitlog['description']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/description'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/description',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_005(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/name for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '225'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'name': Storage.gitlog['name']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/name'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/name',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_006(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/groups for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '234'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'groups': Storage.gitlog['groups']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/groups'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/groups',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_007(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/tags for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '249'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'tags': Storage.gitlog['tags']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_008(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/links for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '269'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'links': Storage.gitlog['links']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/links'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/links',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_009(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/source for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '229'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'source': Storage.gitlog['source']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/source'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/source',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_010(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/versions for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'versions': Storage.gitlog['versions']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/versions'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/versions',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_011(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/filename for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'filename': Storage.gitlog['filename']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/filename'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/filename',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_012(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/created for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '263'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'created': Storage.gitlog['created']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/created'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/created',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_013(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/updated for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '263'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'updated': Storage.gitlog['updated']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/updated'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/updated',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_014(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/uuid for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '261'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'uuid': Reference.GITLOG_UUID
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/uuid'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/uuid',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_015(server):
        """Get resource attribute.

        Send GET /v1/references/{id}/digest for existing resource.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '293'
        }
        expect_body = {
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': {
                    'digest': Reference.GITLOG_DIGEST
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/31cd5827-b6ef-4067-b5ac-3ceac07dde9f/digest'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/digest',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_field_016(server):
        """Get resource attribute.

        Try to send GET /v1/references/{id}/notexist for existing reference.
        In this case the attribute does not exist.
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
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_field_017(server):
        """Get resource attribute.

        Try to send GET /v1/snippets/{id}/notexist for non existing
        snippet with invalid attribute.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '533'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'resource field does not exist: notexist'
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content identity: 0101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/0101010101/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
