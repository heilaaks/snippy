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

        # Export all solutions in defined yaml file
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--solution', '-f', './defined-solutions.yaml']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./defined-solutions.yaml', 'w')
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
