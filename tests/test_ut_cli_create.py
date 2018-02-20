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

"""test_ut_arguments_create.py: Test command line argumens for creating new snippets."""

from __future__ import print_function

from snippy.config.constants import Constants as Const
from snippy.config.source.cli import Cli
from tests.testlib.cli_helper import CliHelper


class TestUtCliCreate(object):
    """Testing command line arguments for creating snippets."""

    def test_no_arguments(self):
        """Test default values when only mandatory arguments are used."""

        obj = Cli(['snippy', 'create'])
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
        obj = Cli(['snippy', 'create', '-c', content])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ()

    def test_create_snippet_with_brief_but_no_tags(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        obj = Cli(['snippy', 'create', '-c', content, '-b', brief])
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.tags == ()

    def test_create_snippet_with_one_tag(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ['docker']
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == tuple(tags,)

    def test_tags_with_quotes_and_separated_by_comma_and_no_space(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup'])
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
        obj = Cli(['snippy', 'create', '-c', content, '-b', brief, '-g', group, '-t', tags, '-l', links])
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.group == group
        assert obj.tags == ('cleanup', 'container', 'docker')
        assert obj.links == (links,)

    def test_tags_with_quotes_and_separated_by_only_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker container cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_separated_by_space(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_separated_by_space_and_comma(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_tags_with_special_characters(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'dockertesting, ', 'container-managemenet, ', 'cleanup_testing'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup_testing', 'container-managemenet', 'dockertesting')

    def test_tags_provided_in_list(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup'])
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
        obj = Cli(['snippy', 'create', '-c', content, '-b', brief, '-t', tags, '-l', links])
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.tags == ('cleanup', 'container', 'docker')
        assert obj.links == tuple(links.split())

    # pylint: disable=duplicate-code
    @classmethod
    def setup_class(cls):
        """Setup class."""

        CliHelper().reset()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        CliHelper().reset()
