#!/usr/bin/env python3

"""test_config_find_snippet.py: Test tool configuration management find snippets."""

import sys
from tests.testlib.arguments_helper import ArgumentsHelper


class TestConfigFindSnippet(object):
    """Testing configurationg management for finding snippets."""

    def test_no_value(self):
        """Test that empty argument list is set to configuration."""

        from snippy.config import Config

        sys.argv = ['snippy']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert not obj.get_find_keywords()

    def test_valid_value_one_find_kw(self):
        """Test that snippets can be found with one keyword and that the keyword
        configuration is a list that can be iterated."""

        from snippy.config import Config

        find_kw = ['docker']
        sys.argv = ['snippy', '-f', 'docker']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 1

    def test_valid_find_kw_quoted_without_spaces(self):
        """Test that snippets can be found with multiple keywords and that the keyword
        configuration is a list that can be iterated. The keywords are inside quotes
        without spaces."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ["snippy", "-f", 'docker,container,cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_quoted_with_spaces(self):
        """Test that snippets can be found with multiple keywords and that the keyword
        configuration is a list that can be iterated. The keywords are inside quotes
        and separated with spaces."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker, container, cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_with_spaces(self):
        """Test that find keywords are accepted if the keywords are elements in a list.
        In here the keywords are separated by spaces before and after the words like in
        '-f docker container cleanup'. The result should be proper sorted list of
        keywords."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker ', 'container ', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_with_comma(self):
        """Test that find keywords are accepted if the keywords are elements in a list.
        In here the keywords are separated by commas after the words like in '-f docker,
        container, cleanup'. The result should be proper sorted list of keywords."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker,', 'container,', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_with_space_inside_quotes(self):
        """Test that find keywords are accepted if the keywords are elements in a list.
        In here the keywords are separated by spaces before and after the words like in
        '-f 'docker container cleanup''. The result should be proper sorted list of
        keywords."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker container cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_with_comma_inside_quotes(self):
        """Test that find keywords are accepted if the keywords are elements in a list.
        In here the keywords are separated by commas after the words like in '-f 'docker,
        container, cleanup''. The result should be proper sorted list of keywords."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker, container, cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_with_list(self):
        """Test that find keywords are accepted if the keywords are elements in a list.
        This might not be realistic case since user might not be able to reproduce this."""

        from snippy.config import Config

        find_kw = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-f', 'docker', 'container', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_find_keywords(), list)
        assert set(obj.get_find_keywords()) == set(find_kw)
        assert len(obj.get_find_keywords()) == 3

    def test_valid_find_kw_with_special_characters(self):
        """Test that find keywords are accepted if they contain special characters."""

        from snippy.config import Config

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
