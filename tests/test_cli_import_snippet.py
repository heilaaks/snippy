#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_cli_import_snippet: Test workflows for importing snippets."""

import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.snippet import Snippet


class TestCliImportSnippet(object):  # pylint: disable=too-many-public-methods
    """Test workflows for importing snippets."""

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_001(snippy):
        """Import all snippets.

        Import all snippets. File name is not defined in command line. This
        must result tool internal default file name and format being used.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.NETCAT
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./snippets.mkdn', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_snippet_002(snippy):
        """Import all snippets.

        Import all snippets from yaml file. File name and format are extracted
        from command line option -f|--file.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.NETCAT
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-snippets.yaml', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_snippet_003(snippy):
        """Import all snippets.

        Import all snippets from json file. File name and format are extracted
        from command line option -f|--file.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.NETCAT
            ]
        }
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-snippets.json', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-snippets-utc')
    def test_cli_import_snippet_004(snippy):
        """Import all snippets.

        Import all snippets from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.txt' in this
        case.

        Because text template does not have UUID, the UUID mock allocates a new
        UUID for the exported comparison. Because of this the imported resource
        UUID cannot be compared to exported text.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Content.deepcopy(Snippet.FORCED)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-snippets-utc')
    def test_cli_import_snippet_005(snippy):
        """Import all snippets.

        Import all snippets from text file. File name and format are extracted
        from command line option -f|--file. File extension is '*.text' in this
        case.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Content.deepcopy(Snippet.FORCED)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-snippets.text', 'r')

    @staticmethod
    def test_cli_import_snippet_006(snippy):
        """Import all snippets.

        Try to import snippet from file which file format is not supported.
        This should result error text for end user and no files should be
        read.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: ./foo.bar'
            Content.assert_storage(None)
            mock_file.assert_not_called()

    @staticmethod
    def test_cli_import_snippet_007(snippy):
        """Import all snippets.

        Try to import snippet from file that is not existing. The file
        extension is one of the supported file formats.
        """

        with mock.patch('snippy.content.migrate.os.path.isfile', return_value=False):
            cause = snippy.run(['snippy', 'import', '-f', './foo.yaml'])
            assert cause == 'NOK: cannot read file ./foo.yaml'
            Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_008(snippy):
        """Import all snippets.

        Try to import snippet from text file that is empty.
        """

        content = {
            'data': []
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.txt'])
            assert cause == 'NOK: could not identify content category - please keep template tags in place'
            Content.assert_storage(None)
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-remove', 'update-remove-utc')
    def test_cli_import_snippet_009(snippy):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as yaml file which contain one snippet. Content is
        not updated in this case because the same content is imported again.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.yml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-snippet.yml', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-remove', 'update-remove-utc')
    def test_cli_import_snippet_010(snippy):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as yaml file which contain one snippet. Content
        tags were updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['tags'] = ('new', 'set', 'tags')
        content['data'][0]['digest'] = '4525613eaecd52970316d7d6495f091fad1fd027834d7d82a523cbccc4aa3582'
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-snippet.yaml', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'json', 'import-remove', 'update-remove-utc')
    def test_cli_import_snippet_011(snippy):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as json file which contain one snippet. Content
        brief were updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['brief'] = 'Updated brief description'
        content['data'][0]['digest'] = 'f07547e7c692741ac5f142853899383ea0398558ffcce7c033adb8b0e12ffda5'
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-snippet.json', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'import-remove', 'update-remove-utc')
    def test_cli_import_snippet_012(snippy):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as text file which contain one snippet. Content
        links were updated. The file extension is '*.txt' in this case.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['links'] = ('https://new.link',)
        content['data'][0]['digest'] = '7681559ca5c001e204dba8ccec3fba3067049692de33a35af4a4647ec2addace'
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-snippet.txt', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'import-remove', 'update-remove-utc')
    def test_cli_import_snippet_013(snippy):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as text file which contain one snippet. Content
        links were updated. The file extension is '*.text' in this case.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['links'] = ('https://new.link', )
        content['data'][0]['digest'] = '7681559ca5c001e204dba8ccec3fba3067049692de33a35af4a4647ec2addace'
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-snippet.text', 'r')

    @staticmethod
    @pytest.mark.usefixtures('import-remove')
    def test_cli_import_snippet_014(snippy):
        """Import defined snippet.

        Try to import defined snippet with message digest that cannot be
        found. In this case there is one snippet stored.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-d', '123456789abcdef0', '-f', 'one-snippet.text'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            Content.assert_storage(content)
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('yaml')
    def test_cli_import_snippet_015(snippy):
        """Import snippet defaults.

        Import snippet defaults. All snippets should be imported from the
        predefined file location under tool data folder from yaml format.

        This case does not defined UTC time mock. This means that the time
        is read as current time by the tool. But because the timestamp is
        defined in the imported content, it must correctly match to the
        expected content.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--defaults'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/defaults/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'r')

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'default-snippets-utc')
    def test_cli_import_snippet_016(snippy):
        """Import snippet defaults.

        Try to import snippet defaults again. The second import should fail
        with an error because the content already exist. The error text must
        be the same for all content categories.

        Because of random order dictionary in the code, the reported digest
        can vary when there are multiple failures to import each content.

        Because there is unique constraint violation for ``data`` and ``uuid``
        attributes and PostgreSQL and Sqlite throw the error from different
        attributes, both attributes must be checked.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--defaults'])
            assert cause in ('NOK: content data already exist with digest 53908d68425c61dc',
                             'NOK: content uuid already exist with digest 53908d68425c61dc',
                             'NOK: content data already exist with digest 54e41e9b52a02b63',
                             'NOK: content uuid already exist with digest 54e41e9b52a02b63')
            Content.assert_storage(content)
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/defaults/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_017(snippy):
        """Import snippet from text template.

        Try to import snippet template without any changes. This should result
        error text for end user and no files should be read. The error text
        must be the same for all content types.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Snippet.TEMPLATE_TEXT))
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--template', '--format', 'text'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            mock_file.assert_called_once_with('./snippet-template.text', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml', 'default-snippets', 'import-netcat-utc')
    def test_cli_import_snippet_018(snippy):
        """Import snippets already existing.

        Import snippets from yaml file that is defined from command line. In
        this case two out of three imported snippets are already stored into
        the database. Because existing content is not considered as an error,
        the third snippet is imported successfully with success cause.

        The UUID is modified to avoid the UUID collision which produces error.
        The test verifies that user modified resource attributes do not stop
        importing multiple resources.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Content.deepcopy(Snippet.FORCED),
                Snippet.NETCAT
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-f', './snippets.yaml'])
            assert cause == Cause.ALL_OK
            content['data'][0]['uuid'] = Snippet.REMOVE_UUID
            content['data'][1]['uuid'] = Snippet.FORCED_UUID
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./snippets.yaml', 'r')

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets')
    def test_cli_import_snippet_019(snippy):
        """Import snippet based on digest.

        Try to import snippet based on message digest that matches to two
        other snippets.

        Note! Don't change the test snippets because this case is produced
        with real digests that just happen to have same digit starting both
        of the cases.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-d', '5', '-f', 'one-snippet.yaml'])
            assert cause == 'NOK: content digest 5 matched 2 times preventing import operation'
            Content.assert_storage(content)
            mock_file.assert_not_called()
            yaml.safe_load.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_020(snippy):
        """Import all snippets.

        Import all snippets from Markdown formatted file.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.NETCAT
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.md'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-snippets.md', 'r')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_021(snippy):
        """Import snippet from Markdown template.

        Try to import snippet template without any changes. This should result
        error text for end user and no files should be read. The error text
        must be the same for all content types.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Snippet.TEMPLATE_MKDN))
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--template'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            mock_file.assert_called_once_with('./snippet-template.mkdn', 'r')

    @staticmethod
    def test_cli_import_snippet_022(snippy):
        """Import all snippets.

        Try to import snippet from file which file format is not supported.
        In this case supported file extension is part of the filename when
        the file is in unknown format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', '.text.bar'])
            assert cause == 'NOK: cannot identify file format for file: .text.bar'
            Content.assert_storage(None)
            mock_file.assert_not_called()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
