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

"""test_ut_arguments_search: Test command line argumens for searching snippets with keywords."""

from snippy.config.source.cli import Cli


class TestUtCliSearch(object):
    """Testing command line argument for search snippets with keywords."""

    def test_search_with_one_kw(self):
        """Test that search can be used with one keyword."""

        obj = Cli(['snippy', 'search', '--sall', 'docker'])
        assert obj.sall == ('docker',)

    def test_search_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that keywords can be added inside quotes separated by
        comma and without spaces."""

        obj = Cli(['snippy', 'search', '--sall', 'docker,container,cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_with_quotes_and_separated_by_comma_and_space(self):
        """Test that search keywords can be added inside quotes separated
        by comma and spaces after comma."""

        obj = Cli(['snippy', 'search', '--sall', 'docker, container, cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_with_quotes_and_separated_by_only_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        obj = Cli(['snippy', 'search', '--sall', 'docker container cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_separated_by_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        obj = Cli(['snippy', 'search', '--sall', 'docker ', 'container ', 'cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_separated_by_space_and_comma(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        obj = Cli(['snippy', 'search', '--sall', 'docker,', 'container,', 'cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_with_special_characters(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        obj = Cli(['snippy', 'search', '--sall', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing'])
        assert obj.sall == ('cleanup_testing', 'container-managemenet', 'dockertesting')
