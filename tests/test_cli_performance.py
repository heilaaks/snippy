#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
from tests.lib.content import Content
from tests.lib.snippet import Snippet
from tests.lib.solution import Solution


class TestCliPerformance(object):
    """Test CLI performance."""

    @pytest.mark.server
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_performance(self, snippy_perf, capsys, caplog):
        """Test CLI performance.

        Verify performance of the tool on a rough scale. The intention
        is to keep a reference test that is just iterated few times and
        the time consumed is measured. This is more for manual analysis
        than automation as of now.

        Reference PC:   1 loop :  0.0252 /   55 loop :  1.0865 / 100 loop : 1.9484
        Reference PC: 880 loop : 17.6897 / 1000 loop : 19.6802

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
            Content.assert_storage_size(4)

            # Search all content.
            cause = snippy_perf.run(['snippy', 'search', '--all', '--sall', '.'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK

            # Delete all content.
            cause = snippy_perf.run(['snippy', 'delete', '-d', '54e41e9b52a02b63'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK
            cause = snippy_perf.run(['snippy', 'delete', '-d', '53908d68425c61dc'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK
            cause = snippy_perf.run(['snippy', 'delete', '-d', 'db712a82662d6932'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK
            cause = snippy_perf.run(['snippy', 'delete', '-d', '5dee85bedb7f4d3a'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK
            Content.assert_storage(None)

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

        file_content = Content.get_file_content(Content.TEXT, {'data': [Snippet.REMOVE]})
        with mock.patch('snippy.content.migrate.open', file_content, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'remove.txt'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK

        file_content = Content.get_file_content(Content.TEXT, {'data': [Snippet.FORCED]})
        with mock.patch('snippy.content.migrate.open', file_content, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'forced.txt'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK

        file_content = Content.get_file_content(Content.TEXT, {'data': [Solution.BEATS]})
        with mock.patch('snippy.content.migrate.open', file_content, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'beats.txt'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK

        file_content = Content.get_file_content(Content.TEXT, {'data': [Solution.NGINX]})
        with mock.patch('snippy.content.migrate.open', file_content, create=True):
            cause = snippy.run(['snippy', 'import', '-f', 'nginx.txt'] + Content.db_cli_params())
            assert cause == Cause.ALL_OK

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
