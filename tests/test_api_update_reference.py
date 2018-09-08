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
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiUpdateReference(object):
    """Test PUT /references/{digest} API."""

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_001(self, server, mocker):
        """Update one reference with PUT request.

        Call PUT /v1/references/5c2071094dbfaa33 to update existing reference
        with specified digest. See 'updating content attributes' for the
        attribute list that can be changed by user.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
                    'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
                    'description': Reference.DEFAULTS[Reference.REGEXP]['description'],
                    'groups': Reference.DEFAULTS[Reference.REGEXP]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.REGEXP]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.REGEXP]['links'])
                }
            }
        }
        content_read = Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        content = {'cb9225a81eab8ce': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '767'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/cb9225a81eab8ced'
            },
            'data': {
                'type': 'reference',
                'id': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832',
                'attributes': content_read
            }
        }
        result_json['data']['attributes']['filename'] = Const.EMPTY
        result_json['data']['attributes']['created'] = Content.GITLOG_TIME
        result_json['data']['attributes']['updated'] = Content.REGEXP_TIME
        result_json['data']['attributes']['digest'] = 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832'
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_002(self, server, mocker):
        """Update one reference with PUT request.

        Call PUT /v1/references/5c2071094dbfaa33 to update existing reference.
        The PUT request contains only the mandatory links attribute. All other
        attributes must be set to their default values.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['links']),
                }
            }
        }
        content_read = {
            'data': [],
            'brief': '',
            'description': '',
            'groups': ['default'],
            'tags': [],
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
        }
        content = {'7e274a3e1266ee4f': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '706'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/7e274a3e1266ee4f'
            },
            'data': {
                'type': 'reference',
                'id': '7e274a3e1266ee4fc0ce8eb7661868825fbcb22e132943f376c1716f26c106fd',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_003(self, server, mocker):
        """Update one reference with PUT request.

        Try to call PUT /v1/references/101010101010101 to update reference with
        digest that cannot be found.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
                    'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
                    'groups': Reference.DEFAULTS[Reference.REGEXP]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.REGEXP]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.REGEXP]['links'])
                }
            }
        }
        content_read = Reference.DEFAULTS[Reference.GITLOG]
        content = {Reference.GITLOG_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '370'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404', 'statusString': '404 Not Found', 'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest: 101010101010101'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_004(self, server):
        """Try to update reference with malformed request.

        Try to call PUT /v1/references/5c2071094dbfaa33 to update reference with
        malformed JSON request.
        """

        request_body = {
            'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
            'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
            'groups': Reference.DEFAULTS[Reference.REGEXP]['groups'],
            'tags': Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.REGEXP]['tags']),
            'links': Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.REGEXP]['links'])
        }
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '785'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '787'}
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'not compared because of hash structure in random order inside the string'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert Database.get_references().size() == 1

    @pytest.mark.usefixtures('import-gitlog', 'caller')
    def test_api_update_reference_005(self, server):
        """Try to update reference with malformed request.

        Try to call PUT /v1/references/5c2071094dbfaa33 to update reference with
        client generated resource ID. In this case the ID looks like a valid
        message digest.
        """

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
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '382'
        }
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403
        assert Database.get_references().size() == 1

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_006(self, server, mocker):
        """Update one reference with PATCH request.

        Call PATCH /v1/references/53908d68425c61dc to update existing snippet
        with specified digest. The PATCH request contains only mandatory links
        attribute. All other attributes that can be updated must be returned
        with their previous values.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'links': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['links']),
                }
            }
        }
        content_read = {
            'data': [],
            'brief': Reference.DEFAULTS[Reference.GITLOG]['brief'],
            'description': Reference.DEFAULTS[Reference.GITLOG]['description'],
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
            'digest': '915d0aa75703093ccb347755bfb597a16c0774b9b70626948dd378bd01310dec'
        }
        content = {'915d0aa75703093c': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '754'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/915d0aa75703093c'
            },
            'data': {
                'type': 'reference',
                'id': '915d0aa75703093ccb347755bfb597a16c0774b9b70626948dd378bd01310dec',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc')
    def test_api_update_reference_007(self, server, mocker):
        """Update one reference with PUT request.

        Try to update reference uuid by calling PUT /v1/references. This must
        not be done because the uuid is not changed once allocated.
        """

        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'links': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['links']),
                    'uuid': '11111111-1111-1111-1111-111111111111'
                }
            }
        }
        content_read = {
            'data': [],
            'brief': '',
            'description': '',
            'groups': ['default'],
            'tags': [],
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
        }
        content = {'7e274a3e1266ee4f': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '706'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/7e274a3e1266ee4f'
            },
            'data': {
                'type': 'reference',
                'id': '7e274a3e1266ee4fc0ce8eb7661868825fbcb22e132943f376c1716f26c106fd',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/references/5c2071094dbfaa33',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
