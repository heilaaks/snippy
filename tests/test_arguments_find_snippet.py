#!/usr/bin/env python3

"""test_arguments_find_snippet.py: Test command line argumens for finding snippet."""

import sys
from tests.testlib.arguments_helper import ArgumentsHelper


class TestArgumentsFindSnippet(object):
    """Testing command line arguments for finding snippet."""

    def test_no_value(self):
        """Test that find keyword missing does not cause problems."""

        from snippy.config import Arguments

        sys.argv = ['snippy']
        obj = Arguments()
        assert obj.get_find() == ''

    def test_valid_value_one_find_kw(self):
        """Test that find can be used with one keyword."""

        from snippy.config import Arguments

        find_kw = ['docker']
        sys.argv = ['snippy', '-f', 'docker']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_quoted_without_spaces(self):
        """Test that new snippet can be found with multiple keywords.
        The keywords are inside quotes without spaces."""

        from snippy.config import Arguments

        find_kw = ['docker,container,cleanup']
        sys.argv = ['snippy', '-f', 'docker,container,cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_quoted_with_spaces(self):
        """Test that new snippet can be found with multiple keywords.
        The keywords are inside quotes with spaces."""

        from snippy.config import Arguments

        find_kw = ['docker, container, cleanup']
        sys.argv = ['snippy', '-f', 'docker, container, cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_with_spaces(self):
        """Test that find keywords are accepted if the keywords are elements
        in a list. In here the keywords are separated by spaces before and after
        the words like in '-f docker container cleanup'. Since the class parses
        the keyword list "as is", the keywords are not processed."""

        from snippy.config import Arguments

        find_kw = ['docker ', 'container ', 'cleanup']
        sys.argv = ['snippy', '-f', 'docker ', 'container ', 'cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_with_comma(self):
        """Test that find keywords are accepted if the keywords are elements in a
        list. In here the keywords are separated by commas after the words like
        in '-f docker, container, cleanup'. Since the class parses the keyword list
        "as is", the keywords are not processed."""

        from snippy.config import Arguments

        find_kw = ['docker,', 'container,', 'cleanup']
        sys.argv = ['snippy', '-f', 'docker,', 'container,', 'cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_with_space_inside_quotes(self):
        """Test that find keywords are accepted if the keywords are elements in a
        list. In here the keywords are separated by spaces before and after the
        words like in '-f 'docker container cleanup''. Since the class parses the
        keyword list "as is", the keywords are not processed."""

        from snippy.config import Arguments

        find_kw = ['docker container cleanup']
        sys.argv = ['snippy', '-f', 'docker container cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_with_comma_inside_quotes(self):
        """Test that find keywords are accepted if the keywords are elements in
        a list. In here the keywords are separated by commas after the words like
        in '-f 'docker, container, cleanup''. Since the class parses the keyword
        list "as is", the keywords are not processed."""

        from snippy.config import Arguments

        find_kw = ['docker, container, cleanup']
        sys.argv = ['snippy', '-f', 'docker, container, cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_with_list(self):
        """Test that find keywords are accepted if the keywords are elements in a
        list. This might not be realistic case since user might not be able to
        reproduce this."""

        from snippy.config import Arguments

        find_kw = ['docker', 'container', 'cleanup']
        sys.argv = ['snippy', '-f', 'docker', 'container', 'cleanup']
        obj = Arguments()
        assert obj.get_find() == find_kw

    def test_valid_find_kw_with_special_characters(self):
        """Test that find keywords are accepted if they contain special characters."""

        from snippy.config import Arguments

        find_kw = ['dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        sys.argv = ['snippy', '-f', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Arguments()
        assert obj.get_find() == find_kw

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
