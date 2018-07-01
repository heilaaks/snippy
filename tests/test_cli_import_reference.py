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

"""test_cli_import_reference: Test workflows for importing references."""

import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliImportReference(object):
    """Test workflows for importing references."""

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_001(self, snippy, yaml_load, mocker):
        """Import all references.

        Import all references. File name is not defined in command line. This
        should result tool internal default file name and format being used.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--reference'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 2
        yaml_load.assert_called_once_with('./references.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_002(self, snippy, yaml_load, mocker):
        """Import all references.

        Import all references from yaml file. File name and format are extracted
        from command line option -f|--file. In this case the content category is
        explicitly defined from command line.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--reference', '-f', './all-references.yaml'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 2
        yaml_load.assert_called_once_with('./all-references.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_003(self, snippy, yaml_load, mocker):
        """Import all references.

        Import all references from yaml file without specifying the reference
        category. File name and format are extracted from command line
        option -f|--file.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-f', './all-references.yaml'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 2
        assert not Database.get_snippets().size()
        yaml_load.assert_called_once_with('./all-references.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_004(self, snippy, json_load, mocker):
        """Import all references.

        Import all references from json file. File name and format are extracted
        from command line option -f|--file.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--reference', '-f', './all-references.json'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 2
        json_load.assert_called_once_with('./all-references.json', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_005(self, snippy, mocker):
        """Import all references.

        Import all references from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.txt' in this
        case.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--reference', '-f', './all-references.txt'])
            assert cause == Cause.ALL_OK
            assert Database.get_references().size() == 2
            mock_file.assert_called_once_with('./all-references.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_006(self, snippy, mocker):
        """Import all references.

        Import all references from txt file without specifying the reference
        category. File name and format are extracted from command line
        option -f|--file. File extension is '*.txt' in this case.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-references.txt'])
            assert cause == Cause.ALL_OK
            assert Database.get_references().size() == 2
            mock_file.assert_called_once_with('./all-references.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_007(self, snippy, mocker):
        """Import all references.

        Import all references from txt file without specifying the reference
        category. File name and format are extracted from command line option
        -f|--file. File extension is '*.text' in this case.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-references.text'])
            assert cause == Cause.ALL_OK
            assert Database.get_references().size() == 2
            mock_file.assert_called_once_with('./all-references.text', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_008(self, snippy):
        """Import all references.

        Try to import empty reference template. The operation will fail because
        content templates without any modifications cannot be imported.
        """

        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Reference.TEMPLATE))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--reference', '-f', './reference-template.txt'])
            assert cause == 'NOK: content was not stored because mandatory content field links is empty'
            assert not Database.get_collection().size()
            mock_file.assert_called_once_with('./reference-template.txt', 'r')

    def test_cli_import_reference_009(self, snippy):
        """Import all references.

        Try to import reference from file which file format is not supported.
        This should result error text for end user and no files should be read.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--reference', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_collection().size()
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc', 'isfile_true')
    def test_cli_import_reference_010(self, snippy, yaml_load, mocker):
        """Import reference based on message digest.

        Import defined reference based on message digest. File name is defined
        from command line as yaml file which contain one reference. One line in
        the reference data was updated. The updated content is timestamped with
        regexp content time.
        """

        content_read = Content.updated_gitlog()
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--reference', '-d', '5c2071094dbfaa33', '-f', 'one-reference.yaml'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        yaml_load.assert_called_once_with('one-reference.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc', 'isfile_true')
    def test_cli_import_reference_011(self, snippy, yaml_load, mocker):
        """Import reference based on message digest.

        Import defined reference based on message digest without specifying
        the content category explicitly. One line in the reference data was
        updated. The updated content is timestamped with regexp content time.
        """

        content_read = Content.updated_gitlog()
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-d', '5c2071094dbfaa33', '-f', 'one-reference.yaml'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        assert not Database.get_snippets().size()
        yaml_load.assert_called_once_with('one-reference.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-gitlog', 'update-regexp-utc', 'isfile_true')
    def test_cli_import_reference_012(self, snippy, mocker):
        """Import reference based on message digest.

        Import defined reference based on message digest. In this case the
        content category is accidentally specified as 'snippet'. This
        should still import the content in reference category.
        """

        content_read = Content.updated_gitlog()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--snippet', '-d', '5c2071094dbfaa33', '-f', 'one-reference.text'])
            assert cause == Cause.ALL_OK
            assert Database.get_references().size() == 1
            assert not Database.get_snippets().size()
            mock_file.assert_called_once_with('one-reference.text', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-pytest', 'update-regexp-utc')
    def test_cli_import_reference_013(self, snippy, mocker):
        """Import reference based on message digest.

        Try to import defined reference with message digest that cannot be
        found. In this case there is one reference stored.
        """

        content_read = Content.updated_gitlog()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--reference', '-d', '123456789abcdef0', '-f', 'one-reference.text'])
            assert cause == 'NOK: cannot find: reference :identified with digest: 123456789abcdef0'
            assert Database.get_references().size() == 1
            assert not Database.get_snippets().size()
            mock_file.assert_not_called()
            Content.verified(mocker, snippy, {Reference.PYTEST_DIGEST: Reference.DEFAULTS[Reference.PYTEST]})

    def test_cli_import_reference_014(self, snippy, yaml_load, mocker):
        """Import references defaults.

        Import reference defaults. All references should be imported from
        predefined file location under tool data folder from yaml format.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.PYTEST_DIGEST: Content.compared(Reference.DEFAULTS[Reference.PYTEST])
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--reference', '--defaults'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 2
        defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
        yaml_load.assert_called_once_with(defaults_references, 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references', 'import-gitlog-utc', 'import-regexp-utc')
    def test_cli_import_reference_015(self, snippy, yaml_load, mocker):
        """Import references defaults.

        Try to import reference defaults again. The second import should fail
        with an error because the content already exist. The error text must
        be the same for all content categories. Because of random order
        dictionary in the code, the reported digest can vary when there are
        multiple failures to import each content.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Content.compared(Reference.DEFAULTS[Reference.GITLOG]),
            Reference.REGEXP_DIGEST: Content.compared(Reference.DEFAULTS[Reference.REGEXP])
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--reference', '--defaults'])
        assert cause == 'NOK: content data already exist with digest 5c2071094dbfaa33' or \
               cause == 'NOK: content data already exist with digest cb9225a81eab8ced'
        assert Database.get_references().size() == 2
        defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
        yaml_load.assert_called_once_with(defaults_references, 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_016(self, snippy):
        """Import references from text template.

        Try to import reference template without any changes. This should result
        error text for end user and no files should be read. The error text must
        be the same for all content types.
        """

        template = Const.NEWLINE.join(Reference.TEMPLATE)
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--reference', '--template'])
            assert cause == 'NOK: content was not stored because mandatory content field links is empty'
            assert not Database.get_collection().size()
            mock_file.assert_called_once_with('./reference-template.txt', 'r')

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
