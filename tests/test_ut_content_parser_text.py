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

"""test_ut_parser: Test ContentParserText() class."""

from snippy.constants import Constants as Const
from snippy.config.source.parsers.text import ContentParserText as Parser


class TestUtContentParserText(object):
    """Test ContentParserText() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+0000'

    def test_parser_snippet_001(self):
        """Test parsing snippet.

        Test case verifies that links are parsed from snippet template where
        the links are the last item in the template. There is no newline at the
        end of the last link.

        Test case verifies that tags are parsed correctly when there is no
        newline after the next item.

        Test case verifies that the trailing whitespaces are removed from each
        tag and link.

        Test case verifies that all items are parsed correctly from template.
        """

        text = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '',
            '# Add optional brief description below.',
            'Remove docker image with force',
            '',
            '# Add optional description below.',
            'Remove all hanging docker images.',
            '',
            '# Add optional comma separated list of groups below.',
            'docker',
            '',
            '# Add optional comma separated list of tags below.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# Add optional links below one link per line.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        brief = 'Remove docker image with force'
        description = 'Remove all hanging docker images.'
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_snippet_002(self):
        """Test parsing snippet.

        Test case verifies that groups are parsed correctly if there is a list
        of groups. The groups must be sorted. This case has also multiline
        description with multiple sequential spaces. In this case there is
        empty line before next content tag.
        """

        text = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '',
            '# Add optional brief description below.',
            'Remove docker image with force',
            '',
            '# Add optional description below.',
            'Remove all hanging docker images. This uses force',
            'command and it removes all with force.',
            '',
            '# Add optional comma separated list of groups below.',
            'moby,docker',
            '',
            '# Add optional comma separated list of tags below.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# Add optional links below one link per line.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        brief = 'Remove docker image with force'
        description = 'Remove all hanging docker images. This uses force command and it removes all with force.'
        groups = ('docker', 'moby')
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_snippet_003(self):
        """Test parsing snippet.

        Test case verifies that a snippet content can be parsed without
        any newlines after each content tag field.
        """

        text = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '# Add optional brief description below.',
            'Remove docker image with force',
            '# Add optional description below.',
            '  Remove all hanging docker images. This uses force',
            'command and it removes all with force.  ',
            '# Add optional comma separated list of groups below.',
            'moby,   docker',
            '# Add optional comma separated list of tags below.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# Add optional links below one link per line.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        brief = 'Remove docker image with force'
        description = 'Remove all hanging docker images. This uses force command and it removes all with force.'
        groups = ('docker', 'moby')
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_snippet_004(self):
        """Test parsing snippet.

        Try to match content that does not match to any of the snippet tags.
        """

        text = '\n'.join((
            '# unknown 1.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '# unknown 2.',
            'Remove docker image with force',
            '# unknown 3.',
            'Remove docker image.',
            '# unknown 4.',
            'moby,   docker',
            '# unknown 5.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# unknown 6.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.empty()

    def test_parser_snippet_005(self):
        """Test parsing snippet.

        Try to match snippet content where the second snippet content does not
        match to any of the snippet tags. In this case the description field is
        missing totally.
        """

        text = '\n'.join((
            '# Add mandatory snippet below.',
            '# unknown 2.',
            'Remove docker image with force',
            '# Add optional brief description below.',
            '# unknown 4.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# unknown 5.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  ',
            '# Add mandatory snippet below',
            '# unknown 2.'
        ))
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.size() == 1
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == ('',)
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.groups == ()
        assert resource.tags == ()
        assert resource.links == ()

    def test_parser_solution_001(self):
        """Test parsing solution.

        Test case verifies that a solution content can be parsed.
        """

        text = '\n'.join((
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
            '## FILE   : kubernetes-docker-log-driver-kafka.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
            '    # This is a one line solution description.',
            '',
            '################################################################################',
            '## references',
            '################################################################################',
            '',
            '    # Kube Kafka log driver',
            '    > https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '    # Logs2Kafka',
            '    > https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '    > https://github.com/garo/logs2kafka',
            '',
            '################################################################################',
            '## commands',
            '################################################################################',
            '',
            '################################################################################',
            '## solutions',
            '################################################################################',
            '',
            '################################################################################',
            '## configurations',
            '################################################################################',
            '',
            '################################################################################',
            '## whiteboard',
            '################################################################################',
            ''
        ))
        links = (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        brief = 'Testing docker log drivers'
        description = 'This is a one line solution description.'
        groups = ('docker',)
        tags = ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        filename = 'kubernetes-docker-log-driver-kafka.txt'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == filename

    def test_parser_solution_002(self):
        """Test parsing solution.

        Test case verifies that multiline solution description can be parsed.
        """

        text = '\n'.join((
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
            '## FILE   : kubernetes-docker-log-driver-kafka.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
            '    # This is two line  ',
            '    # solution description.',
            '',
            '################################################################################',
            '## references',
            '################################################################################',
            '',
            '    # Kube Kafka log driver',
            '    > https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '    # Logs2Kafka',
            '    > https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '    > https://github.com/garo/logs2kafka',
            '',
            '################################################################################',
            '## commands',
            '################################################################################',
            '',
            '################################################################################',
            '## solutions',
            '################################################################################',
            '',
            '################################################################################',
            '## configurations',
            '################################################################################',
            '',
            '################################################################################',
            '## whiteboard',
            '################################################################################',
            ''
        ))
        links = (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        brief = 'Testing docker log drivers'
        description = 'This is two line solution description.'
        groups = ('docker',)
        tags = ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        filename = 'kubernetes-docker-log-driver-kafka.txt'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == filename

    def test_parser_solution_003(self):
        """Test parsing solution.

        Test case verifies that multiline solution description can be parsed.
        """

        text = '\n'.join((
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
            '## FILE   : kubernetes-docker-log-driver-kafka.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
            '    # This is two line  ',
            '    # solution description without newline before next header.',
            '################################################################################',
            '## references',
            '################################################################################',
            '',
            '    # Kube Kafka log driver',
            '    > https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '    # Logs2Kafka',
            '    > https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '    > https://github.com/garo/logs2kafka',
            '',
            '################################################################################',
            '## commands',
            '################################################################################',
            '',
            '################################################################################',
            '## solutions',
            '################################################################################',
            '',
            '################################################################################',
            '## configurations',
            '################################################################################',
            '',
            '################################################################################',
            '## whiteboard',
            '################################################################################',
            ''
        ))
        links = (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        brief = 'Testing docker log drivers'
        description = 'This is two line solution description without newline before next header.'
        groups = ('docker',)
        tags = ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        filename = 'kubernetes-docker-log-driver-kafka.txt'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == filename

    def test_parser_solution_004(self):
        """Test parsing solution.

        Test case verifies that multiline solution description can be parsed.
        In this case the description is not defined.
        """

        text = '\n'.join((
            '################################################################################',
            '## BRIEF  : Testing docker log drivers',
            '##',
            '## GROUPS : docker',
            '## TAGS   : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
            '## FILE   : kubernetes-docker-log-driver-kafka.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
            '################################################################################',
            '## references',
            '################################################################################',
            '',
            '    # Kube Kafka log driver',
            '    > https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '    # Logs2Kafka',
            '    > https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '    > https://github.com/garo/logs2kafka',
            '',
            '################################################################################',
            '## commands',
            '################################################################################',
            '',
            '################################################################################',
            '## solutions',
            '################################################################################',
            '',
            '################################################################################',
            '## configurations',
            '################################################################################',
            '',
            '################################################################################',
            '## whiteboard',
            '################################################################################',
            ''
        ))
        links = (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        brief = 'Testing docker log drivers'
        groups = ('docker',)
        tags = ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        filename = 'kubernetes-docker-log-driver-kafka.txt'
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == brief
        assert resource.description == ''
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links
        assert resource.filename == filename

    def test_parser_solution_005(self):
        """Test parsing solution.

        Try to match content that does not match to any of the solution tags.
        """

        text = '\n'.join((
            '################################################################################',
            '## NONE   : Testing docker log drivers',
            '##',
            '## NONE   : docker',
            '## NONE   : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
            '## NONE   : kubernetes-docker-log-driver-kafka.txt',
            '################################################################################',
            '',
            '################################################################################',
            '## description',
            '################################################################################',
            '',
            '################################################################################',
            '## references',
            '################################################################################',
            '',
            '################################################################################',
            '## commands',
            '################################################################################',
            '',
            '################################################################################',
            '## solutions',
            '################################################################################',
            '',
            '################################################################################',
            '## configurations',
            '################################################################################',
            '',
            '################################################################################',
            '## whiteboard',
            '################################################################################',
            ''
        ))
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.empty()

    def test_parser_reference_001(self):
        """Test parsing reference.

        Test case verifies that links are parsed from reference template where
        the links are the first item in the template. There is a newline after
        the links before the next section.

        Test case verifies that the trailing whitespaces are removed from each
        link and category and brief sections.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            '  https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/  ',
            '',
            '# Add optional brief description below.',
            '  How to write commit messages  ',
            '',
            '# Add optional description below.',
            '  How to write  ',
            '  git   ',
            ' commit.  ',
            '# Add optional comma separated list of groups below.',
            '  git   ',
            '',
            '# Add optional comma separated list of tags below.',
            'commit,git,howto,message,scm'
        ))
        links = (
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/'
        )
        brief = 'How to write commit messages'
        description = 'How to write git commit.'
        groups = ('git',)
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_reference_002(self):
        """Test parsing reference.

        Test case verifies that links are parsed from reference template where
        the links are the first item in the template. There is no newline after
        the links before the next section.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '# Add optional brief description below.',
            'How to write commit messages',
            '',
            '# Add optional description below.',
            'How to write git commit.',
            '# Add optional comma separated list of groups below.',
            'git',
            '',
            '# Add optional comma separated list of tags below.',
            'commit,git,howto,message,scm'
        ))
        links = (
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/'
        )
        brief = 'How to write commit messages'
        description = 'How to write git commit.'
        groups = ('git',)
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_reference_003(self):
        """Test parsing reference.

        Test case verifies that a reference content can be parsed without
        any newlines after each field.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '# Add optional brief description below.',
            'How to write commit messages',
            '# Add optional description below.',
            'How to write git commit.',
            '# Add optional comma separated list of groups below.',
            'git, moby',
            '# Add optional comma separated list of tags below.',
            'commit,git,howto,message,scm'
        ))
        links = (
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/'
        )
        brief = 'How to write commit messages'
        description = 'How to write git commit.'
        groups = ('git', 'moby')
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_reference_004(self):
        """Test parsing reference.

        Try to match content that does not match to any of the reference tags.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# unknown 1.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '# unknown 2.',
            'How to write commit messages',
            '# unknown 3.',
            'git, moby',
            '# unknown 4.',
            'commit,git,howto,message,scm'
        ))
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.empty()

    def test_parser_reference_005(self):
        """Test parsing reference.

        Try to parse reference from snippet template.
        """

        text = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '',
            '# Add optional brief description below.',
            'Remove docker image with force',
            '',
            '# Add optional description below.',
            'Remove docker image.',
            ''
            '# Add optional comma separated list of groups below.',
            'docker',
            '',
            '# Add optional comma separated list of tags below.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# Add optional links below one link per line.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        brief = 'Remove docker image with force'
        description = 'Remove docker image.'
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        resource = next(Parser(self.TIMESTAMP, text).read_collection().resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == brief
        assert resource.description == description
        assert resource.groups == groups
        assert resource.tags == tags
        assert resource.links == links

    def test_parser_unknown_001(self):
        """Test parsing unknown content.

        Try to run parser against content that is not identified.
        """

        text = '\n'.join((
            'git, moby',
            '# unknown 1.',
            'commit,git,howto,message,scm'
        ))
        collection = Parser(self.TIMESTAMP, text).read_collection()
        assert collection.empty()
