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

"""test_api_update_reference: Test PUT /references API endpoint."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.content import Request
from tests.testlib.content import Storage
from tests.testlib.reference import Reference

pytest.importorskip('gunicorn')


# pylint: disable=unsupported-assignment-operation, unsubscriptable-object
class TestApiUpdateReference(object):
    """Test PUT /references API en dpoint."""

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_001(server):
        """Update one reference with PUT request.

        Send PUT /references/{id} to update existing resource with digest.
        See 'updating content attributes' for the attribute list that can be
        changed by user.
        """

        storage = {
            'data': [
                Storage.pytest
            ]
        }
        storage['data'][0]['created'] = Content.GITLOG_TIME
        storage['data'][0]['updated'] = Content.PYTEST_TIME
        storage['data'][0]['uuid'] = Reference.GITLOG_UUID
        storage['data'][0]['digest'] = Reference.PYTEST_DIGEST
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': storage['data'][0]['data'],
                    'brief': storage['data'][0]['brief'],
                    'description': storage['data'][0]['description'],
                    'groups': storage['data'][0]['groups'],
                    'tags': storage['data'][0]['tags'],
                    'links': storage['data'][0]['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '698'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_002(server):
        """Update one reference with PUT request.

        Send PUT /references/{id} to update existing resource. The PUT
        request contains only the mandatory links attribute. All other
        attributes must be set to their default values in the HTTP response.
        """

        storage = {
            'data': [{
                'category': 'reference',
                'data': (),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': Reference.PYTEST['links'],
                'source': '',
                'versions': (),
                'filename': '',
                'created': Content.GITLOG_TIME,
                'updated': Content.PYTEST_TIME,
                'uuid': Reference.GITLOG_UUID,
                'digest': '4a868cc74e3d32a4340e1a2fd17d0df815777c67f827aeedbb35869b740dd720'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': storage['data'][0]['links'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '650'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_003(server):
        """Update one reference with PUT request.

        Try to send PUT /references/{id} to update resource with ``id`` in
        URI path that is not found.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': Request.regexp['links'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '374'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: 101010101010101'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_004(server):
        """Try to update reference with malformed request.

        Try to send PUT /references/{id} to update resource with malformed
        JSON request.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Request.regexp['data']),
            'brief': Request.regexp['brief'],
            'groups': Request.regexp['groups'],
            'tags': Const.DELIMITER_TAGS.join(Request.regexp['tags']),
            'links': Const.DELIMITER_LINKS.join(Request.regexp['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1254'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1294'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_005(server):
        """Try to update reference with malformed request.

        Try to send PUT /references/{id} to update reference with client
        generated resource ID. In this case the ID looks like a valid message
        digest.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'id': Reference.REGEXP_DIGEST,
                'attributes': {
                    'data': Request.regexp['data'],
                    'brief': Request.regexp['brief'],
                    'groups': Request.regexp['groups'],
                    'tags': Request.regexp['tags'],
                    'links': Request.regexp['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '384'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '403',
                'statusString': '403 Forbidden',
                'module': 'snippy.testing.testing:123',
                'title': 'client generated resource id is not supported, remove member data.id'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_006(server):
        """Update one reference with PATCH request.

        Send PATCH /references/{id} to update existing snippet with digest.
        The PATCH request contains only mandatory links attribute. All other
        attributes that can be updated must be returned with their previous
        values.

        The mocked updated timestamp is intentionally the same as with the
        original content to create variation from normal where the timestamp
        is different.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['links'] = Storage.regexp['links']
        storage['data'][0]['created'] = Content.GITLOG_TIME
        storage['data'][0]['updated'] = Content.REGEXP_TIME
        storage['data'][0]['uuid'] = Reference.GITLOG_UUID
        storage['data'][0]['digest'] = '915d0aa75703093ccb347755bfb597a16c0774b9b70626948dd378bd01310dec'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': Request.regexp['links'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '746'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc', 'caller')
    def test_api_update_reference_007(server):
        """Update one reference with PUT request.

        Try to update resource ``uuid`` attribute with PUT /references/{id}.
        This must not work because the ``uuid`` attribute cannot be changed by
        client.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': storage['data'][0]['links'],
                    'uuid': '11111111-1111-1111-1111-111111111111'
                }
            }
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1117'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1156'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_008(server):
        """Try to update reference with PUT request.

        Try to send PUT /references/{id} to replace existing resource by
        using digest as resource ``id`` in URI. The PUT request does not have
        mandatory ``links`` attribute which is why the HTTP request must be
        rejected.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'brief': '',
                    'description': '',
                    'groups': (),
                    'tags': ()
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '387'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field links is empty'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_009(server):
        """Update reference with PUT request.

        Send PUT /references/{id} to replace existing resource with digest.
        The PUT sets all but the mandatory ``links`` attribute to empty values.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['brief'] = ''
        storage['data'][0]['description'] = ''
        storage['data'][0]['name'] = ''
        storage['data'][0]['groups'] = ()
        storage['data'][0]['tags'] = ()
        storage['data'][0]['source'] = ''
        storage['data'][0]['versions'] = ()
        storage['data'][0]['filename'] = ''
        storage['data'][0]['created'] = Content.GITLOG_TIME
        storage['data'][0]['updated'] = Content.PYTEST_TIME
        storage['data'][0]['digest'] = '54c493ade0f808e3d1b16bb606484a51bb0f7eb9c0592c46aea5196bd891881c'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': storage['data'][0]['links'],
                    'brief': '',
                    'description': '',
                    'name': '',
                    'groups': (),
                    'tags': (),
                    'source': '',
                    'versions': (),
                    'filename': ''
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '634'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.skip(reason="OAS 2.0 does not support nullable")
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_010(server):
        """Update reference with PATCH request.

        Send PATCH /references/{id} to update existing reference with digest.
        The PATCH sets all but the mandatory field to empty values.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['brief'] = ''
        storage['data'][0]['description'] = ''
        storage['data'][0]['name'] = ''
        storage['data'][0]['groups'] = ()
        storage['data'][0]['tags'] = ()
        storage['data'][0]['source'] = ''
        storage['data'][0]['versions'] = ()
        storage['data'][0]['filename'] = ''
        storage['data'][0]['created'] = Content.GITLOG_TIME
        storage['data'][0]['updated'] = Content.PYTEST_TIME
        storage['data'][0]['digest'] = '54c493ade0f808e3d1b16bb606484a51bb0f7eb9c0592c46aea5196bd891881c'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'brief': None,
                    'description': None,
                    'name': None,
                    'groups': None,
                    'tags': None,
                    'source': None,
                    'versions': None,
                    'filename': None
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '634'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.skip(reason="OAS 2.0 does not support nullable")
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_011(server):
        """Update reference with PATCH request.

        Send PATCH /references/{id} to update existing resource with
        specified digest. The PATCH sets the data field empty. This should
        result OK. The data field is not used with references and it cannot
        contain any additional information for the client. From the client
        point of view, the data is always empty.
        """

        storage = {
            'data': [
                Storage.gitlog
            ]
        }
        storage['data'][0]['created'] = Content.GITLOG_TIME
        storage['data'][0]['updated'] = Content.PYTEST_TIME
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'data': None
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '691'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/references/' + Reference.GITLOG_UUID
            },
            'data': {
                'type': 'reference',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/api/snippy/rest/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
