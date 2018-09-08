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
            'content-length': '2436'}
        result_json = {
            'data': [{
                'type': 'solution',
                'id': 'a5dd8f3807e084202be2aa96f4d0494e9295e5b4445b3f97b7990167e03ae3d8',
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
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solution',
                'attributes': Solution.DEFAULTS[Solution.KAFKA]
            }]
        }
        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            '15d1688': Solution.DEFAULTS[Solution.KAFKA]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '7072'
        }
        result_json = {
            'data': [{
                'type': 'solution',
                'id': 'a5dd8f3807e084202be2aa96f4d0494e9295e5b4445b3f97b7990167e03ae3d8',
                'attributes': Solution.DEFAULTS[Solution.BEATS]
            }, {
                'type': 'solution',
                'id': '15d1688c970fa336ad6d0b8c705aff18f3d89b49c48e1d6160d77ddccd75f5a8',
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

        Call POST /v1/solutions/a5dd8f3807e08420 to update existing solution
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
                    'description': Solution.DEFAULTS[Solution.NGINX]['description'],
                    'groups': Solution.DEFAULTS[Solution.NGINX]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.NGINX]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.NGINX]['links'])
                }
            }
        }
        content_read = copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])
        content = {'b862cdea9a2b952c': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3049'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/b862cdea9a2b952c'
            },
            'data': {
                'type': 'solution',
                'id': 'b862cdea9a2b952c8f59cc48c34ece4aa4e65e74e8ca8e3bbf0523e9ebaac6c8',
                'attributes': content_read
            }
        }
        result_json['data']['attributes']['filename'] = Const.EMPTY
        result_json['data']['attributes']['created'] = Content.BEATS_TIME
        result_json['data']['attributes']['updated'] = Content.NGINX_TIME
        result_json['data']['attributes']['digest'] = 'b862cdea9a2b952c8f59cc48c34ece4aa4e65e74e8ca8e3bbf0523e9ebaac6c8'
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/a5dd8f3807e08420',
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

        Call POST /v1/solutions/a5dd8f3807e08420 to update existing solution
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
            'description': Solution.DEFAULTS[Solution.BEATS]['description'],
            'groups': Solution.DEFAULTS[Solution.BEATS]['groups'],
            'tags': Solution.DEFAULTS[Solution.BEATS]['tags'],
            'links': Solution.DEFAULTS[Solution.BEATS]['links'],
            'category': Solution.DEFAULTS[Solution.BEATS]['category'],
            'name': Solution.DEFAULTS[Solution.BEATS]['name'],
            'filename': Solution.DEFAULTS[Solution.BEATS]['filename'],
            'versions': Solution.DEFAULTS[Solution.BEATS]['versions'],
            'source': Solution.DEFAULTS[Solution.BEATS]['source'],
            'uuid': Solution.DEFAULTS[Solution.BEATS]['uuid'],
            'created': Content.BEATS_TIME,
            'updated': Content.BEATS_TIME,
            'digest': '2ea79ade8226e8d1f87ad121ce3515de0cfdc2262a7df9983147f43602052760'
        }
        content = {'2ea79ade8226e8d1': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3132'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/solutions/2ea79ade8226e8d1'
            },
            'data': {
                'type': 'solution',
                'id': '2ea79ade8226e8d1f87ad121ce3515de0cfdc2262a7df9983147f43602052760',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions/a5dd8f3807e08420',
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
            path='/snippy/api/app/v1/solutions/15d1688c970fa33',
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
        result_headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '804'}
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

        Try to call POST /v1/solutions to create new solution with empty
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
            'content-length': '737'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data is empty'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data was missing'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'content was not stored because mandatory content field data is empty'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/solutions',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert result.json['errors'][0]['title'] == 'content was not stored because mandatory content field data is empty'

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_solution_009(self, server, mocker):
        """Create one solution from API.

        Call POST /v1/solutions to create new content. In this case every
        attribute has additional leading and trailing whitespaces which must
        be trimmed from rigth only. There must be one newline at the end.
        """

        request_body = {
            'data': [{
                'type': 'solution',
                'attributes': {
                    'data': ['     first row   ', '   second row  ', '', '', ''],
                    'brief': ' short brief  ',
                    'description': ' long description  ',
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
        content_read = {
            'data': ['     first row', '   second row', ''],
            'brief': 'short brief',
            'description': 'long description',
            'groups': ['python'],
            'tags': ['spaces', 'tabs'],
            'links': ['link1', 'link2'],
            'category': 'solution',
            'name': 'short name',
            'filename': 'shortfilename.yaml',
            'versions': 'short versions',
            'source': 'short source link',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.REGEXP_TIME,
            'updated': Content.REGEXP_TIME,
            'digest': '1cc8d8069441cdae5762d04c7730d18bbac40e0a9994fed060dcffa0a1a83429'
        }
        content = {'1cc8d8069441cda': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '668'}
        result_json = {
            'data': [{
                'type': 'solution',
                'id': '1cc8d8069441cdae5762d04c7730d18bbac40e0a9994fed060dcffa0a1a83429',
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

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
