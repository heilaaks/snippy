#!/usr/bin/env python3

"""test_config_find_snippet_with_keywords.py: Test tool configuration management to find snippets."""

import sys
from snippy.config import Config
from tests.testlib.arguments_helper import ArgumentsHelper


class TestConfigFindSnippetWithKeywords(object):
    """Testing configurationg management for finding snippets."""

    def test_find_with_one_kw(self):
        """Test that find can be used with one keyword."""

        find_kw = ['docker']
        sys.argv = ['snippy', '-f', 'docker']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 1

    def test_find_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that keywords can be added inside quotes separated by
        comma and without spaces."""

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ["snippy", "-f", 'docker,container,cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_find_with_quotes_and_separated_by_comma_and_space(self):
        """Test that find keywords can be added inside quotes separated by
        comma and spaces after comma."""

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker, container, cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_find_with_quotes_and_separated_by_only_space(self):
        """Test that find keywords can be added so that they are separated
        by spaces before and after the words."""

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker container cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_find_separated_by_space(self):
        """Test that find keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker ', 'container ', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_find_separated_by_space_and_comma(self):
        """Test that find keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker,', 'container,', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_find_with_special_characters(self):
        """Test that find keywords are accepted if they contain special
        characters."""

        find_kw = ['cleanup_testing', 'container-managemenet', 'dockertesting']
        sys.argv = ['snippy', '-f', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

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
