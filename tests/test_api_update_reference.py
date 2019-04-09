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

"""test_api_update_reference: Test PUT /references API."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference import Reference

pytest.importorskip('gunicorn')


class TestApiUpdateReference(object):
    """Test PUT /references/{digest} API."""

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_001(server):
        """Update one reference with PUT request.

        Call PUT /v1/references/{id} to update existing reference with digest.
        See 'updating content attributes' for the attribute list that can be
        changed by user.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.PYTEST)
            ]
        }
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = Reference.PYTEST_DIGEST
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': content['data'][0]['data'],
                    'brief': content['data'][0]['brief'],
                    'description': content['data'][0]['description'],
                    'groups': content['data'][0]['groups'],
                    'tags': content['data'][0]['tags'],
                    'links': content['data'][0]['links']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '708'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/1f9d9496005736ef'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_002(server):
        """Update one reference with PUT request.

        Call PUT /v1/references/{id} to update existing reference. The PUT
        request contains only the mandatory links attribute. All other
        attributes must be set to their default values.
        """

        content = {
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
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': '4a868cc74e3d32a4340e1a2fd17d0df815777c67f827aeedbb35869b740dd720'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': content['data'][0]['links'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '660'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/4a868cc74e3d32a4'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_003(server):
        """Update one reference with PUT request.

        Try to call PUT /v1/references/{id} to update reference with digest
        that is not found.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': Reference.REGEXP['links'],
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
            path='/snippy/api/app/v1/references/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_004(server):
        """Try to update reference with malformed request.

        Try to call PUT /v1/references/{id} to update reference with malformed
        JSON request.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Reference.REGEXP['data']),
            'brief': Reference.REGEXP['brief'],
            'groups': Reference.REGEXP['groups'],
            'tags': Const.DELIMITER_TAGS.join(Reference.REGEXP['tags']),
            'links': Const.DELIMITER_LINKS.join(Reference.REGEXP['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '805'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '807'}
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
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_005(server):
        """Try to update reference with malformed request.

        Try to call PUT /v1/references/{id} to update reference with client
        generated resource ID. In this case the ID looks like a valid message
        digest.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'id': Reference.REGEXP_DIGEST,
                'attributes': {
                    'data': Const.NEWLINE.join(Reference.REGEXP['data']),
                    'brief': Reference.REGEXP['brief'],
                    'groups': Reference.REGEXP['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Reference.REGEXP['tags']),
                    'links': Const.DELIMITER_LINKS.join(Reference.REGEXP['links'])
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
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_006(server):
        """Update one reference with PATCH request.

        Call PATCH /v1/references/{id} to update existing snippet with digest.
        The PATCH request contains only mandatory links attribute. All other
        attributes that can be updated must be returned with their previous
        values.

        The mocked updated timestamp is intentionally the same as with the
        original content to create variation from normal where the timestamp
        is different.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['links'] = Reference.REGEXP['links']
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.REGEXP_TIME
        content['data'][0]['digest'] = '915d0aa75703093ccb347755bfb597a16c0774b9b70626948dd378bd01310dec'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': Const.NEWLINE.join(Reference.REGEXP['links']),
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '756'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/915d0aa75703093c'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_007(server):
        """Update one reference with PUT request.

        Try to update reference uuid by calling PUT /v1/references/{id}. This
        must not be done because the uuid is not changed once allocated.
        """

        content = {
            'data': [{
                'category': 'reference',
                'data': (),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': Reference.REGEXP['links'],
                'source': '',
                'versions': (),
                'filename': '',
                'created': Content.GITLOG_TIME,
                'updated': Content.REGEXP_TIME,
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': '7e274a3e1266ee4fc0ce8eb7661868825fbcb22e132943f376c1716f26c106fd'
            }]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': content['data'][0]['links'],
                    'uuid': '11111111-1111-1111-1111-111111111111'
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '708'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/7e274a3e1266ee4f'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_008(server):
        """Try to update reference with PUT request.

        Try to call PUT /v1/references/{id} to replace existing reference with
        specified digest. The PUT request does not contain the mandatory link
        field which is why the request must be rejected.
        """

        content = {
            'data': [
                Reference.GITLOG
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
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '515'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '521'}
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
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_009(server):
        """Update reference with PUT request.

        Call PUT /v1/references/{id} to replace existing reference with digest.
        The PUT sets all but the mandatory links field to empty values.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['brief'] = ''
        content['data'][0]['description'] = ''
        content['data'][0]['name'] = ''
        content['data'][0]['groups'] = ()
        content['data'][0]['tags'] = ()
        content['data'][0]['source'] = ''
        content['data'][0]['versions'] = ()
        content['data'][0]['filename'] = ''
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = '54c493ade0f808e3d1b16bb606484a51bb0f7eb9c0592c46aea5196bd891881c'
        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': content['data'][0]['links'],
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
            'content-length': '644'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/54c493ade0f808e3'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_010(server):
        """Update reference with PATCH request.

        Call PATCH /v1/references/{id} to update existing reference with digest.
        The PATCH sets all but the mandatory field to empty values.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['brief'] = ''
        content['data'][0]['description'] = ''
        content['data'][0]['name'] = ''
        content['data'][0]['groups'] = ()
        content['data'][0]['tags'] = ()
        content['data'][0]['source'] = ''
        content['data'][0]['versions'] = ()
        content['data'][0]['filename'] = ''
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = '54c493ade0f808e3d1b16bb606484a51bb0f7eb9c0592c46aea5196bd891881c'
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
            'content-length': '644'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/54c493ade0f808e3'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_011(server):
        """Update reference with PATCH request.

        Call PATCH /v1/references/{id} to update existing reference with
        specified digest. The PATCH sets the data field empty. This should
        result OK. The data field is not used with references and it cannot
        contain any additional information for the client. From the client
        point of view, the data is always empty.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.PYTEST_TIME
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
            'content-length': '701'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/5c2071094dbfaa33'
            },
            'data': {
                'type': 'reference',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
