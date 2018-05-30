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

import copy
import datetime
import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

class Content(object):
    """Helper methods for content testing."""

    # Contents
    EXPORT_TIME = '2018-02-02T02:02:02.000001+0000'

    # Snippets
    REMOVE_TIME = '2017-10-14T19:56:31.000001+0000'
    FORCED_TIME = '2017-10-14T19:56:31.000001+0000'
    EXITED_TIME = '2017-10-20T07:08:45.000001+0000'
    NETCAT_TIME = '2017-10-20T07:08:45.000001+0000'
    UMOUNT_TIME = '2018-05-07T11:11:55.000001+0000'

    # Solutions
    BEATS_TIME = '2017-10-20T11:11:19.000001+0000'
    NGINX_TIME = '2017-10-20T06:16:27.000001+0000'

    @staticmethod
    def ordered(json):
        """Sort JSON in order to compare random order JSON structures."""

        # API errors have special case that containes random order hash
        # structure inside a string. This string is masked. TODO: It should
        # be possible to sort this also.
        if 'errors'  in json:
            for error in json['errors']:
                error['title'] = 'not compared because of hash structure in random order inside the string'

        # Sort rest of the scenarios.
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

        mocker.patch.object(Config, 'utcnow', side_effect=(Content.EXPORT_TIME,)*len(content))
        assert Database.get_collection().size() == len(content)
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open()) as mock_file:
            for digest in content:
                mock_file.reset_mock()
                cause = snippy.run(['snippy', 'export', '-d', digest, '-f', 'content.txt'])
                assert cause == Cause.ALL_OK
                mock_file.assert_called_once_with('content.txt', 'w')
                file_handle = mock_file.return_value.__enter__.return_value
                file_handle.write.assert_has_calls([mock.call(Snippet.get_template(content[digest])),
                                                    mock.call(Const.NEWLINE)])

    @staticmethod
    def get_api_meta():
        """Return default REST API metadata."""

        meta = {
            'version': __version__,
            'homepage': __homepage__,
            'docs': __docs__,
            'openapi': __openapi__
        }

        return meta

    @staticmethod
    def get_cli_meta():
        """Return default metadata for exported data."""

        meta = {
            'updated': Content.EXPORT_TIME,
            'version': __version__,
            'homepage': __homepage__
        }

        return meta

    @staticmethod
    def imported_dict(content_read):
        """Return imported dictionary from content."""

        return {'data': list(content_read.values())}

    @staticmethod
    def mocked_open(content_read):
        """Return mocked open from content."""

        mocked_open = Const.EMPTY
        for item in content_read.values():
            mocked_open = mocked_open + Snippet.get_template(item) + Const.NEWLINE

        return mock.mock_open(read_data=mocked_open)

    @staticmethod
    def updated_nginx():
        """Return updated nginx solution."""

        # Generate updated nginx solution.
        content_read = {
            '8eb8eaa15d745af3': copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])
        }
        content_read['8eb8eaa15d745af3']['data'] = tuple([w.replace('# Instructions how to debug nginx', '# Changed instruction set') for w in content_read['8eb8eaa15d745af3']['data']])  # pylint: disable=line-too-long

        return content_read

    @staticmethod
    def updated_kafka1():
        """Return updated kafka solution."""

        # Generate updated kafka solution. No FILE defined.
        content_read = {
            '7a5bf1bc09939f42': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['7a5bf1bc09939f42']['data'] = tuple([w.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  : ') for w in content_read['7a5bf1bc09939f42']['data']])  # pylint: disable=line-too-long
        content_read['7a5bf1bc09939f42']['filename'] = Const.EMPTY

        return content_read

    @staticmethod
    def updated_kafka2():
        """Return updated kafka solution."""

        # Generate updated kafka solution. No space after FILE.
        content_read = {
            '2c4298ff3c582fe5': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['2c4298ff3c582fe5']['data'] = tuple([w.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  :') for w in content_read['2c4298ff3c582fe5']['data']])  # pylint: disable=line-too-long
        content_read['2c4298ff3c582fe5']['filename'] = Const.EMPTY

        return content_read

    @staticmethod
    def updated_kafka3():
        """Return updated kafka solution."""

        # Generate updated kafka solution. Spaces around filename.
        content_read = {
            '745c9e70eacc304b': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['745c9e70eacc304b']['data'] = tuple([w.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  :  kubernetes-docker-log-driver-kafka.txt ') for w in content_read['745c9e70eacc304b']['data']])  # pylint: disable=line-too-long
        content_read['745c9e70eacc304b']['filename'] = Const.EMPTY

        return content_read

    @staticmethod
    def _sorter(json):
        """Sort nested JSON to allow comparison."""

        if isinstance(json, dict):
            return sorted((k, Content._sorter(v)) for k, v in json.items())
        if isinstance(json, (list, tuple)):
            return sorted(Content._sorter(x) for x in json)

        return json


class Field(object):  # pylint: disable=too-few-public-methods
    """Helper methods for content field testing."""

    @staticmethod
    def is_iso8601(timestamp):
        """Test if timestamp is in ISO8601 format."""

        # Python 2 does not support timezone parsing. The %z directive is
        # available only from Python 3.2 onwards.
        if not Const.PYTHON2:
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                return False
        else:
            timestamp = timestamp[:-5]  # Remove last '+0000'.
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                return False

        return True
