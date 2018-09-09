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

"""test_cli_search_solution: Test workflows for searching solutions."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliSearchSolution(object):
    """Test workflows for searching solutions."""

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_001(self, snippy, capsys):
        """Search solution from all fields.

        Search solutions from all fields. The match is made from one solution
        content data.
        """

        output = (
            '1. Debugging Elastic Beats @beats [a5dd8f3807e08420]',
            Const.NEWLINE.join(Solution.OUTPUT[Solution.BEATS]),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', 'filebeat', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_002(self, snippy, capsys):
        """Search solution from all fields.

        Try to search solutions with keyword that cannot be found.
        """

        output = 'NOK: cannot find content with given search criteria' + Const.NEWLINE
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', 'notfound', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_003(self, snippy, capsys):
        """Search solution with regexp.

        Search all content with regexp filter.
        """

        output = (
            '1. Debugging Elastic Beats @beats [a5dd8f3807e08420]',
            Const.NEWLINE.join(Solution.OUTPUT[Solution.BEATS]),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', '.', '--filter', '.*(\\$.*filebeat)', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_004(self, snippy, capsys):
        """Search solution with --digest option.

        Search solution by explicitly defining short message digest.
        """

        output = (
            '1. Debugging Elastic Beats @beats [a5dd8f3807e08420]',
            Const.NEWLINE.join(Solution.OUTPUT[Solution.BEATS]),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--digest', 'a5dd8f3807e08420', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_005(self, snippy, capsys):
        """Search solution from all field

        Search solutions from all fields and limit the search to specific
        group. The match must not be made from other than defined group. In
        this case the list all must print the content of defined group.
        """

        output = (
            '1. Debugging Elastic Beats @beats [a5dd8f3807e08420]',
            Const.NEWLINE.join(Solution.OUTPUT[Solution.BEATS]),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', '.', '--sgrp', 'beats', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
