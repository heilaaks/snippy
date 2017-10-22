#!/usr/bin/env python3

"""test_wf_export_solution.py: Test workflows for exporting solutions."""

import sys
import unittest
import mock
import yaml
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

        # Export all solutions without defining file name.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mocked_file:
            exported_data1 = Solution.SOLUTIONS_TEXT[0]
            exported_data1.pop()
            exported_data1 = tuple(exported_data1)
            exported_data2 = Solution.SOLUTIONS_TEXT[1]
            exported_data2.pop()
            exported_data2 = tuple(exported_data2)
            export = {'content': [{'data': exported_data1,
                                   'brief': 'Debugging Elastic Beats',
                                   'group': 'beats',
                                   'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                   'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                   'category': 'solution',
                                   'filename': 'howto-debug-elastic-beats.txt',
                                   'utc': None,
                                   'digest': 'e95e9092c92e3440e975d34d4799c7d707f6d319eab36365d08cdcb04de4bd11'},
                                  {'data': exported_data2,
                                   'brief': 'Debugging nginx',
                                   'group': 'nginx',
                                   'tags': ('debug', 'howto', 'logging', 'nginx'),
                                   'links': ('https://www.nginx.com/resources/admin-guide/debug/',),
                                   'category': 'solution',
                                   'filename': 'howto-debug-nginx.txt',
                                   'utc': None,
                                   'digest': '69779f83c3c649e1a61745aaa83d0cdb7fb80285c797e9439c25ea0ac75e4d29'}]}

            sys.argv = ['snippy', 'export', '--solution']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mocked_file.assert_called_once_with('./solutions.yaml', 'w')
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)

        # Export all solutions in defined yaml file
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mocked_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './defined-solutions.yaml']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mocked_file.assert_called_once_with('./defined-solutions.yaml', 'w')
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
