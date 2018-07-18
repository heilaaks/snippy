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
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

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

    # References
    GITLOG_TIME = '2018-06-22T13:11:13.678729+0000'
    REGEXP_TIME = '2018-05-21T13:11:13.678729+0000'
    PYTEST_TIME = '2016-04-21T12:10:11.678729+0000'

    @staticmethod
    def verified(mocker, snippy, content):
        """Compare given content against content stored in database."""

        mocker.patch.object(Config, 'utcnow', side_effect=(Content.EXPORT_TIME,)*len(content))
        assert Database.get_collection().size() == len(content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open()) as mock_file:
            for digest in content:
                mock_file.reset_mock()
                cause = snippy.run(['snippy', 'export', '-d', digest, '-f', 'content.txt'])
                assert cause == Cause.ALL_OK
                mock_file.assert_called_once_with('content.txt', 'w')
                file_handle = mock_file.return_value.__enter__.return_value
                content[digest] = Content.compared(content[digest])
                file_handle.write.assert_has_calls([mock.call(Snippet.get_template(content[digest])),
                                                    mock.call(Const.NEWLINE)])

    @staticmethod
    def ordered(contents):
        """Sort JSON in order to compare random order JSON structures.

        Because the 'contents' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            contents (dict): Server response or content helper default JSON data.
        """

        contents = copy.deepcopy(contents)

        # API errors have special case that containes random order hash
        # structure inside a string. This string is masked.
        #
        # TODO: It should be possible to sort and compare this also.
        if 'errors' in contents:
            for error in contents['errors']:
                error['title'] = 'not compared because of hash structure in random order inside the string'

        # Validate predefined set of UUIDs.
        if 'data' in contents:
            if isinstance(contents['data'], list):
                for data in contents['data']:
                    if Content._any_valid_test_uuid(data['attributes']):
                        data['attributes']['uuid'] = Database.VALID_UUID
            else:
                if Content._any_valid_test_uuid(contents['data']['attributes']):
                    contents['data']['attributes']['uuid'] = Database.VALID_UUID

        # Sort the content structure in order to be able to compare it.
        json_list = []
        if isinstance(contents, list):
            json_list = (contents)
        else:
            json_list.append(contents)

        contents = []
        for content in json_list:
            contents.append(Content._sorter(content))

        return tuple(contents)

    @staticmethod
    def compared(content, validate_uuid=True):
        """Organize reference resource so that it is comparable.

        The content default helpers contains errors in the default input data
        on purpose. Running Snippy formats the input data and outputs it in a
        controlled manner. In order to be able to compare the helper default
        input content to Snippy output, the input content must be formatted
        here.

        Because the 'content' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            content (dict): Server response or content helper default JSON data.
            validate_uuid (bool): Defines if the UUID is validated or not.

        Returns:
            dict: Modified copy from original content for Snippy output reference.
        """

        content = copy.deepcopy(content)

        if 'tags' in content:
            # Remove white spaces around the tags.
            content['tags'] = tuple([tag.strip() for tag in content['tags']])

            # Tags are always sorted for all content.
            content['tags'] = tuple(sorted(content['tags']))

        if Content._any_valid_test_uuid(content) and validate_uuid:
            content['uuid'] = Database.VALID_UUID

        # The helper data may contain links in unsorted order. The links are
        # sorted based on content. Since comparison is made against the helper
        # data and the tools sorts the links in case of snippets and solutions,
        # the other than referece content must be sorted here.
        if content['category'] != Const.REFERENCE:
            content['links'] = tuple(sorted(content['links']))

        # Content data is always empty in reference response.
        if content['category'] == Const.REFERENCE and 'data' in content:
            content['data'] = ()

        return content

    @staticmethod
    def yaml_dump(yaml_dump, mock_file, filename, content):
        """Compare given content against yaml dump.

        Both test data and reference data must be validated for UUIDs. The
        list of UUIDs is predefined but it must be unique so each content may
        have any of the valid UUIDs.

        Because the 'content' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            yaml_dump (obj): Mocked yaml object.
            mock_file (obj): Mocked file object.
            filename (str): Expected filename used to for mocked file.
            content (str): Content expected to be dumped into YAML file.
        """

        content = copy.deepcopy(content)

        dictionary = yaml_dump.safe_dump.mock_calls[0][1][0]
        for data in content['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID

        for data in dictionary['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID
        mock_file.assert_called_once_with(filename, 'w')
        yaml_dump.safe_dump.assert_called_with(content, mock.ANY, default_flow_style=mock.ANY)

    @staticmethod
    def json_dump(json_dump, mock_file, filename, content):
        """Compare given content against yaml dump.

        Both test data and reference data must be validated for UUIDs. The
        list of UUIDs is predefined but it must be unique so each content may
        have any of the valid UUIDs.

        Because the 'content' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            json_dump (obj): Mocked yaml object.
            mock_file (obj): Mocked file object.
            filename (str): Expected filename used to for mocked file.
            content (str): Content expected to be dumped into JSON file.
        """

        content = copy.deepcopy(content)

        dictionary = json_dump.dump.mock_calls[0][1][0]
        for data in content['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID

        for data in dictionary['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID
        mock_file.assert_called_once_with(filename, 'w')
        json_dump.dump.assert_called_with(content, mock.ANY)

    @staticmethod
    def text_dump(mock_file, filename, contents):
        """Compare given content against yaml dump.

        Args:
            mock_file (obj): Mocked file object.
            filename (str): Expected filename used to for mocked file.
            content (str): Content expected to be dumped into text file.
        """

        # Note: The assert_has_calls does not see if one item from given list
        #       is missing. The mock_calls works by verifying all calls.
        #
        # Note: The reference content has meta but in case of text dump, that
        #       is not produced and it is not comapred here.
        references = []
        for content in contents['data']:
            references.append(mock.call(Reference.get_template(content)))
            references.append(mock.call(Const.NEWLINE))
        mock_file.assert_called_once_with(filename, 'w')
        handle = mock_file.return_value.__enter__.return_value
        assert handle.write.mock_calls == references

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
    def updated_gitlog():
        """Return updated gitlog reference."""

        # Generate updated nginx solution.
        content_read = {
            Reference.GITLOG_DIGEST: copy.deepcopy(Reference.DEFAULTS[Reference.GITLOG])
        }
        content_read[Reference.GITLOG_DIGEST]['data'] = tuple([w.replace('# Instructions how to debug nginx', '# Changed instruction set') for w in content_read[Reference.GITLOG_DIGEST]['data']])  # pylint: disable=line-too-long

        return content_read

    @staticmethod
    def _sorter(json):
        """Sort nested JSON to allow comparison."""

        if isinstance(json, dict):
            return sorted((k, Content._sorter(v)) for k, v in json.items())
        if isinstance(json, (list, tuple)):
            return sorted(Content._sorter(x) for x in json)

        return json

    @staticmethod
    def _any_valid_test_uuid(content):
        """Test if content UUID is any of the valid test UUIDs.

        Uuid can be any of the allocated UUIDs for testing. Because the test
        case can contain any order of content, the test UUIDs can in random
        order. Because of this, the test sets always the correct UUID based
        on test. There is no way to ignore specific element and this seems
        to be the only way.

        It may be that the uuid field is not returned by the server for
        example when user limits the returned fields. Because of this,
        missing filed is considered valid.
        """

        if 'uuid' not in content:
            return True

        if any(content['uuid'] in str(uuid_) for uuid_ in Database.TEST_UUIDS):
            return True


        return False


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
