# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""test_cli_import_reference: Test workflows for importing references."""

import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.reference import Reference


class TestCliImportReference(object):  # pylint: disable=too-many-public-methods
    """Test workflows for importing references."""

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_001(snippy):
        """Import all reference resources.

        Import all references. File name is not defined in command line. This
        should result tool internal default file name and format being used.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.io.open', file_content) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './references.mkdn', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_reference_002(snippy):
        """Import all reference resources.

        Import all references from yaml file. File name and format are extracted
        from command line ``--file`` option. In this case the content category is
        explicitly defined from command line.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-f', './all-references.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.yaml', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_reference_003(snippy):
        """Import all reference resources.

        Import all references from yaml file without specifying the reference
        category. File name and format are extracted from command line
        ``--file`` option.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-f', './all-references.yml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.yml', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_reference_004(snippy):
        """Import all reference resources.

        Import all references from json file. File name and format are extracted
        from command line ``--file`` option.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-f', './all-references.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.json', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-references-utc')
    def test_cli_import_reference_005(snippy):
        """Import all reference resources.

        Import all references from txt file. File name and format are extracted
        from command line ``--file`` option. File extension is '*.txt' in this
        case.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.io.open', file_content) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-f', './all-references.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.txt', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-references-utc')
    def test_cli_import_reference_006(snippy):
        """Import all reference resources.

        Import all references from txt file without specifying the reference
        category. File name and format are extracted from command line
        ``--file`` option. File extension is '*.txt' in this case.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.io.open', file_content) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-references.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.txt', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-references-utc')
    def test_cli_import_reference_007(snippy):
        """Import all reference resources.

        Import all references from a text file without specifying reference
        category. File name and format are extracted from the command line
        ``--file`` option. File extension is '*.text' in this case.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.io.open', file_content) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-references.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.text', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_008(snippy):
        """Import all reference resources.

        Try to import empty reference template. The operation will fail because
        content templates without help texts and without any modifications cannot
        be imported.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Reference.TEMPLATE))
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-f', './reference-template.text'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            Content.assert_arglist(mock_file, './reference-template.text', mode='r', encoding='utf-8')

    @staticmethod
    def test_cli_import_reference_009(snippy):
        """Import all reference resources.

        Try to import reference from file which file format is not supported.
        This should result error text for end user and no files should be read.
        """

        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: ./foo.bar'
            Content.assert_storage(None)
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-gitlog', 'update-pytest-utc')
    def test_cli_import_reference_010(snippy):
        """Import reference based on message digest.

        Import defined reference based on message digest. File name is defined
        from command line as YAML file which contain one reference. Links in
        the reference was updated. Content updated field must be updated with a
        new timestamp.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['links'] = ('https://updated-link.html',)
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = 'fafd46eca7ca239bcbff8f1ba3e8cf806cadfbc9e267cdf6ccd3e23e356f9f8d'
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-d', '5c2071094dbfaa33', '-f', 'one-reference.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, 'one-reference.yaml', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-gitlog', 'update-pytest-utc')
    def test_cli_import_reference_011(snippy):
        """Import reference based on message digest.

        Import defined reference based on message digest without specifying
        the content category explicitly. One line in the reference data was
        updated. The updated content is timestamped with regexp content time.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['links'] = ('https://updated-link.html',)
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = 'fafd46eca7ca239bcbff8f1ba3e8cf806cadfbc9e267cdf6ccd3e23e356f9f8d'
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-d', '5c2071094dbfaa33', '-f', 'one-reference.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, 'one-reference.yaml', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'import-gitlog', 'update-pytest-utc')
    def test_cli_import_reference_012(snippy):
        """Import reference based on message digest.

        Import defined reference based on message digest. In this case the
        content category is accidentally specified as 'snippet'. This should
        still import the content in reference category.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['links'] = ('https://updated-link.html',)
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = 'fafd46eca7ca239bcbff8f1ba3e8cf806cadfbc9e267cdf6ccd3e23e356f9f8d'
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.io.open', file_content) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'snippet', '-d', '5c2071094dbfaa33', '-f', 'one-reference.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, 'one-reference.text', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('import-pytest', 'update-regexp-utc')
    def test_cli_import_reference_013(snippy):
        """Import reference based on message digest.

        Try to import defined reference with message digest that cannot be
        found. In this case there is one reference stored.
        """

        content = {
            'data': [
                Reference.PYTEST
            ]
        }
        updates = {
            'data': [
                Reference.GITLOG
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, updates)
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-d', '123456789abcdef0', '-f', 'one-reference.text'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            Content.assert_storage(content)
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'import-gitlog', 'update-pytest-utc', 'isfile_true')
    def test_cli_import_reference_014(snippy):
        """Import reference based on uuid.

        Import defined reference based on uuid.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['links'] = ('https://updated-link.html',)
        content['data'][0]['updated'] = Content.PYTEST_TIME
        content['data'][0]['digest'] = 'fafd46eca7ca239bcbff8f1ba3e8cf806cadfbc9e267cdf6ccd3e23e356f9f8d'
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-u', '31cd5827-b6ef-4067-b5ac-3ceac07dde9f', '-f', 'one-reference.yaml'])  # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, 'one-reference.yaml', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('import-pytest', 'update-regexp-utc')
    def test_cli_import_reference_015(snippy):
        """Import reference based on message uuid.

        Try to import defined reference with uuid that cannot be found.
        """

        content = {
            'data': [
                Reference.PYTEST
            ]
        }
        updates = {
            'data': [
                Reference.GITLOG
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, updates)
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-u', '1234567', '-f', 'one-reference.text'])
            assert cause == 'NOK: cannot find content with content uuid: 1234567'
            Content.assert_storage(content)
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('yaml')
    def test_cli_import_reference_016(snippy):
        """Import references defaults.

        Import reference defaults. All references should be imported from
        predefined file location under tool data folder from yaml format.
        """

        content = {
            'data': [
                Reference.PYTEST,
                Reference.GITLOG,
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '--defaults'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
            Content.assert_arglist(mock_file, defaults_references, mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-references', 'import-gitlog-utc', 'import-regexp-utc')
    def test_cli_import_reference_017(snippy):
        """Import references defaults.

        Try to import reference defaults again. The second import must fail
        with error because resoureces already exist. The error text must be
        the same for all content categories.

        Because of random order dictionary in the code, the reported digest
        can vary when there are multiple failures to import each content.

        Because there is unique constraint violation for ``data`` and ``uuid``
        attributes and PostgreSQL and Sqlite throw the error from different
        attributes, both attributes must be checked.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '--defaults'])
            assert cause in ('NOK: content data already exist with digest 5c2071094dbfaa33',
                             'NOK: content uuid already exist with digest 5c2071094dbfaa33',
                             'NOK: content data already exist with digest cb9225a81eab8ced',
                             'NOK: content uuid already exist with digest cb9225a81eab8ced')
            Content.assert_storage(content)
            defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
            Content.assert_arglist(mock_file, defaults_references, mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_018(snippy):
        """Import reference from text template.

        Try to import reference template without any changes. This should result
        error text for end user and no files should be read. The error text must
        be the same for all content types.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Reference.TEMPLATE_TEXT))
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '--template', '--format', 'text'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            assert mock_file.call_args == mock.call('./reference-template.text', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'update-gitlog-utc')
    def test_cli_import_reference_019(snippy):
        """Try to import reference which uuid collides.

        The uuid must be unique and this causes a database integrity error.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            assert mock_file.call_args == mock.call('./references.mkdn', mode='r', encoding='utf-8')

        content_uuid = {
            'data': [
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content_uuid['data'][0]['uuid'] = content['data'][0]['uuid']
        file_content = Content.get_file_content(Content.MKDN, content_uuid)
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference'])
            assert cause == 'NOK: content uuid already exist with digest 5c2071094dbfaa33'
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './references.mkdn', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_020(snippy):
        """Import all reference resources.

        Import all references from Markdown formatted file.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-f', './all-references.mkdn'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './all-references.mkdn', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-gitlog', 'update-regexp-utc')
    def test_cli_import_reference_021(snippy):
        """Try to import reference from YAML file.

        Try to import a reference from YAML file that does not have any content.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        file_content = Content.get_file_content(Content.YAML, {'data': []})
        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '-d', '5c2071094dbfaa33', '-f', 'one-reference.yaml'])
            assert cause == 'NOK: updates for content 5c2071094dbfaa33 could not be used'
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, 'one-reference.yaml', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_022(snippy):
        """Try to import references wihtout UUID.

        Try to import two references without UUID. When the UUID is missing, it
        must be automatically allocated
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = ''
        content['data'][1]['uuid'] = ''
        file_content = Content.get_file_content(Content.MKDN, content)
        content['data'][0]['uuid'] = 'a1cd5827-b6ef-4067-b5ac-3ceac07dde9f'
        content['data'][1]['uuid'] = 'a2cd5827-b6ef-4067-b5ac-3ceac07dde9f'
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            Content.assert_arglist(mock_file, './references.mkdn', mode='r', encoding='utf-8')

    @staticmethod
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_reference_023(snippy):
        """Import reference from Markdown template.

        Try to import reference template without any changes. This should result
        error text for end user and no files should be read. The error text must
        be the same for all content types.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Reference.TEMPLATE_MKDN))
        with mock.patch('snippy.content.migrate.io.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'reference', '--template'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            Content.assert_arglist(mock_file, './reference-template.mkdn', mode='r', encoding='utf-8')

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
