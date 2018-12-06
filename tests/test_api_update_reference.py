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

"""test_api_update_reference: Test PUT /references API."""

import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference

pytest.importorskip('gunicorn')


class TestApiUpdateReference(object):
    """Test PUT /references/{digest} API."""

    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_001(self, server):
        """Update one reference with PUT request.

        Call PUT /v1/references/<digest> to update existing reference with
        specified digest. See 'updating content attributes' for the attribute
        list that can be changed by user.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.DEFAULTS[Reference.PYTEST])
            ]
        }
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e'
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
            'content-length': '706'
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

    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_api_update_reference_002(self, server):
        """Update one reference with PUT request.

        Call PUT /v1/references/<digest> to update existing reference. The PUT
        request contains only the mandatory links attribute. All other
        attributes must be set to their default values.
        """

        content = {
            'data': [{
                'data': (),
                'brief': '',
                'description': '',
                'groups': ('default',),
                'tags': (),
                'links': Reference.DEFAULTS[Reference.PYTEST]['links'],
                'category': 'reference',
                'name': '',
                'filename': '',
                'versions': '',
                'source': '',
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': Content.GITLOG_TIME,
                'updated': Content.PYTEST_TIME,
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
            'content-length': '658'
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

    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_003(self, server):
        """Update one reference with PUT request.

        Try to call PUT /v1/references/<digest> to update reference with digest
        that cannot be found.
        """

        content = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG]
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': Reference.DEFAULTS[Reference.REGEXP]['links'],
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '370'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest: 101010101010101'
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

    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_004(self, server):
        """Try to update reference with malformed request.

        Try to call PUT /v1/references/<digest> to update reference with
        malformed JSON request.
        """

        content = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG]
            ]
        }
        request_body = {
            'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
            'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
            'groups': Reference.DEFAULTS[Reference.REGEXP]['groups'],
            'tags': Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.REGEXP]['tags']),
            'links': Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.REGEXP]['links'])
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '785'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '787'}
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
        assert result.headers == expect_headers_p2 or result.headers == expect_headers_p3
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_005(self, server):
        """Try to update reference with malformed request.

        Try to call PUT /v1/references/<digest> to update reference with client
        generated resource ID. In this case the ID looks like a valid message
        digest.
        """

        content = {
            'data': [
                Reference.DEFAULTS[Reference.GITLOG]
            ]
        }
        request_body = {
            'data': {
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
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
            'content-length': '382'
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

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_006(self, server):
        """Update one reference with PATCH request.

        Call PATCH /v1/references/<digest> to update existing snippet with
        specified digest. The PATCH request contains only mandatory links
        attribute. All other attributes that can be updated must be returned
        with their previous values.

        The mocked updated timestamp is intentionally the same as with the
        original content to create variation from normal where the timestamp
        is different.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.DEFAULTS[Reference.GITLOG])
            ]
        }
        content['data'][0]['links'] = Reference.DEFAULTS[Reference.REGEXP]['links']
        content['data'][0]['created'] = Content.GITLOG_TIME
        content['data'][0]['updated'] = Content.REGEXP_TIME
        content['data'][0]['digest'] = '915d0aa75703093ccb347755bfb597a16c0774b9b70626948dd378bd01310dec'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['links']),
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '754'
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

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_007(self, server):
        """Update one reference with PUT request.

        Try to update reference uuid by calling PUT /v1/references/<digest>.
        This must not be done because the uuid is not changed once allocated.
        """

        content = {
            'data': [{
                'data': (),
                'brief': '',
                'description': '',
                'groups': ('default',),
                'tags': (),
                'links': Reference.DEFAULTS[Reference.REGEXP]['links'],
                'category': 'reference',
                'name': '',
                'filename': '',
                'versions': '',
                'source': '',
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': Content.GITLOG_TIME,
                'updated': Content.REGEXP_TIME,
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
            'content-length': '706'
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

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
