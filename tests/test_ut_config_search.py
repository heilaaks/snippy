#!/usr/bin/env python3

"""test_ut_config_search.py: Test tool configuration management to search snippets."""

from __future__ import print_function
import sys
import unittest
from snippy.config.config import Config
from snippy.config.source.cli import Cli
from tests.testlib.cli_helper import CliHelper


class TestUtConfigSearch(unittest.TestCase):
    """Testing configuration management for searching snippets."""

    def test_search_with_one_kw(self):
        """Test that search can be used with one keyword."""

        search_kw = ('docker',)
        sys.argv = ['snippy', 'search', '--sall', 'docker']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)

    def test_search_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that search keywords can be added inside quotes separated by
        comma and without spaces."""

        search_kw = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'search', '--sall', 'docker,container,cleanup']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)

    def test_search_with_quotes_and_separated_by_comma_and_space(self):
        """Test that search keywords can be added inside quotes separated by
        comma and spaces after comma."""

        search_kw = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'search', '--sall', 'docker, container, cleanup']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)

    def test_search_with_quotes_and_separated_by_only_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        search_kw = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'search', '--sall', 'docker container cleanup']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)

    def test_search_separated_by_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        search_kw = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'search', '--sall', 'docker ', 'container ', 'cleanup']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)

    def test_search_separated_by_space_and_comma(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        search_kw = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'search', '--sall', 'docker,', 'container,', 'cleanup']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)

    def test_search_with_special_characters(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        search_kw = ('cleanup_testing', 'container-managemenet', 'dockertesting')
        sys.argv = ['snippy', 'search', '--sall', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Config()
        obj.read_source(Cli())
        assert isinstance(obj.get_search_all(), tuple)
        self.assertTupleEqual(obj.get_search_all(), search_kw)
        assert len(obj.get_search_all()) == 3

    # pylint: disable=duplicate-code
    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        print('setup_class()')
        CliHelper().reset()

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        print('teardown_class()')
        CliHelper().reset()
