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

"""test_cli_export_snippet: Test workflows for exporting snippets."""

import json

import mock
import pkg_resources
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliExportSnippet(object):  # pylint: disable=too-many-public-methods
    """Test workflows for exporting snippets."""

    @pytest.mark.usefixtures('default-snippets', 'export-time', 'export-time')
    def test_cli_export_snippet_001(self, snippy, yaml_dump):
        """Export all snippets.

        Export all snippets without defining target file name from command
        line.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE],
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        yaml_dump.assert_called_once_with('./snippets.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time', 'export-time')
    def test_cli_export_snippet_002(self, snippy, yaml_dump):
        """Export all snippets.

        Export all snippets without defining target file name from command
        line. In this case the content category is defined explicitly.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE],
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--snippet'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        yaml_dump.assert_called_once_with('./snippets.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time', 'export-time')
    def test_cli_export_snippet_003(self, snippy, yaml_dump):
        """Export all snippets.

        Export all snippets into yaml file defined from command line.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE],
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export', '-f', './defined-snippets.yaml'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        yaml_dump.assert_called_once_with('./defined-snippets.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time', 'export-time')
    def test_cli_export_snippet_004(self, snippy, yaml_dump):
        """Export all snippets.

        Export all snippets into yaml file defined from command line by
        explicitly defining the content category.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE],
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export', '-f', './defined-snippets.yaml', '--snippet'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        yaml_dump.assert_called_once_with('./defined-snippets.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_export_snippet_005(self, snippy):
        """Export all snippets.

        Try to export all snippets into file format that is not supported.
        This should result error text for end user and no files should be
        created.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-f', 'foo.bar'])
            assert cause == 'NOK: cannot identify file format for file foo.bar'
            assert Database.get_snippets().size() == 2
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @pytest.mark.usefixtures('default-snippets', 'yaml_dump', 'export-time')
    def test_cli_export_snippet_006(self, snippy):
        """Export all snippets.

        Export defined snippet based on message digest. File name is not
        defined in command line -f|--file option. This should result usage
        of default file name and format
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'yaml_dump', 'export-time')
    def test_cli_export_snippet_007(self, snippy):
        """Export all snippets.

        Export defined snippet based on message digest. File name is defined
        in command line as yaml file.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.yaml'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.yaml', 'w')
            yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'json_dump', 'export-time')
    def test_cli_export_snippet_008(self, snippy):
        """Export all snippets.

        Export defined snippet based on message digest. File name is defined
        in command line as json file.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.json'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.json', 'w')
            json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_009(self, snippy):
        """Export defined snippet with digest.

        Export defined snippet based on message digest. File namei s defined
        in command line. This should result file and format defined by command
        line option -f|--file.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_010(self, snippy):
        """Export defined snippet with digest.

        Try to export defined snippet based on message digest that cannot be
        found.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '123456789abcdef0', '-f', 'defined-snippet.txt'])
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_011(self, snippy):
        """Export defined snippet with digest.

        Export defined snippet based on search keyword. File name is not
        defined in command line -f|--file option. This should result usage
        of default file name and format snippet.text.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_012(self, snippy, yaml_dump):
        """Export defined snippet with digest.

        Export defined snippet based on search keyword. File name is defined
        in command line as yaml file.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.yaml'])
        assert cause == Cause.ALL_OK
        yaml_dump.assert_called_once_with('defined-snippet.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_013(self, snippy, json_dump):
        """Export defined snippet with digest.

        Export defined snippet based on search keyword. File name is defined
        in command line as json file.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.json'])
        assert cause == Cause.ALL_OK
        json_dump.assert_called_once_with('defined-snippet.json', 'w')
        json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_014(self, snippy):
        """Export defined snippet with digest.

        Export defined snippet based on search keyword. File name is defined
        in command line as text file with *.txt file extension.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_015(self, snippy):
        """Export defined snippet with search keyword.

        Export defined snippet based on search keyword. File name is defined
        in command line as text file with *.text file extension.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_016(self, snippy):
        """Export defined snippet with search keyword.

        Export defined snippet based on search keyword. In this case the
        search keyword matchies to two snippets that must be exported to
        file defined in command line.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'docker', '-f', 'defined-snippet.text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_017(self, snippy):
        """Export defined snippet with search keyword.

        Try to export snippet based on search keyword that cannot befound.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--sall', 'notfound', '-f', 'defined-snippet.yaml'])
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_018(self, snippy):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is not defined
        in command line -f|--file option. This should result usage of default
        file name and format snippet.text.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--content', 'docker rm --volumes $(docker ps --all --quiet)'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_019(self, snippy, yaml_dump):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is defined in
        command line as yaml file.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE]
            ]
        }
        cause = snippy.run(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.yaml'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        yaml_dump.assert_called_once_with('defined-snippet.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_020(self, snippy, json_dump):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is defined in
        command line as json file.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE]
            ]
        }
        cause = snippy.run(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.json'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        json_dump.assert_called_once_with('defined-snippet.json', 'w')
        json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_021(self, snippy):
        """Export defined snippet with content data.

        Export defined snippet based on content data. File name is defined in
        command line as text file with *.txt file extension.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.txt'])  # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_022(self, snippy):
        """Export snippet template.

        Export snippet template. This should result file name and format based
        on tool internal settings.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Snippet.TEMPLATE))

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_023(self, snippy):
        """Export snippet template.

        Export snippet template by explicitly defining content category. This
        should result file name and format based on tool internal settings.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--snippet', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Snippet.TEMPLATE))

    @pytest.mark.usefixtures('default-snippets', 'export-time')
    def test_cli_export_snippet_024(self, snippy, yaml_dump):
        """Export snippet defaults.

        Export snippet defaults. All snippets should be exported into
        predefined file location under tool data folder in yaml format.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.DEFAULTS[Snippet.REMOVE],
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--defaults'])
        assert cause == Cause.ALL_OK
        defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
        yaml_dump.assert_called_once_with(defaults_snippets, 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('export-time')
    def test_cli_export_snippet_025(self, snippy):
        """Export snippet defaults.

        Try to export snippet defaults when there are no stored snippets. No
        files should be created and OK should printed for end user. The reason
        is that processing list of zero items is considered as an OK case.
        """

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--defaults'])
            assert cause == Cause.ALL_OK
            mock_file.assert_not_called()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
