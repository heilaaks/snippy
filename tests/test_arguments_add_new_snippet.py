#!/usr/bin/env python3

"""test_arguments_add_new_snippet.py: Test command line argumens for creating new snippet."""

import sys


class TestArgumentsAddNewSnippet(object):
    """Testing command line arguments for new snippet."""

    def test_no_value(self):
        """Test that new snippet can be added with comment but no tags."""

        from snippy.config import Arguments

        sys.argv = ["snippy"]
        obj = Arguments()
        assert obj.get_snippet() == ''
        assert obj.get_tags() == ''
        assert obj.get_comment() == ''

    def test_valid_value_no_tags(self):
        """Test that new snippet can be added without tags."""

        from snippy.config import Arguments

        command = "'docker rm $(docker ps -a -q)'"
        sys.argv = ["snippy", "-s", command]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == ''
        assert obj.get_comment() == ''

    def test_valid_value_one_tag(self):
        """Test that new snippet can be added with one tag."""

        from snippy.config import Arguments

        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker"
        sys.argv = ["snippy", "-s", command, "-t", tags]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == tags
        assert obj.get_comment() == ''

    def test_valid_value_with_tags(self):
        """Test that new snippet can be added with multiple tags."""

        from snippy.config import Arguments

        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, container, cleanup"
        sys.argv = ["snippy", "-s", command, "-t", tags]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == tags
        assert obj.get_comment() == ''

    def test_valid_value_with_tags_and_comment(self):
        """Test that new snippet can be added with multiple tags and comment."""

        from snippy.config import Arguments

        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, container, cleanup"
        comment = "Remove all docker containers"
        sys.argv = ["snippy", "-s", command, "-t", tags, "-c", comment]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == tags
        assert obj.get_comment() == comment

    def test_valid_value_with_comment_no_tags(self):
        """Test that new snippet can be added with comment but no tags."""

        from snippy.config import Arguments

        command = "'docker rm $(docker ps -a -q)'"
        comment = "Remove all docker containers"
        sys.argv = ["snippy", "-s", command, "-c", comment]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == ''
        assert obj.get_comment() == comment

    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        print('setup_class()')
        sys.argv = ["snippy"]

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        print('teardown_class()')
        sys.argv = ["snippy"]
