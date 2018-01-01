#!/usr/bin/env python3

"""test_api_update_snippet.py: Test PUT /snippets API."""

import json
import sys
import falcon
from falcon import testing
import mock
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.metadata import __version__
from snippy.metadata import __homepage__
from snippy.snip import Snippy
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiUpdateSnippet(object):
    """Test PUT /snippets/{digest] API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_api_update_snippet_from_api(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Update snippet from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call PUT /api/v1/snippets to update existing snippet.
        snippy = Snippet.add_one(Snippy(), Snippet.FORCED)
        snippet = {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                   'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                   'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                   'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                   'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])}
        compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '450'}
        body = [Snippet.DEFAULTS[Snippet.REMOVE]]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/api/v1/snippets/53908d68425c61dc',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_200
        assert len(Database.get_snippets()) == 1
        Snippet.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

        ## Brief: Try to call PUT /api/v1/snippets to update snippet with digest that cannot be found.
        snippy = Snippet.add_one(Snippy(), Snippet.FORCED)
        snippet = {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
                   'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
                   'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
                   'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags']),
                   'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '248'}
        body = {'metadata': Snippet.get_http_metadata(),
                'errors': [{'code': 404, 'status': '404 Not Found', 'module': 'snippy.testing.testing:123',
                            'message': 'cannot find content with message digest 101010101010101'}]}
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_put(path='/api/v1/snippets/101010101010101',  ## apiflow
                                                                    headers={'accept': 'application/json'},
                                                                    body=json.dumps(snippet))
        assert result.headers == headers
        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_snippets()) == 1
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()