#!/usr/bin/env python3

"""test_config_add_new_snippet.py: Test tool configuration management for new snippets."""

import sys
import unittest
from snippy.config import Config
from tests.testlib.arguments_helper import ArgumentsHelper


class TestConfigAddNewSnippet(unittest.TestCase):
    """Testing configurationg management for new snippets."""

    def test_no_arguments(self):
        """Test that empty argument list is set to configuration."""

        sys.argv = ['snippy']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_resolve(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_links(), list)
        assert isinstance(obj.get_find_keywords(), list)
        assert not obj.get_snippet()
        assert not obj.get_resolve()
        assert not obj.get_brief()
        assert not obj.get_tags()
        assert not obj.get_links()
        assert not obj.get_find_keywords()

    def test_add_snippet_without_optional_arguments(self):
        """Test that new snippet can be added without optional arguments."""

        snippet = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', '-s', snippet]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        assert not obj.get_brief()
        assert not obj.get_tags()

    def test_add_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be added with brief description but
        no tags."""

        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        sys.argv = ['snippy', '-s', snippet, '-b', brief]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == brief
        assert not obj.get_tags()

    def test_add_snippet_with_one_tag(self):
        """Test that new snippet can be added with a single tag."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        assert not obj.get_brief()
        self.assertCountEqual(obj.get_tags(), tags)

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ["snippy", "-s", snippet, "-t", 'docker,container,cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        assert not obj.get_brief()
        self.assertCountEqual(obj.get_tags(), tags)

    def test_tags_with_quotes_and_separated_by_comma_and_space(self):
        """Test that tags can be added inside quotes separated by comma and
        space after comma."""

        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ['cleanup', 'container', 'docker']
        links = ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container']
        sys.argv = ['snippy', '-s', snippet, '-b', brief, '-t', 'docker, container, cleanup', '-l', links[0]]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_links(), list)
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == brief
        self.assertCountEqual(obj.get_tags(), tags)
        self.assertCountEqual(obj.get_links(), links)

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker container cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        self.assertCountEqual(obj.get_tags(), tags)

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker ', 'container ', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        self.assertCountEqual(obj.get_tags(), tags)

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker,', 'container,', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        self.assertCountEqual(obj.get_tags(), tags)

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup_testing', 'container-managemenet', 'dockertesting']
        sys.argv = ['snippy', '-s', snippet, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        self.assertCountEqual(obj.get_tags(), tags)
        assert len(obj.get_tags()) == 3

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['cleanup', 'container', 'docker']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker', 'container', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert obj.get_snippet() == snippet
        self.assertCountEqual(obj.get_tags(), tags)

    def test_links_separated_by_space(self):
        """Test that multiple links can be added by separating them with
        space."""

        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ['cleanup', 'container', 'docker']
        links = ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes']
        sys.argv = ['snippy', '-s', snippet, '-b', brief, '-t', 'docker, container, cleanup', '-l', ' '.join(links)]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_brief(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_links(), list)
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == brief
        self.assertCountEqual(obj.get_tags(), tags)
        self.assertCountEqual(obj.get_links(), links)

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
