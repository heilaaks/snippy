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

"""test_cli_search_reference: Test workflows for searching references."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliSearchReference(object):
    """Test workflows for searching references."""

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_001(self, snippy, capsys):
        """Search reference from all fields.

        Search references from all fields. The match is made from one reference
        content data.
        """

        output = (
            '1. Python regular expression @python [cb9225a81eab8ced]',
            '',
            '   > https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
            '   > https://pythex.org/',
            '   # howto,online,python,regexp',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--reference', '--sall', 'regexp', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_002(self, snippy, capsys):
        """Search reference from all fields.

        Try to search references with keyword that cannot be found.
        """

        output = 'NOK: cannot find content with given search criteria' + Const.NEWLINE
        cause = snippy.run(['snippy', 'search', '--reference', '--sall', 'notfound', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_003(self, snippy, capsys):
        """Search reference with --digest option.

        Search reference by explicitly defining short message digest.
        """

        output = (
            '1. How to write commit messages @git [5c2071094dbfaa33]',
            '',
            '   > https://chris.beams.io/posts/git-commit/',
            '   # commit,git,howto',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--reference', '--digest', '5c20', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_004(self, snippy, capsys):
        """Search reference from all field

        Search references from all fields and limit the search to specific
        group. The match must not be made from other than defined group. In
        this case the list all must print the content of defined group.
        """

        output = (
            '1. How to write commit messages @git [5c2071094dbfaa33]',
            '',
            '   > https://chris.beams.io/posts/git-commit/',
            '   # commit,git,howto',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--reference', '--sall', 'howto', '--sgrp', 'git', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
