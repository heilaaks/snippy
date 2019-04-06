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

"""test_cli_search_reference: Test workflows for searching references."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution import Solution


class TestCliSearchReference(object):
    """Test workflows for searching references."""

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_001(self, snippy, capsys):
        """Search references with ``sall`` option.

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
        """Search references with ``sall`` option.

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
        """Search references with ``digest`` option.

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
        """Search references with ``uuid`` option.

        Search reference by explicitly defining full length content uuid.
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
        cause = snippy.run(['snippy', 'search', '--reference', '--uuid', '12cd5827-b6ef-4067-b5ac-3ceac07dde9f', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_005(self, snippy, capsys):
        """Search references with ``uuid`` option.

        Try to search reference by using resource uuid in short form that
        does not have the last digit. The short form must not be accepted
        and no results must be returned. The UUID is intended to be used
        as fully matching identity.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--reference', '--uuid', '12cd5827-b6ef-4067-b5ac-3ceac07dde9', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_006(self, snippy, capsys):
        """Search references with ``uuid`` option.

        Try to search reference by explicitly defining content uuid that
        cannot be found.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--reference', '--uuid', '1234567', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-netcat')
    def test_cli_search_reference_007(self, snippy, capsys):
        """Search references with ``uuid`` option.

        Try to search references by defining empty string for uuid which is
        invalid. This must not result any content
        """

        output = (
            'NOK: cannot find content with given search criteria',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--reference', '--uuid', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-netcat')
    def test_cli_search_reference_008(self, snippy, capsys):
        """Search references with ``uuid`` option.

        Try to search references by defining short uuid that matches to
        multiple contents in different categories. Since uuid must be
        unique and it must match to only one content, this must not
        find any content.
        """

        output = (
            'NOK: cannot find content with given search criteria',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--reference', '--uuid', '1', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_009(self, snippy, capsys):
        """Search references with ``sall`` and ``sgrp`` options.

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

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_010(self, snippy, capsys):
        """Search references with ``sall`` and `scat` options.

        Search references from all fields. In this case the category has been
        set to 'all' which must find also references.
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
        cause = snippy.run(['snippy', 'search', '--sall', 'regexp', '--no-ansi', '--all'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-remove', 'import-beats')
    def test_cli_search_reference_011(self, snippy, capsys):
        """Search references with ``sall`` and ``sall`` options.

        Search content from all fields. Search category defines that the
        search must be made from snippets, solutions and references.
        """

        output = (
            '1. Debugging Elastic Beats @beats [db712a82662d6932]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   : ',
            '',
            '2. Python regular expression @python [cb9225a81eab8ced]',
            '',
            '   > https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
            '   > https://pythex.org/',
            '   # howto,online,python,regexp',
            '',
            '3. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'regexp,docker,beats', '--no-ansi', '--scat', 'reference,solution,snippet'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-remove', 'import-beats')
    def test_cli_search_reference_012(self, snippy, capsys):
        """Search references with ``sall`` and `scat` options.

        Search content from all fields. Search category defines that the
        search must be made from snippets and references.
        """

        output = (
            '1. Python regular expression @python [cb9225a81eab8ced]',
            '',
            '   > https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
            '   > https://pythex.org/',
            '   # howto,online,python,regexp',
            '',
            '2. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'regexp,docker,beats', '--no-ansi', '--scat', 'reference,snippet'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-remove', 'import-beats')
    def test_cli_search_reference_013(self, snippy, capsys):
        """Search references with ``sall`` option.

        Search content from all fields. The content category is defined with
        ``all`` so the search must result a hit from each category.
        """

        output = (
            '1. Debugging Elastic Beats @beats [db712a82662d6932]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   : ',
            '',
            '2. Python regular expression @python [cb9225a81eab8ced]',
            '',
            '   > https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
            '   > https://pythex.org/',
            '   # howto,online,python,regexp',
            '',
            '3. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'regexp,docker,beats', '--no-ansi', '--all'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-remove', 'import-beats')
    def test_cli_search_reference_014(self, snippy, capsys):
        """Search references with ``sall`` and ``scat`` options.

        Search content from all fields. Content category is set to --all but
        the search category defines that the search must be made from snippets
        and references. This must result hits only from snippets and
        references.
        """

        output = (
            '1. Python regular expression @python [cb9225a81eab8ced]',
            '',
            '   > https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
            '   > https://pythex.org/',
            '   # howto,online,python,regexp',
            '',
            '2. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--all', '--sall', 'regexp,docker,beats', '--no-ansi', '--scat', 'reference,snippet'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references', 'import-remove', 'import-beats')
    def test_cli_search_reference_015(self, snippy, capsys):
        """Search references with ``scat`` and ``stag`` options.

        In this case the search category is defined explicitly. The search
        result must contain only resources within selected category and with
        defined tag. This test must not find resource from reference category
        which also contains the howto tag.
        """

        output = (
            '1. Debugging Elastic Beats @beats [db712a82662d6932]',
            Const.NEWLINE.join(Solution.BEATS_OUTPUT),
            '   :',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'solution', '--stag', 'howto', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-references')
    def test_cli_search_reference_016(self, snippy, capsys):
        """Search references with ``scat`` and ``stag`` options.

        Try to define search category ``scat`` option in plural form. This
        must not work because only singular forms in the search category
        ``scat`` option are supported.

        It is possible to define the content category with content catefory
        option long format like ``--snippets`` in plural form from command
        line. But this is not supported for the ``scat`` option which is also
        used in the REST API.

        This limits the supported values in the REST API and thus it makes
        error handling simpler.
        """

        output = "NOK: search categories ('solutions') are not a subset of ('snippet', 'solution', 'reference')\n"
        cause = snippy.run(['snippy', 'search', '--scat', 'solutions', '--stag', 'howto', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == "NOK: search categories ('solutions') are not a subset of ('snippet', 'solution', 'reference')"
        assert out == output
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
