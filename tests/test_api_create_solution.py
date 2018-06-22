#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""test_api_create_solution: Test POST /solutions API."""

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


class TestApiCreateSolution(object):
    """Test POST solutions collection API."""

    @pytest.mark.usefixtures('create-beats-utc')
    def test_api_create_solution_001(self, server, mocker):
        """Create one solution from API.

        Call POST /v1/solutions to create new solution.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }]
        }
        content_read = Solution.DEFAULTS[Solution.BEATS]
        content = {Solution.BEATS_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2386'}
        result_json = {
            'data': [{
                'type': 'solution',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('create-beats-utc', 'create-kafka-utc')
    def test_api_create_solution_002(self, server, mocker):
        """Create multiple solutions from API.

        Call POST /v1/solutions in list context to create new solutions.
        """

        request_body = {
            'data': [{
                'type': 'solution', 'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solution', 'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            'eeef5ca': Solution.DEFAULTS[Solution.KAFKA]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '6972'
        }
        result_json = {
            'data': [{
                'type': 'solution',
                'id': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solution',
                'id': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-beats', 'update-nginx-utc')
    def test_api_create_solution_003(self, server, mocker):
        """Update solution with POST that maps to PUT.

        Call POST /v1/solutions/a96accc25dd23ac0 to update existing solution
        with X-HTTP-Method-Override header that overrides the operation as
        PUT. In this case the created timestamp must remain in initial value
        and the updated timestamp must be updated to reflect the update time.
        """

        request_body = {
            'data': {
                'type': 'solution',
                'attributes': {
                    'data': Const.NEWLINE.join(Solution.DEFAULTS[Solution.NGINX]['data']),
                    'brief': Solution.DEFAULTS[Solution.NGINX]['brief'],
                    'group': Solution.DEFAULTS[Solution.NGINX]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        content_read = copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])
        content = {'2cd0e794244a07f': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2999'
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
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('import-beats', 'update-beats-utc')
    def test_api_create_solution_004(self, server, mocker):
        """Update solution with POST that maps to PATCH.

        Call POST /v1/solutions/a96accc25dd23ac0 to update existing solution
        with X-HTTP-Method-Override header that overrides the operation as
        PATCH.
        """

        request_body = {
            'data': {
                'type': 'solution',
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
            'filename': Solution.DEFAULTS[Solution.BEATS]['filename'],
            'runalias': Solution.DEFAULTS[Solution.BEATS]['runalias'],
            'versions': Solution.DEFAULTS[Solution.BEATS]['versions'],
            'created': Content.BEATS_TIME,
            'updated': Content.BEATS_TIME,
            'digest': '21c737e704b972268565e23369c6038a7997bae796a6befbf6be88cbdb3721d0'
        }
        content = {'21c737e704b97226': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3082'
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
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/a96accc25dd23ac0',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('default-solutions', 'import-kafka')
    def test_api_create_solution_005(self, server, mocker):
        """Update solution with POST that maps to DELETE.

        Call POST /v1/solutions with X-HTTP-Method-Override header to delete
        solution. In this case the resource exists and the content is deleted.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        result_headers = {}
        assert Database.get_solutions().size() == 3
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/eeef5ca3ec9cd36',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.headers == result_headers
        assert not result.text
        assert result.status == falcon.HTTP_204
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_006(self, server):
        """Try to create solution with resource id.

        Try to call POST /v1/solutions/53908d68425c61dc to create new solution
        with resource ID in URL. The POST method is not overriden with custom
        X-HTTP-Method-Override header.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.NGINX]
            }]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '398'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot create resource with id, use x-http-method-override to override the request'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('caller')
    def test_api_create_solution_007(self, server):
        """Try to create solution with malformed JSON request.

        Try to call POST /v1/solutions to create new solution with malformed
        JSON request. In this case the top level json object is incorrect
        because it contains only an empty list.
        """

        request_body = {
            'data': [{}]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '954'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'not compared because of hash structure in random order inside the string'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('create-beats-utc', 'caller')
    def test_api_create_solution_008(self, server):
        """Create one solution from API.

        Try to call POST /v1/solutions to create new solutuon with empty
        content data.
        """

        request_body = {
            'data': [{
                'type': 'solution',
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
            path='/snippy/api/app/v1/solutions',
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
