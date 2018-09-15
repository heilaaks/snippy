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

import pytest

from snippy.constants import Constants as Const
from snippy.config.source.parsers.markdown import ContentParserMarkdown as Parser


class TestUtContentParserMarkdown(object):
    """Test ContentParserMarkdown() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+0000'

    @pytest.mark.skip(reason="no way of currently testing this")
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
            '> [1]: `https://docs.docker.com/engine/reference/commandline/images/`  ',
            '[2]: `https://docs.docker.com/engine/reference/commandline/rm/`',
            '',
            '- Remove all exited containers',
            '',
            '    `$ docker rm $(docker ps --all -q -f status=exited)`',
            '',
            '- Remove all dangling images',
            '',
            '    `$ docker images -q --filter dangling=true | xargs docker rmi`',
            '',
            '# Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-12T11:52:11.000001+0000  ',
            'updated  : 2017-10-12T11:52:11.000001+0000  ',
            'tags     : cleanup, container, docker, docker-ce, moby  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'versions :  ',
            'uuid     : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
        ))
        data = (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
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
        assert resource.brief == brief
        assert resource.groups == groups
        assert resource.description == description
        assert resource.tags == tags
        assert resource.links == links
        assert resource.uuid == uuid
        assert resource.digest == digest
