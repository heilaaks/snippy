#!/usr/bin/env python3

"""test_cli_performance.py: Verify that there are no major impacts to performance in console usage."""

from __future__ import print_function
import sys
import time
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.source.editor import Editor
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
    from StringIO import StringIO  # pylint: disable=import-error


class TestCliPerformance(object):
    """Test tool performance."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_cli_performance(self, mock_isfile, mock_get_db_location, mock_call_editor):
        """Test console performance."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Verify performance of the tool on a rough scale. The intention
        ##        is to keep a reference test that is just iterated few times and
        ##        the time consumed is measured. This is more for manual analysis
        ##        than automation as of now.
        ##
        ##        Reference PC:   1 loop :  0.0237 /   55 loop : 0.7971 / 100 loop : 1.4365
        ##        Reference PC: 880 loop : 12.7213 / 1000 loop : 14.3598
        ##
        ##        The reference is with sqlite database in memory as with all tests.
        ##        There is naturally jitter in results and the values are as of now
        ##        hand picked from few examples.
        ##
        ##        Note that when run on Python2, will use sqlite database in disk
        ##        that is naturally slower than memory database.
        ##
        ##        No errors should be printed and the runtime should be below 10
        ##        seconds. The runtime is intentionally set 10 times higher value
        ##        than with the reference PC.
        real_stderr = sys.stderr
        real_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()
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
        result_stdout = sys.stdout.getvalue().strip()
        sys.stderr = real_stderr
        sys.stdout = real_stdout
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("There are %d rows in stdout" % len(result_stdout))
        print("There are %d rows in stderr" % len(result_stderr))
        print("====================================")

        assert not result_stderr
        assert runtime < 10

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
