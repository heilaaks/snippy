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

"""test_api_create_snippet: Test POST /snippets API."""

import json

from falcon import testing
import falcon
import pytest

from snippy.config.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

pytest.importorskip('gunicorn')


class TestApiCreateSnippet(object):
    """Test POST snippets collection API."""

    @pytest.mark.usefixtures('remove-utc')
    def test_api_create_snippet_001(self, server, mocker):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }]
        }
        content_read = Snippet.DEFAULTS[Snippet.REMOVE]
        content = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '608'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': content_read
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('remove-utc')
    def test_api_create_snippet_002(self, server, mocker):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the links
        and list are defined as list in the JSON message. Note that the
        default input for tags and links from Snippet.REMOVE maps to a string
        but the syntax in this case maps to lists with multiple items.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                    'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                    'tags': ['cleanup', 'container', 'docker', 'docker-ce', 'moby'],
                    'links': ['https://docs.docker.com/engine/reference/commandline/rm/']
                }
            }]
        }
        content_read = Snippet.DEFAULTS[Snippet.REMOVE]
        content = {Snippet.REMOVE_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '608'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': content_read
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('exited-utc')
    def test_api_create_snippet_003(self, server, mocker):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the content
        data is defined in string context where each line is separated with a
        newline.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.EXITED]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
                    'group': Snippet.DEFAULTS[Snippet.EXITED]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])
                }
            }]
        }
        content_read = Snippet.DEFAULTS[Snippet.EXITED]
        content = {Snippet.EXITED_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '813'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('exited-utc')
    def test_api_create_snippet_004(self, server, mocker):
        """Create one snippet with POST.

        Call POST /v1/snippets to create new snippet. In this case the content
        data is defined in list context where each line is an item in a list.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': {
                    'data': [
                        'docker rm $(docker ps --all -q -f status=exited)\n\n\n\n',
                        'docker images -q --filter dangling=true | xargs docker rmi'
                    ],
                    'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
                    'group': Snippet.DEFAULTS[Snippet.EXITED]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])
                }
            }]
        }
        content_read = Snippet.DEFAULTS[Snippet.EXITED]
        content = {Snippet.EXITED_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '813'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('remove-utc')
    def test_api_create_snippet_005(self, server, mocker):
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
            'data': ['docker rm $(docker ps --all -q -f status=exited)'],
            'brief': '',
            'group':
            'default',
            'tags': [],
            'links': [],
            'category': 'snippet',
            'filename': '',
            'runalias': '',
            'versions': '',
            'created': '2017-10-14 19:56:31',
            'updated': '2017-10-14 19:56:31',
            'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'
        }
        content = {'3d855210284302d5': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '459'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                'attributes': content_read
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('remove-utc', 'forced-utc')
    def test_api_create_snippet_006(self, server, mocker):
        """Create list of snippets from API.

        Call POST /v1/snippets in list context to create new snippets.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        content = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1275'
        }
        result_json = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippets',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_007(self, server):
        """Try to create snippet with malformed queries.

        Try to call POST /v1/snippets to create new snippet with malformed
        JSON request. In this case the top level json object is incorrect.
        """

        request_body = Snippet.DEFAULTS[Snippet.REMOVE]
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '656'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '652'}
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'not compared because of hash structure in random order inside the string'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_008(self, server):
        """Try to create snippet with malformed queries.

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
                    'group':
                    'default',
                    'tags': [],
                    'links': [],
                    'category': 'snippet',
                    'filename': '',
                    'runalias': '',
                    'versions': '',
                    'utc': '2017-10-14 19:56:31',
                    'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'}}]}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '404'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': "json media validation failed: top level data object type must be 'snippet' or 'solution'"
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_009(self, server):
        """Try to create snippet with malformed queries.

        Try to call POST /v1/snippets to create new snippet with client
        generated ID. This is not supported and it will generate error.
        """

        request_body = {
            'data': [{
                'type': 'snippet',
                'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
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
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_010(self, server):
        """Try to create snippet with malformed queries.

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
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '624'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '623'}
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'not compared because of hash structure in random order inside the string'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert not Database.get_snippets()

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_011(self, server):
        """Try to create snippet with malformed queries.

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
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_403
        assert not Database.get_snippets()

    @pytest.mark.usefixtures('forced', 'remove-utc')
    def test_api_create_snippet_012(self, server, mocker):
        """Update snippet with POST that maps to PUT.

        Call POST /v1/snippets with X-HTTP-Method-Override header to update
        snippet. In this case the resource exists and the content is updated.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                    'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                    'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                    'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
                }
            }
        }
        content_read = Snippet.DEFAULTS[Snippet.REMOVE]
        content = {Snippet.REMOVE_DIGEST: content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '695'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/snippets/54e41e9b52a02b63'
            },
            'data': {
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': content_read
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PUT'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('forced', 'forced-utc')
    def test_api_create_snippet_013(self, server, mocker):
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
            'group': Snippet.DEFAULTS[Snippet.FORCED]['group'],
            'tags': Snippet.DEFAULTS[Snippet.FORCED]['tags'],
            'links': Snippet.DEFAULTS[Snippet.FORCED]['links'],
            'category': 'snippet',
            'filename': Snippet.DEFAULTS[Snippet.FORCED]['filename'],
            'runalias': Snippet.DEFAULTS[Snippet.FORCED]['runalias'],
            'versions': Snippet.DEFAULTS[Snippet.FORCED]['versions'],
            'created': Content.FORCED_TIME,
            'updated': Content.FORCED_TIME,
            'digest': 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
        }
        content = {'a9e137c08aee0985': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '787'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/snippets/a9e137c08aee0985'
            },
            'data': {
                'type': 'snippets',
                'id': 'a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2',
                'attributes': content_read
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('default-snippets', 'netcat')
    def test_api_create_snippet_014(self, server, mocker):
        """Update snippet with POST that maps to DELETE.

        Call POST /v1/snippets with X-HTTP-Method-Override header to delete
        snippet. In this case the resource exists and the content is deleted.
        """

        content = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        result_headers = {}
        server.run()
        assert len(Database.get_snippets()) == 3
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets/f3fd167c64b6f97e',
            headers={'accept': 'application/json', 'X-HTTP-Method-Override': 'DELETE'})
        assert result.headers == result_headers
        assert not result.text
        assert result.status == falcon.HTTP_204
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('caller')
    def test_api_create_snippet_015(self, server):
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
        server.run()
        result = testing.TestClient(server.server.api).simulate_post(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
