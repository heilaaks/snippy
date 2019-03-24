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

"""test_api_create_reference: Test POST /references API."""

import json
import sqlite3

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.helper import Helper
from tests.testlib.reference import Reference

pytest.importorskip('gunicorn')


class TestApiCreateReference(object):
    """Test POST references collection API."""

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_001(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new referece. The created reference
        is sent in the POST request 'data' attribute as a list of reference
        objects.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '608'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_002(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new reference. The created reference
        is sent in the POST request 'data' attribute as a plain object. The
        response that contains the created reference must be received as a list
        of reference objects.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': content['data'][0]
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '608'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Reference.GITLOG_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-pytest-utc', 'create-gitlog-utc')
    def test_api_create_reference_003(self, server):
        """Create multiple references from API.

        Call POST /v1/references in list context to create new references.
        """

        content = {
            'data': [
                Reference.PYTEST,
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }, {
                'type': 'reference',
                'attributes': content['data'][1]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1213'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Reference.PYTEST_DIGEST,
                'attributes': content['data'][0]
            }, {
                'type': 'reference',
                'id': Reference.GITLOG_DIGEST,
                'attributes': content['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_create_reference_004(self, server):
        """Update reference with POST that maps to PUT.

        Call POST /v1/references/<digest> to update existing reference with
        X-HTTP-Method-Override header that overrides the operation as PUT. In
        this case the created timestamp must remain in initial value and the
        updated timestamp must be updated to reflect the update time.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': content['data'][0]
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '769'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/cb9225a81eab8ced'
            },
            'data': {
                'type': 'reference',
                'id': Reference.REGEXP_DIGEST,
                'attributes': content['data'][0]
            }
        }
        expect_body['data']['attributes']['created'] = Content.GITLOG_TIME
        expect_body['data']['attributes']['updated'] = Content.REGEXP_TIME
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_create_reference_005(self, server):
        """Update reference with POST that maps to PATCH.

        Call POST /v1/references/<digest> to update existing reference with
        X-HTTP-Method-Override header that overrides the operation as PATCH.
        Only the updated attributes must be changed.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['brief'] = Reference.REGEXP['brief']
        content['data'][0]['description'] = Reference.REGEXP['description']
        content['data'][0]['links'] = Reference.REGEXP['links']
        content['data'][0]['updated'] = Content.REGEXP_TIME
        content['data'][0]['digest'] = 'ee4a072a5a7a661a8c5d8e8f2aac88267c47fbf0b26db19b97d0b72bae3d74f0'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'brief': content['data'][0]['brief'],
                    'links': Const.DELIMITER_LINKS.join(content['data'][0]['links']),
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '753'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/ee4a072a5a7a661a'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_create_reference_006(self, server):
        """Update reference with POST that maps to DELETE.

        Call POST /v1/references with X-HTTP-Method-Override header to delete
        reference. In this case the resource exists and the content is deleted.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/1f9d9496005736ef',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

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
            'content-length': '689'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because it was matching to an empty template'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field links is empty'
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'no content to be stored'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-gitlog-utc', 'caller')
    def test_api_create_reference_008(self, server_db, used_database):
        """Try to create reference.

        Try to POST new reference when database throws an integrity error from
        UUID column's unique constraint violation. In this case there is no
        stored content and the digest in generated error message cannot filled
        based on database content. Database tries to insert the content twice
        and both of the inserts result same unique constraint violation.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '580'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '500',
                'statusString': '500 Internal Server Error',
                'module': 'snippy.testing.testing:123',
                'title': 'internal error when searching content possibly violating database unique constraints'
            }, {
                'status': '500',
                'statusString': '500 Internal Server Error',
                'module': 'snippy.testing.testing:123',
                'title': 'content: uuid :already exist with digest: not found'
            }]
        }
        server = server_db[0]
        db_connect = server_db[1]
        if used_database == Helper.DB_SQLITE:
            db_connect.return_value.commit.side_effect = [
                sqlite3.IntegrityError('UNIQUE constraint failed: contents.uuid'),
                sqlite3.IntegrityError('UNIQUE constraint failed: contents.uuid')
            ]
        elif used_database == Helper.DB_POSTGRESQL:
            db_connect.return_value.commit.side_effect = [
                sqlite3.IntegrityError(
                    'duplicate key value violates unique constraint "contents_data_key"\n' +
                    'DETAIL:  Key (uuid)=11cd5827-b6ef-4067-b5ac-3ceac07dde9f already exists.'
                ),
                sqlite3.IntegrityError(
                    'duplicate key value violates unique constraint "contents_data_key"\n' +
                    'DETAIL:  Key (uuid)=11cd5827-b6ef-4067-b5ac-3ceac07dde9f already exists.'
                ),
            ]
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_500
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_009(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new reference with two groups.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['groups'] = ('python', 'regexp')
        content['data'][0]['digest'] = 'e5a94aae97e43273b37142d242e9669b97a899a44b6d73b340b191d3fee4b58a'
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '686'}
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_010(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new content. In this case every
        attribute has additional leading and trailing whitespaces which must
        be trimmed.
        """

        content = {
            'data': [{
                'category': 'reference',
                'data': (),
                'brief': 'short brief',
                'description': 'longer description',
                'name': 'short name',
                'groups': ('python',),
                'tags': ('spaces', 'tabs'),
                'links': ('link1', 'link2'),
                'source': 'short source link',
                'versions': ('kafka=1.0.0',),
                'filename': 'shortfilename.yaml',
                'created': Content.REGEXP_TIME,
                'updated': Content.REGEXP_TIME,
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': '08083cf156f5f0e69cd8a1081634021141bc42aeb395d0d150fe3eb049e7f643'
            }]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'data': ['     first row   ', '   second row  '],
                    'brief': ' short brief  ',
                    'description': ' longer description  ',
                    'name': '  short name   ',
                    'groups': ['    python   ',],
                    'tags': ['  spaces   ', '  tabs    '],
                    'links': ['  link1  ', '    link2   '],
                    'source': '  short source link   ',
                    'versions': ['  kafka=1.0.0   '],
                    'filename': '  shortfilename.yaml   '
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '636'}
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_011(self, server):
        """Create one reference from API.

        Call POST /v1/references to create new content. In this case only the
        links field is defined
        """

        content = {
            'data': [{
                'category': 'reference',
                'data': (),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default', ),
                'tags': (),
                'links': ('link1', 'link2'),
                'source': '',
                'versions': (),
                'filename': '',
                'created': Content.REGEXP_TIME,
                'updated': Content.REGEXP_TIME,
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': 'b978df98e539644f9861a13803c19345d286544302ccedfd98c36cf16724eb80'
            }]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'links': ['link1', 'link2'],
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '534'}
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_012(self, server):
        """Create new reference with duplicated content field values.

        Call POST /v1/references to create new reference. In this case content
        fields contain duplicated values. For example there are tag 'python'
        added twice. Only unique values must be added.

        Links are not sorted because the order is assumed to convey relevant
        information related to link importance in case of reference content.
        Because of this, removal of duplicated links must not change the
        order which links are insert.
        """

        content = {
            'data': [{
                'category': 'reference',
                'data': (),
                'brief': 'short brief',
                'description': '',
                'name': '',
                'groups': ('docker', 'python'),
                'tags': ('pypy', 'swarm'),
                'links': ('http://www.dot.com/link2', 'http://www.dot.com/link1'),
                'source': '',
                'versions': (),
                'filename': '',
                'created': '2018-06-22T13:11:13.678729+00:00',
                'updated': '2018-06-22T13:11:13.678729+00:00',
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': 'aa6aa8c9a94f1959c9935d7bc6aca060edd5369ae5a24d26ce2960852751d09d'
            }]
        }
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'brief': 'short brief',
                    'description': '',
                    'groups': ['docker', 'docker', 'python'],
                    'tags': ['swarm', 'swarm', 'pypy'],
                    'links': ['http://www.dot.com/link2', 'http://www.dot.com/link2', 'http://www.dot.com/link1'],
                    'versions': []
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '607'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body, ensure_ascii=False))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
