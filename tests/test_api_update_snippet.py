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

"""test_api_update_snippet: Test PUT /snippets API."""

import copy
import json

from falcon import testing
import falcon
import pytest

from snippy.config.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiUpdateSnippet(object):
    """Test PUT /snippets/{digest} API."""

    @pytest.mark.usefixtures('forced', 'remove-utc')
    def test_api_update_snippet_001(self, server, mocker):
        """Update one snippet with PUT."""

        ## Brief: Call PUT /snippy/api/v1/snippets to update existing snippet
        ##        with specified digest.
        content_read = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        content_send = {
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
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_put(  ## apiflow
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content_read)

    @pytest.mark.usefixtures('forced', 'caller')
    def test_api_update_snippet_002(self, server):
        """Update snippet from API."""

        ## Brief: Try to call PUT /snippy/api/v1/snippets to update snippet
        ##        with digest that cannot be found.
        content_send = {
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
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '369'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest 101010101010101'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_put(  ## apiflow
            path='/snippy/api/v1/snippets/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 1

    @pytest.mark.usefixtures('forced', 'caller')
    def test_api_update_snippet_003(self, server):
        """Try to update snippet with malformed queries."""

        ## Brief: Try to call PUT /snippy/api/v1/snippets to update new
        ##        snippet with malformed JSON request.
        content_send = {
            'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
            'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
            'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
            'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
            'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        }
        result_headers_p3 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '442'}
        result_headers_p2 = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '443'}
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
        result = testing.TestClient(server.server.api).simulate_put(  ## apiflow
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert len(Database.get_snippets()) == 1

    @pytest.mark.usefixtures('forced', 'netcat-utc')
    def test_api_update_snippet_004(self, server, mocker):
        """Updated snippet and verify created and updated timestamps."""

        ## Brief: Call PUT /snippy/api/v1/snippets to update existing snippet
        ##        with specified digest. This test verifies that the created
        ##        timestamp does not change and the updated timestamp changes
        ##        when the content is updated.
        content_send = {
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
        content_read = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        result_headers = {'content-type': 'application/vnd.api+json; charset=UTF-8', 'content-length': '695'}
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/snippets/54e41e9b52a02b63'
            },
            'data': {
                'type': 'snippets',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': copy.deepcopy(Snippet.DEFAULTS[Snippet.REMOVE])
            }
        }
        result_json['data']['attributes']['updated'] = Content.NETCAT_TIME
        server.run()
        result = testing.TestClient(server.server.api).simulate_put(  ## apiflow
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(content_send))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
