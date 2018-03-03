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
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfExportSnippet(object):
    """Test workflows for exporting snippets."""

    @pytest.mark.usefixtures('snippy', 'default-snippets', 'export-time', 'export-time')
    def test_cli_export_snippet_001(self, snippy, yaml_dump):
        """Export all snippets."""

        ## Brief: Export all snippets without defining target file name from
        ##        command line.
        content_dict = {
            'meta': Snippet.get_metadata(Content.EXPORT_TIME),
            'content': [
                Snippet.DEFAULTS[Snippet.REMOVE],
                Snippet.DEFAULTS[Snippet.FORCED]
            ]
        }
        cause = snippy.run_cli(['snippy', 'export'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 2
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)
        yaml_dump.assert_called_once_with('./snippets.yaml', 'w')

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_all_snippets(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_safe_dump):
        """Export all snippets."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Snippet.UTC1
        mock_storage_file.return_value = Database.get_storage()
        export_dict = {'meta': Snippet.get_metadata(Snippet.UTC1),
                       'content': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]}

        ## Brief: Export all snippets without defining target file name from command line.
        ##        In this case the content category is defined explicitly.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--snippet'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./snippets.yaml', 'w')
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all snippets into yaml file defined from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-f', './defined-snippets.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./defined-snippets.yaml', 'w')
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all snippets into yaml file defined from command line by explicitly defining
        ##        the content category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-f', './defined-snippets.yaml', '--snippet'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./defined-snippets.yaml', 'w')
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export all snippets into file format that is not supported. This should
        ##        result error text for end user and no files should be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-f', 'foo.bar'])  ## workflow
            assert cause == 'NOK: cannot identify file format for file foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_snippet_digest(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export defined snippet with digest."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = Snippet.UTC1
        export_dict = {'meta': Snippet.get_metadata(Snippet.UTC1),
                       'content': [Snippet.DEFAULTS[Snippet.FORCED]]}

        ## Brief: Export defined snippet based on message digest. File name is not defined in command
        ##        line -f|--file option. This should result usage of default file name and format
        ##        snippet.text.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-d', '53908d68425c61dc'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on message digest. File name is defined in command
        ##        line as yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on message digest. File name is defined in command
        ##        line as json file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.json'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on message digest. File name is defined in command
        ##        line. This should result file and format defined by command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export defined snippet based on message digest that cannot be found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-d', '123456789abcdef0', '-f', 'defined-snippet.txt'])  ## workflow
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_snippet_keyword(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export defined snippet with search keyword."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = Snippet.UTC1
        export_dict = {'meta': Snippet.get_metadata(Snippet.UTC1),
                       'content': [Snippet.DEFAULTS[Snippet.FORCED]]}

        ## Brief: Export defined snippet based on search keyword. File name is not defined in
        ##        command line -f|--file option. This should result usage of default file name
        #         and format snippet.text.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'force'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on search keyword. File name is defined in
        ##        command line as yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on search keyword. File name is defined in
        ##        command line as json file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.json'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on search keyword. File name is defined in
        ##        command line as text file with *.txt file extension.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on search keyword. File name is defined in
        ##        command line as text file with *.text file extension.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'force', '-f', 'defined-snippet.text'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on search keyword. In this case the search keyword
        ##        matchies to two snippets that must be exported to file defined in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'docker', '-f', 'defined-snippet.text'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export snippet based on search keyword that cannot befound.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--sall', 'notfound', '-f', 'defined-snippet.yaml'])  ## workflow
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_snippet_data(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export defined snippet with content data."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = Snippet.UTC1
        export_dict = {'meta': Snippet.get_metadata(Snippet.UTC1),
                       'content': [Snippet.DEFAULTS[Snippet.REMOVE]]}

        ## Brief: Export defined snippet based on content data. File name is not defined in
        ##        command line -f|--file option. This should result usage of default file name
        #         and format snippet.text.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--content', 'docker rm --volumes $(docker ps --all --quiet)'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on content data. File name is defined in
        ##        command line as yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.yaml'])  ## workflow # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on content data. File name is defined in
        ##        command line as json file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.json'])  ## workflow # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on content data. File name is defined in
        ##        command line as text file with *.txt file extension.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '-f', 'defined-snippet.txt'])  ## workflow # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_export_snippet_template(self, mock_storage_file, mock_get_utc_time):
        """Export snippet template."""

        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = Snippet.UTC1
        template = Snippet.TEMPLATE

        ## Brief: Export snippet template. This should result file name and format based on
        ##        tool internal settings.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy(['snippy', 'export', '--template'])  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(template))
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export snippet template by explicitly defining content category. This should
        ##        result file name and format based on tool internal settings.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy(['snippy', 'export', '--snippet', '--template'])  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(template))
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_snippet_defaults(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump):
        """Export snippet defaults."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = Snippet.UTC1
        export_dict = {'meta': Snippet.get_metadata(Snippet.UTC1),
                       'content': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]}

        ## Brief: Export snippet defaults. All snippets should be exported into predefined file
        ##        location under tool data folder in yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'export', '--defaults'])  ## workflow
            assert cause == Cause.ALL_OK
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export snippet defaults when there are no stored snippets. No files
        ##        should be created and OK should printed for end user. The reason is that
        ##        processing list of zero items is considered as an OK case.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'export', '--defaults'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_not_called()
            mock_yaml_dump.assert_not_called()
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
