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

"""test_api_create_snippet: Test POST /snippets API."""


import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet import Snippet

pytest.importorskip('gunicorn')


class TestApiCreateSnippet(object):  # pylint: disable=too-many-public-methods
    """Test POST snippets collection API."""

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_001(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. The created snippet is
        sent in the POST request 'data' attribute as a list of snippet objects.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': content['data'][0]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '713'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_002(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. The created snippet is
        sent in the POST request 'data' attribute as a plain object. The
        response that contains the created snippet must be received as a list
        of snippet objects.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': content['data'][0]
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '713'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_003(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case there are
        only part of the snippet content attributes defined.

        The tags must be sorted and trimmed after parsing.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.REMOVE['data']),
                    'brief': Snippet.REMOVE['brief'],
                    'groups': Snippet.REMOVE['groups'],
                    'tags': [' moby ', 'cleanup  ', '  container', 'docker', 'docker-ce'],
                    'links': ['https://docs.docker.com/engine/reference/commandline/rm/']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '713'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-exited-utc')
    def test_api_create_snippet_004(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the snippet
        content data, tags and links attributes are defined in string context
        where each line is separated with a newline.
        """

        content = {
            'data': [
                Snippet.EXITED
            ]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.DELIMITER_DATA.join(content['data'][0]['data']),
                    'brief': content['data'][0]['brief'],
                    'groups': content['data'][0]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(content['data'][0]['tags']),
                    'links': Const.DELIMITER_LINKS.join(content['data'][0]['links'])
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '918'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.EXITED_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-exited-utc')
    def test_api_create_snippet_005(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the snippet
        content data attribute is defined as list where each line is a separate
        element in a list.

        Additional newlines must be removed from the snippet data attribute.
        """

        content = {
            'data': [
                Snippet.EXITED
            ]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': [
                        'docker rm $(docker ps --all -q -f status=exited)\n\n\n\n',
                        'docker images -q --filter dangling=true | xargs docker rmi'
                    ],
                    'brief': content['data'][0]['brief'],
                    'groups': content['data'][0]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(content['data'][0]['tags']),
                    'links': Const.DELIMITER_LINKS.join(content['data'][0]['links'])
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '918'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.EXITED_DIGEST,
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_006(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet with only data.
        """

        content = {
            'data': [{
                'data': ('docker rm $(docker ps --all -q -f status=exited)',),
                'brief': '',
                'description': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': (),
                'source': '',
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['docker rm $(docker ps --all -q -f status=exited)\n']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '564'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc', 'create-forced-utc')
    def test_api_create_snippet_007(self, server):
        """Create list of snippets from API.

        Call POST /v1/snippets in list context to create new snippets.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': content['data'][0]
            }, {
                'type': 'snippet',
                'attributes': content['data'][1]
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1485'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content['data'][0]
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_DIGEST,
                'attributes': content['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_008(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create new snippet with malformed
        JSON request. In this case the top level json object is incorrect.
        """

        request_body = Snippet.REMOVE
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '909'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '911'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_009(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create new snippet with malformed
        JSON request. In this case the top level data JSON object type is
        not 'snippet' or 'solution'.
        """

        request_body = {
            'data': [{
                'type': 'snippe',
                'id': '1',
                'attributes': {
                    'data': ['docker rm $(docker ps --all -q -f status=exited)'],
                    'brief': '',
                    'groups': ['default'],
                    'tags': [],
                    'links': [],
                    'category': 'snippet',
                    'name': '',
                    'filename': '',
                    'versions': (),
                    'utc': '2017-10-14T19:56:31.000001+00:00',
                    'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'}}]}
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '584'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '586'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_010(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create new snippet with client
        generated ID. This is not supported and it will generate error.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.REMOVE
            }]
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
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_011(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create two snippets. First one is
        correctly defind but the second one contains error in JSON structure.
        This must not create any resources and the whole request must be
        considered erroneous.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.REMOVE
            }, {
                'type': 'snippet',
                'attributes': {'brief': ''}
            }]
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '470'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '472'}
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'json media validation failed'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_012(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create two snippets. First snippet is
        correctly defind but the second one contains an error in the JSON data
        structure. The error is the client generated ID which is not supported.
        This request must not create any resources and the whole request must
        be considered request.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.REMOVE
            }, {
                'type': 'snippet',
                'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                'attributes':{
                    'data': ['docker rm $(docker ps --all -q -f status=exited)']
                }
            }]
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
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_create_snippet_013(self, server):
        """Update snippet with POST that maps to PUT.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. In this case the resource exists and the content is updated.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': content['data'][0]
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '804'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63'
            },
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-forced-utc')
    def test_api_create_snippet_014(self, server):
        """Update snippet with POST that maps to PATCH.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. In this case the resource exists and the content is updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.FORCED)
            ]
        }
        content['data'][0]['data'] = Snippet.REMOVE['data']
        content['data'][0]['digest'] = 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.REMOVE['data'])
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '896'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/a9e137c08aee0985'
            },
            'data': {
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-exited-utc')
    def test_api_create_snippet_015(self, server):
        """Update snippet with POST that maps to PATCH.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. All fields are tried to be updated but only the that can be
        modified by user must be modified.
        """

        content = {
            'data': [{
                'data': ('data row1', 'data row2'),
                'brief': 'brief description',
                'description': 'long description',
                'groups': ('solution',),
                'tags': ('tag1', 'tag2'),
                'links': ('link1', 'link2'),
                'category': 'snippet',
                'name': 'runme',
                'filename': 'filename.txt',
                'versions': ('version=1.1',),
                'source': 'http://testing/snippets.html',
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': Content.FORCED_TIME,
                'updated': Content.EXITED_TIME,
                'digest': 'a488856d2c0156328afa398458a4f991b2ee3c5bb4dd010f7b740777c015ae83'
            }]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': 'data row1\ndata row2',
                    'brief': 'brief description',
                    'description': 'long description',
                    'groups': 'solution',
                    'tags': 'tag1,tag2',
                    'links': 'link1\nlink2',
                    'categeory': 'solution',
                    'name': 'runme',
                    'filename': 'filename.txt',
                    'versions': 'version=1.1',
                    'source': 'http://testing/snippets.html',
                    'created': 'invalid time',
                    'updated': 'invalid time',
                    'digest': 'invalid digest'
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '751'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/a488856d2c015632'
            },
            'data': {
                'type': 'snippet',
                'id': 'a488856d2c0156328afa398458a4f991b2ee3c5bb4dd010f7b740777c015ae83',
                'attributes': content['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_api_create_snippet_016(self, server):
        """Update snippet with POST that maps to DELETE.

        Call POST /v1/snippets with X-HTTP-Method-Override header to delete
        snippet. In this case the resource exists and the content is deleted.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/f3fd167c64b6f97e',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_017(self, server):
        """Try to create snippet with resource id.

        Try to call POST /v1/snippets/53908d68425c61dc to create new snippet
        with resource ID in URL. The POST method is not overriden with custom
        X-HTTP-Method-Override header.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.REMOVE
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '400'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot create resource with id, use x-http-method-override to override the request'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-exited-utc', 'caller')
    def test_api_create_snippet_018(self, server):
        """Create one snippet with POST.

        Try to call POST /v1/snippets to create new snippet with empty content
        data. In case of snippets, the resulting error string is misleading.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': []
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '688'
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
                'title': 'content was not stored because mandatory content field data is empty'
            }, {
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'no content to be stored'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_019(self, server):
        """Create and search snippet with unicode characters.

        Call POST /v1/snippets to create new snippet. In this case the content
        contains unicode characters in string and list fields. The content must
        be also returned correctly when searching with unicode characters.
        """

        content = {
            'data': [{
                'data': (u'Sîne klâwen durh die wolken sint geslagen', u'er stîget ûf mit grôzer kraft'),
                'brief': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                'description': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                'groups': (u'Düsseldorf',),
                'tags': (u'έδωσαν', u'γλώσσα', u'ελληνική'),
                'links': (u'http://www.чухонца.edu/~fdc/utf8/',),
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': (),
                'source': '',
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'digest': 'c267233096b6977ea4dd9ef41faa1559d3886ad550d8932ddb4513eae5b84fbf'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': [u'Sîne klâwen durh die wolken sint geslagen', u'er stîget ûf mit grôzer kraft'],
                    'brief': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                    'description': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                    'groups': u'Düsseldorf',
                    'tags': [u'έδωσαν', u'γλώσσα', u'ελληνική'],
                    'links': [u'http://www.чухонца.edu/~fdc/utf8/']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '935'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body, ensure_ascii=False))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '995'
        }
        expect_body = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=Düsseldorf&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_snippet_020(self, server):
        """Create one snippet from API.

        Call POST /v1/snippets to create new content. In this case every
        attribute has additional leading and trailing whitespaces which must
        be trimmed. Tags and links must be sorted.
        """

        content = {
            'data': [{
                'data': ('first row', 'second row'),
                'brief': 'short brief',
                'description': 'long description',
                'groups': ('python',),
                'tags': ('spaces', 'tabs'),
                'links': ('link1', 'link2'),
                'category': 'snippet',
                'name': 'short name',
                'filename': 'shortfilename.yaml',
                'versions': ('version=1.1.1',),
                'source': 'short source link',
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': Content.REGEXP_TIME,
                'updated': Content.REGEXP_TIME,
                'digest': '9551cc17fe962ceee85cca9d22b2c2d0694970898c3e7c7a8a6ec162a5b438e7'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['     first row   ', '   second row  '],
                    'brief': ' short brief  ',
                    'description': ' long description  ',
                    'groups': ['    python   ',],
                    'tags': ['  tabs   ', '  spaces    '],
                    'links': ['  link2  ', '    link1   '],
                    'name': '  short name   ',
                    'filename': '  shortfilename.yaml   ',
                    'versions': ['  version=1.1.1   '],
                    'source': '  short source link   '
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '657'}
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_021(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet with data that have line
        breaks in the middle of the snippet. In this case the line breaks in
        middle of the snippet must not be interpolated.
        """

        content = {
            'data': [{
                'data': ('docker rm $(docker\\nps \\n --all -q -f status=exited)',),
                'brief': '',
                'description': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': (),
                'source': '',
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'digest': 'c10b8614d264ed75ad3b671526efb9718895974291627b4fd21307051c6928c1'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['docker rm $(docker\\nps \\n --all -q -f status=exited)\n']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '570'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_022(self, server):
        """Create new snippet with duplicated content field values.

        Call POST /v1/snippets to create new snippet. In this case content
        fields contain duplicated values. For example there are tag 'python'
        added twice. Only unique values must be added.
        """

        content = {
            'data': [{
                'data': ('duplicated field values', ),
                'brief': 'short brief',
                'description': '',
                'groups': ('docker', 'python'),
                'tags': ('pypy', 'swarm'),
                'links': ('http://www.dot.com/link1', 'http://www.dot.com/link2'),
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': ('1.1', '1.2'),
                'source': '',
                'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'digest': '88c5f66a1fc61ddde43b5ebc32dc762e9134b0fb78cda4f5600c243658d63c0f'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['duplicated field values'],
                    'brief': 'short brief',
                    'description': '',
                    'groups': ['docker', 'docker', 'python'],
                    'tags': ['swarm', 'swarm', 'pypy'],
                    'links': ['http://www.dot.com/link2', 'http://www.dot.com/link2', 'http://www.dot.com/link1'],
                    'versions': ['1.1', '1.2', '1.1']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '640'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': content['data'][0]['digest'],
                'attributes': content['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
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
