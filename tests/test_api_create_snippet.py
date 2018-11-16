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

"""test_api_create_snippet: Test POST /snippets API."""


import json

from falcon import testing
import falcon
import pytest

from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet

pytest.importorskip('gunicorn')


class TestApiCreateSnippet(object):
    """Test POST snippets collection API."""

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_001(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. The snippet is sent in
        list context in POST request.
        """

        content_read = Snippet.DEFAULTS[Snippet.REMOVE]
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': content_read
            }]
        }
        content = {Snippet.REMOVE_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '711'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_002(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the there
        are only part of the content attributes defined.

        The tags must be sorted and trimmed after parsing.
        """

        content_read = Snippet.DEFAULTS[Snippet.REMOVE]
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                    'groups': Snippet.DEFAULTS[Snippet.REMOVE]['groups'],
                    'tags': [' moby ', 'cleanup  ', '  container', 'docker', 'docker-ce'],
                    'links': ['https://docs.docker.com/engine/reference/commandline/rm/']
                }
            }]
        }
        content = {Snippet.REMOVE_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '711'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-exited-utc')
    def test_api_create_snippet_003(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the content
        data is defined in string context where each line is separated with a
        newline.
        """

        content_read = Snippet.DEFAULTS[Snippet.EXITED]
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.EXITED]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
                    'groups': Snippet.DEFAULTS[Snippet.EXITED]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])
                }
            }]
        }
        content = {Snippet.EXITED_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '916'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.EXITED_DIGEST,
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-exited-utc')
    def test_api_create_snippet_004(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the content
        data is defined in list context where each line is an item in a list.
        """

        content_read = Snippet.DEFAULTS[Snippet.EXITED]
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': [
                        'docker rm $(docker ps --all -q -f status=exited)\n\n\n\n',
                        'docker images -q --filter dangling=true | xargs docker rmi'
                    ],
                    'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
                    'groups': Snippet.DEFAULTS[Snippet.EXITED]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])
                }
            }]
        }
        content = {Snippet.EXITED_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '916'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.EXITED_DIGEST,
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_005(self, server):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet with only data.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': ['docker rm $(docker ps --all -q -f status=exited)\n']
                }
            }]
        }
        content_read = {
            'data': ('docker rm $(docker ps --all -q -f status=exited)',),
            'brief': '',
            'description': '',
            'groups': ('default',),
            'tags': (),
            'links': (),
            'category': 'snippet',
            'name': '',
            'filename': '',
            'versions': '',
            'source': '',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': '2017-10-14T19:56:31.000001+0000',
            'updated': '2017-10-14T19:56:31.000001+0000',
            'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'
        }
        content = {'3d855210284302d5': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '562'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc', 'create-forced-utc')
    def test_api_create_snippet_006(self, server):
        """Create list of snippets from API.

        Call POST /v1/snippets in list context to create new snippets.
        """

        content = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1481'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': Snippet.FORCED_DIGEST,
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_007(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create new snippet with malformed
        JSON request. In this case the top level json object is incorrect.
        """

        request_body = Snippet.DEFAULTS[Snippet.REMOVE]
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '889'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '891'}
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
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p3 or result.headers == result_headers_p2
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_008(self, server):
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
                    'versions': '',
                    'utc': '2017-10-14T19:56:31.000001+0000',
                    'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'}}]}
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '582'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '584'}
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': "json media validation failed: top level data object type must be 'snippet' or 'solution'"
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_009(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create new snippet with client
        generated ID. This is not supported and it will generate error.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }]
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
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_010(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create two snippets. First one is
        correctly defind but the second one contains error in JSON structure.
        This must not create any resources and the whole request must be
        considered erronous.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'attributes': {'brief': ''}
            }]
        }
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '754'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '758'}
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
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p3 or result.headers == result_headers_p2
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        Content.assert_storage(None)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_011(self, server):
        """Try to create snippet with malformed JSON request.

        Try to call POST /v1/snippets to create two snippets. First one is
        correctly defind but the second one contains error in JSON structure.
        The error is the client generated ID which is not supported. This must
        not create any resources and the whole request must be considered
        erronous request.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                'attributes':{
                    'data': ['docker rm $(docker ps --all -q -f status=exited)']
                }
            }]
        }
        result_headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '382'}
        result_json = {
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
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403
        Content.assert_storage(None)

    @pytest.mark.usefixtures('import-forced', 'update-remove-utc')
    def test_api_create_snippet_012(self, server):
        """Update snippet with POST that maps to PUT.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. In this case the resource exists and the content is updated.
        """

        content_read = Snippet.DEFAULTS[Snippet.REMOVE]
        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                    'groups': Snippet.DEFAULTS[Snippet.REMOVE]['groups'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
                }
            }
        }
        content = {Snippet.REMOVE_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '802'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63'
            },
            'data': {
                'type': 'snippet',
                'id': Snippet.REMOVE_DIGEST,
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-forced-utc')
    def test_api_create_snippet_013(self, server):
        """Update snippet with POST that maps to PATCH.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. In this case the resource exists and the content is updated.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
                }
            }
        }
        content_read = {
            'data': Snippet.DEFAULTS[Snippet.REMOVE]['data'],
            'brief': Snippet.DEFAULTS[Snippet.FORCED]['brief'],
            'description': Snippet.DEFAULTS[Snippet.FORCED]['description'],
            'groups': Snippet.DEFAULTS[Snippet.FORCED]['groups'],
            'tags': Snippet.DEFAULTS[Snippet.FORCED]['tags'],
            'links': Snippet.DEFAULTS[Snippet.FORCED]['links'],
            'category': 'snippet',
            'name': Snippet.DEFAULTS[Snippet.FORCED]['name'],
            'filename': Snippet.DEFAULTS[Snippet.FORCED]['filename'],
            'versions': Snippet.DEFAULTS[Snippet.FORCED]['versions'],
            'source': Snippet.DEFAULTS[Snippet.FORCED]['source'],
            'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.FORCED_TIME,
            'updated': Content.FORCED_TIME,
            'digest': 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
        }
        content = {'a9e137c08aee0985': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '894'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/a9e137c08aee0985'
            },
            'data': {
                'type': 'snippet',
                'id': 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-forced', 'update-exited-utc')
    def test_api_create_snippet_014(self, server):
        """Update snippet with POST that maps to PATCH.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. All fields are tried to be updated but only the that can be
        modified by user must be modified.
        """

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
                    'versions': 'versions 1.1',
                    'source': 'http://testing/snippets.html',
                    'created': 'invalid time',
                    'updated': 'invalid time',
                    'digest': 'invalid digest'
                }
            }
        }
        content_read = {
            'data': tuple(request_body['data']['attributes']['data'].split(Const.DELIMITER_DATA)),
            'brief': request_body['data']['attributes']['brief'],
            'description': request_body['data']['attributes']['description'],
            'groups': tuple(request_body['data']['attributes']['groups'].split(Const.DELIMITER_GROUPS)),
            'tags': tuple(request_body['data']['attributes']['tags'].split(Const.DELIMITER_TAGS)),
            'links': tuple(request_body['data']['attributes']['links'].split(Const.DELIMITER_LINKS)),
            'category': 'snippet',
            'name': request_body['data']['attributes']['name'],
            'filename': request_body['data']['attributes']['filename'],
            'versions': request_body['data']['attributes']['versions'],
            'source': request_body['data']['attributes']['source'],
            'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.FORCED_TIME,
            'updated': Content.EXITED_TIME,
            'digest': 'ea89da812a61078069c34bd7c45bcaca55b84e14c11b2565402bb37075d243c4'
        }
        content = {'ea89da812a610780': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '748'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/ea89da812a610780'
            },
            'data': {
                'type': 'snippet',
                'id': 'ea89da812a61078069c34bd7c45bcaca55b84e14c11b2565402bb37075d243c4',
                'attributes': content_read
            }
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_api_create_snippet_015(self, server):
        """Update snippet with POST that maps to DELETE.

        Call POST /v1/snippets with X-HTTP-Method-Override header to delete
        snippet. In this case the resource exists and the content is deleted.
        """

        content = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        result_headers = {}
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets/f3fd167c64b6f97e',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.headers == result_headers
        assert not result.text
        assert result.status == falcon.HTTP_204
        Content.assert_storage(content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_016(self, server):
        """Try to create snippet with resource id.

        Try to call POST /v1/snippets/53908d68425c61dc to create new snippet
        with resource ID in URL. The POST method is not overriden with custom
        X-HTTP-Method-Override header.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
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
            path='/snippy/api/app/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-exited-utc', 'caller')
    def test_api_create_snippet_017(self, server):
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
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '558'
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
                'title': 'content was not stored because it was matching to an empty template'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert result.json['errors'][0]['title'] == 'content was not stored because mandatory content field data is empty'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_api_create_snippet_018(self, server):
        """Create and search snippet with unicode characters.

        Call POST /v1/snippets to create new snippet. In this case the content
        contains unicode characters in string and list fields. The content must
        be also returned correctly when searching with unicode characters.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': [u'Sîne klâwen durh die wolken sint geslagen', u'er stîget ûf mit grôzer kraft'],
                    'brief': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                    'description': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                    'groups': u'Düsseldorf',
                    'tags': [u'γλώσσα', u'έδωσαν', u'ελληνική'],
                    'links': [u'http://www.чухонца.edu/~fdc/utf8/']
                }
            }]
        }
        content_read = {
            'data': tuple(request_body['data'][0]['attributes']['data']),
            'brief': request_body['data'][0]['attributes']['brief'],
            'description': request_body['data'][0]['attributes']['description'],
            'groups': [request_body['data'][0]['attributes']['groups']],
            'tags': tuple(request_body['data'][0]['attributes']['tags']),
            'links': tuple(request_body['data'][0]['attributes']['links']),
            'category': 'snippet',
            'name': '',
            'filename': '',
            'versions': '',
            'source': '',
            'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': '2017-10-14T19:56:31.000001+0000',
            'updated': '2017-10-14T19:56:31.000001+0000',
            'digest': 'c267233096b6977ea4dd9ef41faa1559d3886ad550d8932ddb4513eae5b84fbf'
        }
        content = {'c267233096b697': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '933'
        }
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': 'c267233096b6977ea4dd9ef41faa1559d3886ad550d8932ddb4513eae5b84fbf',
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body, ensure_ascii=False))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '993'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': [{
                'type': 'snippet',
                'id': 'c267233096b6977ea4dd9ef41faa1559d3886ad550d8932ddb4513eae5b84fbf',
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json; charset=UTF-8'},
            query_string='sall=Düsseldorf&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('create-regexp-utc')
    def test_api_create_snippet_019(self, server):
        """Create one snippet from API.

        Call POST /v1/snippets to create new content. In this case every
        attribute has additional leading and trailing whitespaces which must
        be trimmed. Tags and links must be sorted.
        """

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
                    'versions': '  short versions   ',
                    'source': '  short source link   '
                }
            }]
        }
        content_read = {
            'data': ('first row', 'second row'),
            'brief': 'short brief',
            'description': 'long description',
            'groups': ('python',),
            'tags': ('spaces', 'tabs'),
            'links': ('link1', 'link2'),
            'category': 'snippet',
            'name': 'short name',
            'filename': 'shortfilename.yaml',
            'versions': 'short versions',
            'source': 'short source link',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': Content.REGEXP_TIME,
            'updated': Content.REGEXP_TIME,
            'digest': 'a861de558c95d7d371a5f3664a062444fd905e225c9e7ec69ae54a5b3b4197f5'
        }
        content = {'a861de558c95d7d3': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '654'}
        result_json = {
            'data': [{
                'type': 'snippet',
                'id': 'a861de558c95d7d371a5f3664a062444fd905e225c9e7ec69ae54a5b3b4197f5',
                'attributes': content_read
            }]
        }
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json; charset=UTF-8'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
