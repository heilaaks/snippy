#!/usr/bin/env python3

"""test_arguments_search_snippet_with_keywords.py: Test command line argumens for searching snippets with keywords."""

import sys
from snippy.config import Arguments
from tests.testlib.arguments_helper import ArgumentsHelper


class TestArgumentsSearchSnippetWithKeywords(object):
    """Testing command line argument for search snippets with keywords."""

    def test_search_with_one_kw(self):
        """Test that search can be used with one keyword."""

        search_kw = ['docker']
        sys.argv = ['snippy', '-s', 'docker']
        obj = Arguments()
        assert obj.get_search() == search_kw

    def test_search_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that keywords can be added inside quotes separated by
        comma and without spaces."""

        search_kw = ['docker,container,cleanup']
        sys.argv = ['snippy', '-s', 'docker,container,cleanup']
        obj = Arguments()
        assert obj.get_search() == search_kw

    def test_search_with_quotes_and_separated_by_comma_and_space(self):
        """Test that search keywords can be added inside quotes separated
        by comma and spaces after comma."""

        search_kw = ['docker, container, cleanup']
        sys.argv = ['snippy', '-s', 'docker, container, cleanup']
        obj = Arguments()
        assert obj.get_search() == search_kw

    def test_search_with_quotes_and_separated_by_only_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        search_kw = ['docker container cleanup']
        sys.argv = ['snippy', '-s', 'docker container cleanup']
        obj = Arguments()
        assert obj.get_search() == search_kw

    def test_search_separated_by_space(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        search_kw = ['docker ', 'container ', 'cleanup']
        sys.argv = ['snippy', '-s', 'docker ', 'container ', 'cleanup']
        obj = Arguments()
        assert obj.get_search() == search_kw

    def test_search_separated_by_space_and_comma(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        search_kw = ['docker,', 'container,', 'cleanup']
        sys.argv = ['snippy', '-s', 'docker,', 'container,', 'cleanup']
        obj = Arguments()
        assert obj.get_search() == search_kw

    def test_search_with_special_characters(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        search_kw = ['dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        sys.argv = ['snippy', '-s', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Arguments()
        assert obj.get_search() == search_kw

    # pylint: disable=duplicate-code
    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        print('setup_class()')
        ArgumentsHelper().reset()

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        print('teardown_class()')
        ArgumentsHelper().reset()
