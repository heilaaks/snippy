# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
from tests.lib.content import Content
from tests.lib.solution import Solution


class TestCliSearchSolution(object):
    """Test workflows for searching solutions."""

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_001(snippy, capsys):
        """Search solutions with ``sall`` option.

        Search solutions from all content fields. The match is made from one
        solution content data.
        """

        output = (
            '1. Debugging Elastic Beats @beats [4346ba4c79247430]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--sall', 'filebeat', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_002(snippy, capsys):
        """Search solutions with ``sall`` option.

        Try to search solutions with keyword that cannot be found.
        """

        output = 'NOK: cannot find content with given search criteria' + Const.NEWLINE
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--sall', 'notfound', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_003(snippy, capsys):
        """Search solutions with ``filter`` option.

        Search all content with regexp filter.
        """

        output = (
            '1. Debugging Elastic Beats @beats [4346ba4c79247430]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--sall', '.', '--filter', '.*(\\$.*filebeat)', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_004(snippy, capsys):
        """Search solutions with ``digest`` option.

        Search a solution by explicitly defining the solutions message digest
        short format.
        """

        output = (
            '1. Debugging Elastic Beats @beats [4346ba4c79247430]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--digest', '4346ba4c79247430', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_005(snippy, capsys):
        """Search solutions with ``sall`` and ``sgrp`` options.

        Search solutions from all fields and limit the search to a specific
        group. The match must not be made from other than the defined group.
        In this case the ``sall`` option must print content only from defined
        group.
        """

        output = (
            '1. Debugging Elastic Beats @beats [4346ba4c79247430]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--sall', '.', '--sgrp', 'beats', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_006(snippy, capsys):
        """Search solutions with ``headers`` option.

        Search resources and print only the content headers.
        """

        output = (
            '1. Debugging Elastic Beats @beats [4346ba4c79247430]',
            '2. Debugging nginx @nginx [6cfe47a8880a8f81]',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--sall', '.', '--headers', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
