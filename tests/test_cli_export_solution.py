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

"""test_cli_export_solution: Test workflows for exporting solutions."""

import json

import mock
import pkg_resources
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliExportSolution(object):  # pylint: disable=too-many-public-methods
    """Test workflows for exporting solutions."""

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_001(self, snippy, yaml_dump):
        """Export all solutions.

        Export all solutions into file. File name or format are not defined
        in command line which must result tool default file and format.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.NGINX]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution'])
        assert cause == Cause.ALL_OK
        assert Database.get_solutions().size() == 2
        yaml_dump.assert_called_once_with('./solutions.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_002(self, snippy, yaml_dump):
        """Export all solutions.

        Export all solutions into defined yaml file. File name and format are
        defined in command line.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.NGINX]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '-f', './all-solutions.yaml']) ## workflow
        assert cause == Cause.ALL_OK
        yaml_dump.assert_called_once_with('./all-solutions.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_003(self, snippy, json_dump):
        """Export all solutions.

        Export all solutions into defined json file. File name and format are
        defined in command line.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.NGINX]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '-f', './all-solutions.json']) ## workflow
        assert cause == Cause.ALL_OK
        json_dump.assert_called_once_with('./all-solutions.json', 'w')
        json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_004(self, snippy):
        """Export all solutions.

        Export all solutions into defined text file with file extension 'txt'.
        File name and format are defined in command line.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Solution.get_template(Solution.DEFAULTS[Solution.NGINX])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_005(self, snippy):
        """Export all solutions.

        Export all solutions into defined text file with file extension
        'text'. File name and format are defined in command line.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Solution.get_template(Solution.DEFAULTS[Solution.NGINX])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_006(self, snippy):
        """Export all solutions.

        Try to export all solutions into file format that is not supported.
        This should result error text for end user and no files should be
        created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @pytest.mark.usefixtures('default-solutions', 'export-time', 'export-time')
    def test_cli_export_solution_007(self, snippy):
        """Export all solutions.

        Try to export all content by defining the content category to --all.
        This is not supported with export operation and error cause is
        returned.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--all'])
            assert cause == 'NOK: content category \'all\' is supported only with search operation'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_008(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata but not by command line -f|--file option.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_009(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata but not by command line -f|--file option. In
        this case the content category is not specified explicitly from
        command line.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'a96accc25dd23ac0'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'import-kafka', 'update-kafka-utc', 'export-time', 'isfile_true')
    def test_cli_export_solution_010(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. Content file name is
        not defined in metadata, solution data or in command line -f|--file
        option. This should result the file name and format defined by tool
        internal defaults.
        """

        content_read = Content.updated_kafka1()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', 'eeef5ca3ec9cd364', '-f', 'kafka.text'])
            assert cause == Cause.ALL_OK
            assert Database.get_solutions().size() == 3
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', '7a5bf1bc09939f42'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(content_read['7a5bf1bc09939f42'])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_011(self, snippy, yaml_dump):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option.
        In this case the created file format is yaml.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.yaml'])
        assert cause == Cause.ALL_OK
        yaml_dump.assert_called_once_with('./defined-solution.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_012(self, snippy, yaml_dump):
        """Export defined solution with digest.

        Export defined solution based on message digest to yaml file without
        specifying the content category explicitly.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.yaml'])
        assert cause == Cause.ALL_OK
        yaml_dump.assert_called_once_with('./defined-solution.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_013(self, snippy, json_dump):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the created file format is json.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.json'])
        assert cause == Cause.ALL_OK
        json_dump.assert_called_once_with('./defined-solution.json', 'w')
        json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_014(self, snippy, json_dump):
        """Export defined solution with digest.

        Export defined solution based on message digest to json file without
        specifying the content category explicitly.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.json'])
        assert cause == Cause.ALL_OK
        json_dump.assert_called_once_with('./defined-solution.json', 'w')
        json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_015(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the text format file extension is 'txt'.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_016(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest to text file without
        specifying the content category explicitly. In this case the file
        extension is *.txt.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_017(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the text format file extension is 'text'.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_018(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest to text file without
        specifying the content category explicitly. In this case the file
        extension is *.text.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_019(self, snippy):
        """Export defined solution with digest.

        Try to export defined solution based on message digest into file
        format that is not supported. This should result error string for
        end user and no files should be created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @pytest.mark.usefixtures('default-solutions', 'import-kafka', 'update-kafka-utc', 'export-time', 'isfile_true')
    def test_cli_export_solution_020(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is not
        defined in solution metadata or by command line -f|--file option.
        In this case there is no space after colon in the file name in the
        content header. In this case there is no space after colon.
        """

        content_read = Content.updated_kafka2()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', 'eeef5ca3ec9cd364', '-f', 'kafka.text'])
            assert cause == Cause.ALL_OK
            assert Database.get_solutions().size() == 3
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', '2c4298ff3c582fe5'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(content_read['2c4298ff3c582fe5'])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'import-kafka-utc', 'export-time', 'isfile_true')
    def test_cli_export_solution_021(self, snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is not
        defined in solution metadata or by command line -f|--file option.
        In this case there are extra spaces around file name. The kafka
        solution must be imported from text file in order to avoid filling
        the meta information. When the data is imported from yaml file, the
        content data is not parsed for filename like with the text template.
        """

        content_read = Content.updated_kafka3()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './kafka.text'])
            assert cause == Cause.ALL_OK
            assert Database.get_solutions().size() == 3
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', '745c9e70eacc304b'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('kubernetes-docker-log-driver-kafka.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(content_read['745c9e70eacc304b'])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_export_solution_022(self, snippy):
        """Export defined solution with digest.

        Try to export defined solution based on message digest that cannot be
        found. This should result error text for end user and no files should
        be created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '-d', '123456789abcdef0', '-f' './defined-solution.text'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_023(self, snippy):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata but not by command line -f|--file option.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '--sall', 'beats'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_024(self, snippy, yaml_dump):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and yaml format defined by the command line
        option.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '--sall', 'beats', '-f', './defined-solution.yaml'])
        assert cause == Cause.ALL_OK
        yaml_dump.assert_called_once_with('./defined-solution.yaml', 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_025(self, snippy, json_dump):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and json format defined by the command line
        option.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '--sall', 'beats', '-f', './defined-solution.json'])
        assert cause == Cause.ALL_OK
        json_dump.assert_called_once_with('./defined-solution.json', 'w')
        json.dump.assert_called_with(content_dict, mock.ANY)

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_026(self, snippy):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the text format file extension is 'txt'.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '--sall', 'beats', '-f' './defined-solution.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_027(self, snippy):
        """Export solution with search keyword.

        Export defined solution based on search keyword. In this case the
        search keyword matchies to two solutions that must be exported to
        file defined in command line.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '--sall', 'howto', '-f' './defined-solutions.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solutions.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Solution.get_template(Solution.DEFAULTS[Solution.NGINX])),
                                                mock.call(Const.NEWLINE)])

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_028(self, snippy):
        """Export solution with search keyword.

        Try to export snippet based on search keyword that cannot befound.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '--sall', 'notfound', '-f', './defined-solution.yaml'])
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('template-utc')
    def test_cli_export_solution_029(self, snippy):
        """Export solution template.

        Export solution template. This should result file name and format
        based on tool internal settings.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solution-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.TEMPLATE))

    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_030(self, snippy, yaml_dump):
        """Export solution defaults.

        Export solution defaults. All solutions should be exported into
        predefined file location under tool data folder in yaml format.
        """

        content_dict = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.NGINX]
            ]
        }
        cause = snippy.run(['snippy', 'export', '--solution', '--defaults'])
        assert cause == Cause.ALL_OK
        defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
        yaml_dump.assert_called_once_with(defaults_solutions, 'w')
        yaml.safe_dump.assert_called_with(content_dict, mock.ANY, default_flow_style=mock.ANY)

    @pytest.mark.usefixtures('snippy')
    def test_cli_export_solution_031(self, snippy):
        """Export solution defaults.

        Try to export solution defaults when there are no stored solutions.
        No files should be created and OK should printed for end user. The
        reason is that processing list of zero items is considered as an OK
        case.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--solution', '--defaults'])
            assert cause == Cause.ALL_OK
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('default-solutions', 'update-kafka-utc', 'export-time', 'isfile_true')
    def test_cli_export_solution_032(self, snippy):
        """Export solution without date field.

        Export solution that has been updated with empty date field in the
        content data header. The export operation must fill the date in
        content data header from solution metadata. An import operation where
        content is identified by message digest, is considered as update
        operation. In case of update operation, the content metadata
        timestamp is set to match the update time. The actual date in the
        solution content data header is not changed from empty string because
        it is considered that end user may want to keep it as is. Only in
        export, the date is updated based on metadata on behalf of user.
        """

        original = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        import_data = original
        import_data = import_data.replace('## DATE  : 2017-10-20T11:11:19.000001+0000', '## DATE  : ')
        mocked_open = mock.mock_open(read_data=import_data)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', 'mocked_file.txt', '-d', 'a96accc25dd23ac0'])
            assert cause == Cause.ALL_OK
            assert Database.get_solutions().size() == 2
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            original = original.replace('## DATE  : 2017-10-20T11:11:19.000001+0000', '## DATE  :  2017-10-20T06:16:27.000001+0000')
            cause = snippy.run(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(original),
                                                mock.call(Const.NEWLINE)])

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
