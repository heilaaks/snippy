#!/usr/bin/env python3

"""test_ut_arguments_create.py: Test command line argumens for creating new snippets."""

from __future__ import print_function
import sys
from snippy.config.constants import Constants as Const
from snippy.config.source.cli import Cli
from tests.testlib.cli_helper import CliHelper


class TestUtCliCreate(object):
    """Testing command line arguments for creating snippets."""

    def test_no_arguments(self):
        """Test default values when only mandatory arguments are used."""

        sys.argv = ['snippy', 'create']
        obj = Cli()
        assert obj.operation == 'create'
        assert obj.category == Const.SNIPPET
        assert obj.data == ()
        assert obj.brief == ''
        assert obj.tags == ()
        assert obj.links == ()
        assert obj.digest is None
        assert obj.sall == ()
        assert obj.stag == ()
        assert obj.sgrp == ()
        assert obj.regexp == ''
        assert not obj.editor
        assert obj.filename == ''
        assert not obj.no_ansi
        assert not obj.defaults
        assert not obj.template

    def test_create_snippet_without_optional_arguments(self):
        """Test that new snippet can be created without optional arguments."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content]
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ()

    def test_create_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        sys.argv = ['snippy', 'create', '-c', content, '-b', brief]
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.tags == ()

    def test_create_snippet_with_one_tag(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ['docker']
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == tuple(tags,)

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_with_quotes_and_separated_by_comma_and_space(self):
        """Test that tags can be added inside quotes separated by comma and
        spaces after comma."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        group = 'docker'
        tags = 'docker, container, cleanup'
        links = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
        sys.argv = ['snippy', 'create', '-c', content, '-b', brief, '-g', group, '-t', tags, '-l', links]
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.group == group
        assert obj.tags == ('cleanup', 'container', 'docker')
        assert obj.links == (links,)

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker container cleanup']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup_testing', 'container-managemenet', 'dockertesting')

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup']
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_links_separated_by_space(self):
        """Test that multiple links can be added by separating them with
        space."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = 'docker, container, cleanup'
        links = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container \
                 https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
        sys.argv = ['snippy', 'create', '-c', content, '-b', brief, '-t', tags, '-l', links]
        obj = Cli()
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.tags == ('cleanup', 'container', 'docker')
        print(obj.links)
        assert obj.links == tuple(links.split())

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
