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

"""test_ut_config_search.py: Test tool configuration management to search snippets."""

import unittest

from snippy.config.config import Config
from snippy.config.source.cli import Cli


class TestUtConfigSearch(unittest.TestCase):
    """Testing configuration management for searching snippets."""

    def test_search_with_one_kw(self):
        """Test that search can be used with one keyword."""

        search_kw = ('docker',)
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)

    def test_search_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that search keywords can be added inside quotes separated by
        comma and without spaces."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker,container,cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)

    def test_search_with_quotes_and_separated_by_comma_and_space(self):
        """Test that search keywords can be added inside quotes separated by
        comma and spaces after comma."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker, container, cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)

    def test_search_with_quotes_and_separated_by_only_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker, container, cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)

    def test_search_separated_by_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker ', 'container ', 'cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)

    def test_search_separated_by_space_and_comma(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker,', 'container,', 'cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)

    def test_search_with_special_characters(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        search_kw = ('cleanup_testing', 'container-managemenet', 'dockertesting')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']))
        assert isinstance(Config.search_all_kws, tuple)
        self.assertTupleEqual(Config.search_all_kws, search_kw)
        assert len(Config.search_all_kws) == 3

    # pylint: disable=duplicate-code
    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        Config.init(None)

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        Config.init(None)
