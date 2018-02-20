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
import mock
import pytest

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiCreateSnippet(object):
    """Test POST /snippets API."""

    @pytest.mark.usefixtures('server', 'snippy', 'remove_utc')
    def test_api_create_snippet_001(self, snippy, mocker):
        """Create one snippet with POST."""

        ## Brief: Call POST /snippy/api/v1/snippets to create new snippet.
        content_read = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
        content_send = {
            'data': [{
                'type': 'snippet',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '608'
        }
        result_body = {
            'data': [{
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }]
        }
        snippy.run_server()
        result = testing.TestClient(snippy.server.api).simulate_post(  ## apiflow
            path='/snippy/api/v1/snippets',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_body)
        assert result.status == falcon.HTTP_201
        Content.verified(mocker, snippy, content_read)

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_create_snippet_002(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Create one snippet from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.REMOVE_CREATED
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call POST /snippy/api/v1/snippets to create new snippet. In
        ##        this case the links and list are defined as list in the JSON
        ##        message. Note that the default input for tags and links from
        ##        Snippet.REMOVE maps to a string but the syntax in this case
        ##        maps to lists with multiple items.
        snippet = {'data': [{'type': 'snippet',
                             'attributes': {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                                            'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                                            'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                                            'tags': ['cleanup', 'container', 'docker', 'docker-ce', 'moby'],
                                            'links': ['https://docs.docker.com/engine/reference/commandline/rm/']}}]}
        compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '608'}
        body = {'data': [{'type': 'snippets',
                          'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                          'attributes': Snippet.DEFAULTS[Snippet.REMOVE]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Snippet.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call POST /snippy/api/v1/snippets to create new snippet. In
        ##        this case the content data is defined in string context where
        ##        each line is separated with a newline.
        mock_get_utc_time.return_value = Snippet.EXITED_CREATED
        snippet = {'data': [{'type': 'snippet',
                             'attributes': {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.EXITED]['data']),
                                            'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
                                            'group': Snippet.DEFAULTS[Snippet.EXITED]['group'],
                                            'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
                                            'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])}}]}
        compare_content = {'49d6916b6711f13d': Snippet.DEFAULTS[Snippet.EXITED]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '813'}
        body = {'data': [{'type': 'snippets',
                          'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                          'attributes': Snippet.DEFAULTS[Snippet.EXITED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Snippet.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call POST /snippy/api/v1/snippets to create new snippet. In
        ##        this case the content data is defined in list context where
        ##        each line is an item in a list.
        mock_get_utc_time.return_value = Snippet.EXITED_CREATED
        snippet = {'data': [{'type': 'snippet',
                             'attributes': {'data': ['docker rm $(docker ps --all -q -f status=exited)\n\n\n\n',
                                                     'docker images -q --filter dangling=true | xargs docker rmi'],
                                            'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
                                            'group': Snippet.DEFAULTS[Snippet.EXITED]['group'],
                                            'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
                                            'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])}}]}
        compare_content = {'49d6916b6711f13d': Snippet.DEFAULTS[Snippet.EXITED]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '813'}
        body = {'data': [{'type': 'snippets',
                          'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                          'attributes': Snippet.DEFAULTS[Snippet.EXITED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Snippet.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Call POST /snippy/api/v1/snippets to create new snippet with
        ##        only data.
        mock_get_utc_time.return_value = Snippet.REMOVE_CREATED
        snippet = {'data': [{'type': 'snippet',
                             'attributes': {'data': ['docker rm $(docker ps --all -q -f status=exited)\n']}}]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '459'}
        body = {'data': [{'type': 'snippets',
                          'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                          'attributes': {'data': ['docker rm $(docker ps --all -q -f status=exited)'],
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
                                         'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'}}]}
        compare = {'3d855210284302d5': body['data'][0]['attributes']}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 1
        Snippet.test_content2(compare)
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_create_snippets(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Create list of snippets from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.FORCED_CREATED
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call POST /api/v1/snippets in list context to create
        ##        new snippets.
        snippets = {'data': [{'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]}]}
        compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '1275'}
        body = {'data': [{'type': 'snippets',
                          'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                          'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                         {'type': 'snippets',
                          'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                          'attributes': Snippet.DEFAULTS[Snippet.FORCED]}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippets))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_snippets()) == 2
        Snippet.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_create_snippet_errors(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Try to create snippet with malformed queries."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.REMOVE_CREATED
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Try to call POST /snippy/api/v1/snippets to create new
        ##        snippet with malformed JSON request. In this case the
        ##        top level json object is incorrect.
        snippet = Snippet.DEFAULTS[Snippet.REMOVE]
        headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '656'}
        headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '652'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '400', 'statusString': '400 Bad Request', 'module': 'snippy.testing.testing:123',
                            'title': 'not compared because of hash structure in random order inside the string'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers_p2 or result.headers == headers_p3
        assert Snippet.error_body(result.json) == Snippet.error_body(body)
        assert result.status == falcon.HTTP_400
        snippy.release()
        snippy = None
        Database.delete_storage()

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.REMOVE_CREATED
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Try to call POST /snippy/api/v1/snippets to create new
        ##        snippet with malformed JSON request. In this case the
        ##        top level data JSON object type is not 'snippet' or
        ##        'solution'.
        snippet = {'data': [{'type': 'snippe',
                             'id': '1',
                             'attributes': {'data': ['docker rm $(docker ps --all -q -f status=exited)'],
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
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '404'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '400', 'statusString': '400 Bad Request', 'module': 'snippy.testing.testing:123',
                            'title': "json media validation failed: top level data object type must be 'snippet' or 'solution'"}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_400
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call POST /snippy/api/v1/snippets to create new
        ##        snippet with client generated ID. This is not supported
        ##        and it will generate error.
        snippet = {'data': [{'type': 'snippet',
                             'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                             'attributes': Snippet.DEFAULTS[Snippet.REMOVE]}]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '382'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '403', 'statusString': '403 Forbidden', 'module': 'snippy.testing.testing:123',
                            'title': 'client generated resource id is not supported, remove member data.id'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_403
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call POST /snippy/api/v1/snippets to create two
        ##        snippets. First one is correctly defind but the second
        ##        one contains error in JSON strcutre. This must not create
        ##        any resources and the whole request must be considered
        ##        erronous.
        snippets = {'data': [{'type': 'snippet',
                              'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet',
                              'attributes': {'brief': ''}}]}
        headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '624'}
        headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '623'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '400', 'statusString': '400 Bad Request', 'module': 'snippy.testing.testing:123',
                            'title': 'not compared because of hash structure in random order inside the string'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippets))
        assert result.headers == headers_p2 or result.headers == headers_p3
        assert Snippet.error_body(result.json) == Snippet.error_body(body)
        assert result.status == falcon.HTTP_400
        assert not Database.get_snippets()
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call POST /snippy/api/v1/snippets to create two
        ##        snippets. First one is correctly defind but the second
        ##        one contains error in JSON strcutre. The error is the
        ##        client generated ID which is not supported. This must
        ##        not create any resources and the whole request must be
        ##        considered erronous
        snippets = {'data': [{'type': 'snippet',
                              'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet',
                              'id': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd',
                              'attributes': {'data': ['docker rm $(docker ps --all -q -f status=exited)']}}]}
        headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '382'}
        body = {'meta': Snippet.get_http_metadata(),
                'errors': [{'status': '403', 'statusString': '403 Forbidden', 'module': 'snippy.testing.testing:123',
                            'title': 'client generated resource id is not supported, remove member data.id'}]}
        snippy = Snippy(['snippy', '--server'])
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/snippets',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(snippets))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_403
        assert not Database.get_snippets()
        snippy.release()
        snippy = None
        Database.delete_storage()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
