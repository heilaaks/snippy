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

"""test_api_create_reference: Test POST /references API."""

import json
import sqlite3

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference

pytest.importorskip('gunicorn')


class TestApiCreateReference(object):
    """Test POST references collection API."""

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_001(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new reference. In this case there
        is the resource data object in JSON API request in list context.
        """

        content = Reference.DEFAULTS[Reference.GITLOG]
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '606'}
        expect_json = {
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_DIGEST,
                'attributes': content
            }]
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_002(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new reference. In this case the
        created resource is a resource object without list context in the
        JSON API request data object.
        """

        content = Reference.DEFAULTS[Reference.GITLOG]
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': content
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '606'}
        expect_json = {
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_DIGEST,
                'attributes': content
            }]
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('create-gitlog-utc', 'create-pytest-utc')
    def test_api_create_reference_003(self, server):
        """Create multiple references from API.

        Call POST /v1/references in list context to create new references.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }, {
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.PYTEST]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1209'
        }
        expect_json = {
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_DIGEST,
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }, {
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': Reference.DEFAULTS[Reference.PYTEST]
            }]
        }
        expect_storage = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG],
                Reference.DEFAULTS[Reference.PYTEST]
            ]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        assert Content.ordered(result.json) == Content.ordered(expect_json)
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_create_reference_004(self, server):
        """Update reference with POST that maps to PUT.

        Call POST /v1/references/<digest> to update existing reference with
        X-HTTP-Method-Override header that overrides the operation as PUT. In
        this case the created timestamp must remain in initial value and the
        updated timestamp must be updated to reflect the update time.
        """

        content = Content.deepcopy(Reference.DEFAULTS[Reference.REGEXP])
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
                    'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
                    'groups': Reference.DEFAULTS[Reference.REGEXP]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.REGEXP]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.REGEXP]['links'])
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '767'
        }
        expect_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/cb9225a81eab8ced'
            },
            'data': {
                'type': 'reference',
                'id': Reference.REGEXP_DIGEST,
                'attributes': content
            }
        }
        expect_json['data']['attributes']['created'] = Content.GITLOG_TIME
        expect_json['data']['attributes']['updated'] = Content.REGEXP_TIME
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_create_reference_005(self, server):
        """Update reference with POST that maps to PATCH.

        Call POST /v1/references/<digest> to update existing reference with
        X-HTTP-Method-Override header that overrides the operation as PATCH.
        Only the updated attributes must be changed.
        """

        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
                    'links': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['links']),
                }
            }
        }
        content = {
            'data': Reference.DEFAULTS[Reference.GITLOG]['data'],
            'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
            'description': Reference.DEFAULTS[Reference.REGEXP]['description'],
            'groups': Reference.DEFAULTS[Reference.GITLOG]['groups'],
            'tags': Reference.DEFAULTS[Reference.GITLOG]['tags'],
            'links': Reference.DEFAULTS[Reference.REGEXP]['links'],
            'category': Reference.DEFAULTS[Reference.GITLOG]['category'],
            'name': Reference.DEFAULTS[Reference.GITLOG]['name'],
            'filename': Reference.DEFAULTS[Reference.GITLOG]['filename'],
            'versions': Reference.DEFAULTS[Reference.GITLOG]['versions'],
            'source': Reference.DEFAULTS[Reference.GITLOG]['source'],
            'uuid': Reference.DEFAULTS[Reference.GITLOG]['uuid'],
            'created': Content.GITLOG_TIME,
            'updated': Content.REGEXP_TIME,
            'digest': 'ee4a072a5a7a661a8c5d8e8f2aac88267c47fbf0b26db19b97d0b72bae3d74f0'
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '751'
        }
        expect_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/ee4a072a5a7a661a'
            },
            'data': {
                'type': 'reference',
                'id': 'ee4a072a5a7a661a8c5d8e8f2aac88267c47fbf0b26db19b97d0b72bae3d74f0',
                'attributes': content
            }
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_create_reference_006(self, server):
        """Update reference with POST that maps to DELETE.

        Call POST /v1/references with X-HTTP-Method-Override header to delete
        reference. In this case the resource exists and the content is deleted.
        """

        expect_headers = {}
        expect_storage = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG],
                Reference.DEFAULTS[Reference.REGEXP]
            ]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/1f9d9496005736ef',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('create-gitlog-utc', 'caller')
    def test_api_create_reference_007(self, server):
        """Create one reference from API.

        Try to call POST /v1/references to create new solutuon with empty
        content links. The links are mandatory in case of reference content.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'links': [],
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '559'
        }
        expect_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field links is empty'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because it was matching to an empty template'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-gitlog-utc', 'caller')
    def test_api_create_reference_008(self, server_db):
        """Try to create reference.

        Try to POST new reference when database throws an integrity error from
        uuid column unique constraint violation error. In this case there is
        no content and the digest in error message is not filled.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '706'}
        expect_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '500',
                'statusString': '500 Internal Server Error',
                'module': 'snippy.testing.testing:123',
                'title': 'internal error when searching content possibly violating database unique constraints'
            }, {
                'status': '409',
                'statusString': '409 Conflict',
                'module': 'snippy.testing.testing:123',
                'title': 'content already exist with digest: not found'
            }, {
                'status': '409',
                'statusString': '409 Conflict',
                'module': 'snippy.testing.testing:123',
                'title': 'content already exist with digest: not found'
            }]
        }
        server = server_db[0]
        db_connect = server_db[1]
        db_connect.return_value.commit.side_effect = [sqlite3.IntegrityError('UNIQUE constraint failed: contents.uuid')]
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_500
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_009(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new reference with two groups.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
                    'groups': ['python', 'regexp'],
                    'tags': Reference.DEFAULTS[Reference.REGEXP]['tags'],
                    'links': Reference.DEFAULTS[Reference.REGEXP]['links']
                }
            }]
        }
        content = {
            'data': [],
            'brief': 'Python regular expression',
            'description': '',
            'groups': ['python', 'regexp'],
            'tags': ['howto', 'online', 'python', 'regexp'],
            'links': ['https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/', 'https://pythex.org/'],
            'category': 'reference',
            'name': '',
            'filename': '',
            'versions': '',
            'source': '',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.REGEXP_TIME,
            'updated': Content.REGEXP_TIME,
            'digest': 'e5a94aae97e43273b37142d242e9669b97a899a44b6d73b340b191d3fee4b58a'
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '684'}
        expect_json = {
            'data': [{
                'type': 'reference',
                'id': 'e5a94aae97e43273b37142d242e9669b97a899a44b6d73b340b191d3fee4b58a',
                'attributes': content
            }]
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        assert Content.ordered(result.json) == Content.ordered(expect_json)
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_010(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new content. In this case every
        attribute has additional leading and trailing whitespaces which must
        be trimmed.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'data': ['     first row   ', '   second row  '],
                    'brief': ' short brief  ',
                    'description': ' longer description  ',
                    'groups': ['    python   ',],
                    'tags': ['  spaces   ', '  tabs    '],
                    'links': ['  link1  ', '    link2   '],
                    'name': '  short name   ',
                    'filename': '  shortfilename.yaml   ',
                    'versions': '  short versions   ',
                    'source': '  short source link   '
                }
            }]
        }
        content = {
            'data': [],
            'brief': 'short brief',
            'description': 'longer description',
            'groups': ['python'],
            'tags': ['spaces', 'tabs'],
            'links': ['link1', 'link2'],
            'category': 'reference',
            'name': 'short name',
            'filename': 'shortfilename.yaml',
            'versions': 'short versions',
            'source': 'short source link',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.REGEXP_TIME,
            'updated': Content.REGEXP_TIME,
            'digest': '8d9f1e1e92e358325fce7bea07ab2b77e2ad82cd960a9bc3146d1e3f10d21bc8'
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '635'}
        expect_json = {
            'data': [{
                'type': 'reference',
                'id': '8d9f1e1e92e358325fce7bea07ab2b77e2ad82cd960a9bc3146d1e3f10d21bc8',
                'attributes': content
            }]
        }
        expect_storage = {'data': [content]}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        assert Content.ordered(result.json) == Content.ordered(expect_json)
        Content.assert_restapi(result.json, expect_json)
        Content.assert_storage(expect_storage)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
