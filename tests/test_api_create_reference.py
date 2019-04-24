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

"""test_api_create_reference: Test POST /references API endpoint."""

import json
import sqlite3

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content
from tests.lib.content import Request
from tests.lib.content import Storage
from tests.lib.helper import Helper
from tests.lib.reference import Reference

pytest.importorskip('gunicorn')


# pylint: disable=unsupported-assignment-operation
class TestApiCreateReference(object):
    """Test POST /references API endpoint."""

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_001(server):
        """Create one Reference resource.

        Send POST /references to create a new resource. Created resource
        is sent in the POST method resource ``data`` attribute as a list of
        objects. The HTTP response must send the created resource in the
        resource ``data`` attribute as list of objects.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.gitlog
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '580'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_002(server):
        """Create one Reference reference.

        Send POST /references to create a new reference. Created resource
        is sent in the POST method resource ``data`` attribute as object. The
        HTTP response must send the created resource in the resource ``data``
        attribute as list of objects.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': Request.gitlog
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '580'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-pytest-utc', 'create-gitlog-utc')
    def test_api_create_reference_003(server):
        """Create multiple Reference references.

        Send POST /references in a list context to create new resources.
        The external UUID must not be created from the resource sent by the
        client. The Snippy server must allocate new UUID that is a resource
        identity. This resource identity is used also in the URI and it is
        immutable.
        """

        storage = {
            'data': [
                Storage.pytest,
                Storage.gitlog
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        storage['data'][1]['uuid'] = Content.UUID2
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.pytest
            }, {
                'type': 'reference',
                'attributes': Request.gitlog
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1157'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }, {
                'type': 'reference',
                'id': Content.UUID2,
                'attributes': storage['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_create_reference_004(server):
        """Update Reference resource with POST that maps to PUT.

        Send POST /references/{id} to update existing resource with the
        ``X-HTTP-Method-Override`` header that maps the operation as PUT.

        In this case the resource ``created`` attribute must remain in the
        initial value and the ``updated`` attribute must be set to reflect
        the update time.

        The ``uuid`` attribute must not be changed from it's initial value.
        """

        storage = {
            'data': [
                Storage.regexp
            ]
        }
        storage['data'][0]['created'] = Content.GITLOG_TIME
        storage['data'][0]['updated'] = Content.REGEXP_TIME
        storage['data'][0]['uuid'] = Reference.GITLOG_UUID
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': Request.regexp
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '759'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_create_reference_005(server):
        """Update Reference resource with POST that maps to PATCH.

        Send POST /references/{id} to update existing resource with the
        ``X-HTTP-Method-Override`` header that overrides the POST method as
        PATCH. Only the attributes sent in the PATCH method must be changed.

        In this case the resource ``created`` attribute must remain in the
        initial value and the ``updated`` attribute must be set to reflect
        the update time.

        The ``uuid`` attribute must not be changed from it's initial value.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['brief'] = Reference.REGEXP['brief']
        storage['data'][0]['links'] = Reference.REGEXP['links']
        storage['data'][0]['updated'] = Content.REGEXP_TIME
        storage['data'][0]['digest'] = 'ee4a072a5a7a661a8c5d8e8f2aac88267c47fbf0b26db19b97d0b72bae3d74f0'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'brief': Reference.REGEXP['brief'],
                    'links': Reference.REGEXP['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '743'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': Reference.GITLOG_UUID,
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_create_reference_006(server):
        """Update Reference resource with POST that maps to DELETE.

        Send POST /references with the ``X-HTTP-Method-Override`` header to
        delete a resource. In this case the resource exists and the content is
        deleted.
        """

        storage = {
            'data': [
                Storage.gitlog,
                Storage.regexp
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references/1f9d9496005736ef',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc', 'caller')
    def test_api_create_reference_007(server):
        """Try to create a Reference resource.

        Try to send POST /references to create a new reference with empty
        content links. The links are mandatory in case of Reference content
        and the request must be rejected with an error.
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
            'content-length': '692'
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
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc', 'caller')
    def test_api_create_reference_008(server_db, used_database):
        """Try to create a Reference resource.

        Try to POST new resource when database throws an unique constraint
        violation error from the ``uuid`` attribute.

        In this case there is no stored resources and digest in generated
        error message cannot filled fromi database. The database tries to
        insert the content twice once batched and then one by one. Both of
        the inserts result same unique constraint violation.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.gitlog
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '583'}
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
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_500
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_009(server):
        """Create one Reference resource.

        Send POST /references to create a new resource. In the case there
        are multiple values in the ``groups`` attribute.
        """

        storage = {
            'data': [
                Storage.regexp
            ]
        }
        storage['data'][0]['groups'] = ('python', 'regexp')
        storage['data'][0]['uuid'] = Content.UUID1
        storage['data'][0]['digest'] = 'e5a94aae97e43273b37142d242e9669b97a899a44b6d73b340b191d3fee4b58a'
        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Request.storage(storage['data'][0])
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '658'}
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_010(server):
        """Create one Reference resource.

        Send POST /references to create a new resource. In this case every
        attribute has additional leading and trailing whitespaces that must
        be trimmed when stored.
        """

        storage = {
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
                'versions': ('kafka==1.0.0',),
                'filename': 'shortfilename.yaml',
                'created': Content.REGEXP_TIME,
                'updated': Content.REGEXP_TIME,
                'uuid': Content.UUID1,
                'digest': 'f68078e62794f6e1e00ccff301fb83ea01b7587959d6ab7b444c18b637f6e61b'
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
                    'versions': ['  kafka==1.0.0   '],
                    'filename': '  shortfilename.yaml   '
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '609'}
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_011(server):
        """Create one Reference resource.

        Send POST /references to create a new resource. In this case only
        the mandatory ``links`` attribute for Reference resource is defined.
        """

        storage = {
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
                'uuid': Content.UUID1,
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
            'content-length': '506'}
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_reference_012(server):
        """Create new reference with duplicated content field values.

        Send POST /references to create a new resource. In this case the
        resource attributes contain duplicated values. For example, there is
        a tag 'python' included twice in the ``tags`` attribute. Only unique
        values in attributes in array context must be added.

        Links are not sorted because the order is assumed to convey relevant
        information related to link importance in case of Reference resource.
        Because of this, removal of duplicated values in ``links`` attribute
        must not change the order which links are added.
        """

        storage = {
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
                'uuid': Content.UUID1,
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
            'content-length': '579'
        }
        expect_body = {
            'data': [{
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body, ensure_ascii=False))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
