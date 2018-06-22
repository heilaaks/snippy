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

"""test_cli_import_snippet: Test workflows for importing snippets."""

import copy
import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliImportSnippet(object):
    """Test workflows for importing snippets."""

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_001(self, snippy, yaml_load, mocker):
        """Import all snippets.

        Import all snippets. File name is not defined in command line. This
        must result tool internal default file name and format being used.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.NETCAT_DIGEST: Snippet.DEFAULTS[Snippet.NETCAT]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        yaml_load.assert_called_once_with('./snippets.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_002(self, snippy, yaml_load, mocker):
        """Import all snippets.

        Import all snippets from yaml file. File name and format are extracted
        from command line option -f|--file.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.NETCAT_DIGEST: Snippet.DEFAULTS[Snippet.NETCAT]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-f', './all-snippets.yaml'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        yaml_load.assert_called_once_with('./all-snippets.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_003(self, snippy, json_load, mocker):
        """Import all snippets.

        Import all snippets from json file. File name and format are extracted
        from command line option -f|--file.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.NETCAT_DIGEST: Snippet.DEFAULTS[Snippet.NETCAT]
        }
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-f', './all-snippets.json'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        json_load.assert_called_once_with('./all-snippets.json', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_004(self, snippy, mocker):
        """Import all snippets.

        Import all snippets from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.txt' in this
        case.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.NETCAT_DIGEST: Snippet.DEFAULTS[Snippet.NETCAT]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert Database.get_snippets().size() == 2
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_005(self, snippy, mocker):
        """Import all snippets.

        Import all snippets from text file. File name and format are extracted
        from command line option -f|--file. File extension is '*.text' in this
        case.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.NETCAT_DIGEST: Snippet.DEFAULTS[Snippet.NETCAT]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert Database.get_snippets().size() == 2
            mock_file.assert_called_once_with('./all-snippets.text', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_snippet_006(self, snippy):
        """Import all snippets.

        Try to import snippet from file which file format is not supported.
        This should result error text for end user and no files should be
        read.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './foo.bar'])  ## workflow
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_collection().size()
            mock_file.assert_not_called()

    def test_cli_import_snippet_007(self, snippy):
        """Import all snippets.

        Try to import snippet from file that is not existing. The file
        extension is one of the supported file formats.
        """

        with mock.patch('snippy.content.migrate.os.path.isfile', return_value=False):
            cause = snippy.run(['snippy', 'import', '-f', './foo.yaml'])  ## workflow
            assert cause == 'NOK: cannot read file ./foo.yaml'
            assert not Database.get_collection().size()

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_008(self, snippy):
        """Import all snippets.

        Try to import snippet from text file that is empty.
        """

        mocked_open = mock.mock_open(read_data=Const.EMPTY)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-snippets.txt'])  ## workflow
            assert cause == 'NOK: could not identify text template content category'
            assert not Database.get_collection().size()
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')

    @pytest.mark.usefixtures('import-remove', 'import-remove-utc', 'isfile_true')
    def test_cli_import_snippet_009(self, snippy, yaml_load, mocker):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as yaml file which contain one snippet. Content is
        not updated in this case because the same content is imported again.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.yaml'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        yaml_load.assert_called_once_with('one-snippet.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-remove', 'import-remove-utc', 'isfile_true')
    def test_cli_import_snippet_010(self, snippy, yaml_load, mocker):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as yaml file which contain one snippet. Content
        tags were updated.
        """

        content_read = {
            '4525613eaecd5297': copy.deepcopy(Snippet.DEFAULTS[Snippet.REMOVE])
        }
        content_read['4525613eaecd5297']['tags'] = ('new', 'tags', 'set')
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.yaml'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        yaml_load.assert_called_once_with('one-snippet.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-remove', 'import-remove-utc', 'isfile_true')
    def test_cli_import_snippet_011(self, snippy, json_load, mocker):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as json file which contain one snippet. Content
        brief were updated.
        """

        content_read = {
            'f07547e7c692741a': copy.deepcopy(Snippet.DEFAULTS[Snippet.REMOVE])
        }
        content_read['f07547e7c692741a']['brief'] = 'Updated brief description'
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.json'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        json_load.assert_called_once_with('one-snippet.json', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-remove', 'update-remove-utc', 'isfile_true')
    def test_cli_import_snippet_012(self, snippy, mocker):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as text file which contain one snippet. Content
        links were updated. The file extenansion is '*.txt' in this case.
        """

        content_read = {
            '7681559ca5c001e2': copy.deepcopy(Snippet.DEFAULTS[Snippet.REMOVE])
        }
        content_read['7681559ca5c001e2']['links'] = ('https://new.link', )
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert Database.get_snippets().size() == 1
            mock_file.assert_called_once_with('one-snippet.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-remove', 'update-remove-utc', 'isfile_true')
    def test_cli_import_snippet_013(self, snippy, mocker):
        """Import defined snippet.

        Import defined snippet based on message digest. File name is defined
        from command line as text file which contain one snippet. Content
        links were updated. The file extenansion is '*.text' in this case.
        """

        content_read = {
            '7681559ca5c001e2': copy.deepcopy(Snippet.DEFAULTS[Snippet.REMOVE])
        }
        content_read['7681559ca5c001e2']['links'] = ('https://new.link', )
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert Database.get_snippets().size() == 1
            mock_file.assert_called_once_with('one-snippet.text', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-remove')
    def test_cli_import_snippet_014(self, snippy, mocker):
        """Import defined snippet.

        Try to import defined snippet with message digest that cannot be
        found. In this case there is one snippet stored.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-d', '123456789abcdef0', '-f', 'one-snippet.text'])  ## workflow
            assert cause == 'NOK: cannot find: snippet :identified with digest: 123456789abcdef0'
            assert Database.get_snippets().size() == 1
            mock_file.assert_not_called()
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_snippet_015(self, snippy, yaml_load, mocker):
        """Import snippet defaults.

        Import snippet defaults. All snippets should be imported from
        predefined file location under tool data folder from yaml format.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--defaults'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
        yaml_load.assert_called_once_with(defaults_snippets, 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets', 'import-remove-utc', 'import-forced-utc')
    def test_cli_import_snippet_016(self, snippy, yaml_load, mocker):
        """Import snippet defaults.

        Try to import snippet defaults again. The second import should fail
        with an error because the content already exist. The error text must
        be the same for all content categories. Because of random order
        dictionary in the code, the reported digest can vary if there are
        multiple failures.

        TODO: The UTC time mocking is likely incorrect here.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--defaults'])  ## workflow
        assert cause == 'NOK: content data already exist with digest 53908d68425c61dc' or \
               cause == 'NOK: content data already exist with digest 54e41e9b52a02b63'
        assert Database.get_snippets().size() == 2
        defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
        yaml_load.assert_called_once_with(defaults_snippets, 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_snippet_017(self, snippy):
        """Import defined snippet.

        Try to import snippet template without any changes. This should result
        error text for end user and no files should be read. The error text
        must be the same for all content types.
        """

        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Snippet.TEMPLATE))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--template'])  ## workflow
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            assert not Database.get_snippets().size()
            mock_file.assert_called_once_with('./snippet-template.txt', 'r')

    @pytest.mark.usefixtures('default-snippets', 'import-remove-utc', 'import-netcat-utc', 'isfile_true')
    def test_cli_import_snippet_018(self, snippy, yaml_load, mocker):
        """Import snippets already existing.

        Import snippets from yaml file that is defined from command line. In
        this case one of the two snippets is already existing. Because the
        content existing is not considered as an error and another snippet
        is imported successfully, the result cause is OK.

        TODO: The UTC time mocking is likely incorrect here.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.NETCAT_DIGEST: Snippet.DEFAULTS[Snippet.NETCAT]
        }
        yaml.safe_load.return_value = copy.deepcopy(Content.imported_dict(content_read))
        content_read[Snippet.FORCED_DIGEST] = Snippet.DEFAULTS[Snippet.FORCED]
        cause = snippy.run(['snippy', 'import', '-f', './snippets.yaml'])  ## workflow
        assert cause == Cause.ALL_OK
        assert Database.get_collection().size() == 3
        yaml_load.assert_called_once_with('./snippets.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_import_snippet_019(self, snippy, yaml_load, mocker):
        """Import snippet based on digest.

        Try to import snippet based on message digest that matches to two
        snippets. Note! Don't not change the test snippets because this case
        is produced with real digests that just happen to have same digit
        starting both of the cases.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-d', '5', '-f', 'one-snippet.yaml'])  ## workflow
        assert cause == 'NOK: cannot import: snippet :because digest: 5 :matched: 2 :times'
        assert Database.get_snippets().size() == 2
        assert not yaml_load.mock_calls
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
