#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""test_cli_performance: Track CLI performance with reference test."""

from __future__ import print_function

import time

import mock
import pytest

from snippy.cause import Cause
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliPerformance(object):
    """Test CLI performance."""

    @pytest.mark.serial
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_performance(self, snippy_perf, capsys, caplog):
        """Test CLI performance.

        Verify performance of the tool on a rough scale. The intention
        is to keep a reference test that is just iterated few times and
        the time consumed is measured. This is more for manual analysis
        than automation as of now.

        Reference PC:   1 loop :  0.0225 /   55 loop :  1.0290 / 100 loop : 1.8829
        Reference PC: 880 loop : 16.3486 / 1000 loop : 18.5014

        The reference is with sqlite database in memory as with all tests.
        There is naturally jitter in results and the values are as of now
        hand picked from few examples.

        Note that when run on Python2, will use sqlite database in disk
        that is naturally slower than memory database.

        No errors should be printed and the runtime should be below 10
        seconds. The runtime is intentionally set 15 times higher value
        than with the reference PC to cope with slow test envrironments.
        """

        start = time.time()
        for _ in range(55):
            self.create_defaults(snippy_perf)
            assert Database.get_snippets().size() == 2
            assert Database.get_solutions().size() == 2

            # Search all content.
            cause = snippy_perf.run(['snippy', 'search', '--all', '--sall', '.'])
            assert cause == Cause.ALL_OK

            # Delete all content.
            cause = snippy_perf.run(['snippy', 'delete', '-d', '54e41e9b52a02b63'])
            assert cause == Cause.ALL_OK
            cause = snippy_perf.run(['snippy', 'delete', '-d', '53908d68425c61dc'])
            assert cause == Cause.ALL_OK
            cause = snippy_perf.run(['snippy', 'delete', '-d', 'db712a82662d6932'])
            assert cause == Cause.ALL_OK
            cause = snippy_perf.run(['snippy', 'delete', '-d', '7c226ee33a088381'])
            assert cause == Cause.ALL_OK
            assert not Database.get_collection().size()

        runtime = time.time() - start
        out, err = capsys.readouterr()
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("There are %d rows in stdout" % len(out))
        print("There are %d rows in stderr" % len(err))
        print("====================================")

        assert not err
        assert not caplog.records[:]
        assert runtime < 15

    @staticmethod
    def create_defaults(snippy):
        """Add default snippets for testing purposes."""

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE]))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'remove.txt'])
            assert cause == Cause.ALL_OK

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Snippet.DEFAULTS[Snippet.FORCED]))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'forced.txt'])
            assert cause == Cause.ALL_OK

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Solution.DEFAULTS[Solution.BEATS]))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'beats.txt'])
            assert cause == Cause.ALL_OK

        mocked_open = mock.mock_open(read_data=Snippet.get_template(Solution.DEFAULTS[Solution.NGINX]))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'nginx.txt'])
            assert cause == Cause.ALL_OK

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
