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

"""test_cli_export_reference: Test workflows for exporting references."""

import json

import mock
import pkg_resources
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.reference import Reference
from tests.lib.snippet import Snippet
from tests.lib.solution import Solution


class TestCliExportReference(object):  # pylint: disable=too-many-public-methods
    """Test workflows for exporting references."""

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_001(snippy):
        """Export all references.

        Export all references without defining target filename from command
        line. In this case the default filename and format is used.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-references', 'export-time')
    def test_cli_export_reference_002(snippy):
        """Export all references.

        Export all references into yaml formatted file as  defined in command
        line option. In this case the reference category is explicitly defined.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', './defined-references.yaml', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './defined-references.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_export_reference_003(snippy):
        """Export all references.

        Try to export all references into file format that is not supported.
        This should result error text for end user and no files should be
        created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', 'foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_004(snippy):
        """Export all references.

        Export defined reference based on message digest. File name is not
        defined in command line -f|--file option. This should result usage
        of default file name and format even when the content category is
        not explicitly defined from command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'cb9225a81eab8ced'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-references', 'export-time')
    def test_cli_export_reference_005(snippy):
        """Export all references.

        Export defined reference based on message digest. File name is defined
        in command line as yaml file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'cb9225a81eab8ced', '-f', 'defined-reference.yml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, 'defined-reference.yml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-references', 'export-time')
    def test_cli_export_reference_006(snippy):
        """Export all references.

        Export defined reference based on message digest. File name is defined
        in command line as json file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'cb9225a81eab8ced', '-f', 'defined-reference.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, 'defined-reference.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_007(snippy):
        """Export defined reference with digest.

        Export defined reference based on message digest. File name is defined
        in command line. This should result file and format defined by command
        line option ``-f|--file``.

        Because text template does not have UUID, the UUID mock allocates a new
        UUID for the exported comparison. Because of this the imported resource
        UUID cannot be compared to exported text.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'cb9225a81eab8ced', '-f', 'defined-reference.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-reference.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_008(snippy):
        """Export defined reference with digest.

        Try to export defined reference based on message digest that cannot be
        found.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '123456789abcdef0', '-f', 'defined-reference.txt'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_009(snippy):
        """Export all references.

        Export defined reference based on uuid.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-u', '32cd5827-b6ef-4067-b5ac-3ceac07dde9f'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_010(snippy):
        """Export defined reference with uuid.

        Try to export defined reference based on uudi that cannot be found.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--uuid', '123456789abcdef0', '-f', 'defined-reference.txt'])
            assert cause == 'NOK: cannot find content with content uuid: 123456789abcdef0'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_011(snippy):
        """Export defined reference with digest.

        Export defined reference based on search keyword. File name is not
        defined in command line -f|--file option. This should result usage
        of default file name and format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'regexp', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_012(snippy):
        """Export defined reference with digest.

        Export defined reference based on search keyword. File name is defined
        in command line as text file with *.txt file extension.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'regexp', '-f', 'defined-reference.txt', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-reference.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_013(snippy):
        """Export defined reference with search keyword.

        Export defined reference based on search keyword. File name is defined
        in command line as text file with *.text file extension.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'regexp', '-f', 'defined-reference.text', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-reference.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_014(snippy):
        """Export references with search keyword.

        Export references based on search keyword. In this case the search
        keyword matchies to two references that must be exported to file
        defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Content.deepcopy(Reference.REGEXP)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'howto', '-f', 'defined-reference.text', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-reference.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_015(snippy):
        """Export defined reference with search keyword.

        Try to export reference based on search keyword that cannot befound.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'notfound', '-f', 'defined-reference.yaml', '--scat', 'reference'])
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-references', 'export-time')
    def test_cli_export_reference_016(snippy):
        """Export defined reference with content data.

        Export defined reference based on content data. File name is defined in
        command line as yaml file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-c', 'https://chris.beams.io/posts/git-commit/', '-f', 'defined-reference.yaml', '--scat', 'reference'])  # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, 'defined-reference.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_017(snippy):
        """Export reference template.

        Export reference template by explicitly defining content category.
        This must result file name and format based on the tool internal
        default settings.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./reference-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Reference.TEMPLATE_MKDN))

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-references', 'export-time')
    def test_cli_export_reference_018(snippy):
        """Export reference defaults.

        Export reference defaults. All references should be exported into
        predefined file location under tool data folder in yaml format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--defaults', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
            Content.assert_yaml(yaml, mock_file, defaults_references, content)

    @staticmethod
    @pytest.mark.usefixtures('export-time')
    def test_cli_export_reference_019(snippy):
        """Export reference defaults.

        Try to export reference defaults when there are no stored references.
        Files should not be created and proper NOK cause should be printed for
        end user.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--defaults', '--scat', 'reference'])
            assert cause == 'NOK: no content found to be exported'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'import-gitlog', 'import-remove', 'import-beats', 'export-time-all-categories')
    def test_cli_export_reference_020(snippy):
        """Export defaults with ``scat`` option.

        Export snippet, solution and reference defaults with category
        set to ``all`` and so that the defauls will be updated. This must
        store the content from each category to own file that stores the
        default content.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Solution.BEATS,
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--defaults', '--scat', 'all'])
            assert cause == Cause.ALL_OK
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/defaults/snippets.yaml')
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
            defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
            Content.assert_yaml(yaml, mock_file, [defaults_snippets, defaults_solutions, defaults_references], content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_021(snippy):
        """Export references with search keyword.

        Export references based on search keyword. In this case the search
        keyword matchies to two references that must be exported to default
        file since the -f|-file option is not used.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'howto', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'import-remove', 'import-beats', 'export-time')
    def test_cli_export_reference_022(snippy):
        """Export content with search keyword.

        Export content from two categories with search keyword. In this case
        -f|--file option is not used and the content must be stored into a
        single default file and format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Snippet.REMOVE
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference,snippet', '--sall', 'volumes,git'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './content.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'import-remove', 'import-beats', 'export-time')
    def test_cli_export_reference_023(snippy):
        """Export content with search keyword.

        Export content from one category when search category is set to
        search from two categories. In this case -f|--file option is not
        used and the content must be stored into a single file defined
        by the searched category.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference,snippet', '--sall', 'git'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'import-gitlog', 'import-remove', 'import-beats', 'export-time')
    def test_cli_export_reference_024(snippy):
        """Export content with search keyword.

        Export content from two category with search keyword. In this case
        -f|--file option is used and the content must be stored into a file
        defined by user.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Snippet.REMOVE
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference,snippet', '--sall', 'volumes,git', '-f', 'defined-content.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, 'defined-content.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'import-gitlog', 'import-remove', 'import-beats', 'export-time')
    def test_cli_export_reference_025(snippy):
        """Exporting defaults while using search category.

        Export default content by selecting single category with the --scat
        option.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference', '--default'])
            assert cause == Cause.ALL_OK
            defaults_references = pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml')
            Content.assert_yaml(yaml, mock_file, defaults_references, content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_export_reference_026(snippy):
        """Export all references.

        Try to export all references into file format that is not supported.
        In this case the file format contains just one additional letter to
        supported yaml format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', 'foo.yamll'])
            assert cause == 'NOK: cannot identify file format for file: foo.yamll'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_export_reference_027(snippy):
        """Export all references.

        Try to export all references into file format that is not supported.
        In this case the file format contains just one additional letter to
        supported text format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', 'foo.itext'])
            assert cause == 'NOK: cannot identify file format for file: foo.itext'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_export_reference_028(snippy):
        """Export all references.

        Try to export all references into file format that is not supported.
        In this case the file format contains just one additional letter to
        supported json format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', 'foo.jsontext'])
            assert cause == 'NOK: cannot identify file format for file: foo.jsontext'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_029(snippy):
        """Export all references.

        Export all references in Markdown format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference', '--file', 'references.mkdn'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, 'references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_030(snippy):
        """Export reference template.

        Export reference template by explicitly defining content category
        and the template text format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference', '--template', '--format', 'text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./reference-template.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Reference.TEMPLATE_TEXT))

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'export-time')
    def test_cli_export_reference_031(snippy):
        """Export reference template.

        Export reference template by explicitly defining content category
        and the template Markdown format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'reference', '--template', '--format', 'mkdn'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./reference-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Reference.TEMPLATE_MKDN))

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
