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

"""test_api_update_solution: Test PUT /solutions API."""

import copy
import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiUpdateSolution(object):
    """Test PUT /solutions/{digest} API."""

    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_update_solution_001(self, server, mocker):
        """Update one solution with PUT request.

        Call PUT /v1/solutions/a96accc25dd23ac0 to update existing solution
        with specified digest. See 'updating content attributes' for the
        attribute list that can be changed by user.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        content_read = copy.copy(Solution.DEFAULTS[Solution.NGINX])
        content = {'2cd0e794244a07f': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2995'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/2cd0e794244a07f8'
            },
            'data': {
                'type': 'solution',
                'id': '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d',
                'attributes': content_read
            }
        }
        result_json['data']['attributes']['filename'] = Const.EMPTY
        result_json['data']['attributes']['created'] = Content.BEATS_TIME
        result_json['data']['attributes']['updated'] = Content.NGINX_TIME
        result_json['data']['attributes']['digest'] = '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d'
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_update_solution_002(self, server, mocker):
        """Update one solution with PUT request.

        Call PUT /v1/solutions/a96accc25dd23ac0 to update existing solution.
        The PUT request contains only the mandatory data attribute. All other
        attributes must be set to their default values.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                }
            }
        }
        content_read = {
            'data': Solution.DEFAULTS[Solution.NGINX]['data'],
            'brief': '',
            'group': 'default',
            'tags': [],
            'links': [],
            'category': 'solution',
            'name': '',
            'filename': '',
            'versions': '',
            'created': Content.BEATS_TIME,
            'updated': Content.BEATS_TIME,
            'digest': '8d400d39568354f90c52f94e1d7f76240e52a39b0ace61d445fe96e0c617524b'
        }
        content = {'8d400d39568354f9': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2894'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/8d400d39568354f9'
            },
            'data': {
                'type': 'solution',
                'id': '8d400d39568354f90c52f94e1d7f76240e52a39b0ace61d445fe96e0c617524b',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_003(self, server, mocker):
        """Update one solution with PUT request.

        Try to call PUT /v1/solutions/101010101010101 to update solution with
        digest that cannot be found.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        content_read = Solution.DEFAULTS[Solution.BEATS]
        content = {Solution.BEATS_DIGEST: content_read}
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
            path='/snippy/api/app/v1/solutions/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_004(self, server):
        """Try to update solution with malformed request.

        Try to call PUT /v1/solutions/a96accc25dd23ac0 to update solution with
        malformed JSON request.
        """

        request_body = {
            'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
            'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
            'group': Solution.DEFAULTS[Solution.NGINX]['group'],
            'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
            'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
        }
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '5427'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '5237'}
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
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert Database.get_solutions().size() == 1

    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_005(self, server):
        """Try to update solution with malformed request.

        Try to call PUT /v1/solutions/a96accc25dd23ac0 to update solution with
        client generated resource ID. In this case the ID looks like a valid
        message digest.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'id': '2cd0e794244a07f81f6ebfd61dffa5c85f09fc7690dc0dc68ee0108be8cc908d',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
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
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403
        assert Database.get_solutions().size() == 1

    @pytest.mark.usefixtures('import-beats', 'caller')
    def test_api_update_solution_006(self, server):
        """Try to update solution with malformed request.

        Try to call PUT //v1/solutions/a96accc25dd23ac0 to update solution
        with client generated resource ID. In this case the ID is empty
        string.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'id': '',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])}}}
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
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403
        assert Database.get_solutions().size() == 1

    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_update_solution_007(self, server, mocker):
        """Update one solution with PATCH request.

        Call PATCH /v1/solutions/53908d68425c61dc to update existing snippet
        with specified digest. The PATCH request contains only mandatory data
        attribute. All other attributes that can be updated must be returned
        with their previous values.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                }
            }
        }
        content_read = {
            'data': Solution.DEFAULTS[Solution.NGINX]['data'],
            'brief': Solution.DEFAULTS[Solution.BEATS]['brief'],
            'group': Solution.DEFAULTS[Solution.BEATS]['group'],
            'tags': Solution.DEFAULTS[Solution.BEATS]['tags'],
            'links': Solution.DEFAULTS[Solution.BEATS]['links'],
            'category': Solution.DEFAULTS[Solution.BEATS]['category'],
            'name': Solution.DEFAULTS[Solution.BEATS]['name'],
            'filename': Solution.DEFAULTS[Solution.BEATS]['filename'],
            'versions': Solution.DEFAULTS[Solution.BEATS]['versions'],
            'created': Content.BEATS_TIME,
            'updated': Content.BEATS_TIME,
            'digest': '21c737e704b972268565e23369c6038a7997bae796a6befbf6be88cbdb3721d0'
        }
        content = {'21c737e704b97226': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3078'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/21c737e704b97226'
            },
            'data': {
                'type': 'solution',
                'id': '21c737e704b972268565e23369c6038a7997bae796a6befbf6be88cbdb3721d0',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
