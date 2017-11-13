#!/usr/bin/env python3

"""test_performance.py: Verify that there are no major impacts to performance."""

import sys
import time
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.editor import Editor
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
    from StringIO import StringIO  # pylint: disable=import-error


class TestPerformance(unittest.TestCase):
    """Test tool performance."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_performance(self, mock_isfile, mock_get_db_location, mock_call_editor):
        """Test tool performance."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Verify performance of the tool on a rough scale. The intention
        ##        is to keep a reference test that is just iterated few times and
        ##        the time consumed is measured. This is more for manual analysis
        ##        than automation as of now.
        ##
        ##        Reference PC: 1 loop : 0.0309 / 55 loop : 0.9461 / 100 loop : 1.7419
        ##
        ##        The reference is with sqlite database in memory as with all tests.
        ##        There is naturally jitter in results and the values are as of now
        ##        hand picked from few examples.
        ##
        ##        Note that when run on Python2, will use sqlite database in disk
        ##        that is naturally slower than memory database.
        ##
        ##        No errors shoould be printed and the runtime should be below 10
        ##        seconds. The runtime is intentionally to 10 times higher value
        ##        than with reference PC.
        real_stderr = sys.stderr
        sys.stderr = StringIO()
        start = time.time()
        for _ in range(55):
            snippy = Snippet.add_defaults(Snippy())
            snippy = Solution.add_defaults(snippy)

            assert len(Database.get_contents()) == 4
            # Search all content
            sys.argv = ['snippy', 'search', '--all', '--sall', '.']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK

            # Create solution with editor
            template = Solution.get_template(Solution.DEFAULTS[Solution.KAFKA])
            mock_call_editor.return_value = template
            sys.argv = ['snippy', 'create', '--editor']  ## workflow

            # Delete all content
            sys.argv = ['snippy', 'delete', '-d', '54e41e9b52a02b63']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            sys.argv = ['snippy', 'delete', '-d', '53908d68425c61dc']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            sys.argv = ['snippy', 'delete', '-d', 'a96accc25dd23ac0']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            sys.argv = ['snippy', 'delete', '-d', '61a24a156f5e9d2d']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert not Database.get_contents()

            snippy.release()
            snippy = None
        runtime = time.time() - start
        result_stderr = sys.stderr.getvalue().strip()
        sys.stderr = real_stderr
        print("runtime %.4f" % runtime)

        assert not result_stderr
        assert runtime < 10

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
