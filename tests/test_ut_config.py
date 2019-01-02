#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_ut_config: Test Config() class."""

from collections import OrderedDict

import mock

from snippy.config.config import Config
from snippy.config.source.cli import Cli
from snippy.constants import Constants as Const


class TestUtConfig(object):  # pylint: disable=too-many-public-methods
    """Test Config() class."""

    @mock.patch.object(Config, 'utcnow')
    def test_config_create_001(self, mock_utcnow):
        """Create new snippet.

        Test default values when only mandatory arguments are used.
        """

        mock_utcnow.return_value = '2018-02-17 13:23:43'

        Config.init(None)
        Config.load(Cli(['snippy', 'create']))
        assert isinstance(Config.content_category, str)
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_description, Const.TEXT_TYPE)
        assert isinstance(Config.content_groups, tuple)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert isinstance(Config.content_name, Const.TEXT_TYPE)
        assert isinstance(Config.content_filename, Const.TEXT_TYPE)
        assert isinstance(Config.content_versions, Const.TEXT_TYPE)
        assert isinstance(Config.content_source, Const.TEXT_TYPE)
        assert isinstance(Config.operation_digest, type(None))
        assert isinstance(Config.search_cat_kws, tuple)
        assert isinstance(Config.search_all_kws, tuple)
        assert isinstance(Config.search_tag_kws, tuple)
        assert isinstance(Config.search_grp_kws, tuple)
        assert Config.search_filter is None
        assert Config.search_limit == 99
        assert Config.search_offset == 0
        assert Config.remove_fields == ()
        assert Config.sort_fields == OrderedDict([('brief', 'ASC')])
        assert isinstance(Config.get_operation_file(), str)
        assert not Config.get_resource(None)
        assert not Config.get_collection()
        assert Config.is_operation_create
        assert not Config.is_operation_search
        assert not Config.is_operation_update
        assert not Config.is_operation_delete
        assert not Config.is_operation_export
        assert not Config.is_operation_import
        assert Config.is_category_snippet
        assert not Config.is_category_solution
        assert not Config.is_category_reference
        assert not Config.is_category_all
        assert Config.content_category == Const.SNIPPET
        assert not Config.content_data
        assert not Config.content_brief
        assert Config.content_groups == Const.DEFAULT_GROUPS
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

    def test_config_create_002(self):
        """Test that new snippet can be created without optional arguments."""

        content = 'docker rm $(docker ps -a -q)'
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert not Config.content_brief
        assert not Config.content_tags

    def test_config_create_003(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-b', brief]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        assert not Config.content_tags

    def test_config_create_004(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('docker',)
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert not Config.content_brief
        assert Config.content_tags == tags

    def test_config_create_005(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert not Config.content_brief
        assert Config.content_tags == tags

    def test_config_create_006(self):
        """Test that tags can be added inside quotes separated by comma and
        space after comma."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker')
        links = ('https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container',)
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-b', brief, '-g', 'docker', '-t', 'docker, container, cleanup',
                         '-l', links[0]]))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_groups, tuple)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        assert Config.content_groups == groups
        assert Config.content_tags == tags
        assert Config.content_links == links

    def test_config_create_007(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker container cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_tags == tags

    def test_config_create_008(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_tags == tags

    def test_config_create_009(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_tags == tags

    def test_config_create_010(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        tags = (u'cleanup_testing', u'container-managemenet', u'docker–testing')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker–testing, ', 'container-managemenet, ', 'cleanup_testing']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_tags == tags
        assert len(Config.content_tags) == 3

    def test_config_create_011(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        tags = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup']))
        assert isinstance(Config.content_data, tuple)
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_tags == tags

    def test_config_create_012(self):
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
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        assert Config.content_tags == tags
        assert Config.content_links == links

    def test_config_create_013(self):
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
        assert isinstance(Config.content_brief, Const.TEXT_TYPE)
        assert isinstance(Config.content_tags, tuple)
        assert isinstance(Config.content_links, tuple)
        assert Config.content_data == tuple([content])
        assert Config.content_brief == brief
        assert Config.content_tags == tags
        assert Config.content_links == links

    def test_config_search_001(self):
        """Test that search can be used with one keyword."""

        search_kw = ('docker',)
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw

    def test_config_search_002(self):
        """Test that search keywords can be added inside quotes separated by
        comma and without spaces."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker,container,cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw

    def test_config_search_003(self):
        """Test that search keywords can be added inside quotes separated by
        comma and spaces after comma."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker, container, cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw

    def test_config_search_004(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker, container, cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw

    def test_config_search_005(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker ', 'container ', 'cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw

    def test_config_search_006(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        search_kw = ('cleanup', 'container', 'docker')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker,', 'container,', 'cleanup']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw

    def test_config_search_007(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        search_kw = (u'cleanup_testing', u'container-managemenet', u'docker–testing')
        Config.init(None)
        Config.load(Cli(['snippy', 'search', '--sall', 'docker–testing, ', 'container-managemenet, ', 'cleanup_testing']))
        assert isinstance(Config.search_all_kws, tuple)
        assert Config.search_all_kws == search_kw
        assert len(Config.search_all_kws) == 3

    @classmethod
    def setup_class(cls):
        """Test class setup before any of the tests are run."""

        Config.init(None)

    @classmethod
    def teardown_class(cls):
        """Test class teardown after all tests run."""

        Config.init(None)
