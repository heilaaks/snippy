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

pytest.importorskip('gunicorn')


class TestApiUpdateSnippet(object):
    """Test PUT /snippets/{digest} API."""

    @pytest.mark.usefixtures('forced', 'remove-utc')
    def test_api_update_snippet_001(self, server, mocker):
        """Update one snippet with PUT request.

        Call PUT /v1/snippets/53908d68425c61dc to update existing snippet with
        specified digest. See 'updating content attributes' for the attribute
        list that can be changed by user.
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('forced', 'remove-utc')
    def test_api_update_snippet_002(self, server, mocker):
        """Update one snippet with PUT request.

        Call PUT /v1/snippets/53908d68425c61dc to update existing snippet with
        specified digest. Only partial set of attributes that can be modified
        is sent in request.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                    'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                    'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
                }
            }
        }
        content_read = {
            'data': Snippet.DEFAULTS[Snippet.REMOVE]['data'],
            'brief': '',
            'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
            'tags': [],
            'links': Snippet.DEFAULTS[Snippet.REMOVE]['links'],
            'category': 'snippet',
            'filename': '',
            'runalias': '',
            'versions': '',
            'created': Content.REMOVE_TIME,
            'updated': Content.REMOVE_TIME,
            'digest': 'e56c2183edcc3a67cab99e6064439495a8af8a1d0b78bc538acd6079c841f27f'
        }
        content = {'e56c2183edcc3a67': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '601'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/snippets/e56c2183edcc3a67'
            },
            'data': {
                'type': 'snippets',
                'id': 'e56c2183edcc3a67cab99e6064439495a8af8a1d0b78bc538acd6079c841f27f',
                'attributes': content_read
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('forced', 'remove-utc')
    def test_api_update_snippet_003(self, server, mocker):
        """Update one snippet with PUT request.

        Call PUT /v1/snippets/53908d68425c61dc to update existing snippet with
        specified digest. The PUT request contains only the mandatory data
        attribute. All other attributes must be set to their default values.
        """

        request_body = {
            'data': {
                'type': 'snippet',
                'attributes': {
                    'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                }
            }
        }
        content_read = {
            'data': Snippet.DEFAULTS[Snippet.REMOVE]['data'],
            'brief': '',
            'group': 'default',
            'tags': [],
            'links': [],
            'category': 'snippet',
            'filename': '',
            'runalias': '',
            'versions': '',
            'created': Content.REMOVE_TIME,
            'updated': Content.REMOVE_TIME,
            'digest': '26128ea95707a3a2623bb2613a17f50e29a5ab5232b8ba7ca7f1c96cb1ea5c58'
        }
        content = {'26128ea95707a3a26': content_read}
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '544'
        }
        result_json = {
            'links': {
                'self': 'http://falconframework.org/snippy/api/v1/snippets/26128ea95707a3a2'
            },
            'data': {
                'type': 'snippets',
                'id': '26128ea95707a3a2623bb2613a17f50e29a5ab5232b8ba7ca7f1c96cb1ea5c58',
                'attributes': content_read
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @pytest.mark.usefixtures('forced', 'caller')
    def test_api_update_snippet_004(self, server):
        """Try to update snippet with malformed request.

        Try to call PUT /v1/snippets/101010101010101 to update snippet with
        digest that cannot be found.
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/v1/snippets/101010101010101',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 1

    @pytest.mark.usefixtures('forced', 'caller')
    def test_api_update_snippet_005(self, server):
        """Try to update snippet with malformed request.

        Try to call PUT /v1/snippets/53908d68425c61dc to update new snippet
        with malformed JSON request.
        """

        request_body = {
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers_p2 or result.headers == result_headers_p3
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400
        assert len(Database.get_snippets()) == 1

    @pytest.mark.usefixtures('forced', 'netcat-utc')
    def test_api_update_snippet_006(self, server, mocker):
        """Updated snippet and verify created and updated timestamps.

        Call PUT /v1/snippets/53908d68425c61dc to update existing snippet
        with specified digest. This test verifies that the created timestamp
        does not change and the updated timestamp changes when the content is
        updated.
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
        result = testing.TestClient(server.server.api).simulate_put(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content_read)

    @pytest.mark.usefixtures('forced', 'forced-utc')
    def test_api_update_snippet_007(self, server, mocker):
        """Update one snippet with PATCH request.

        Call PATCH /v1/snippets/53908d68425c61dc to update existing snippet
        with specified digest. The PATCH request contains only mandatory data
        attribute. All other attributes must be returned with their previous
        values.
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
        result = testing.TestClient(server.server.api).simulate_patch(
            path='/snippy/api/v1/snippets/53908d68425c61dc',
            headers={'accept': 'application/vnd.api+json'},
            body=json.dumps(request_body))
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, server, content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
