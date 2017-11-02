#!/usr/bin/env python3

"""test_wf_export_solution.py: Test workflows for exporting solutions."""

import sys
import unittest
import json
import yaml
import mock
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfExportSolution(unittest.TestCase):
    """Test workflows for exporting solutions."""

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_all_solutions(self, mock_isfile, mock_get_db_location, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export all solutions."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        mock_isfile.return_value = True
        snippy = Snippet.add_defaults(None)
        snippy = Solution.add_defaults(snippy)
        export_dict = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                    'brief': 'Debugging Elastic Beats',
                                    'group': 'beats',
                                    'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                    'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-elastic-beats.txt',
                                    'utc': '2017-10-20 11:11:19',
                                    'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                                   {'data': tuple(Solution.SOLUTIONS_TEXT[1]),
                                    'brief': 'Debugging nginx',
                                    'group': 'nginx',
                                    'tags': ('debug', 'howto', 'logging', 'nginx'),
                                    'links': ('https://www.nginx.com/resources/admin-guide/debug/',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-nginx.txt',
                                    'utc': '2017-10-20 06:16:27',
                                    'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'}]}

        ## Brief: Export all solutions into file. File name or format are not defined in command
        ##        line which should result tool default file and format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solutions.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)

        ## Brief: Export all solutions into defined yaml file. File name and format are defined
        ##        in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './all-solutions.yaml'] ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)

        ## Brief: Export all solutions into defined json file. File name and format are defined
        ##        in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './all-solutions.json'] ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)

        ## Brief: Export all solutions into defined text file with file extension 'txt'. File name
        ##        and format are defined in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './all-solutions.txt'] ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[1])),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Export all solutions into defined text file with file extension 'text'. File name
        ##        and format are defined in command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './all-solutions.text'] ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./all-solutions.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0])),
                                                mock.call(Const.NEWLINE),
                                                mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[1])),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Try to export all solutions into file format that is not supported. This should
        ##        result error text for end user and no files should be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './foo.bar'] ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

        # Release all resources
        snippy.release()

    @mock.patch.object(json, 'dump')
    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_defined_solution(self, mock_isfile, mock_get_db_location, mock_get_utc_time, mock_yaml_dump, mock_json_dump):
        """Export defined solution."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        mock_isfile.return_value = True
        snippy = Snippet.add_defaults(None)
        snippy = Solution.add_defaults(snippy)
        export_dict = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                    'brief': 'Debugging Elastic Beats',
                                    'group': 'beats',
                                    'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                    'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-elastic-beats.txt',
                                    'utc': '2017-10-20 11:11:19',
                                    'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'}]}

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata but not by command line -f|--file option.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0])),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Export defined solution based on message digest. File name is not defined in
        ##        solution metada or by command line -f|--file option. This should result the
        ##        file name and format defined by tool internal defaults.
        mocked_data = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2])
        mocked_data = mocked_data.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  : ')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            sys.argv = ['snippy', 'import', '-f', 'mocked_file.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 3

            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '--solution', '-d', '7a5bf1bc09939f42']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(mocked_data),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the created file
        ##        format is yaml.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.yaml']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.yaml', 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the created file
        ##        format is json.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.json']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.json', 'w')
            mock_json_dump.assert_called_with(export_dict, mock.ANY)

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the text format file
        ##        extension is 'txt'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.txt']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0])),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Export defined solution based on message digest. File name is defined in solution
        ##        metadata and in command line -f|--file option. This should result the file name
        ##        and format defined by the command line option. In this case the text format file
        ##        extension is 'text'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.text']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0])),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Try to export defined solution based on message digest into file format that is
        ##        not supported. This should result error string for end user and no files should
        ##        be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f', './foo.bar']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

        ## Brief: Export defined solution based on message digest. File name is not defined in
        ##        solution metadata or by command line -f|--file option. In this case there is
        ##        no space after colon. In this case there is no space after colon.
        mocked_data = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2])
        mocked_data = mocked_data.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt', '## FILE  :')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy.reset()
            sys.argv = ['snippy', 'delete', '-d', '7a5bf1bc09939f42']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK

            sys.argv = ['snippy', 'import', '-f', 'mocked_file.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 3

            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '--solution', '-d', '2c4298ff3c582fe5']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(mocked_data),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Export defined solution based on message digest. File name is not defined in
        ##        solution metadata or by command line -f|--file option. In this case there are
        ##        extra spaces around file name.
        mocked_data = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2])
        mocked_data = mocked_data.replace('## FILE  : kubernetes-docker-log-driver-kafka.txt',
                                          '## FILE  :  kubernetes-docker-log-driver-kafka.txt ')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy.reset()
            sys.argv = ['snippy', 'delete', '-d', '2c4298ff3c582fe5']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK

            sys.argv = ['snippy', 'import', '-f', 'mocked_file.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 3

            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '--solution', '-d', '745c9e70eacc304b']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('kubernetes-docker-log-driver-kafka.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(mocked_data),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Try to export defined solution based on message digest that cannot be found.
        ##        This should result error text for end user and no files should be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', '123456789abcdef0', '-f' './defined-solution.text']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find solution to be exported with digest 123456789abcdef0'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

        # Release all resources
        snippy.release()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_solution_template(self, mock_get_db_location, mock_get_utc_time):
        """Export solution template."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        template = Solution.TEMPLATE

        ## Brief: Export solution template. This should result file name and format based on
        ##        tool internal settings.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            from snippy.snip import Snippy
            sys.argv = ['snippy', 'export', '--solution', '--template']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solution-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(template))

        # Release all resources
        snippy.release()

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_solution_defaults(self, mock_isfile, mock_get_db_location, mock_get_utc_time, mock_yaml_dump):
        """Export solution defaults."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        mock_isfile.return_value = True
        snippy = Snippet.add_defaults(None)
        snippy = Solution.add_defaults(snippy)
        export_dict = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                    'brief': 'Debugging Elastic Beats',
                                    'group': 'beats',
                                    'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                    'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-elastic-beats.txt',
                                    'utc': '2017-10-20 11:11:19',
                                    'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                                   {'data': tuple(Solution.SOLUTIONS_TEXT[1]),
                                    'brief': 'Debugging nginx',
                                    'group': 'nginx',
                                    'tags': ('debug', 'howto', 'logging', 'nginx'),
                                    'links': ('https://www.nginx.com/resources/admin-guide/debug/',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-nginx.txt',
                                    'utc': '2017-10-20 06:16:27',
                                    'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'}]}

        ## Brief: Export solution defaults. All solutions should be exported into predefined file
        ##        location under tool data folder in yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '--defaults']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'w')
            mock_yaml_dump.assert_called_with(export_dict, mock.ANY, default_flow_style=mock.ANY)

        ## Brief: Try to export solution defaults when there are no stored solutions. No files
        ##        should be created and OK should printed for end user. The reason is that
        ##        processing list of zero items is considered as an OK case.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            Database.delete_all_contents()
            mock_file.reset_mock()
            mock_yaml_dump.reset_mock()
            sys.argv = ['snippy', 'export', '--solution', '--defaults']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_not_called()
            mock_yaml_dump.assert_not_called()

        # Release all resources
        snippy.release()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_solution_incomplete_header(self, mock_isfile, mock_get_db_location, mock_get_utc_time):
        """Export solution without date field."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        mock_isfile.return_value = True
        snippy = Solution.add_defaults(None)

        ## Brief: Export solution that has been updated with empty date field in the content
        ##        data. The export operation must fill the date in text content from solution
        ##        metadata. The import operation with content identified by message digest is
        ##        considered as update operation. In case of update operation, the content
        ##        metadata timestamp is set to match the update time. The date in the solution
        ##        content data is not changes because it is considered that end user may want
        ##        to keep it as is.
        mocked_data = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0])
        original = mocked_data
        mocked_data = mocked_data.replace('## DATE  : 2017-10-20 11:11:19',
                                          '## DATE  : ')
        mocked_open = mock.mock_open(read_data=mocked_data)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            sys.argv = ['snippy', 'import', '-f', 'mocked_file.txt', '-d', 'a96accc25dd23ac0']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2

            mock_file.reset_mock()
            original = original.replace('## DATE  : 2017-10-20 11:11:19', '## DATE  :  2017-10-14 19:56:31')
            sys.argv = ['snippy', 'export', '--solution', '-d', '2b4428c3c022abff']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(original),
                                                mock.call(Const.NEWLINE)])

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
