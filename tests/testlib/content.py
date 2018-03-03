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

"""content: Content helpers for testing."""

import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

class Content(object):
    """Helper methods for content testing."""

    EXPORT_TIME = '2018-02-02 02:02:02'

    @staticmethod
    def ordered(json):
        """Sort JSON in order to compare random order JSON structures."""

        json_list = []
        if isinstance(json, list):
            json_list = (json)
        else:
            json_list.append(json)

        jsons = []
        for json_item in json_list:
            jsons.append(Content._sorter(json_item))

        return tuple(jsons)

    @staticmethod
    def verified(mocker, snippy, content):
        """Compare given content against content stored in database."""

        mocker.patch.object(Config, 'get_utc_time', side_effect=(Content.EXPORT_TIME,)*len(content))
        assert len(Database.get_contents()) == len(content)
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open()) as mock_file:
            for digest in content:
                mock_file.reset_mock()
                cause = snippy.run_cli(['snippy', 'export', '-d', digest, '-f', 'content.txt'])
                assert cause == Cause.ALL_OK
                mock_file.assert_called_once_with('content.txt', 'w')
                file_handle = mock_file.return_value.__enter__.return_value
                file_handle.write.assert_has_calls([mock.call(Snippet.get_template(content[digest])),
                                                    mock.call(Const.NEWLINE)])

    @staticmethod
    def get_api_meta():
        """Return default REST API metadata."""

        meta = {'version': __version__,
                'homepage': __homepage__,
                'docs': __docs__,
                'openapi': __openapi__}

        return meta

    @staticmethod
    def _sorter(json):
        """Sort nested JSON to allow comparison."""

        if isinstance(json, dict):
            return sorted((k, Content._sorter(v)) for k, v in json.items())
        if isinstance(json, (list, tuple)):
            return sorted(Content._sorter(x) for x in json)

        return json
