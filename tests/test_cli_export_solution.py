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

"""test_cli_export_solution: Test workflows for exporting solutions."""

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


class TestCliExportSolution(object):  # pylint: disable=too-many-public-methods
    """Test workflows for exporting solutions."""

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_001(snippy):
        """Export all solutions.

        Export all solutions into file. File name or format are not defined
        in command line which must result tool default file and format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './solutions.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-solutions', 'export-time')
    def test_cli_export_solution_002(snippy):
        """Export all solutions.

        Export all solutions into defined yaml file. File name and format are
        defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-f', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './all-solutions.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-solutions', 'export-time')
    def test_cli_export_solution_003(snippy):
        """Export all solutions.

        Export all solutions into defined json file. File name and format are
        defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-f', './all-solutions.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, './all-solutions.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_004(snippy):
        """Export all solutions.

        Export all solutions into defined text file with file extension 'txt'.
        File name and format are defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS),
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './all-solutions.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_005(snippy):
        """Export all solutions.

        Export all solutions into defined text file with file extension
        'text'. File name and format are defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS),
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './all-solutions.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_006(snippy):
        """Export all solutions.

        Try to export all solutions into file format that is not supported.
        This should result error text for end user and no files should be
        created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_007(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata but not by command line -f|--file option.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'db712a82662d6932'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'howto-debug-elastic-beats.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_008(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata but not by command line -f|--file option. In
        this case the content category is not specified explicitly from
        command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'db712a82662d6932'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'howto-debug-elastic-beats.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-solutions', 'import-kafka', 'update-kafka-utc', 'export-time')
    def test_cli_export_solution_009(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. Content file name is
        not defined in metadata, solution data or in command line -f|--file
        option. This should result the file name and format defined by tool
        internal defaults.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.KAFKA)
            ]
        }
        content['data'][0]['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   : ') for w in content['data'][0]['data']])  # pylint: disable=line-too-long
        content['data'][0]['filename'] = Const.EMPTY
        content['data'][0]['digest'] = '3cbade9454ac80d20eb1b8300dc7537a3851c078791b6e69af48e289c9d62e09'
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'solution', '-d', 'fffeaf31e98e68a3', '-f', 'kafka.text'])
            assert cause == Cause.ALL_OK

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', '3cbade9454ac80d2'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './solutions.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-solutions', 'export-time')
    def test_cli_export_solution_010(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option.
        In this case the created file format is yaml.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'db712a82662d6932', '-f', './defined-solution.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './defined-solution.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-solutions', 'export-time')
    def test_cli_export_solution_011(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest to yaml file without
        specifying the content category explicitly.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'db712a82662d6932', '-f', './defined-solution.yml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './defined-solution.yml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-solutions', 'export-time')
    def test_cli_export_solution_012(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the created file format is json.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'db712a82662d6932', '-f', './defined-solution.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, './defined-solution.json', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-solutions', 'export-time')
    def test_cli_export_solution_013(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest to json file without
        specifying the content category explicitly.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'db712a82662d6932', '-f', './defined-solution.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, './defined-solution.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_014(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the text format file extension is 'txt'.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'db712a82662d6932', '-f', './defined-solution.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './defined-solution.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_015(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest to text file without
        specifying the content category explicitly. In this case the file
        extension is *.txt.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'db712a82662d6932', '-f', './defined-solution.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './defined-solution.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_016(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the text format file extension is 'text'.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'db712a82662d6932', '-f', './defined-solution.text'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './defined-solution.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_017(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest to text file without
        specifying the content category explicitly.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', 'db712a82662d6932', '-f', './defined-solution.text'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './defined-solution.text', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_018(snippy):
        """Export defined solution with digest.

        Try to export defined solution based on message digest into file
        format that is not supported. This should result error string for
        end user and no files should be created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'db712a82662d6932', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-solutions', 'import-kafka', 'update-kafka-utc', 'export-time')
    def test_cli_export_solution_019(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is not
        defined in solution metadata or by command line -f|--file option.
        In this case there is no space after colon in the file name in the
        content header.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.KAFKA)
            ]
        }
        content['data'][0]['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   :') for w in content['data'][0]['data']])  # pylint: disable=line-too-long
        content['data'][0]['filename'] = Const.EMPTY
        content['data'][0]['digest'] = 'fb657e3b49deb5b8e55bb2aa3e81aef4fe54a161a26be728791fb6d4a423f560'
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--scat', 'solution', '-d', 'fffeaf31e98e68a3', '-f', 'kafka.text'])
            assert cause == Cause.ALL_OK

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'fb657e3b49deb5b8'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './solutions.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('isfile_true', 'default-solutions', 'import-kafka-utc', 'export-time')
    def test_cli_export_solution_020(snippy):
        """Export defined solution with digest.

        Export defined solution based on message digest. File name is not
        defined in command line -f|--file option. In this case there are
        extra spaces around file name which does not prevent parsing the
        filename.

        Because the filename is available, the output default must follow
        filename field file format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.KAFKA)
            ]
        }
        content['data'][0]['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   :  kubernetes-docker-log-driver-kafka.txt ') for w in content['data'][0]['data']])  # pylint: disable=line-too-long
        content['data'][0]['filename'] = Const.EMPTY
        content['data'][0]['digest'] = 'e22e8ee4cbbe681ec3f9cba409ae40b8704a52436e102b42d08d57b4ed1d395d'
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './kafka.text'])
            assert cause == Cause.ALL_OK

        content['data'][0]['filename'] = 'kubernetes-docker-log-driver-kafka.txt'
        content['data'][0]['uuid'] = Content.UUID2
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', 'e22e8ee4cbbe681e'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'kubernetes-docker-log-driver-kafka.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_export_solution_021(snippy):
        """Export defined solution with digest.

        Try to export defined solution based on message digest that cannot be
        found. This should result error text for end user and no files should
        be created.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-d', '123456789abcdef0', '-f', './defined-solution.text'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-solutions', 'export-time')
    def test_cli_export_solution_022(snippy):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata but not by command line -f|--file option. Content
        filename fields is used because the search result is a single content.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'beats'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, 'howto-debug-elastic-beats.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-solutions', 'export-time')
    def test_cli_export_solution_023(snippy):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and yaml format defined by the command line
        option because the search result is a single content.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'beats', '-f', './defined-solution.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_yaml(yaml, mock_file, './defined-solution.yaml', content)

    @staticmethod
    @pytest.mark.usefixtures('json', 'default-solutions', 'export-time')
    def test_cli_export_solution_024(snippy):
        """Export solution with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and json format defined by the command line
        option.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'beats', '-f', './defined-solution.json'])
            assert cause == Cause.ALL_OK
            Content.assert_json(json, mock_file, './defined-solution.json', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_025(snippy):
        """Export solutions with search keyword.

        Export defined solution based on search keyword. File name is defined
        in solution metadata and in command line -f|--file option. This should
        result the file name and format defined by the command line option. In
        this case the text format file extension is 'txt'.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'beats', '-f', './defined-solution.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './defined-solution.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_026(snippy):
        """Export solutions with search keyword.

        Export solutions based on search keyword. In this case the search
        keyword matchies to two solutions that must be exported to file
        defined in command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Content.deepcopy(Solution.BEATS),
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][1]['uuid'] = Content.UUID2
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'howto', '-f', './defined-solutions.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_text(mock_file, './defined-solutions.txt', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_027(snippy):
        """Export solution with search keyword.

        Try to export snippet based on search keyword that cannot befound.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'notfound', '-f', './defined-solution.yaml'])
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('template-utc')
    def test_cli_export_solution_028(snippy):
        """Export solution template.

        Export solution template by explicitly defining content category.
        This must result file name and format based on the tool internal
        default settings.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--template'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solution-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.TEMPLATE_MKDN))

    @staticmethod
    @pytest.mark.usefixtures('yaml', 'default-solutions', 'export-time')
    def test_cli_export_solution_029(snippy):
        """Export solution defaults.

        Export solution defaults. All solutions should be exported into
        predefined file location under tool data folder in yaml format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--defaults'])
            assert cause == Cause.ALL_OK
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
            Content.assert_yaml(yaml, mock_file, defaults_solutions, content)

    @staticmethod
    @pytest.mark.usefixtures('snippy')
    def test_cli_export_solution_030(snippy):
        """Export solution defaults.

        Try to export solution defaults when there are no stored solutions.
        Files should not be created and proper NOK cause should be printed
        for end user.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--defaults'])
            assert cause == 'NOK: no content found to be exported'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-remove', 'import-gitlog', 'export-time')
    def test_cli_export_solution_031(snippy):
        """Export all solutions.

        Export all content by defining the content category to ``all``. This
        must export solutions, snippets and references.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Solution.BEATS,
                Solution.NGINX,
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'all'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './content.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-remove', 'import-gitlog', 'export-time')
    def test_cli_export_solution_032(snippy):
        """Export all solutions.

        Export all content by defining the content category to --scat option.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Snippet.REMOVE,
                Solution.BEATS,
                Solution.NGINX,
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'snippet,reference,solution'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './content.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-remove', 'import-gitlog', 'export-time')
    def test_cli_export_solution_033(snippy):
        """Export all solutions.

        Export content only from solution and reference categories.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX,
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution,reference'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './content.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-remove', 'import-gitlog', 'export-time')
    def test_cli_export_solution_034(snippy):
        """Export all references.

        Export content only from reference category when the operation
        category is set to solution. In this case the search category must
        override the content category and only references are exported.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Reference.GITLOG
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--scat', 'reference'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './references.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'import-remove', 'import-gitlog')
    def test_cli_export_solution_035(snippy):
        """Export all solutions.

        Try to export content only from solution and reference categories. The
        solution category name is not correctly spelled which must faile the
        operation.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solutions,reference'])
            assert cause == "NOK: content categories ('reference', 'solutions') are not a subset of ('snippet', 'solution', 'reference')"
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_036(snippy):
        """Export solutions with search keyword.

        Export solutions based on search keyword. In this case the search
        keyword matchies to two solutions that must be exported to default
        file since the -f|-file option is not used.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--sall', 'howto'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './solutions.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'export-time')
    def test_cli_export_solution_037(snippy):
        """Export all solutions.

        Export all snippets in Markdown format.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '-f', './all-solutions.md'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, './all-solutions.md', content)

    @staticmethod
    @pytest.mark.usefixtures('import-kafka-mkdn', 'export-time')
    def test_cli_export_solution_038(snippy):
        """Export defined solution with digest.

        Export Markdown native solution. The solution data must not be
        surrounded with additional Markdown code blocks that are added for
        text content. The exported file name must be based on content
        metadata because the file name is not defined from command line.
        """

        content = {
            'meta': Content.get_cli_meta(),
            'data': [
                Solution.KAFKA_MKDN
            ]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '-d', '18473ec207798670'])
            assert cause == Cause.ALL_OK
            Content.assert_mkdn(mock_file, 'kubernetes-docker-log-driver-kafka.mkdn', content)

    @staticmethod
    @pytest.mark.usefixtures('template-utc')
    def test_cli_export_solution_039(snippy):
        """Export solution template.

        Export solution template by explicitly defining content category
        and the template text format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--template', '--format', 'text'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solution-template.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.TEMPLATE_TEXT))

    @staticmethod
    @pytest.mark.usefixtures('template-utc')
    def test_cli_export_solution_040(snippy):
        """Export solution template.

        Export solution template by explicitly defining content category
        and the template text format.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--scat', 'solution', '--template', '--format', 'mkdn'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solution-template.mkdn', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.TEMPLATE_MKDN))

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
