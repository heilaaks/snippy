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

"""test_cli_performance.py: Verify that there are no major impacts to performance in console usage."""

from __future__ import print_function

import sys
import time

import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
    from StringIO import StringIO  # pylint: disable=import-error


class TestCliPerformance(object):
    """Test tool performance."""

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_cli_performance(self, mock_isfile, mock_storage_file):
        """Test console performance."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Verify performance of the tool on a rough scale. The intention
        ##        is to keep a reference test that is just iterated few times and
        ##        the time consumed is measured. This is more for manual analysis
        ##        than automation as of now.
        ##
        ##        Reference PC:   1 loop :  0.0249 /   55 loop :  0.9093 / 100 loop : 1.5871
        ##        Reference PC: 880 loop : 14.1233 / 1000 loop : 15.9744
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
            snippy = Snippet.add_defaults()
            snippy = Solution.add_defaults(snippy)

            assert len(Database.get_contents()) == 4
            # Search all content
            cause = snippy.run_cli(['snippy', 'search', '--all', '--sall', '.'])
            assert cause == Cause.ALL_OK

            # Delete all content
            cause = snippy.run_cli(['snippy', 'delete', '-d', '54e41e9b52a02b63'])
            assert cause == Cause.ALL_OK
            cause = snippy.run_cli(['snippy', 'delete', '-d', '53908d68425c61dc'])
            assert cause == Cause.ALL_OK
            cause = snippy.run_cli(['snippy', 'delete', '-d', 'a96accc25dd23ac0'])
            assert cause == Cause.ALL_OK
            cause = snippy.run_cli(['snippy', 'delete', '-d', '61a24a156f5e9d2d'])
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
