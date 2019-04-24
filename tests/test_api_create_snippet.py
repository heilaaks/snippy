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
from tests.lib.content import Content
from tests.lib.content import Request
from tests.lib.content import Storage
from tests.lib.snippet import Snippet

pytest.importorskip('gunicorn')


# pylint: disable=unsupported-assignment-operation, unsubscriptable-object
class TestApiCreateSnippet(object):  # pylint: disable=too-many-public-methods
    """Test POST snippets collection API."""

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_001(server):
        """Create one Snippet with POST.

        Send POST /snippets to create a new resource. The created snippet
        is sent in the HTTP request ``data`` attribute as a list of objects.
        """

        storage = {
            'data': [
                Storage.remove
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Request.remove
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '685'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_002(server):
        """Create one Snippet with POST.

        Send POST /snippets to create a new resource. The created snippet
        is sent in the POST request ``data`` attribute as an object. The HTTP
        response that contains the created resource must be received as a
        list of snippet objects.
        """

        storage = {
            'data': [
                Storage.remove
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': Request.remove
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '685'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_003(server):
        """Create one Snippet with POST.

        Send POST /snippets to create a new resource. In this case there
        is only part of the resource attributes that are defined.

        The ``tags`` attribute must be sorted and the tags trimmed when they
        are stored into the database.
        """

        storage = {
            'data': [
                Storage.remove
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Snippet.REMOVE['data'],
                    'brief': Snippet.REMOVE['brief'],
                    'groups': Snippet.REMOVE['groups'],
                    'tags': [' moby ', 'cleanup  ', '  container', 'docker', 'docker-ce'],
                    'links': ['https://docs.docker.com/engine/reference/commandline/rm/']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '685'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_004(server):
        """Create one Snippet with POST.

        Send POST /snippets to create a new resource. In this case snippet
        content data, tags and links attributes are defined in string context
        where each line is separated with a newline.

        The string format is not supported for these attributes and this must
        generate a HTTP error.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.DELIMITER_DATA.join(Snippet.EXITED['data']),
                    'brief': Snippet.EXITED['brief'],
                    'groups': Snippet.EXITED['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.EXITED['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.EXITED['links'])
                }
            }]
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1838'}
        expect_headers_p34 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1841'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1871'}
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3, expect_headers_p34)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-exited-utc')
    def test_api_create_snippet_005(server):
        """Create one Snippet with POST.

        Send POST /snippets to create a new resource. In this case snippet
        resource ``data`` attribute is defined as list where each line is a
        separate element in the list.

        Additional newlines must be removed from the ``data`` attribute.
        """

        storage = {
            'data': [
                Storage.exited
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': [
                        'docker rm $(docker ps --all -q -f status=exited)\n\n\n\n',
                        'docker images -q --filter dangling=true | xargs docker rmi'
                    ],
                    'brief': storage['data'][0]['brief'],
                    'groups': storage['data'][0]['groups'],
                    'tags': storage['data'][0]['tags'],
                    'links': storage['data'][0]['links']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '890'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_006(server):
        """Create one Snippet with POST.

        Send POST /snippets to create a new resource. In this case the
        request resource has only the ``data`` attribute.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': ('docker rm $(docker ps --all -q -f status=exited)',),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'source': '',
                'versions': (),
                'filename': '',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'uuid': Content.UUID1,
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
            'content-length': '536'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc', 'create-forced-utc')
    def test_api_create_snippet_007(server):
        """Create two Snippets with POST.

        Send POST /snippets in list context to create new resources.
        """

        storage = {
            'data': [
                Storage.remove,
                Storage.forced
            ]
        }
        storage['data'][0]['uuid'] = Content.UUID1
        storage['data'][1]['uuid'] = Content.UUID2
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Request.remove
            }, {
                'type': 'snippet',
                'attributes': Request.forced
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1429'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }, {
                'type': 'snippet',
                'id': Content.UUID2,
                'attributes': storage['data'][1]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_008(server):
        """Try to create snippet with malformed JSON request.

        Try to send POST /snippets to create a new resource with malformed
        JSON request. In this case the top level json object is incorrect.
        """

        request_body = Snippet.REMOVE
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '2004'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '2093'}
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_009(server):
        """Try to create snippet with malformed JSON request.

        Try to send POST /snippets to create a new resource with malformed
        JSON request. In this case the top level data object type is not valid.
        """

        request_body = {
            'data': [{
                'type': 'snippe',
                'attributes': {
                    'category': 'snippet',
                    'data': ['docker rm $(docker ps --all -q -f status=exited)'],
                    'brief': '',
                    'name': '',
                    'groups': ['default'],
                    'tags': [],
                    'links': [],
                    'versions': (),
                    'filename': '',
                    'created': '2017-10-14T19:56:31.000001+00:00',
                    'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'}}]}
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1545'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1611'}
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_010(server):
        """Try to create snippet with malformed JSON request.

        Try to send POST /snippets to create new a resource with client
        generated ``id``. This is not supported and it will generate error.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Request.remove
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '387'
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_011(server):
        """Try to create snippet with malformed JSON request.

        Try to send POST /snippets to create two snippets. First one is
        correctly defined but the second contains an error in the JSON data.
        This must not create any resources and the whole request must be
        considered erroneous.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Request.remove
            }, {
                'type': 'snippet',
                'attributes': {'brief': []}
            }]
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1718'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1797'}
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_012(server):
        """Try to create snippet with malformed JSON request.

        Try to send POST /snippets to create two resources. First snippet
        is correctly defind but the second one contains an error in the JSON
        data structure. The error is the client generated ``id`` that is not
        supported. This request must not create any resources and the whole
        HTTP request must be considered invalid.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Request.remove
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
            'content-length': '387'
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_403
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_create_snippet_013(server):
        """Update snippet with POST that maps to PUT.

        Send POST /snippets with X-HTTP-Method-Override header to update
        resource. In this case the resource exists and the content is updated.
        """

        storage = {
            'data': [
                Storage.remove
            ]
        }
        storage['data'][0]['uuid'] = Snippet.FORCED_UUID
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': Request.remove
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '794'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_create_snippet_014(server):
        """Update snippet with POST that maps to PATCH.

        Send POST /snippets with the ``X-HTTP-Method-Override`` header to
        update a resource. In this case the resource exists and the content
        is updated.

        In this case the resource ``created`` attribute must remain in the
        initial value and the ``updated`` attribute must be set to reflect
        the update time.

        The ``uuid`` attribute must not be changed from it's initial value.
        """

        storage = {
            'data': [
                Storage.forced
            ]
        }
        storage['data'][0]['data'] = Snippet.REMOVE['data']
        storage['data'][0]['updated'] = Content.FORCED_TIME
        storage['data'][0]['uuid'] = Snippet.FORCED_UUID
        storage['data'][0]['digest'] = 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Snippet.REMOVE['data']
                }
            }
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '886'
        }
        expect_body = {
            'links': {
                'self': 'http://falconframework.org/api/snippy/rest/snippets/' + Snippet.FORCED_UUID
            },
            'data': {
                'type': 'snippet',
                'id': Snippet.FORCED_UUID,
                'attributes': storage['data'][0]
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('import-forced', 'caller')
    def test_api_create_snippet_015(server):
        """Update snippet with POST that maps to PATCH.

        Send POST /snippets with the ``X-HTTP-Method-Override`` header to
        update a resource. All resource attributes are tried to be updated.
        This must generate HTTP error because it is not possible to update
        for example the ``uuid`` attribute by client.
        """

        storage = {
            'data': [
                Storage.forced
            ]
        }
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'categeory': 'solution',
                    'data': 'data row1\ndata row2',
                    'brief': 'brief description',
                    'description': 'long description',
                    'name': 'runme',
                    'groups': 'solution',
                    'tags': 'tag1,tag2',
                    'links': 'link1\nlink2',
                    'source': 'http://testing/snippets.html',
                    'versions': 'version==1.1',
                    'filename': 'filename.txt',
                    'created': 'invalid time',
                    'updated': 'invalid time',
                    'uuid': Snippet.EXITED_UUID,
                    'digest': 'invalid digest'
                }
            }
        }
        expect_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1784'}
        expect_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1875'}
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
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers in (expect_headers_p2, expect_headers_p3)
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_api_create_snippet_016(server):
        """Update snippet with POST that maps to DELETE.

        Send POST /snippets with the ``X-HTTP-Method-Override`` header to
        delete a snippet. In this case the resource exists and the content is
        deleted.
        """

        storage = {
            'data': [
                Storage.remove,
                Storage.forced
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets/f3fd167c64b6f97e',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_017(server):
        """Try to create snippet with resource id.

        Try to send POST /snippets/{id} to create a new resource with the
        resource ID in the URL. The POST method is not overriden with custom
        ``X-HTTP-Method-Override`` header.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Request.remove
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '403'
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
            path='/api/snippy/rest/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-exited-utc', 'caller')
    def test_api_create_snippet_018(server):
        """Create one snippet with POST.

        Try to send POST /snippets to create a new snippet with an empty
        resource ``data``. In case of snippets, the resulting error string is
        misleading because the only given attribute is ``data`` that is empty
        which maps the resource to a resource template.
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
            'content-length': '691'
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
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_019(server):
        """Create and search snippet with unicode characters.

        Send POST /snippets to create a new resource. In this case resource
        contains unicode characters in string and list fields. The content must
        be also returned correctly when searching with unicode characters.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': (u'Sîne klâwen durh die wolken sint geslagen', u'er stîget ûf mit grôzer kraft'),
                'brief': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                'description': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                'name': '',
                'groups': (u'Düsseldorf',),
                'tags': (u'έδωσαν', u'γλώσσα', u'ελληνική'),
                'links': (u'http://www.чухонца.edu/~fdc/utf8/',),
                'source': '',
                'versions': (),
                'filename': '',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'uuid': Content.UUID1,
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
                    'groups': [u'Düsseldorf'],
                    'tags': [u'έδωσαν', u'γλώσσα', u'ελληνική'],
                    'links': [u'http://www.чухонца.edu/~fdc/utf8/']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '907'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': Content.UUID1,
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body, ensure_ascii=False))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '967'
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
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=Düsseldorf&limit=20&sort=brief')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_snippet_020(server):
        """Create one Snippet resource.

        Send POST /snippets to create new resource. In this case all fields
        have unnecessary leading and trailing whitespaces which are removed.
        Tags and links must be sorted.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': ('first row', 'second row'),
                'brief': 'short brief',
                'description': 'long description',
                'name': 'short name',
                'groups': ('python',),
                'tags': ('spaces', 'tabs'),
                'links': ('link1', 'link2'),
                'source': 'short source link',
                'versions': ('version==1.1.1',),
                'filename': 'shortfilename.yaml',
                'created': Content.REGEXP_TIME,
                'updated': Content.REGEXP_TIME,
                'uuid': Content.UUID1,
                'digest': 'b04d8c1f2913fc3c501e129505265986f1294da0cd3e9f758561cf5443ccf69f'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['     first row   ', '   second row  '],
                    'brief': ' short brief  ',
                    'description': ' long description  ',
                    'name': '  short name   ',
                    'groups': ['    python   ',],
                    'tags': ['  tabs   ', '  spaces    '],
                    'links': ['  link2  ', '    link1   '],
                    'source': '  short source link   ',
                    'versions': ['  version==1.1.1   '],
                    'filename': '  shortfilename.yaml   '
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '630'}
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_021(server):
        """Create one Snippet resource.

        Send POST /snippets to create new resource with data that have line
        breaks in the middle of the snippet which must not be interpolated to
        newlines.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': ('docker rm $(docker\\nps \\n --all -q -f status=exited)',),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'source': '',
                'versions': (),
                'filename': '',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'uuid': Content.UUID1,
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
            'content-length': '542'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_022(server):
        """Create new snippet with duplicated content field values.

        Send POST /snippets to create a new resource. In this case the
        resource attributes contain duplicated values. For example, there is
        a tag 'python' included twice in the ``tags`` attribute. Only unique
        values in attributes in array context must be added.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': ('duplicated field values', ),
                'brief': 'short brief',
                'description': '',
                'name': '',
                'groups': ('docker', 'python'),
                'tags': ('pypy', 'swarm'),
                'links': ('http://www.dot.com/link1', 'http://www.dot.com/link2'),
                'source': '',
                'versions': ('docker-ce>17.09.2',),
                'filename': '',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'uuid': Content.UUID1,
                'digest': '800af62696ab9592c23dd5674642b91854e73a0c23f7659ac553de7fc66400d5'
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
                    'versions': ['docker-ce>17.09.2']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '619'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body, ensure_ascii=False))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_023(server):
        """Create one snippet with POST.

        Send POST /snippets to create a new resource. The ``groups`` field
        is not defined at all in the HTTP request. The default value for this
        attribute must be always added if no value is provided by client.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': ('test',),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'source': '',
                'versions': (),
                'filename': '',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'uuid': Content.UUID1,
                'digest': '4531ade7232dda7debd7ec3a20b2669afb57d665bd058184155442de203c76af',
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['test']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '492'
        }
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_201
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_snippet_024(server):
        """Create one snippet from API.

        Send POST /snippets to create a new resource with invalid version
        string. The mathematical operator ``=`` is not supported. The equal
        operation must be ``==``. This causes the version to be stored as
        empty list.
        """

        storage = {
            'data': [{
                'category': 'snippet',
                'data': ('first row', ),
                'brief': '',
                'description': '',
                'name': '',
                'groups': ('default',),
                'tags': (),
                'links': (),
                'source': '',
                'versions': (),
                'filename': '',
                'created': '2018-06-22T13:11:13.678729+00:00',
                'updated': '2018-06-22T13:11:13.678729+00:00',
                'uuid': Content.UUID1,
                'digest': '1ff004f146c8771b93eed01bf65a837ab1617d264495187560cc33347f2cd0a3'
            }]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['first row'],
                    'versions': ['version=1.1.1']
                }
            }]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '497'}
        expect_body = {
            'data': [{
                'type': 'snippet',
                'id': storage['data'][0]['uuid'],
                'attributes': storage['data'][0]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/api/snippy/rest/snippets',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.status == falcon.HTTP_400
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
