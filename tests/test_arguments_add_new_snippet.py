#!/usr/bin/env python3

"""test_arguments_add_new_snippet.py: Test command line argumens for creating new snippets."""

import sys
from snippy.config import Arguments
from tests.testlib.arguments_helper import ArgumentsHelper


class TestArgumentsAddNewSnippet(object):
    """Testing command line arguments for creating new snippets."""

    def test_no_arguments(self):
        """Test that default values are set when no arguments are used."""

        sys.argv = ['snippy']
        obj = Arguments()
        assert obj.get_snippet() == ''
        assert obj.get_resolve() == ''
        assert obj.get_brief() == ''
        assert obj.get_tags() == ''
        assert obj.get_links() == ''
        assert obj.get_find() == ''

    def test_add_snippet_without_optional_arguments(self):
        """Test that new snippet can be added without optional arguments."""

        snippet = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', '-s', snippet]
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == ''

    def test_add_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be added with brief description but
        no tags."""

        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        sys.argv = ['snippy', '-s', snippet, '-b', brief]
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == brief
        assert obj.get_tags() == ''

    def test_add_snippet_with_one_tag(self):
        """Test that new snippet can be added with a single tag."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker,container,cleanup']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker,container,cleanup']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_tags_with_quotes_and_separated_by_comma_and_space(self):
        """Test that tags can be added inside quotes separated by comma and
        spaces after comma."""

        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ['docker, container, cleanup']
        links = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
        sys.argv = ['snippy', '-s', snippet, '-b', brief, '-t', 'docker, container, cleanup', '-l', links]
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == brief
        assert obj.get_tags() == tags
        assert obj.get_links() == links

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker container cleanup']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker container cleanup']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker ', 'container ', 'cleanup']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker ', 'container ', 'cleanup']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker,', 'container,', 'cleanup']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker,', 'container,', 'cleanup']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        sys.argv = ['snippy', '-s', snippet, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        snippet = 'docker rm $(docker ps -a -q)'
        tags = ['docker', 'container', 'cleanup']
        sys.argv = ['snippy', '-s', snippet, '-t', 'docker', 'container', 'cleanup']
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == ''
        assert obj.get_tags() == tags

    def test_links_separated_by_space(self):
        """Test that multiple links can be added by separating them with
        space."""

        snippet = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ['docker, container, cleanup']
        links = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container \
                 https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
        sys.argv = ['snippy', '-s', snippet, '-b', brief, '-t', 'docker, container, cleanup', '-l', links]
        obj = Arguments()
        assert obj.get_snippet() == snippet
        assert obj.get_brief() == brief
        assert obj.get_tags() == tags
        assert obj.get_links() == links

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
