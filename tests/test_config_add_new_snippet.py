#!/usr/bin/env python3

"""test_config_add_new_snippet.py: Test tool configuration management new snippet."""

import sys


class TestConfigAddNewSnippet(object):
    """Testing configurationg management for new snippet."""

    def test_no_value(self):
        """Test that empty argument list is set to configuration."""

        from cuma.config import Config

        sys.argv = ["cuma"]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert len(obj.get_snippet()) == 0
        assert len(obj.get_tags()) == 0
        assert len(obj.get_comment()) == 0

    def test_valid_value_no_tags(self):
        """Test that new snippet can be configured without tags."""

        from cuma.config import Config

        command = "'docker rm $(docker ps -a -q)'"
        sys.argv = ["cuma", "-s", command]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert len(obj.get_tags()) == 0
        assert len(obj.get_comment()) == 0

    def test_valid_value_one_tag(self):
        """Test that new snippet can be configured with one tag and that the
        tag configuration is a list that can be iterated."""

        from cuma.config import Config

        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker"
        sys.argv = ["cuma", "-s", command, "-t", tags]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags.split(','))
        assert len(obj.get_tags()) == 1
        assert len(obj.get_comment()) == 0

    def test_valid_value_with_tags(self):
        """Test that new snippet can be configured with multiple tags and that the
        tag configuration is a list that can be iterated."""

        from cuma.config import Config

        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, image, cleanup"
        sys.argv = ["cuma", "-s", command, "-t", tags]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags.split(','))
        assert len(obj.get_tags()) == 3
        assert len(obj.get_comment()) == 0

    def test_valid_value_with_tags_and_comment(self):
        """Test that new snippet can be configured with multiple tags and comment and
        that the tag configuration is a list that can be iterated."""

        from cuma.config import Config

        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, image, cleanup"
        comment = "Remove docker container"
        sys.argv = ["cuma", "-s", command, "-t", tags, "-c", comment]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags.split(','))
        assert len(obj.get_tags()) == 3
        assert obj.get_comment() == comment

    def test_valid_value_with_comment_no_tags(self):
        """Test that new snippet can be added with comment but no tags."""

        from cuma.config import Config

        command = "'docker rm $(docker ps -a -q)'"
        comment = "Remove docker container"
        sys.argv = ["cuma", "-s", command, "-c", comment]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert len(obj.get_tags()) == 0
        assert obj.get_comment() == comment

    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        print('setup_class()')
        sys.argv = ["cuma"]

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""
        
        print('teardown_class()')
        sys.argv = ["cuma"]
