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
from snippy.config.source.parsers.mkdn import ContentParserMkdn as Parser


class TestUtContentParserMarkdown(object):
    """Test ContentParserMarkdown() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+0000'

    def test_parser_snippet_001(self):
        """Test parsing snippet.

        Test case verifies that standard snippet is parsed correctly from
        Markdown template.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            "> \\[1\\] https://docs.docker.com/engine/reference/commandline/images/  ",
            "\\[2\\] https://docs.docker.com/engine/reference/commandline/rm/",
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
            'digest   : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
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
        brief = 'Remove all exited containers and dangling images'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'
        assert resource.digest == digest

    def test_parser_snippet_002(self):
        """Test parsing two snippets.

        Test case verifies that standard snippets are parsed correctly from
        Markdown template. In this case the first snippet contains commands
        with headers which are missing from the second snippet.

        The second snippet is part of two groups and it's description is
        one liner.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            "> \\[1\\] https://docs.docker.com/engine/reference/commandline/images/  ",
            "\\[2\\] https://docs.docker.com/engine/reference/commandline/rm/",
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
            'digest   : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
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
            '# Solve docker networking \'has active endpoints\' problem @docker, python',
            '',
            '> Fix docker problem that results \'has active endpoints\' error log.',
            '',
            "> \\[1\\] https://github.com/moby/moby/issues/23302",
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
            'digest   : 0bcf78d5c36a96a556fa3293f9b68c3dca577ea9c7fa5de76b354ccf27885df2  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     :   ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f31c752e-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            ''
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited) # Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi # Remove all dangling images'
        )
        brief = 'Remove all exited containers and dangling images'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69'
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.size() == 2
        resource = collection[list(collection.keys())[0]]['data']
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'
        assert resource.digest == digest

        data = (
            'docker network ls',
            'docker network inspect y0fdm2xoyuca',
            'docker network disconnect -f y0fdm2xoyuca devstack_logstash.1.7iqgrfd2xwcidj87zbkmauw4l',
            'docker network rm y0fdm2xoyuca'
        )
        brief = 'Solve docker networking \'has active endpoints\' problem'
        description = ('Fix docker problem that results \'has active endpoints\' error log.')
        groups = ('docker', 'python')
        tags = ()
        links = (
            'https://github.com/moby/moby/issues/23302',
        )
        uuid = 'f31c752e-8830-11e8-a114-2c4d54508088'
        digest = '0bcf78d5c36a96a556fa3293f9b68c3dca577ea9c7fa5de76b354ccf27885df2'
        resource = collection[list(collection.keys())[1]]['data']
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'
        assert resource.digest == digest

    def test_parser_snippet_003(self):
        """Test parsing snippet.

        Test case verifies that optional fields brief, groups, description and
        links can be ommitted and the content is still parsed correctly.
        """

        text = Const.NEWLINE.join((
            '# @default',
            '',
            '> ',
            '',
            '> ',
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
            'digest   : 852ca349dc05fb75bccfac743318230b7fc5360e8d3d4e61674e71aba2e469ff  ',
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
        groups = ('default',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '852ca349dc05fb75bccfac743318230b7fc5360e8d3d4e61674e71aba2e469ff'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == Const.EMPTY
        assert resource.groups == groups
        assert resource.description == Const.EMPTY
        assert resource.tags == tags
        assert resource.links == ()
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'
        assert resource.digest == digest

    def test_parser_snippet_004(self):
        """Test parsing snippet.

        Test case verifies that real content example is parsed correctly.
        """

        text = Const.NEWLINE.join((
            '# Manipulate compressed tar files @linux',
            '',
            '> ',
            '',
            '> ',
            '',
            '- Compress folder excluding the tar.',
            '',
            '    `$ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./`',
            '',
            '- List content of compressed tar.',
            '',
            '    `$ tar tvf mytar.tar.gz`',
            '',
            '- Cat file in compressed tar.',
            '',
            '    `$ tar xfO mytar.tar.gz manifest.json`',
            '',
            '- Extract and exclude one file.',
            '',
            '    `$ tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"`',
            '',
            '- Extract only one file.',
            '',
            '    `$ tar -xf mytar.tar.gz manifest.json`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2018-05-07T11:13:17.000001+0000  ',
            'digest   : 1115c9c843d1ffae45997d68c96d02af83fef49db677a9a7298ba135436e4ca8  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : howto,linux,tar,untar  ',
            'updated  : 2018-05-07T11:13:17.000001+0000  ',
            'uuid     : f21c8ed8-8830-11e8-a114-2c4d54508088  ',
            'versions : ',
            ''
        ))
        data = (
            'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./ # Compress folder excluding the tar.',
            'tar tvf mytar.tar.gz # List content of compressed tar.',
            'tar xfO mytar.tar.gz manifest.json # Cat file in compressed tar.',
            'tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz" # Extract and exclude one file.',
            'tar -xf mytar.tar.gz manifest.json # Extract only one file.'
        )
        brief = 'Manipulate compressed tar files'
        groups = ('linux',)
        tags = ('howto', 'linux', 'tar', 'untar')
        uuid = 'f21c8ed8-8830-11e8-a114-2c4d54508088'
        digest = '1115c9c843d1ffae45997d68c96d02af83fef49db677a9a7298ba135436e4ca8'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == Const.EMPTY
        assert resource.tags == tags
        assert resource.links == ()
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2018-05-07T11:13:17.000001+0000'
        assert resource.updated == '2018-05-07T11:13:17.000001+0000'
        assert resource.digest == digest

    def test_parser_solution_001(self):
        """Test parsing solution.

        Test case verifies that Snippy text formatted solution is parsed correctly
        from Markdown source. In this case there are no optional links defined.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> ',
            '',
            '```',
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : cleanup, container, docker, docker-ce, moby',
            '## FILE   : docker-example.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '```',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Testing docker log drivers'
        description = (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        data = (
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : cleanup, container, docker, docker-ce, moby',
            '## FILE   : docker-example.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
        )
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == ()
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'

    def test_parser_solution_002(self):
        """Test parsing solution.

        Test case verifies that Snippy Markdown formatted solution is parsed
        correctly from Markdown source. In this case the Markdown formatted
        solution data contains code block which must be stored correctly with
        the content data.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            "> \\[1\\] https://docs.docker.com/engine/reference/commandline/images/  ",
            "\\[2\\] https://docs.docker.com/engine/reference/commandline/rm/",
            '',
            '## Solution',
            '',
            '### Description',
            '',
            'Testing docker log drivers',
            '',
            '### Commands',
            '',
            '```',
            '# Get logs from pods',
            '$ kubectl get pods',
            '$ kubectl logs kafka-0',
            '```',
            '',
            '### Configurations',
            '',
            '### Whiteboard',
            '',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Testing docker log drivers'
        description = (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        data = (
            '## Solution',
            '',
            '### Description',
            '',
            'Testing docker log drivers',
            '',
            '### Commands',
            '',
            '```',
            '# Get logs from pods',
            '$ kubectl get pods',
            '$ kubectl logs kafka-0',
            '```',
            '',
            '### Configurations',
            '',
            '### Whiteboard',
            '',
        )
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'

    def test_parser_solution_003(self):
        """Test parsing solution.

        Test case verifies that Snippy Markdown formatted solution is parsed
        correctly from Markdown source. In this case the Markdown formatted
        solution data contains code block just before the Meta heaader which
        indicates the end of the solution data.

        The Solution and Meta headers are by default defined to be level two
        headers. These headers are also supported as level one headers. The
        reason to use level two headers by default is that in this case all
        the content falls nicely under the main header. This allows saving
        mulitple contents in Markdown format in a single file.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            "> \\[1\\] https://docs.docker.com/engine/reference/commandline/images/  ",
            "\\[2\\] https://docs.docker.com/engine/reference/commandline/rm/",
            '',
            '# Solution',
            '',
            '## Description',
            '',
            'Testing docker log drivers',
            '',
            '## Commands',
            '',
            '',
            '## Configurations',
            '',
            '## Whiteboard',
            '```',
            '# Get logs from pods',
            '$ kubectl get pods',
            '$ kubectl logs kafka-0',
            '```',
            '',
            '# Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Testing docker log drivers'
        description = (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        data = (
            '# Solution',
            '',
            '## Description',
            '',
            'Testing docker log drivers',
            '',
            '## Commands',
            '',
            '',
            '## Configurations',
            '',
            '## Whiteboard',
            '```',
            '# Get logs from pods',
            '$ kubectl get pods',
            '$ kubectl logs kafka-0',
            '```',
            '',
        )
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'

    def test_parser_solution_004(self):
        """Test parsing solution.

        Test case verifies that optional fields brief, groups, description and
        links can be ommitted and the content is still parsed correctly with
        text based solution content in Markdown format.
        """

        text = Const.NEWLINE.join((
            '# @default',
            '',
            '> ',
            '',
            '> ',
            '',
            '```',
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : cleanup, container, docker, docker-ce, moby',
            '## FILE   : docker-example.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '```',
            '',
            '# Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
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
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : cleanup, container, docker, docker-ce, moby',
            '## FILE   : docker-example.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
        )
        groups = ('default',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == Const.EMPTY
        assert resource.groups == groups
        assert resource.description == Const.EMPTY
        assert resource.tags == tags
        assert resource.links == ()
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'

    def test_parser_solution_005(self):
        """Test parsing solution.

        Test case verifies that optional fields brief, groups, description and
        links can be ommitted and the content is still parsed correctly with
        Markdown based solution content in Markdown format.
        """

        text = Const.NEWLINE.join((
            '# @default',
            '',
            '> ',
            '',
            '> ',
            '',
            '## Solution',
            '',
            '### Description',
            '',
            'Testing docker log drivers',
            '',
            '### Commands',
            '',
            '### Configurations',
            '',
            '### Whiteboard',
            '```',
            '# Get logs from pods',
            '$ kubectl get pods',
            '$ kubectl logs kafka-0',
            '```',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
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
            '## Solution',
            '',
            '### Description',
            '',
            'Testing docker log drivers',
            '',
            '### Commands',
            '',
            '### Configurations',
            '',
            '### Whiteboard',
            '```',
            '# Get logs from pods',
            '$ kubectl get pods',
            '$ kubectl logs kafka-0',
            '```',
            '',
        )
        groups = ('default',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == Const.EMPTY
        assert resource.groups == groups
        assert resource.description == Const.EMPTY
        assert resource.tags == tags
        assert resource.links == ()
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2017-10-12T11:52:11.000001+0000'

    def test_parser_solution_006(self):
        """Test parsing solution.

        Test case verifies that Snippy text formatted solution is parsed correctly
        from Markdown source. In this case there are links in the Markdown header
        and in the solution data. Only the links from Markdown header must be read
        in order to avoid duplicating the links. The links in the header must be
        previously parsed from the content data and thus they must be the same in
        the Markdown header as well as in the content data.

        Same comment than for the links apply also other metadata like filename.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            "> \\[1\\] https://github.com/MickayG/moby-kafka-logdriver  ",
            "\\[2\\] https://github.com/garo/logs2kafka",
            "\\[3\\] https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ",
            '',
            '```',
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : cleanup, container, docker, docker-ce, moby',
            '## FILE   : docker-example.txt',
            '################################################################################',
            '',
            '# Kube Kafka log driver',
            '> https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '# Logs2Kafka',
            '> https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '> https://github.com/garo/logs2kafka',
            '################################################################################',
            '## description',
            '################################################################################',
            '```',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename :  docker-example.txt ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Testing docker log drivers'
        description = (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        data = (
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : cleanup, container, docker, docker-ce, moby',
            '## FILE   : docker-example.txt',
            '################################################################################',
            '',
            '# Kube Kafka log driver',
            '> https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '# Logs2Kafka',
            '> https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '> https://github.com/garo/logs2kafka',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
        )
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        links = (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == 'docker-example.txt'
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'

    def test_parser_reference_001(self):
        """Test parsing reference.

        Test case verifies that standard reference is parsed correctly from
        Markdown template.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            "> \\[1\\] https://docs.docker.com/engine/reference/commandline/images/  ",
            "\\[2\\] https://docs.docker.com/engine/reference/commandline/rm/",
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : ec6ff1c1e8c52bc2ca8de76c71cd2eebd4f5ca07e6bdd9bba42ad2154d40503b  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, python, docker-ce, moby  ',
            'updated  : 2018-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        brief = 'Remove all exited containers and dangling images'
        description = ('Remove all exited containers and dangling images. The command examples ' +
                       'first remove all exited containers and the all dangling images.')
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker-ce', 'moby', 'python')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = 'ec6ff1c1e8c52bc2ca8de76c71cd2eebd4f5ca07e6bdd9bba42ad2154d40503b'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2018-10-12T11:52:11.000001+0000'
        assert resource.digest == digest

    def test_parser_reference_002(self):
        """Test parsing reference.

        Test case verifies that optional fields brief, groups, description and
        links can be ommitted and the content is still parsed correctly.
        """

        text = Const.NEWLINE.join((
            '# @default',
            '',
            '> ',
            '',
            '> ',
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'digest   : 1c7501ac802d98aeb161c973ec51c1b96d56774cdc8936c17df0fa9315d3e1c7  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup, container, python, docker-ce, moby  ',
            'updated  : 2018-10-12T11:52:11.000001+0000  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions :',
            '',
        ))
        groups = ('default',)
        tags = ('cleanup', 'container', 'docker-ce', 'moby', 'python')
        uuid = 'f21c6318-8830-11e8-a114-2c4d54508088'
        digest = '1c7501ac802d98aeb161c973ec51c1b96d56774cdc8936c17df0fa9315d3e1c7'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == ()
        assert resource.brief == Const.EMPTY
        assert resource.groups == groups
        assert resource.description == Const.EMPTY
        assert resource.tags == tags
        assert resource.links == ()
        assert resource.filename == Const.EMPTY
        assert resource.name == Const.EMPTY
        assert resource.versions == Const.EMPTY
        assert resource.source == Const.EMPTY
        assert resource.uuid == uuid
        assert resource.created == '2017-10-12T11:52:11.000001+0000'
        assert resource.updated == '2018-10-12T11:52:11.000001+0000'
        assert resource.digest == digest
