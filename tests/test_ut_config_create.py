#!/usr/bin/env python3

"""test_ut_config_create.py: Test tool configuration management for creating new snippets."""

from __future__ import print_function
import sys
import unittest
from snippy.config.constants import Constants as Const
from snippy.config.config import Config
from snippy.content.content import Content
from tests.testlib.arguments_helper import ArgumentsHelper


class TestUtConfigCreate(unittest.TestCase):
    """Testing configurationg management for creating snippets."""

    def test_no_arguments(self):
        """Test that empty argument list is set to configuration."""

        sys.argv = ['snippy', 'create']
        snippet = ((), '', Const.DEFAULT_GROUP, (), (), Const.SNIPPET, '', None, None, None, None)
        obj = Config()
        assert isinstance(obj.get_category(), str)
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_group(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert isinstance(obj.get_content_links(), tuple)
        assert isinstance(obj.get_content_digest(), str)
        assert isinstance(obj.get_filename(), str)
        assert isinstance(obj.get_search_keywords(), tuple)
        assert isinstance(obj.get_search_filter(), str)
        assert isinstance(obj.get_operation_file(), str)
        assert obj.get_content(Content()).get() == snippet
        assert obj.is_operation_create()
        assert not obj.is_operation_search()
        assert not obj.is_operation_update()
        assert not obj.is_operation_delete()
        assert not obj.is_operation_export()
        assert not obj.is_operation_import()
        assert obj.is_category_snippet()
        assert not obj.is_category_solution()
        assert not obj.is_category_all()
        assert obj.get_category() == Const.SNIPPET
        assert not obj.get_content_data()
        assert not obj.get_content_brief()
        assert obj.get_content_group() == Const.DEFAULT_GROUP
        assert not obj.get_content_tags()
        assert not obj.get_content_links()
        assert not obj.get_search_keywords()
        assert not obj.get_search_filter()
        assert not obj.get_content_digest()
        assert not obj.get_filename()
        assert not obj.is_editor()
        assert not obj.is_file_type_yaml()
        assert not obj.is_file_type_json()
        assert not obj.is_file_type_text()
        assert obj.use_ansi()

    def test_create_snippet_without_optional_arguments(self):
        """Test that new snippet can be created without optional arguments."""

        content = 'docker rm $(docker ps -a -q)'
        sys.argv = ['snippy', 'create', '-c', content]
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        assert not obj.get_content_brief()
        assert not obj.get_content_tags()

    def test_create_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        sys.argv = ['snippy', 'create', '-c', content, '-b', brief]
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        assert obj.get_content_brief() == brief
        assert not obj.get_content_tags()

    def test_create_snippet_with_one_tag(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('docker',)
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        assert not obj.get_content_brief()
        self.assertTupleEqual(obj.get_content_tags(), tags)

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        assert not obj.get_content_brief()
        self.assertTupleEqual(obj.get_content_tags(), tags)

    def test_tags_with_quotes_and_separated_by_comma_and_space(self):
        """Test that tags can be added inside quotes separated by comma and
        space after comma."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        group = 'docker'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',)
        sys.argv = ['snippy', 'create', '-c', content, '-b', brief, '-g', group, '-t', 'docker, container, cleanup',
                    '-l', links[0]]
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_group(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert isinstance(obj.get_content_links(), tuple)
        assert obj.get_content_data() == tuple([content])
        assert obj.get_content_brief() == brief
        assert obj.get_content_group() == group
        self.assertTupleEqual(obj.get_content_tags(), tags)
        self.assertTupleEqual(obj.get_content_links(), links)

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker container cleanup']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        self.assertTupleEqual(obj.get_content_tags(), tags)

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        self.assertTupleEqual(obj.get_content_tags(), tags)

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        self.assertTupleEqual(obj.get_content_tags(), tags)

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup_testing', 'container-managemenet', 'dockertesting')
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        self.assertTupleEqual(obj.get_content_tags(), tags)
        assert len(obj.get_content_tags()) == 3

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        sys.argv = ['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup']
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert obj.get_content_data() == tuple([content])
        self.assertTupleEqual(obj.get_content_tags(), tags)

    def test_links_separated_by_space(self):
        """Test that multiple links can be added by separating them with
        space."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
        sys.argv = ['snippy', 'create', '-c', content, '-b', brief, '-t', 'docker, container, cleanup', '-l', ' '.join(links)]
        obj = Config()
        assert isinstance(obj.get_content_data(), tuple)
        assert isinstance(obj.get_content_brief(), str)
        assert isinstance(obj.get_content_tags(), tuple)
        assert isinstance(obj.get_content_links(), tuple)
        assert obj.get_content_data() == tuple([content])
        assert obj.get_content_brief() == brief
        self.assertTupleEqual(obj.get_content_tags(), tags)
        self.assertTupleEqual(obj.get_content_links(), links)

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
