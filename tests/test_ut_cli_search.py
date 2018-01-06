#!/usr/bin/env python3

"""test_ut_arguments_search.py: Test command line argumens for searching snippets with keywords."""

from __future__ import print_function
import sys
from snippy.config.source.cli import Cli
from tests.testlib.cli_helper import CliHelper


class TestUtCliSearch(object):
    """Testing command line argument for search snippets with keywords."""

    def test_search_with_one_kw(self):
        """Test that search can be used with one keyword."""

        sys.argv = ['snippy', 'search', '--sall', 'docker']
        obj = Cli()
        assert obj.sall == ('docker',)

    def test_search_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that keywords can be added inside quotes separated by
        comma and without spaces."""

        sys.argv = ['snippy', 'search', '--sall', 'docker,container,cleanup']
        obj = Cli()
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_with_quotes_and_separated_by_comma_and_space(self):
        """Test that search keywords can be added inside quotes separated
        by comma and spaces after comma."""

        sys.argv = ['snippy', 'search', '--sall', 'docker, container, cleanup']
        obj = Cli()
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_with_quotes_and_separated_by_only_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        sys.argv = ['snippy', 'search', '--sall', 'docker container cleanup']
        obj = Cli()
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_separated_by_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        sys.argv = ['snippy', 'search', '--sall', 'docker ', 'container ', 'cleanup']
        obj = Cli()
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_separated_by_space_and_comma(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        sys.argv = ['snippy', 'search', '--sall', 'docker,', 'container,', 'cleanup']
        obj = Cli()
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_search_with_special_characters(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        sys.argv = ['snippy', 'search', '--sall', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Cli()
        assert obj.sall == ('cleanup_testing', 'container-managemenet', 'dockertesting')

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
