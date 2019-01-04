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

"""test_ut_cli: Test Cli() class."""

from collections import OrderedDict

from snippy.config.source.cli import Cli
from snippy.constants import Constants as Const


class TestUtCli(object):
    """Test Cli() class."""

    def test_cli_create_001(self):
        """Create new snippet.

        Test default values when only mandatory arguments are used.
        """

        cli = Cli(['snippy', 'create'])
        assert cli.brief == ''
        assert cli.category == Const.SNIPPET
        assert cli.data == ()
        assert not cli.debug
        assert not cli.defaults
        assert cli.description == ''
        assert cli.digest is None
        assert not cli.editor
        assert not cli.failure
        assert cli.filename == ''
        assert cli.groups == ('default',)
        assert cli.links == ()
        assert not cli.log_json
        assert cli.log_msg_max == Cli.DEFAULT_LOG_MSG_MAX
        assert not cli.merge
        assert cli.name == ''
        assert not cli.no_ansi
        assert cli.operation == 'create'
        assert not cli.profiler
        assert not cli.quiet
        assert cli.remove_fields == ()
        assert cli.sall == ()
        assert cli.scat == ('snippet',)
        assert cli.search_filter is None
        assert cli.search_limit == Cli.LIMIT_DEFAULT_CLI
        assert cli.search_offset == 0
        assert cli.server_app_base_path == '/snippy/api/app/v1/'
        assert cli.server_host == ''
        assert not cli.server_minify_json
        assert cli.server_ssl_ca_cert is None
        assert cli.server_ssl_cert is None
        assert cli.server_ssl_key is None
        assert cli.sgrp == ()
        assert cli.sort_fields == OrderedDict([('brief', 'ASC')])
        assert cli.source == ''
        assert cli.stag == ()
        assert cli.storage_path == ''
        assert cli.tags == ()
        assert not cli.template
        assert cli.uuid is None
        assert cli.version is None  # Tool version
        assert cli.versions == ''   # Content versions
        assert not cli.very_verbose

    def test_cli_create_002(self):
        """Test that new snippet can be created without optional arguments."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ()

    def test_cli_create_003(self):
        """Test that new snippet can be created with brief description but
        no tags."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        obj = Cli(['snippy', 'create', '-c', content, '-b', brief])
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.tags == ()

    def test_cli_create_004(self):
        """Test that new snippet can be created with a single tag."""

        content = 'docker rm $(docker ps -a -q)'
        tags = ['docker']
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == tuple(tags,)

    def test_cli_create_005(self):
        """Test that tags can be added inside quotes separated by comma and
        without spaces."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker,container,cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_cli_create_006(self):
        """Test that tags can be added inside quotes separated by comma and
        spaces after comma."""

        content = 'docker rm $(docker ps -a -q)'
        brief = 'Remove all docker containers'
        groups = 'docker'
        tags = 'docker, container, cleanup'
        links = 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
        obj = Cli(['snippy', 'create', '-c', content, '-b', brief, '-g', groups, '-t', tags, '-l', links])
        assert obj.data == (content,)
        assert obj.brief == brief
        assert obj.groups == (groups,)
        assert obj.tags == ('cleanup', 'container', 'docker')
        assert obj.links == (links,)

    def test_cli_create_007(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker container cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_cli_create_008(self):
        """Test that tags can be added so that they are separated by spaces
        before and after the words like in '-t docker container cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker ', 'container ', 'cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_cli_create_009(self):
        """Test that tags can be added so that they are separated by comma
        after the words like in '-t docker, container, cleanup'."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker,', 'container,', 'cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_cli_create_010(self):
        """Test that tags are accepted if they contain special characters."""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker–testing, ', 'container-managemenet, ', 'cleanup_testing'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == (u'cleanup_testing', u'container-managemenet', u'docker–testing')

    def test_cli_create_011(self):
        """Test that tags are accepted if the tags are elements in a list.
        This might not be realistic case since user might not be able to
        reproduce this?"""

        content = 'docker rm $(docker ps -a -q)'
        obj = Cli(['snippy', 'create', '-c', content, '-t', 'docker', 'container', 'cleanup'])
        assert obj.data == (content,)
        assert obj.brief == ''
        assert obj.tags == ('cleanup', 'container', 'docker')

    def test_cli_create_012(self):
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

    def test_cli_search_001(self):
        """Test that search can be used with one keyword."""

        obj = Cli(['snippy', 'search', '--sall', 'docker'])
        assert obj.sall == ('docker',)

    def test_cli_search_002(self):
        """Test that keywords can be added inside quotes separated by
        comma and without spaces."""

        obj = Cli(['snippy', 'search', '--sall', 'docker,container,cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_cli_search_003(self):
        """Test that search keywords can be added inside quotes separated
        by comma and spaces after comma."""

        obj = Cli(['snippy', 'search', '--sall', 'docker, container, cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_cli_search_004(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words."""

        obj = Cli(['snippy', 'search', '--sall', 'docker container cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_cli_search_005(self):
        """Test that search keywords can be added so that they are separated
        by spaces before and after the words like in '-t docker container
        cleanup'."""

        obj = Cli(['snippy', 'search', '--sall', 'docker ', 'container ', 'cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_cli_search_006(self):
        """Test that search keywords can be added so that they are separated
        by comma after the words like in '-t docker, container, cleanup'."""

        obj = Cli(['snippy', 'search', '--sall', 'docker,', 'container,', 'cleanup'])
        assert obj.sall == ('cleanup', 'container', 'docker')

    def test_cli_search_007(self):
        """Test that search keywords are accepted if they contain special
        characters."""

        obj = Cli(['snippy', 'search', '--sall', 'docker–testing, ', 'container-managemenet, ', 'cleanup_testing'])
        assert obj.sall == (u'cleanup_testing', u'container-managemenet', u'docker–testing')
