#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""test_ut_config_create.py: Test tool configuration management for creating new snippets."""

from __future__ import print_function
import sys
import unittest
from snippy.config.constants import Constants as Const
from snippy.config.config import Config
from snippy.config.source.cli import Cli
from snippy.content.content import Content
from tests.testlib.cli_helper import CliHelper


class TestUtConfigCreate(unittest.TestCase):
    """Testing configurationg management for creating snippets."""

    def test_no_arguments(self):
        """Test that empty argument list is set to configuration."""

        snippet = ((), '', Const.DEFAULT_GROUP, (), (), Const.SNIPPET, '', '', '', None, None, None, None)
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create']))
        assert isinstance(obj.content_category, str)
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_group, str)
        assert isinstance(obj.content_tags, tuple)
        assert isinstance(obj.content_links, tuple)
        assert isinstance(obj.content_filename, str)
        assert isinstance(obj.operation_digest, type(None))
        assert isinstance(obj.search_all_kws, tuple)
        assert isinstance(obj.search_tag_kws, tuple)
        assert isinstance(obj.search_grp_kws, tuple)
        assert isinstance(obj.search_filter, str)
        assert isinstance(obj.get_operation_file(), str)
        assert obj.get_contents(Content(category=Const.SNIPPET))[0].get() == snippet
        assert obj.is_operation_create
        assert not obj.is_operation_search
        assert not obj.is_operation_update
        assert not obj.is_operation_delete
        assert not obj.is_operation_export
        assert not obj.is_operation_import
        assert obj.is_category_snippet
        assert not obj.is_category_solution
        assert not obj.is_category_all
        assert obj.content_category == Const.SNIPPET
        assert not obj.content_data
        assert not obj.content_brief
        assert obj.content_group == Const.DEFAULT_GROUP
        assert not obj.content_tags
        assert not obj.content_links
        assert not obj.search_all_kws
        assert not obj.search_tag_kws
        assert not obj.search_grp_kws
        assert obj.operation_digest is None
        assert not obj.search_filter
        assert not obj.content_filename
        assert not obj.editor
        assert obj.get_operation_file() == './snippets.yaml'
        assert obj.is_operation_file_yaml
        assert not obj.is_operation_file_json
        assert not obj.is_operation_file_text
        assert obj.use_ansi

    def test_create_snippet_without_optional_arguments(self):
        """Test that new snippet can be created without optional arguments."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content]))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        assert not obj.content_brief
        assert not obj.content_tags

    def test_create_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-b', brief]))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        assert obj.content_brief == brief
        assert not obj.content_tags

    def test_create_snippet_with_one_tag(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('docker',)
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'docker']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        assert not obj.content_brief
        self.assertTupleEqual(obj.content_tags, tags)

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        assert not obj.content_brief
        self.assertTupleEqual(obj.content_tags, tags)

    def test_tags_with_quotes_and_separated_by_comma_and_space(self):
        """Test that tags can be added inside quotes separated by comma and
        space after comma."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        group = 'docker'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',)
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-b', brief, '-g', group, '-t', 'docker, container, cleanup',
                             '-l', links[0]]))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_group, str)
        assert isinstance(obj.content_tags, tuple)
        assert isinstance(obj.content_links, tuple)
        assert obj.content_data == tuple([content])
        assert obj.content_brief == brief
        assert obj.content_group == group
        self.assertTupleEqual(obj.content_tags, tags)
        self.assertTupleEqual(obj.content_links, links)

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'docker container cleanup']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        self.assertTupleEqual(obj.content_tags, tags)

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        self.assertTupleEqual(obj.content_tags, tags)

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        self.assertTupleEqual(obj.content_tags, tags)

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup_testing', 'container-managemenet', 'dockertesting')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        self.assertTupleEqual(obj.content_tags, tags)
        assert len(obj.content_tags) == 3

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup']))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert obj.content_data == tuple([content])
        self.assertTupleEqual(obj.content_tags, tags)

    def test_links_separated_by_space(self):
        """Test that multiple links can be added by separating them with
        space."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-b', brief, '-t', 'docker, container, cleanup', '-l', ' '.join(links)]))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert isinstance(obj.content_links, tuple)
        assert obj.content_data == tuple([content])
        assert obj.content_brief == brief
        self.assertTupleEqual(obj.content_tags, tags)
        self.assertTupleEqual(obj.content_links, links)

    def test_links_separated_by_bar(self):
        """Test that multiple links can be added by separating them with
        bar."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
        obj = Config(None)
        obj.read_source(Cli(['snippy', 'create', '-c', content, '-b', brief, '-t', 'docker, container, cleanup', '-l', '|'.join(links)]))
        assert isinstance(obj.content_data, tuple)
        assert isinstance(obj.content_brief, str)
        assert isinstance(obj.content_tags, tuple)
        assert isinstance(obj.content_links, tuple)
        assert obj.content_data == tuple([content])
        assert obj.content_brief == brief
        self.assertTupleEqual(obj.content_tags, tags)
        self.assertTupleEqual(obj.content_links, links)

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
