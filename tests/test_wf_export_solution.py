#!/usr/bin/env python3

"""test_wf_export_solution.py: Test workflows for exporting solutions."""

import sys
import unittest
import mock
import yaml
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfExportSolution(unittest.TestCase):
    """Test workflows for exporting solutions."""

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_all_solutions_yaml(self, mock_isfile, mock_get_db_location, mock_get_utc_time, mock_safe_dump):
        """Export solutions to defined yaml file.

        Workflow:
            @ export solution
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py import SolutionHelper().get_solution(0)
            $ python snip.py import SolutionHelper().get_solution(1)
            $ python snip.py export --solution
            $ python snip.py export --solution -f ./defined-solutions.yaml
        Expected results:
            1 Two solutions are exported.
            2 Filename defined from command line will be honored when the whole content is exported.
            3 Default filename will be used when user does not defined exported filename.
            4 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        mock_isfile.return_value = True
        snippy = Snippet.add_snippets(self)
        snippy = Solution.add_solutions(snippy)
        export = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                               'brief': 'Debugging Elastic Beats',
                               'group': 'beats',
                               'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                               'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                               'category': 'solution',
                               'filename': 'howto-debug-elastic-beats.txt',
                               'utc': None,
                               'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                              {'data': tuple(Solution.SOLUTIONS_TEXT[1]),
                               'brief': 'Debugging nginx',
                               'group': 'nginx',
                               'tags': ('debug', 'howto', 'logging', 'nginx'),
                               'links': ('https://www.nginx.com/resources/admin-guide/debug/',),
                               'category': 'solution',
                               'filename': 'howto-debug-nginx.txt',
                               'utc': None,
                               'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'}]}

        # Export all solutions without defining file name.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solutions.yaml', 'w')
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)

        # Export all solutions in defined yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './defined-solutions.yaml']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solutions.yaml', 'w')
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_export_defined_solution(self, mock_isfile, mock_get_db_location, mock_get_utc_time):  # pylint: disable=too-many-statements
        """Export solutions to defined yaml file.

        Workflow:
            @ export solution
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py import SolutionHelper().get_solution(0)
            $ python snip.py import SolutionHelper().get_solution(1)
            $ python snip.py export --solution -d a96accc25dd23ac0
            $ python snip.py export --solution -d a96accc25dd23ac0 -f ./defined-solutions.text
        Expected results:
            1 Only defined solution is exported.
            2 Filename defined in the content data will be used when no file is defined from command line.
            3 Filename defined from command line will be honored when defined content is exported.
            4 In case there is no filename in solution data or in commmand line, default filename is used.
            5 Filename parsing is able to handle failures with additional spaces in filename in text template.
            6 Exit cause is always OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        mock_isfile.return_value = True
        snippy = Snippet.add_snippets(self)
        snippy = Solution.add_solutions(snippy)

        # Export defined solution to text file defined in the solution.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('howto-debug-elastic-beats.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0]))

        # Export defined solution to text file defined in the command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-d', 'a96accc25dd23ac0', '-f' './defined-solution.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0]))

        # Export defined solution to text file when there is no file name in content data or
        # in command line. In this case there is extra space in the content data FILE template.
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
            sys.argv = ['snippy', 'export', '--solution', '-d', '7a5bf1bc09939f42']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(mocked_data)

        # Export defined solution to text file when there is no file name in content data or
        # in command line. In this case there is no space in the content data FILE template.
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
            sys.argv = ['snippy', 'export', '--solution', '-d', '2c4298ff3c582fe5']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('solution.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(mocked_data)

        # Export defined solution to text file when there is no file name in content data or
        # in command line. In this case there are additional spaces around the file name.
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
            sys.argv = ['snippy', 'export', '--solution', '-d', '745c9e70eacc304b']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('kubernetes-docker-log-driver-kafka.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(mocked_data)

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
