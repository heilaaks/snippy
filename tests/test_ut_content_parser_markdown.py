#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""test_ut_parser: Test ContentParserMarkdown() class."""

from snippy.constants import Constants as Const
from snippy.config.source.parsers.markdown import ContentParserMarkdown as Parser


class TestUtContentParserMarkdown(object):
    """Test ContentParserMarkdown() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+0000'

    def test_parser_snippet_001(self):
        """Test parsing snippet.

        Test case verifies that standard snippet is parsed correctly from
        Markdown template.
        """

        text = '\n'.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> \[1\]: `https://docs.docker.com/engine/reference/commandline/images/`  ',
            '\[2\]: `https://docs.docker.com/engine/reference/commandline/rm/`',
            '',
            '- Remove all exited containers',
            '',
            '    `$ docker rm $(docker ps --all -q -f status=exited)`',
            '',
            '- Remove all dangling images',
            '',
            '    `$ docker images -q --filter dangling=true | xargs docker rmi`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited) # Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi # Remove all dangling images'
        )
        brief = 'Remove docker image with force'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        #assert resource.brief == brief
        #assert resource.groups == groups
        #assert resource.description == description
        #assert resource.tags == tags
        #assert resource.links == links
        #assert resource.uuid == uuid
        #assert resource.digest == digest

    def test_parser_snippet_002(self):
        """Test parsing two snippets.

        Test case verifies that standard snippets are parsed correctly from
        Markdown template. In this case the first snippet contains commands
        with headers which are missing from the second snippet.
        """

        text = '\n'.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> \[1\]: `https://docs.docker.com/engine/reference/commandline/images/`  ',
            '\[2\]: `https://docs.docker.com/engine/reference/commandline/rm/`',
            '',
            '- Remove all exited containers',
            '',
            '    `$ docker rm $(docker ps --all -q -f status=exited)`',
            '',
            '- Remove all dangling images',
            '',
            '    `$ docker images -q --filter dangling=true | xargs docker rmi`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
            '---',
            '',
            '# Solve docker networking \'has active endpoints\' problem @docker',
            '',
            '> Fix docker problem that results \'has active endpoints\' error log.',
            '',
            '> \[1\]: `https://github.com/moby/moby/issues/23302`',
            '',
            '`$ docker network ls`',
            '`$ docker network inspect y0fdm2xoyuca`',
            '`$ docker network disconnect -f y0fdm2xoyuca devstack_logstash.1.7iqgrfd2xwcidj87zbkmauw4l`',
            '`$ docker network rm y0fdm2xoyuca`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 6dc4b06991780012f02f89d2490e6a51b5ef83723a23da2b0aa697355e4f876c  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : container, docker, docker-ce, moby, network, remove, solution, swarm  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c752e-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            'docker network rm y0fdm2xoyuca'
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited) # Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi # Remove all dangling images'
        )
        brief = 'Remove docker image with force'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.size() == 2
        resource = collection[list(collection.keys())[0]]['data']
        assert resource.category == Const.SNIPPET
        assert resource.data == data

        data = (
            'docker network ls',
            'docker network inspect y0fdm2xoyuca',
            'docker network disconnect -f y0fdm2xoyuca devstack_logstash.1.7iqgrfd2xwcidj87zbkmauw4l',
            'docker network rm y0fdm2xoyuca'
        )
        brief = 'Remove docker image with force'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        resource = collection[list(collection.keys())[1]]['data']
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        #assert resource.brief == brief
        #assert resource.groups == groups
        #assert resource.description == description
        #assert resource.tags == tags
        #assert resource.links == links
        #assert resource.uuid == uuid
        #assert resource.digest == digest

    def test_parser_solution_001(self):
        """Test parsing solution.

        Test case verifies that standard solution is parsed correctly from
        Markdown template. In this case the template is fully in Markdown
        format. This causes the solution data field to be just like the input
        Markdown text.
        """

        text = '\n'.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> \[1\]: `https://docs.docker.com/engine/reference/commandline/images/`  ',
            '\[2\]: `https://docs.docker.com/engine/reference/commandline/rm/`',
            '',
            '- Remove all exited containers',
            '',
            '    `$ docker rm $(docker ps --all -q -f status=exited)`',
            '',
            '- Remove all dangling images',
            '',
            '    `$ docker images -q --filter dangling=true | xargs docker rmi`',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Remove docker image with force'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        #assert resource.brief == brief
        #assert resource.groups == groups
        #assert resource.description == description
        #assert resource.tags == tags
        #assert resource.links == links
        #assert resource.uuid == uuid
        #assert resource.digest == digest

    def test_parser_solution_002(self):
        """Test parsing solution.

        Test case verifies that standard solution is parsed correctly from
        Markdown template. In this case the input is based on text formatted
        template. In this case there are no optional links used.
        """

        text = '\n'.join((
            '# Testing docker log drivers @docker',
            '',
            '> An email client and Usenet newsgroup program with a pico/nano-inspired interface.  ',
            'Supports most modern email services through IMAP.',
            '',
            '    ################################################################################',
            '    ## BRIEF  : Testing docker log drivers',
            '    ##',
            '    ## GROUPS : docker',
            '    ## TAGS   : cleanup, container, docker, docker-ce, moby',
            '    ## FILE   : docker-example.txt',
            '    ################################################################################',
            '',
            '    ################################################################################',
            '    ## description',
            '    ################################################################################',
            '',
            '# Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Remove docker image with force'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        #assert resource.brief == brief
        #assert resource.groups == groups
        #assert resource.description == description
        #assert resource.tags == tags
        #assert resource.links == links
        #assert resource.uuid == uuid
        #assert resource.digest == digest

    def test_parser_reference_001(self):
        """Test parsing reference.

        Test case verifies that standard reference is parsed correctly from
        Markdown template.
        """

        text = '\n'.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> \[1\]: `https://docs.docker.com/engine/reference/commandline/images/`  ',
            '\[2\]: `https://docs.docker.com/engine/reference/commandline/rm/`',
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Remove docker image with force'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == ()
        #assert resource.brief == brief
        #assert resource.groups == groups
        #assert resource.description == description
        #assert resource.tags == tags
        #assert resource.links == links
        #assert resource.uuid == uuid
        #assert resource.digest == digest
