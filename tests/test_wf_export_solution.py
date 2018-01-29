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

"""test_wf_export_solution.py: Test workflows for exporting solutions."""

import sys
import unittest
import json
import yaml
import mock
import pkg_resources
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfExportSolution(unittest.TestCase):
    """Test workflows for exporting solutions."""

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_all_solutions(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export all solutions."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock_storage_file.return_value = Database.get_storage()
        export_dict = {'metadata': Solution.get_metadata(Solution.UTC1),
                       'content': [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.NGINX]]}

        ## Brief: Export all solutions into file. File name or format are not defined in command
        ##        line which should result tool default file and format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solutions.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all solutions into defined yaml file. File name and format are defined
        ##        in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-f', './all-solutions.yaml']) ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all solutions into defined json file. File name and format are defined
        ##        in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-f', './all-solutions.json']) ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all solutions into defined text file with file extension 'txt'. File name
        ##        and format are defined in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-f', './all-solutions.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Solution.get_template(Solution.DEFAULTS[Solution.NGINX])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all solutions into defined text file with file extension 'text'. File name
        ##        and format are defined in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-f', './all-solutions.text'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Solution.get_template(Solution.DEFAULTS[Solution.NGINX])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export all solutions into file format that is not supported. This should
        ##        result error text for end user and no files should be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-f', './foo.bar'])  ## workflow
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export all content by defining the content category to --all. This is not
        ##        supported with export operation and error cause is returned.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--all'])  ## workflow
            assert cause == 'NOK: content category \'all\' is supported only with search operation'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_solution_digest(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export defined solution with digest."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock_storage_file.return_value = Database.get_storage()
        export_dict = {'metadata': Solution.get_metadata(Solution.UTC1),
                       'content': [Solution.DEFAULTS[Solution.BEATS]]}

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata but not by command line -f|--file option.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata but not by command line -f|--file option. In this case the content
        ##        category is not specified explicitly from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '-d', 'a96accc25dd23ac0'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is not defined in
        ##        solution metada or by command line -f|--file option. This should result the
        ##        file name and format defined by tool internal defaults.
        mocked_data = Solution.get_template(Solution.DEFAULTS[Solution.KAFKA])
        mocked_data = mocked_data.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  : ')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'import', '-f', 'mocked_file.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 3

            mock_file.reset_mock()
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', '7a5bf1bc09939f42'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(mocked_data),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the created file
        ##        format is yaml.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest to yaml file without specifying
        ##        the content category explicitly.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the created file
        ##        format is json.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.json'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest to json file without specifying
        ##        the content category explicitly.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.json'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the text format file
        ##        extension is 'txt'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest to text file without specifying
        ##        the content category explicitly. In this case the file extension is *.txt.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the text format file
        ##        extension is 'text'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.text'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest to text file without specifying
        ##        the content category explicitly. In this case the file extension is *.text.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.text'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export defined solution based on message digest into file format that is
        ##        not supported. This should result error string for end user and no files should
        ##        be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f', './foo.bar'])  ## workflow
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is not defined in
        ##        solution metadata or by command line -f|--file option. In this case there is
        ##        no space after colon. In this case there is no space after colon.
        mocked_data = Solution.get_template(Solution.DEFAULTS[Solution.KAFKA])
        mocked_data = mocked_data.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  :')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'import', '-f', 'mocked_file.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 3

            mock_file.reset_mock()
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', '2c4298ff3c582fe5'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(mocked_data),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on message digest. File name is not defined in
        ##        solution metadata or by command line -f|--file option. In this case there are
        ##        extra spaces around file name.
        mocked_data = Solution.get_template(Solution.DEFAULTS[Solution.KAFKA])
        mocked_data = mocked_data.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt',
                                          '## FILE  :  kubernetes-docker-log-driver-kafka.txt ')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'import', '-f', 'mocked_file.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 3

            mock_file.reset_mock()
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', '745c9e70eacc304b'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('kubernetes-docker-log-driver-kafka.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(mocked_data),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export defined solution based on message digest that cannot be found.
        ##        This should result error text for end user and no files should be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', '123456789abcdef0', '-f' './defined-solution.text'])  ## workflow
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
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
    def test_export_solution_keyword(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export defined solution with search keyword."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock_storage_file.return_value = Database.get_storage()
        export_dict = {'metadata': Solution.get_metadata(Solution.UTC1),
                       'content': [Solution.DEFAULTS[Solution.BEATS]]}

        ## Brief: Export defined solution based on search keyword. File name is defined in solution
        ##        metadata but not by command line -f|--file option.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--sall', 'beats'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on search keyword. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and yaml format defined by the command line option.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--sall', 'beats', '-f', './defined-solution.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on search keyword. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and json format defined by the command line option.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--sall', 'beats', '-f', './defined-solution.json'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)
            mock_json_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on search keyword. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the text format file
        ##        extension is 'txt'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--sall', 'beats', '-f' './defined-solution.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined solution based on search keyword. In this case the search keyword
        ##        matchies to two solutions that must be exported to file defined in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--sall', 'howto', '-f' './defined-solutions.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solutions.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Solution.get_template(Solution.DEFAULTS[Solution.BEATS])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Solution.get_template(Solution.DEFAULTS[Solution.NGINX])),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export snippet based on search keyword that cannot befound.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--sall', 'notfound', '-f', './defined-solution.yaml'])  ## workflow
            assert cause == 'NOK: cannot find content with given search criteria'
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_export_solution_template(self, mock_storage_file, mock_get_utc_time):
        """Export solution template."""

        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = Solution.TEMPLATE_UTC
        template = Solution.TEMPLATE

        ## Brief: Export solution template. This should result file name and format based on
        ##        tool internal settings.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy(['snippy', 'export', '--solution', '--template'])  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solution-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(template))
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_solution_defaults(self, mock_isfile, mock_storage_file, mock_get_utc_time, mock_yaml_dump):
        """Export solution defaults."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock_storage_file.return_value = Database.get_storage()
        export_dict = {'metadata': Solution.get_metadata(Solution.UTC1),
                       'content': [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.NGINX]]}

        ## Brief: Export solution defaults. All solutions should be exported into predefined file
        ##        location under tool data folder in yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--defaults'])  ## workflow
            assert cause == Cause.ALL_OK
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export solution defaults when there are no stored solutions. No files
        ##        should be created and OK should printed for end user. The reason is that
        ##        processing list of zero items is considered as an OK case.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'export', '--solution', '--defaults'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_not_called()
            mock_yaml_dump.assert_not_called()
            mock_yaml_dump.reset_mock()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_solution_incomplete_header(self, mock_isfile, mock_storage_file, mock_get_utc_time):
        """Export solution without date field."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'

        ## Brief: Export solution that has been updated with empty date field in the content
        ##        data. The export operation must fill the date in text content from solution
        ##        metadata. The import operation with content identified by message digest is
        ##        considered as update operation. In case of update operation, the content
        ##        metadata timestamp is set to match the update time. The date in the solution
        ##        content data is not changes because it is considered that end user may want
        ##        to keep it as is.
        mocked_data = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        original = mocked_data
        mocked_data = mocked_data.replace('## DATE  : 2017-10-20 11:11:19',
                                          '## DATE  : ')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'import', '-f', 'mocked_file.txt', '-d', 'a96accc25dd23ac0'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2

            mock_file.reset_mock()
            original = original.replace('## DATE  : 2017-10-20 11:11:19', '## DATE  :  2017-10-14 19:56:31')
            cause = snippy.run_cli(['snippy', 'export', '--solution', '-d', '2b4428c3c022abff'])  ## workflow
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(original),
                                                mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
