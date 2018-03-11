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

import time

import mock
import pytest

from snippy.cause import Cause
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliPerformance(object):
    """Test CLI reference performance."""

    @pytest.mark.usefixtures('snippy')
    def test_cli_performance(self, snippy, capsys, caplog):
        """Test console performance."""

        ## Brief: Verify performance of the tool on a rough scale. The intention
        ##        is to keep a reference test that is just iterated few times and
        ##        the time consumed is measured. This is more for manual analysis
        ##        than automation as of now.
        ##
        ##        Reference PC:   1 loop :  0.0206 /   55 loop :  0.8335 / 100 loop : 1.4925
        ##        Reference PC: 880 loop : 13.1008 / 1000 loop : 15.0400
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
        start = time.time()
        for _ in range(55):
            self.create_defaults(snippy)
            assert len(Database.get_snippets()) == 2
            assert len(Database.get_solutions()) == 2

            # Search all content
            cause = snippy.run_cli(['snippy', 'search', '--all', '--sall', '.', '-vv'])
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

        runtime = time.time() - start
        out, err = capsys.readouterr()
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("There are %d rows in stdout" % len(out))
        print("There are %d rows in stderr" % len(err))
        print("====================================")

        assert not err
        assert not caplog.records[:]
        assert runtime < 10

    @staticmethod
    def create_defaults(snippy):
        """Add default snippets for testing purposes."""

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'remove.txt'])
            assert cause == Cause.ALL_OK

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'forced.txt'])
            assert cause == Cause.ALL_OK

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Solution.DEFAULTS[Solution.BEATS]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'beats.txt'])
            assert cause == Cause.ALL_OK

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Solution.DEFAULTS[Solution.NGINX]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'nginx.txt'])
            assert cause == Cause.ALL_OK

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
