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

"""test_cli_export_snippet: Test workflows for exporting snippets."""

import json

import mock
import pkg_resources
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet import Snippet


class TestCliExportSnippet(object):  # pylint: disable=too-many-public-methods
    """Test workflows for exporting snippets."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_001(snippy):
        """Export all snippets.

        Export all snippets without defining target file name from command
        line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_002(snippy):
        """Export all snippets.

        Export all snippets without defining target file name from command
        line. In this case the content category is defined explicitly.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--snippets'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'export-time')
    def test_cli_export_snippet_003(snippy):
        """Export all snippets.

        Export all snippets into yaml file defined from command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', './defined-snippets.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './defined-snippets.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'export-time')
    def test_cli_export_snippet_004(snippy):
        """Export all snippets.

        Export all snippets into yaml file by explicitly defining the content
        category and file name from command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', './defined-snippets.yml', '--snippet'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './defined-snippets.yml', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_export_snippet_005(snippy):
        """Export all snippets.

        Try to export all snippets into file format that is not supported.
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
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_006(snippy):
        """Export defined snippets.

        Export defined snippet based on message digest. File name is not
        defined in command line -f|--file option. This should result usage
        of default file name and format
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'export-time')
    def test_cli_export_snippet_007(snippy):
        """Export defined snippets.

        Export defined snippet based on message digest. File name is defined
        in command line as yaml file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, 'defined-snippet.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-snippets', 'export-time')
    def test_cli_export_snippet_008(snippy):
        """Export defined snippets.

        Export defined snippet based on message digest. File name is defined
        in command line as json file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, 'defined-snippet.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_009(snippy):
        """Export defined snippets.

        Export defined snippet based on message digest. File name is defined
        in command line. This should result file and format defined by command
        line option -f|--file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-snippet.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_010(snippy):
        """Export defined snippets.

        Try to export defined snippet based on message digest that cannot be
        found.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '123456789abcdef0', '-f', 'defined-snippet.txt'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            Content.assert_text(mock_file, None, None)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_011(snippy):
        """Export defined snippets.

        Export defined snippet based on search keyword. File name is not
        defined in command line -f|--file option. This should result usage
        of default file name and format snippet.text.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'export-time')
    def test_cli_export_snippet_012(snippy):
        """Export defined snippets.

        Export defined snippet based on search keyword. File name is defined
        in command line as yaml file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, 'defined-snippet.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-snippets', 'export-time')
    def test_cli_export_snippet_013(snippy):
        """Export defined snippets.

        Export defined snippet based on search keyword. File name is defined
        in command line as json file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, 'defined-snippet.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_014(snippy):
        """Export defined snippets.

        Export defined snippet based on search keyword. File name is defined
        in command line as text file with *.txt file extension.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-snippet.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_015(snippy):
        """Export defined snippets.

        Export defined snippet based on search keyword. File name is defined
        in command line as text file with *.text file extension.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.text'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-snippet.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_016(snippy):
        """Export snippets with search keyword.

        Export snippets based on search keyword. In this case the search
        keyword matches to two snippets that must be exported to file
        defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'docker', '-f', 'defined-snippet.text'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-snippet.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_017(snippy):
        """Export defined snippet with search keyword.

        Try to export snippet based on search keyword that cannot befound.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'notfound', '-f', 'defined-snippet.yaml'])
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_018(snippy):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is not defined
        in command line -f|--file option. This should result usage of default
        file name and format snippet.text.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--content', 'docker rm --volumes $(docker ps --all --quiet)'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'export-time')
    def test_cli_export_snippet_019(snippy):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is defined in
        command line as yaml file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.yaml'])  # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, 'defined-snippet.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-snippets', 'export-time')
    def test_cli_export_snippet_020(snippy):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is defined in
        command line as json file.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.json'])  # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, 'defined-snippet.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_021(snippy):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is defined in
        command line as text file with *.txt file extension.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.txt'])  # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'defined-snippet.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_022(snippy):
        """Export snippet template.

        Export snippet template. This should result file name and format based
        on tool internal settings.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Snippet.TEMPLATE_MKDN))

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_023(snippy):
        """Export snippet template.

        Export snippet template by explicitly defining content category. This
        should result file name and format based on tool internal settings.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--snippet', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Snippet.TEMPLATE_MKDN))

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-snippets', 'export-time')
    def test_cli_export_snippet_024(snippy):
        """Export snippet defaults.

        Export snippet defaults. All snippets should be exported into
        predefined file location under tool data folder in yaml format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--defaults'])
            assert cause == Cause.ALL_OK
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/defaults/snippets.yaml')
            Content.assert_yaml(yaml, mock_file, defaults_snippets, content)

    @staticmethod
    @pytest.mark.usefixtures('export-time')
    def test_cli_export_snippet_025(snippy):
        """Export snippet defaults.

        Try to export snippet defaults when there are no stored snippets.
        Files should not be created and proper NOK cause should be printed
        for end user.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--defaults'])
            assert cause == 'NOK: no content found to be exported'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_026(snippy):
        """Export snippets with search keyword.

        Export snippets based on search keyword. In this case the search
        keyword matches to two snippets that must be exported to default
        file since the -f|-file option is not used.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'docker'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_027(snippy):
        """Export all snippets.

        Export all snippets in Markdown format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', './snippets.mkdn'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('export-time')
    def test_cli_export_snippet_028(snippy):
        """Export all snippets.

        Export snippet with two lines content description. There must be two
        spaces after the newline in order to force a newline in Mardown format
        for the long description.
        """

        Content.store({
            'data': [
                'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./  #  Compress folder excluding the tar.'],
            'brief': 'Manipulate compressed tar files',
            'description': 'Manipulate compressed tar files and define very long descrption for the content to extend to two lines.',
            'groups': ['linux'],
            'tags': ['howto', 'linux', 'tar', 'untar'],
            'category': Const.SNIPPET,
        })
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', './snippets.md'])
            assert cause == Cause.ALL_OK
            call = mock_file.return_value.__enter__.return_value.write.mock_calls[0][1][0]
            assert 'Manipulate compressed tar files and define very long descrption for the content to  \nextend to two lines.\n\n' in call

    @staticmethod
    @pytest.mark.usefixtures('import-exited', 'export-time')
    def test_cli_export_snippet_029(snippy):
        """Export all snippets.

        Export snippets in Markdown format. This case verified that there is
        two spaces at the end of lists like links, data and metadata. This
        forces newlines in exported Markdown format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.EXITED
            ]
        }
        markdown = (
            '# Remove all exited containers and dangling images @docker',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/  ',
            '[3] https://docs.docker.com/engine/reference/commandline/rmi/',
            '',
            '`$ docker rm $(docker ps --all -q -f status=exited)`  ',
            '`$ docker images -q --filter dangling=true | xargs docker rmi`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-20T07:08:45.000001+00:00  ',
            'digest   : 49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : cleanup,container,docker,docker-ce,image,moby  ',
            'updated  : 2017-10-20T07:08:45.000001+00:00  ',
            'uuid     : 12cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            ''
        )
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', './snippets.mkdn'])
            assert cause == Cause.ALL_OK
            assert mock_file.return_value.__enter__.return_value.write.mock_calls[0][1][0] == '\n'.join(markdown)
            Content.assert_mkdn(mock_file, './snippets.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_030(snippy):
        """Export snippet template.

        Export reference template by explicitly defining content category
        and the template text format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--template', '--format', 'text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Snippet.TEMPLATE_TEXT))

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_031(snippy):
        """Export snippet template.

        Export reference template by explicitly defining content category
        and the template Markdown format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--template', '--format', 'mkdn'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Snippet.TEMPLATE_MKDN))

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
