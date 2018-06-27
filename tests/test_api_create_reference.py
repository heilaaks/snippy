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

import copy
import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiCreateReference(object):
    """Test POST references collection API."""

    @pytest.mark.skip(reason='not done')
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_api_create_reference_001(self, server, mocker):
        """Create one reference from API.

        Call POST /v1/references to create new reference.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }]
        }
        content_read = Reference.DEFAULTS[Reference.GITLOG]
        content = {Reference.GITLOG_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '528'}
        result_json = {
            'data': [{
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        print(result.json)
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.skip(reason='not done')
    @pytest.mark.usefixtures('create-gitlog-utc', 'create-pytest-utc')
    def test_api_create_reference_002(self, server, mocker):
        """Create multiple references from API.

        Call POST /v1/references in list context to create new references.
        """

        request_body = {
            'data': [{
                'type': 'reference', 'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }, {
                'type': 'reference', 'attributes': Reference.DEFAULTS[Reference.PYTEST]
            }]
        }
        content = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            'eeef5ca': Reference.DEFAULTS[Reference.PYTEST]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6972'
        }
        result_json = {
            'data': [{
                'type': 'reference',
                'id': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f',
                'attributes': Reference.DEFAULTS[Reference.GITLOG]
            }, {
                'type': 'reference',
                'id': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e',
                'attributes': Reference.DEFAULTS[Reference.PYTEST]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert Database.get_references().size() == 2
        Content.verified(mocker, server, content)

    @pytest.mark.skip(reason='not done')
    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_create_reference_003(self, server, mocker):
        """Update reference with POST that maps to PUT.

        Call POST /v1/references/a96accc25dd23ac0 to update existing reference
        with X-HTTP-Method-Override header that overrides the operation as
        PUT. In this case the created timestamp must remain in initial value
        and the updated timestamp must be updated to reflect the update time.
        """

        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
                    'brief': Reference.DEFAULTS[Reference.REGEXP]['brief'],
                    'group': Reference.DEFAULTS[Reference.REGEXP]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.REGEXP]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.REGEXP]['links'])
                }
            }
        }
        content_read = copy.deepcopy(Reference.DEFAULTS[Reference.REGEXP])
        content = {'2cd0e794244a07f': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2999'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/2cd0e794244a07f8'
            },
            'data': {
                'type': 'reference',
                'id': '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d',
                'attributes': content_read
            }
        }
        result_json['data']['attributes']['filename'] = Const.EMPTY
        result_json['data']['attributes']['created'] = Content.GITLOG_TIME
        result_json['data']['attributes']['updated'] = Content.REGEXP_TIME
        result_json['data']['attributes']['digest'] = '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d'
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.skip(reason='not done')
    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_create_reference_004(self, server, mocker):
        """Update reference with POST that maps to PATCH.

        Call POST /v1/references/a96accc25dd23ac0 to update existing reference
        with X-HTTP-Method-Override header that overrides the operation as
        PATCH.
        """

        request_body = {
            'data': {
                'type': 'reference',
                'attributes': {
                    'data': Const.NEWLINE.join(Reference.DEFAULTS[Reference.REGEXP]['data']),
                }
            }
        }
        content_read = {
            'data': Reference.DEFAULTS[Reference.REGEXP]['data'],
            'brief': Reference.DEFAULTS[Reference.GITLOG]['brief'],
            'group': Reference.DEFAULTS[Reference.GITLOG]['group'],
            'tags': Reference.DEFAULTS[Reference.GITLOG]['tags'],
            'links': Reference.DEFAULTS[Reference.GITLOG]['links'],
            'category': Reference.DEFAULTS[Reference.GITLOG]['category'],
            'filename': Reference.DEFAULTS[Reference.GITLOG]['filename'],
            'runalias': Reference.DEFAULTS[Reference.GITLOG]['runalias'],
            'versions': Reference.DEFAULTS[Reference.GITLOG]['versions'],
            'created': Content.GITLOG_TIME,
            'updated': Content.GITLOG_TIME,
            'digest': '21c737e704b972268565e23369c6038a7997bae796a6befbf6be88cbdb3721d0'
        }
        content = {'21c737e704b97226': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3082'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/references/21c737e704b97226'
            },
            'data': {
                'type': 'reference',
                'id': '21c737e704b972268565e23369c6038a7997bae796a6befbf6be88cbdb3721d0',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_references().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.skip(reason='not done')
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_create_reference_005(self, server, mocker):
        """Update reference with POST that maps to DELETE.

        Call POST /v1/references with X-HTTP-Method-Override header to delete
        reference. In this case the resource exists and the content is deleted.
        """

        content = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        result_headers = {}
        assert Database.get_references().size() == 3
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references/eeef5ca3ec9cd36',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.headers == result_headers
        assert not result.text
        assert result.status == falcon.HTTP_204
        assert Database.get_references().size() == 2
        Content.verified(mocker, server, content)

    @pytest.mark.skip(reason='not done')
    @pytest.mark.usefixtures('create-beats-utc', 'caller')
    def test_api_create_reference_006(self, server):
        """Create one reference from API.

        Try to call POST /v1/references to create new solutuon with empty
        content data.
        """

        request_body = {
            'data': [{
                'type': 'reference',
                'attributes': {
                    'data': [],
                }
            }]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '381'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content data was missing'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
