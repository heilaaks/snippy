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

import unittest

import mock

from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.config.source.cli import Cli


class TestUtConfigCreate(unittest.TestCase):
    """Testing configurationg management for creating snippets."""

    @mock.patch.object(Config, 'utcnow')
    def test_no_arguments(self, mock_utcnow):
        """Test that empty argument list is set to configuration."""

        mock_utcnow.return_value = '2018-02-17 13:23:43'

        resource = {
            'data': (),
            'brief': '',
            'group': 'default',
            'tags': (),
            'links': (),
            'category': 'snippet',
            'filename': '',
            'runalias': '',
            'versions': '',
            'created': '2018-02-17 13:23:43',
            'updated': '2018-02-17 13:23:43',
            'digest': 'b4bedc2603e3b9ea95bcf53cb7b8aa6efa31eabb788eed60fccf3d8029a6a6cc'}
        Config.init(None)
        Config.load(Cli(['snippy', 'create']))
        assert isinstance(Config.content_category, str)
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_group, str)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert isinstance(Config.content_filename, str)
        assert isinstance(Config.operation_digest, type(None))
        assert isinstance(Config.search_all_kws, tuple)
        assert isinstance(Config.search_tag_kws, tuple)
        assert isinstance(Config.search_grp_kws, tuple)
        assert isinstance(Config.search_filter, str)
        assert isinstance(Config.get_operation_file(), str)
        assert Config.get_resource().dump_dict([]), resource
        assert next(Config.get_collection().resources()).dump_dict([]), resource
        assert Config.is_operation_create
        assert not Config.is_operation_search
        assert not Config.is_operation_update
        assert not Config.is_operation_delete
        assert not Config.is_operation_export
        assert not Config.is_operation_import
        assert Config.is_category_snippet
        assert not Config.is_category_solution
        assert not Config.is_category_all
        assert Config.content_category == Const.SNIPPET
        assert not Config.content_data
        assert not Config.content_brief
        assert Config.content_group == Const.DEFAULT_GROUP
        assert not Config.content_tags
        assert not Config.content_links
        assert not Config.search_all_kws
        assert not Config.search_tag_kws
        assert not Config.search_grp_kws
        assert Config.operation_digest is None
        assert not Config.search_filter
        assert not Config.content_filename
        assert not Config.editor
        assert Config.get_operation_file() == './snippets.yaml'
        assert Config.is_operation_file_yaml
        assert not Config.is_operation_file_json
        assert not Config.is_operation_file_text
        assert Config.use_ansi

    def test_create_snippet_without_optional_arguments(self):
        """Test that new snippet can be created without optional arguments."""

        content = 'docker rm $(docker ps -a -q)'
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert not Config.content_brief
        assert not Config.content_tags

    def test_create_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-b', brief]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        assert not Config.content_tags

    def test_create_snippet_with_one_tag(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('docker',)
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert not Config.content_brief
        self.assertTupleEqual(Config.content_tags, tags)

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert not Config.content_brief
        self.assertTupleEqual(Config.content_tags, tags)

    def test_tags_with_quotes_and_separated_by_comma_and_space(self):
        """Test that tags can be added inside quotes separated by comma and
        space after comma."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        group = 'docker'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',)
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-b', brief, '-g', group, '-t', 'docker, container, cleanup',
                         '-l', links[0]]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_group, str)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        assert Config.content_group == group
        self.assertTupleEqual(Config.content_tags, tags)
        self.assertTupleEqual(Config.content_links, links)

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker container cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        self.assertTupleEqual(Config.content_tags, tags)

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        self.assertTupleEqual(Config.content_tags, tags)

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        self.assertTupleEqual(Config.content_tags, tags)

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup_testing', 'container-managemenet', 'dockertesting')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        self.assertTupleEqual(Config.content_tags, tags)
        assert len(Config.content_tags) == 3

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        self.assertTupleEqual(Config.content_tags, tags)

    def test_links_separated_by_space(self):
        """Test that multiple links can be added by separating them with
        space."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-b', brief, '-t', 'docker, container, cleanup', '-l', ' '.join(links)]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        self.assertTupleEqual(Config.content_tags, tags)
        self.assertTupleEqual(Config.content_links, links)

    def test_links_separated_by_bar(self):
        """Test that multiple links can be added by separating them with
        bar."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',
                 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-b', brief, '-t', 'docker, container, cleanup', '-l', '|'.join(links)]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, str)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        self.assertTupleEqual(Config.content_tags, tags)
        self.assertTupleEqual(Config.content_links, links)

    # pylint: disable=duplicate-code
    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        Config.init(None)

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        Config.init(None)
