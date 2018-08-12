#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""test_api_search_reference: Test GET /snippy/api/references API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiSearchReference(object):  # pylint: disable=too-many-public-methods
    """Test GET /snippy/api/references API."""

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_001(self, server):
        """Search reference with GET.

        Call GET /v1/references and search keywords from all attributes. The
        search query matches to two references and both of them are returned.
        The search is sorted based on one attribute. The search result limit
        defined in the search query is not exceeded.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1292'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.GITLOG])
            }, {
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.REGEXP])
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=commit%2Cregular&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_search_reference_002(self, server):
        """Search reference with GET.

        Call GET /v1/references and search keywords from all attributes. The
        search query matches to three references but limit defined in search
        query results only two of them sorted by the brief attribute. The
        sorting must be applied before limit is applied. The search is case
        insensitive and the search keywords are stored with initial letters
        capitalized when the search keys are all small letters. The search
        keywords must still match.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1230'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 3
            },
            'data': [{
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.GITLOG])
            }, {
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.PYTEST])
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=PYTHON%2Cgit&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_003(self, server):
        """Search reference with GET.

        Call GET /v1/references and search keywords from all attributes. The
        search query matches to two references but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting
        attributes are limited to brief and category.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '245'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared({field: Reference.DEFAULTS[Reference.REGEXP][field] for field in ['brief', 'category']})
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=howto&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_004(self, server):
        """Search reference with GET.

        Call GET /v1/references and search keywords from all attributes but
        return only two fields. This syntax that separates the sorted fields
        causes the parameter to be processed in string context which must
        handle multiple attributes.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '245'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared({field: Reference.DEFAULTS[Reference.REGEXP][field] for field in ['brief', 'category']})
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=howto&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_005(self, server):
        """Search reference with GET.

        Call GET /v1/references to return only defined attributes. In this case
        the fields are defined by setting the 'fields' parameter multiple
        times.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '245'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared({field: Reference.DEFAULTS[Reference.REGEXP][field] for field in ['brief', 'category']})
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=howto&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_006(self, server):
        """Search reference with GET.

        Try to call GET /v1/references with search keywords that do not result
        any results.
        """

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
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_007(self, server):
        """Search reference from tag fields.

        Try to call GET /v1/references with search tag keywords that do not
        result any matches.
        """

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
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_008(self, server):
        """Search reference with digets.

        Call GET /snippy/api/app/v1/references/{digest} to get explicit reference
        based on digest. In this case the reference is found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '740'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.GITLOG])
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c20',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_009(self, server):
        """Search reference with digets.

        Try to call GET /v1/references/{digest} with digest that cannot be
        found.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '388'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'content digest: 101010101010101 was not unique and matched to: 0 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/101010101010101',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_010(self, server):
        """Search reference without search parameters.

        Call GET /v1/references without defining search parameters. In this
        case all content should be returned based on filtering parameters.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1292'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.GITLOG])
            }, {
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.REGEXP])
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_011(self, server):
        """Search reference without search parameters.

        Call GET /v1/references without defining search parameters.
        In this case only one reference must be returned because the
        limit is set to one. Also the sorting based on brief field
        causes the last reference to be returned.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '714'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.REGEXP])
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.parametrize('server', [['--server', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_012(self, server):
        """Search reference with GET.

        Call GET /v1/references and search keywords from all attributes. The
        search query matches to two references and both of them are returned.
        The response JSON is sent as pretty printed.

        TODO: The groups refactoring changed the lenght from 2196 to 2278.
              Why so much? Is there a problem in the result JSON?
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2278'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.GITLOG])
            }, {
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': Content.compared(Reference.DEFAULTS[Reference.REGEXP])
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=python%2CGIT&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_search_reference_paginate_001(self, server):
        """Search reference with GET.

        Call GET /v1/reference so that pagination is applied with limit zero.
        This is a special case that returns the metadata but the data list
        is empty. This query uses sall parameter with regexp filter . (dot)
        which matches to all references. The non-zero offset does not affect
        to the total count of query result and it is just returned in the
        meta as it was provided.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '71'
        }
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_001(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/data for existing reference. In this
        case the digest is shorter than the default 16 octet digest.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'data': []
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/data'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c20/data',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_002(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/brief for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '263'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'brief': Reference.DEFAULTS[Reference.GITLOG]['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/brief'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_003(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/groups for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '242'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'groups': Reference.DEFAULTS[Reference.GITLOG]['groups']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/groups'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/groups',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_004(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/tags for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '257'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'tags': Reference.DEFAULTS[Reference.GITLOG]['tags']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/tags'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_005(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/links for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '277'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'links': Reference.DEFAULTS[Reference.GITLOG]['links']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/links'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/links',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_006(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/category for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '250'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'category': Reference.DEFAULTS[Reference.GITLOG]['category']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/category'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/category',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_007(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/name for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '233'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'name': Reference.DEFAULTS[Reference.GITLOG]['name']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/name'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/name',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_008(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/filename for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '241'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'filename': Reference.DEFAULTS[Reference.GITLOG]['filename']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/filename'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/filename',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_009(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/versions for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '241'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'versions': Reference.DEFAULTS[Reference.GITLOG]['versions']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/versions'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/versions',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_010(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/source for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '237'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'source': Reference.DEFAULTS[Reference.GITLOG]['source']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/source'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/source',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references')
    def test_api_search_reference_field_011(self, server):
        """Get specific reference field.

        Call GET /v1/references/<digest>/uuid for existing reference.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '269'
        }
        result_json = {
            'data': {
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': {
                    'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f'
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33/uuid'
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33/uuid',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_field_012(self, server):
        """Get specific reference field.

        Try to call GET /v1/references/<digest>/notexist for existing reference.
        In this case the field name does not exist.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '355'
        }
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_search_reference_field_013(self, server):
        """Get specific reference field.

        Try to call GET /v1/snippets/0101010101/notexist for non existing
        snippet with invalid field.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '529'
        }
        result_json = {
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
                'title': 'content digest 0101010101 was not unique and matched to: 3 resources'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/references/0101010101/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
