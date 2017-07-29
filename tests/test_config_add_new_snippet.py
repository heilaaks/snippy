#!/usr/bin/env python3

"""test_config_add_new_snippet.py: Test tool configuration management new snippet."""

import sys


class TestConfigAddNewSnippet(object):
    """Testing configurationg management for new snippet."""

    def test_no_value(self):
        """Test that empty argument list is set to configuration."""

        from snippy.config import Config

        sys.argv = ['snippy']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert not obj.get_snippet()
        assert not obj.get_tags()
        assert not obj.get_comment()

    def test_valid_value_no_tags(self):
        """Test that new snippet can be configured without tags."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', '-s', command]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert not obj.get_tags()
        assert not obj.get_comment()

    def test_valid_value_one_tag(self):
        """Test that new snippet can be configured with one tag and that the
        tag configuration is a list that can be iterated."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['docker']
        sys.argv = ['snippy', '-s', command, '-t', 'docker']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 1
        assert not obj.get_comment()

    def test_valid_value_with_tags(self):
        """Test that new snippet can be configured with multiple tags and that
        the tag configuration is a list that can be iterated. The tags are inside
        quotes without spaces."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ["snippy", "-s", command, "-t", 'docker,container,cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3
        assert not obj.get_comment()

    def test_valid_value_with_tags_and_comment(self):
        """Test that new snippet can be configured with multiple tags and comment
        and that the tag configuration is a list that can be iterated. The tags are
        inside quotes and separated with spaces."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        comment = 'Remove all docker containers'
        sys.argv = ['snippy', '-s', command, '-t', 'docker, container, cleanup', '-c', comment]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3
        assert obj.get_comment() == comment

    def test_valid_value_with_comment_no_tags(self):
        """Test that new snippet can be added with comment but no tags."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        comment = 'Remove all docker containers'
        sys.argv = ['snippy', '-s', command, '-c', comment]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert not obj.get_tags()
        assert obj.get_comment() == comment

    def test_valid_value_with_tags_with_space(self):
        """Test that tags are accepted if the tags are elements in a list.
        In here the tags are separated by spaces before and after the words
        like in '-t docker container cleanup'. The result should be proper
        sorted list of keywords."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', command, '-t', 'docker ', 'container ', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3

    def test_valid_value_with_tags_with_comma(self):
        """Test that tags are accepted if the tags are elements in a list.
        In here the tags are separated by commas after the words like in
        '-t docker, container, cleanup'. The result should be proper
        sorted list of keywords."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', command, '-t', 'docker,', 'container,', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3

    def test_valid_value_with_tags_with_space_inside_quotes(self):
        """Test that tags are accepted if the tags are elements in a list.
        In here the tags are separated by spaces before and after the words
        like in '-t 'docker container cleanup''. The result should be proper
        sorted list of keywords."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', command, '-t', 'docker container cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3

    def test_valid_value_with_tags_with_comma_inside_quotes(self):
        """Test that tags are accepted if the tags are elements in a list.
        In here the tags are separated by commas after the words like in
        '-t 'docker, container, cleanup''. The result should be proper
        sorted list of keywords."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', command, '-t', 'docker, container, cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3

    def test_valid_value_with_tags_with_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this."""

        from snippy.config import Config

        command = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', command, '-t', 'docker', 'container', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags)
        assert len(obj.get_tags()) == 3

    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        print('setup_class()')
        sys.argv = ['snippy']

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        print('teardown_class()')
        sys.argv = ['snippy']
