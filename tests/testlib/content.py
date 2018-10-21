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
import re

import mock
import pprintpp

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
    INTERP_TIME = '2018-01-11T07:59:46.000001+0000'

    # Solutions
    BEATS_TIME = '2017-10-20T11:11:19.000001+0000'
    NGINX_TIME = '2017-10-20T06:16:27.000001+0000'

    # References
    GITLOG_TIME = '2018-06-22T13:11:13.678729+0000'
    REGEXP_TIME = '2018-05-21T13:11:13.678729+0000'
    PYTEST_TIME = '2016-04-21T12:10:11.678729+0000'

    JSON = Const.CONTENT_FORMAT_JSON
    MKDN = Const.CONTENT_FORMAT_MKDN
    TEXT = Const.CONTENT_FORMAT_TEXT
    YAML = Const.CONTENT_FORMAT_YAML

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
                file_handle.write.assert_has_calls([mock.call(Snippet.get_template(content[digest]) + Const.NEWLINE)])

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
    def compare_mkdn(mock_file, filename, content):
        """Compare Markdown content against reference content.

        Reference content and calls to file mock are modified so that the
        UUID's can be compated.

        The reference content is modifed in a local copy in order to avoid
        changing the given reference content which may affect to sequential
        tests.

        Args:
            mock_file (obj): Mocked file where the Markdown content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content.
        """

        references = Const.EMPTY
        content = copy.deepcopy(content)
        for data in content['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID
            references = references + Reference.dump(data, Content.MKDN)
            references = references + '\n---\n\n'
        references = references[:-6]  # Remove last separator added by the loop.
        references = [references]

        mock_calls = []
        handle = mock_file.return_value.__enter__.return_value
        for call in handle.write.mock_calls:
            match = re.compile(r'''
                uuid\s+[:]\s+    # Match tag for uuid.
                (?P<uuids>\S+)   # Catch uuid.
                \s+
                ''', re.VERBOSE).findall(call[1][0])
            if match:
                if set(match) < set(Database.TEST_UUIDS_STR):
                    mock_calls.append(re.sub(r'uuid     : \S+', 'uuid     : ' + Database.VALID_UUID, call[1][0]))
        try:
            mock_file.assert_called_once_with(filename, 'w')
            assert mock_calls == references
        except AssertionError:
            Content._print_compare(mock_file, mock_calls, references, filename)
            raise AssertionError

    @staticmethod
    def text_dump(mock_file, filename, content):
        """Compare given content against yaml dump.

        Args:
            mock_file (obj): Mocked file where the text content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content.
        """

        references = Const.EMPTY
        content = copy.deepcopy(content)
        for data in content['data']:
            references = references + Reference.dump(data, Content.TEXT)
            references = references + '\n'
        references = [references]

        mock_calls = []
        handle = mock_file.return_value.__enter__.return_value
        for call in handle.write.mock_calls:
            mock_calls.append(call[1][0])
        try:
            mock_file.assert_called_once_with(filename, 'w')
            assert mock_calls == references
        except AssertionError:
            Content._print_compare(mock_file, mock_calls, references, filename)
            raise AssertionError

    @staticmethod
    def yaml_dump(yaml_dump, mock_file, filename, content, call=0):
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
            call (int): The call order number for yaml dump.
        """

        content = copy.deepcopy(content)
        for data in content['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID

        dictionary = yaml_dump.safe_dump.mock_calls[call][1][0]
        for data in dictionary['data']:
            if Content._any_valid_test_uuid(data):
                data['uuid'] = Database.VALID_UUID

        try:
            mock_file.assert_any_call(filename, 'w')
            yaml_dump.safe_dump.assert_any_call(content, mock.ANY, default_flow_style=mock.ANY)
        except AssertionError:
            print("===REFERENCES===")
            pprintpp.pprint(content)
            print("===MOCK_CALLS===")
            pprintpp.pprint(yaml_dump.safe_dump.mock_calls[0][1][0])
            print("================")

            raise AssertionError

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
            '95f16957636d5da3': copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])
        }
        content_read['95f16957636d5da3']['data'] = tuple([w.replace('# Instructions how to debug nginx', '# Changed instruction set') for w in content_read['95f16957636d5da3']['data']])  # pylint: disable=line-too-long

        return content_read

    @staticmethod
    def updated_kafka1():
        """Return updated kafka solution."""

        # Generate updated kafka solution. No FILE defined.
        content_read = {
            '6363c15263ea0a77': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['6363c15263ea0a77']['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   : ') for w in content_read['6363c15263ea0a77']['data']])  # pylint: disable=line-too-long
        content_read['6363c15263ea0a77']['filename'] = Const.EMPTY
        content_read['6363c15263ea0a77']['digest'] = '6363c15263ea0a77c17adbe0ef1e032abe39eb9ceb45b99fb87875df297d2950'

        return content_read

    @staticmethod
    def updated_kafka2():
        """Return updated kafka solution."""

        # Generate updated kafka solution. No space after FILE.
        content_read = {
            '981c93230a869f56': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['981c93230a869f56']['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   :') for w in content_read['981c93230a869f56']['data']])  # pylint: disable=line-too-long
        content_read['981c93230a869f56']['filename'] = Const.EMPTY
        content_read['981c93230a869f56']['digest'] = '981c93230a869f5616bb18046ebd7a3b6c02a1bfcfc03d4a1ca5111b410e165c'

        return content_read

    @staticmethod
    def updated_kafka3():
        """Return updated kafka solution."""

        # Generate updated kafka solution. Spaces around filename.
        content_read = {
            '21c1d813c414aec8': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['21c1d813c414aec8']['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   :  kubernetes-docker-log-driver-kafka.txt ') for w in content_read['21c1d813c414aec8']['data']])  # pylint: disable=line-too-long
        content_read['21c1d813c414aec8']['filename'] = Const.EMPTY

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

    @staticmethod
    def _print_compare(mock_file, mock_calls, references, filename):
        """Print comparison data.

        Compare mock and references so that the first difference is searched
        and then add few extra lines after first failure. The failure and all
        following lines are colored differently from standard line color.

        The comparing output is printed side by side from mock and references.
        """

        # Color code lengths must be equal to align output correctly. Also when
        # the failure colors are added, the normal coloring is removed in order
        # to maintain correct text alignment.
        fail = '\033[1m'
        succ = '\x1b[2m'
        endc = '\x1b[0m'
        references = references[0].splitlines()
        mock_calls = mock_calls[0].splitlines()
        references = [succ + line + endc for line in references]
        mock_calls = [succ + line + endc for line in mock_calls]
        idx = 0
        for idx, line in enumerate(references):
            if line != mock_calls[idx]:
                break
        references = references[0:idx+5]
        mock_calls = mock_calls[0:idx+5]
        for i in range(idx, len(references)):
            references[i] = fail + Const.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', references[i]) + endc
            mock_calls[i] = fail + Const.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', mock_calls[i]) + endc
        max_len = len(max(references+mock_calls, key=len))
        compare = Const.NEWLINE.join("| {:<{len}} | {:{len}}".format(x, y, len=max_len) for x, y in zip(references, mock_calls))

        print('+' + "=" *(80*2))
        reference_file = filename + ' - w'
        mock_call_file = mock_file.mock_calls[0][1][0] + ' - ' + mock_file.mock_calls[0][1][1]
        max_len_header = max_len-len(succ)-len(endc)- len('references: ')
        print("| references: {:<{len}} | mock calls: {:{len}}".format(reference_file, mock_call_file, len=max_len_header))
        print('+' + "=" *(80*2))
        print(compare)
        print('+' + "=" *(80*2))


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
