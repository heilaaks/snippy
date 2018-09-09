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

"""test_ut_parser: Test Parser() class."""

from snippy.constants import Constants as Const
from snippy.config.source.parsers.text import ContentParserText as Parser


class TestUtContentParserText(object):
    """Test Parser() class."""

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

        source = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '',
            '# Add optional brief description below.',
            'Remove docker image with force',
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
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert data == Parser.content_data(Const.SNIPPET, source)
        assert brief == Parser.content_brief(Const.SNIPPET, source)
        assert groups == Parser.content_groups(Const.SNIPPET, source)
        assert tags == Parser.content_tags(Const.SNIPPET, source)
        assert links == Parser.content_links(Const.SNIPPET, source)

    def test_parser_snippet_002(self):
        """Test parsing snippet.

        Test case verifies that groups are parsed corrected if there is
        a list of groups. The groups must be sorted.
        """

        source = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '',
            '# Add optional brief description below.',
            'Remove docker image with force',
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
        groups = ('docker', 'moby')
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert data == Parser.content_data(Const.SNIPPET, source)
        assert brief == Parser.content_brief(Const.SNIPPET, source)
        assert groups == Parser.content_groups(Const.SNIPPET, source)
        assert tags == Parser.content_tags(Const.SNIPPET, source)
        assert links == Parser.content_links(Const.SNIPPET, source)

    def test_parser_snippet_003(self):
        """Test parsing snippet.

        Test case verifies that a snippet content can be parsed without
        any newlines after each field.
        """

        source = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '# Add optional brief description below.',
            'Remove docker image with force',
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
        groups = ('docker', 'moby')
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert data == Parser.content_data(Const.SNIPPET, source)
        assert brief == Parser.content_brief(Const.SNIPPET, source)
        assert groups == Parser.content_groups(Const.SNIPPET, source)
        assert tags == Parser.content_tags(Const.SNIPPET, source)
        assert links == Parser.content_links(Const.SNIPPET, source)

    def test_parser_snippet_004(self):
        """Test parsing snippet.

        Try to match content that does not match to any of the snippet tags.
        """

        source = '\n'.join((
            '# unknown 1.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '# unknown 2.',
            'Remove docker image with force',
            '# unknown 3.',
            'moby,   docker',
            '# unknown 4.',
            '  cleanup,  container,docker,docker-ce,image,moby  ',
            '# unknown 5.',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        data = ()
        brief = ''
        groups = ()
        tags = ()
        links = ()
        assert data == Parser.content_data(Const.SNIPPET, source)
        assert brief == Parser.content_brief(Const.SNIPPET, source)
        assert groups == Parser.content_groups(Const.SNIPPET, source)
        assert tags == Parser.content_tags(Const.SNIPPET, source)
        assert links == Parser.content_links(Const.SNIPPET, source)

    def test_parser_reference_001(self):
        """Test parsing reference.

        Test case verifies that links are parsed from reference template where
        the links are the first item in the template. There is a newline after
        the links before the next section.

        Test case verifies that the trailing whitespaces are removed from each
        link and category and brief sections.
        """

        source = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            '  https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/  ',
            '',
            '# Add optional brief description below.',
            '  How to write commit messages  ',
            '',
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
        data = ()
        brief = 'How to write commit messages'
        groups = ('git',)
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        assert data == Parser.content_data(Const.REFERENCE, source)
        assert brief == Parser.content_brief(Const.REFERENCE, source)
        assert groups == Parser.content_groups(Const.REFERENCE, source)
        assert tags == Parser.content_tags(Const.REFERENCE, source)
        assert links == Parser.content_links(Const.REFERENCE, source)

    def test_parser_reference_002(self):
        """Test parsing reference.

        Test case verifies that links are parsed from reference template where
        the links are the first item in the template. There is no newline after
        the links before the next section.
        """

        source = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '# Add optional brief description below.',
            'How to write commit messages',
            '',
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
        data = ()
        brief = 'How to write commit messages'
        groups = ('git',)
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        assert data == Parser.content_data(Const.REFERENCE, source)
        assert brief == Parser.content_brief(Const.REFERENCE, source)
        assert groups == Parser.content_groups(Const.REFERENCE, source)
        assert tags == Parser.content_tags(Const.REFERENCE, source)
        assert links == Parser.content_links(Const.REFERENCE, source)

    def test_parser_reference_003(self):
        """Test parsing reference.

        Test case verifies that a reference content can be parsed without
        any newlines after each field.
        """

        source = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '# Add optional brief description below.',
            'How to write commit messages',
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
        groups = ('git', 'moby')
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        assert brief == Parser.content_brief(Const.REFERENCE, source)
        assert groups == Parser.content_groups(Const.REFERENCE, source)
        assert tags == Parser.content_tags(Const.REFERENCE, source)
        assert links == Parser.content_links(Const.REFERENCE, source)

    def test_parser_reference_004(self):
        """Test parsing reference.

        Try to match content that does not match to any of the reference tags.
        """

        source = '\n'.join((
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
        links = ()
        brief = ''
        groups = ()
        tags = ()
        assert brief == Parser.content_brief(Const.REFERENCE, source)
        assert groups == Parser.content_groups(Const.REFERENCE, source)
        assert tags == Parser.content_tags(Const.REFERENCE, source)
        assert links == Parser.content_links(Const.REFERENCE, source)


    def test_parser_reference_005(self):
        """Test parsing reference.

        Try to parse reference from snippet content
        """

        source = '\n'.join((
            '# Add mandatory snippet below.',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm',
            '',
            '# Add optional brief description below.',
            'Remove docker image with force',
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
        data = ()
        brief = 'Remove docker image with force'
        groups = ('docker',)
        tags = ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert data == Parser.content_data(Const.REFERENCE, source)
        assert brief == Parser.content_brief(Const.REFERENCE, source)
        assert groups == Parser.content_groups(Const.REFERENCE, source)
        assert tags == Parser.content_tags(Const.REFERENCE, source)
        assert links == Parser.content_links(Const.REFERENCE, source)

    def test_parser_solution_001(self):
        """Test parsing solution.

        Test case verifies that a solution content can be parsed.
        """

        source = '\n'.join((
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
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            'https://github.com/garo/logs2kafka'
        )
        brief = 'Testing docker log drivers'
        groups = ('docker',)
        tags = ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        filename = 'kubernetes-docker-log-driver-kafka.txt'
        assert source == '\n'.join(Parser.content_data(Const.SOLUTION, source))
        assert brief == Parser.content_brief(Const.SOLUTION, source)
        assert groups == Parser.content_groups(Const.SOLUTION, source)
        assert tags == Parser.content_tags(Const.SOLUTION, source)
        assert links == Parser.content_links(Const.SOLUTION, source)
        assert filename == Parser.content_filename(Const.SOLUTION, source)

    def test_parser_solution_002(self):
        """Test parsing solution.

        Try to match content that does not match to any of the solution tags.
        """

        source = '\n'.join((
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
        links = ()
        brief = ''
        groups = ()
        tags = ()
        filename = ''
        assert source == '\n'.join(Parser.content_data(Const.SOLUTION, source))
        assert brief == Parser.content_brief(Const.SOLUTION, source)
        assert groups == Parser.content_groups(Const.SOLUTION, source)
        assert tags == Parser.content_tags(Const.SOLUTION, source)
        assert links == Parser.content_links(Const.SOLUTION, source)
        assert filename == Parser.content_filename(Const.SOLUTION, source)

    def test_parser_unknown_001(self):
        """Test parsing unknown content.

        Try to run parser against content that is not identified.
        """

        source = '\n'.join((
            'git, moby',
            '# unknown 1.',
            'commit,git,howto,message,scm'
        ))
        data = ()
        brief = ''
        groups = ()
        tags = ()
        links = ()
        filename = ''
        assert data == Parser.content_data(Const.UNKNOWN_CATEGORY, source)
        assert brief == Parser.content_brief(Const.UNKNOWN_CATEGORY, source)
        assert groups == Parser.content_groups(Const.UNKNOWN_CATEGORY, source)
        assert tags == Parser.content_tags(Const.UNKNOWN_CATEGORY, source)
        assert links == Parser.content_links(Const.UNKNOWN_CATEGORY, source)
        assert filename == Parser.content_filename(Const.UNKNOWN_CATEGORY, source)
