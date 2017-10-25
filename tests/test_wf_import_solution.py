#!/usr/bin/env python3

"""test_wf_import_solution.py: Test workflows for importing solutions."""

import sys
import unittest
import mock
import yaml
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSolution(unittest.TestCase):
    """Test workflows for importing solutions."""

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_importing_solutions(self, mock_isfile, mock_get_db_location, mock_safe_load):
        """Import solutions from defined yaml file.

        Workflow:
            @ import solution
        Execution:
            $ python snip.py import SolutionHelper().get_solution(0)
            $ python snip.py import SolutionHelper().get_solution(1)
            $ python snip.py import -f ./solutions.yaml
        Expected results:
            1 One solution is imported.
            2 One imported solution data already exist and the existing one is not updated.
            3 Two existing solutions are not changed when one new solution is imported.
            4 Solutions can be imported without explicitly defining the solution category
            5 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        solutions = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                  'brief': 'Debugging Elastic Beats',
                                  'group': 'beats',
                                  'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                  'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                  'category': 'solution',
                                  'filename': 'howto-debug-elastic-beats.txt',
                                  'utc': None,
                                  'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                                 {'data': tuple(Solution.SOLUTIONS_TEXT[2]),
                                  'brief': 'Testing docker log driver',
                                  'group': 'docker',
                                  'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
                                  'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                                            'https://github.com/garo/logs2kafka',
                                            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
                                  'category': 'solution',
                                  'filename': 'kubernetes-docker-log-driver-kafka.txt',
                                  'utc': '2017-10-12 11:53:17',
                                  'digest': '50249fd7264a8af3580aa684ad98b64180ca8c58b2217af91d1c4569e80c7046'}]}
        mock_safe_load.return_value = solutions
        snippy = Snippet.add_snippets(self)
        snippy = Solution.add_solutions(snippy)

        # Import solutions from yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'import', '-f', './solutions.yaml']
            snippy.reset()
            assert len(Database.get_contents()) == 4
            content_before = snippy.storage.search(Const.SOLUTION, data=solutions['content'][0]['data'])
            cause = snippy.run_cli()
            content_after = snippy.storage.search(Const.SOLUTION, data=solutions['content'][0]['data'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solutions.yaml', 'r')
            Snippet().compare(self, content_after[0], content_before[0])
            assert len(Database.get_contents()) == 5

            # Verify the imported solution by exporting it again to text file.
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', '50249fd7264a8af3', '-f', 'defined-solution.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2]))

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
