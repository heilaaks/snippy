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
from snippy.config.source.parser import Parser


class TestUtParser(object):
    """Test Parser() class."""

    def test_parser_001(self):
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

    def test_parser_002(self):
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
        brief = 'How to write commit messages'
        groups = ('git',)
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        assert links == Parser.content_links(Const.REFERENCE, source)
        assert brief == Parser.content_brief(Const.SNIPPET, source)
        assert groups == Parser.content_groups(Const.SNIPPET, source)
        assert tags == Parser.content_tags(Const.SNIPPET, source)

    def test_parser_003(self):
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
        brief = 'How to write commit messages'
        groups = ('git',)
        tags = ('commit', 'git', 'howto', 'message', 'scm')
        assert links == Parser.content_links(Const.REFERENCE, source)
        assert brief == Parser.content_brief(Const.SNIPPET, source)
        assert groups == Parser.content_groups(Const.SNIPPET, source)
        assert tags == Parser.content_tags(Const.SNIPPET, source)

    def test_parser_004(self):
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
