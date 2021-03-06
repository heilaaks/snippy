# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_ut_content_parser_mkdn: Test ContentParserMkdn() class."""

from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.content.parsers.mkdn import ContentParserMkdn as Parser


class TestUtContentParserMkdn(object):  # pylint: disable=too-many-lines
    """Test ContentParserMkdn() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+00:00'

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
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
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
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
            'filename  : snippet.txt',
            'languages : language',
            'name      : example text',
            'source    : https://www.random.org/',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : git<=1.1.1,python>=2.7.0,python==3.7.0',
            '',
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)  #  Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi  #  Remove all dangling images'
        )
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == 'example text'
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        assert resource.source == 'https://www.random.org/'
        assert resource.versions == ('git<=1.1.1', 'python==3.7.0', 'python>=2.7.0')
        assert resource.languages == ('language',)
        assert resource.filename == 'snippet.txt'
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '3306409c0901e27d754a3273a5964652e2e8ea80fe82f3aa80d1aef6e8ab8cef'

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
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
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
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  :',
            '',
            '---',
            '',
            '# Solve docker networking \'has active endpoints\' problem @docker, python',
            '',
            '> Fix docker problem that results \'has active endpoints\' error log.',
            '',
            '> [1] https://github.com/moby/moby/issues/23302',
            '',
            '`$ docker network ls`',
            '`$ docker network inspect y0fdm2xoyuca`',
            '`$ docker network disconnect -f y0fdm2xoyuca devstack_logstash.1.7iqgrfd2xwcidj87zbkmauw4l`',
            '`$ docker network rm y0fdm2xoyuca`',
            '',
            '## Meta',
            '',
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0bcf78d5c36a96a556fa3293f9b68c3dca577ea9c7fa5de76b354ccf27885df2  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      :  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f31c752e-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
            ''
        ))
        digest = '9dcf81a0484d6551a3a0a0cf892d22bfba6b25b0f0ec6ef7080a617e3cf0b092'
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        assert len(collection) == 2
        resource = collection[digest]
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)  #  Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi  #  Remove all dangling images'
        )
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == digest

        digest = '0bcf78d5c36a96a556fa3293f9b68c3dca577ea9c7fa5de76b354ccf27885df2'
        resource = collection[digest]
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker network ls',
            'docker network inspect y0fdm2xoyuca',
            'docker network disconnect -f y0fdm2xoyuca devstack_logstash.1.7iqgrfd2xwcidj87zbkmauw4l',
            'docker network rm y0fdm2xoyuca'
        )
        assert resource.brief == 'Solve docker networking \'has active endpoints\' problem'
        assert resource.description == ('Fix docker problem that results \'has active endpoints\' error log.')
        assert resource.name == ''
        assert resource.groups == ('docker', 'python')
        assert resource.tags == ()
        assert resource.links == ('https://github.com/moby/moby/issues/23302',)
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f31c752e-8830-11e8-a114-2c4d54508088'
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
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 852ca349dc05fb75bccfac743318230b7fc5360e8d3d4e61674e71aba2e469ff  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
            '',
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)  #  Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi  #  Remove all dangling images'
        )
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ('default',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == 'd8cc7d0f05108952002ab2dffab29e60bdb1b7a8abc41416ff4e43812eb5bb14'

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
            '    `$ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./`',
            '',
            '- List content of compressed tar.',
            '',
            '    `$ tar tvf mytar.tar.gz`',
            '',
            '- Cat file in compressed tar.',
            '',
            '    `$ tar xfO mytar.tar.gz manifest.json`',
            '',
            '- Extract and exclude one file.',
            '',
            '    `$ tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"`',
            '',
            '- Extract only one file.',
            '',
            '    `$ tar -xf mytar.tar.gz manifest.json`',
            '',
            '## Meta',
            '',
            '> category  : snippet  ',
            'created   : 2018-05-07T11:13:17.000001+00:00  ',
            'digest    : 1115c9c843d1ffae45997d68c96d02af83fef49db677a9a7298ba135436e4ca8  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : howto,linux,tar,untar  ',
            'updated   : 2018-05-07T11:13:17.000001+00:00  ',
            'uuid      : f21c8ed8-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
            ''
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./  #  Compress folder excluding the tar.',
            'tar tvf mytar.tar.gz  #  List content of compressed tar.',
            'tar xfO mytar.tar.gz manifest.json  #  Cat file in compressed tar.',
            'tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"  #  Extract and exclude one file.',
            'tar -xf mytar.tar.gz manifest.json  #  Extract only one file.'
        )
        assert resource.brief == 'Manipulate compressed tar files'
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ('linux',)
        assert resource.tags == ('howto', 'linux', 'tar', 'untar')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2018-05-07T11:13:17.000001+00:00'
        assert resource.updated == '2018-05-07T11:13:17.000001+00:00'
        assert resource.uuid == 'f21c8ed8-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '61014e2d1ec56a9ae6fa71f781221b2706f69c8bd3090bf35af179c7a87f284a'

    def test_parser_snippet_005(self):
        """Test parsing snippet.

        Test case verifies that link list can be parsed with blockquote >
        delimiters before each link not just the first one. This helps user
        to fill the template intuitively by just copy pasting the example
        link with blockquote > delimiter.

        The link numbers are not updated but the same first index is
        copy pasted in each link.

        The last link contains index which has two digit index.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '> [1] https://docs.docker.com/engine/reference/commandline/rm/  ',
            '> [11] https://docs.docker.com/engine/reference/commandline/test/',
            '',
            '`$ docker rm $(docker ps --all -q -f status=exited)`',
            '`$ docker images -q --filter dangling=true | xargs docker rmi`',
            '',
            '## Meta',
            '',
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
            '',
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rmi'
        )
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/test/'
        )
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '38f478ac1f85234f7885960f72c27ec36049bea32007a46b032f18cbf86f3f08'

    def test_parser_snippet_006(self):
        """Test parsing snippet.

        Try parsing snippet data with incorrectly formatted snippets. It is
        not possible to loosen the parsin conditions because the commands may
        contain almost any characters. Because of this, the format of the
        command with leading dollar sign and surrounded by backtics (`) must
        be followed. Because of this, only one command from this case must
        be parsed.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '> [1] https://docs.docker.com/engine/reference/commandline/rm/  ',
            '> [11] https://docs.docker.com/engine/reference/commandline/test/',
            '',
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker ps -a',
            '`$ docker rm $(docker ps --all -q -f status=exited)`',
            '$ docker images -q --filter dangling=true | xargs docker rmi',
            'docker exec -it $(docker ps | egrep -m 1 \'kibana:latest\' | awk \'{print $1}\') /bin/bash',
            '',
            '## Meta',
            '',
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
            '',
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == ('docker rm $(docker ps --all -q -f status=exited)',)
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/test/'
        )
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == 'b1ddb8f29d857a9f654c99a5c1c46cb1fd6d71aa321d4ba4063e9ae549a2b63d'

    def test_parser_snippet_007(self):
        """Test parsing snippet.

        Test case verifies that snippet with multiline attributes that are
        not intended to be multiline attributres are read correctly. In case
        of Markdown content it is considered that it is less likely that user
        makes a mistake with attributes that are meant as one liners. Because
        of this, the ``brief`` attribute is the only one split to multiple
        lines in this test.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers ',
            ' and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
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
            '> category  : snippet  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69  ',
            'filename  : snippet.txt',
            'languages : language',
            'name      : example text',
            'source    : https://www.random.org/',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : git<=1.1.1,python>=2.7.0,python==3.7.0',
            '',
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)  #  Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi  #  Remove all dangling images'
        )
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == 'example text'
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        assert resource.source == 'https://www.random.org/'
        assert resource.versions == ('git<=1.1.1', 'python==3.7.0', 'python>=2.7.0')
        assert resource.languages == ('language',)
        assert resource.filename == 'snippet.txt'
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '3306409c0901e27d754a3273a5964652e2e8ea80fe82f3aa80d1aef6e8ab8cef'

    def test_parser_snippet_008(self):
        """Test parsing snippet.

        Test case verifies that the MKDN metadata is parsed correctly. In this
        case there are new whitespaces at the end of metadata fields and the
        ``source`` field is empty. The Tags must be read correctly here.
        """

        text = Const.NEWLINE.join((
            '# Remove all exited containers and dangling images @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
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
            '> category  : snippet',
            'created   : 2017-10-12T11:52:11.000001+00:00',
            'digest    : 0a8b31f0ab442991e56dcaef1fc65aa6bff479c567e04dd7990948f201187c69',
            'filename  : snippet.txt',
            'languages : language',
            'name      : example text',
            'source    :',
            'tags      : cleanup, container, docker, docker-ce, moby',
            'updated   : 2017-10-12T11:52:11.000001+00:00',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088',
            'versions  : git<=1.1.1,python>=2.7.0,python==3.7.0',
            '',
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)  #  Remove all exited containers',
            'docker images -q --filter dangling=true | xargs docker rmi  #  Remove all dangling images'
        )
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == 'example text'
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        assert resource.source == ''
        assert resource.versions == ('git<=1.1.1', 'python==3.7.0', 'python>=2.7.0')
        assert resource.languages == ('language',)
        assert resource.filename == 'snippet.txt'
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '3306409c0901e27d754a3273a5964652e2e8ea80fe82f3aa80d1aef6e8ab8cef'

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
            '> category  : solution  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : docker==1.1.1,moby!=2.7.0',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ('docker==1.1.1', 'moby!=2.7.0')
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'

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
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
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
            '> category  : solution  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'

    def test_parser_solution_003(self):
        """Test parsing solution.

        Test case verifies that Snippy Markdown formatted solution is parsed
        correctly from Markdown source. In this case the Markdown formatted
        solution data contains code block just before the Meta header which
        indicates the end of the solution data.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '## Solution',
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
            '## Meta',
            '',
            '> category  : solution  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
            '',
        ))
        data = (
            '## Solution',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'

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
            '## Meta',
            '',
            '> category  : solution  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : ',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ('default',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'

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
            '> category  : solution  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename  :   ',
            'languages :   ',
            'name      :   ',
            'source    :   ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  :',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ('default',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'

    def test_parser_solution_006(self):
        """Test parsing solution.

        Test case verifies that Snippy text formatted solution is parsed correctly
        from Markdown source. In this case there are links in the Markdown header
        and in the solution data. The links in the header must be automatically
        updated based on the content in the data part.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Remove all exited containers and dangling images. The command examples  ',
            'first remove all exited containers and the all dangling images.',
            '',
            '> [1] https://github.com/MickayG/moby-kafka-logdriver  ',
            '[2] https://github.com/garo/logs2kafka  ',
            '[3] https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
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
            '################################################################################',
            '## description',
            '################################################################################',
            '```',
            '',
            '## Meta',
            '',
            '> category  : solution  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : e167e4e2e06eba6bf041d1b9d56c41f39d199ced9a2174f2e4b92c658a23c56c  ',
            'filename  :  docker-example.txt ',
            'languages :  example-language ',
            'name      :   ',
            'source    :   ',
            'tags      : cleanup, container, docker, docker-ce, moby  ',
            'updated   : 2017-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  :',
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
            '# Kube Kafka log driver',
            '> https://github.com/MickayG/moby-kafka-logdriver',
            '',
            '# Logs2Kafka',
            '> https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '################################################################################',
            '## description',
            '################################################################################',
            ''
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'moby')
        assert resource.links == (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == 'docker-example.txt'
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'

    def test_parser_solution_007(self):
        """Test parsing solution.

        Test case verifies that Snippy text formatted solution is parsed correctly
        from Markdown source. In this case there are links in the Markdown header
        but not in the solution data. The links in the header must be automatically
        updated based on the content in the data part.
        """

        text = Const.NEWLINE.join((
            '# Testing docker log drivers @docker',
            '',
            '> Investigate docker log drivers and the logs2kafka log plugin',
            '',
            '> [1] https://github.com/MickayG/moby-kafka-logdriver  ',
            '[2] https://github.com/garo/logs2kafka  ',
            '[3] https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '',
            '## Description',
            '',
            'Investigate docker log drivers.',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            '',
            '## Meta',
            '',
            '> category  : solution  ',
            'created   : 2019-01-04T10:54:49.265512+00:00  ',
            'digest    : 18473ec207798670c302fb711a40df6555e8973e26481e4cd6b2ed205f5e633c  ',
            'filename  : kubernetes-docker-log-driver-kafka.mkdn  ',
            'languages :   ',
            'name      :   ',
            'source    :   ',
            'tags      : docker,driver,kafka,kubernetes,logging,logs2kafka,moby,plugin  ',
            'updated   : 2019-01-05T10:54:49.265512+00:00  ',
            'uuid      : 24cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  : ',
            ''
        ))
        data = (
            '## Description',
            '',
            'Investigate docker log drivers.',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            ''
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == ('Investigate docker log drivers and the logs2kafka log plugin')
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == 'kubernetes-docker-log-driver-kafka.mkdn'
        assert resource.created == '2019-01-04T10:54:49.265512+00:00'
        assert resource.uuid == '24cd5827-b6ef-4067-b5ac-3ceac07dde9f'

    def test_parser_solution_008(self):
        """Test parsing solution.

        Test case verifies that a solution content is split correctly. There
        are hyphens in the middle of the solution that must not split a single
        solution into multiple solutions.
        """

        text = Const.NEWLINE.join((
            '# Debug Kubernetes @k8s',
            '',
            '> Debug and configure Kubernetes',
            '',
            '> [1]  https://blog.codeship.com/getting-started-with-kubernetes/',
            '[2] https://github.com/kubernetes/kubernetes/releases',
            '[3] https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-the-dashboard-ui',
            '',
            '## Description',
            '',
            'Debug and configure Kubernetes.',
            '',
            '## Solutions',
            '',
            '### The connection to the server <host>:6443 was refused - did you specify the right host or port?',
            '',
            '    # Delete cache',
            '    ls -al ~/.kube/cache',
            '    rm -drf ~/.kube/cache',
            '',
            '### Kubernetes networking',
            '',
            '    # Flannel based networking',
            '    #',
            '    # Connecting PODs to host',
            '    #',
            '    # Containers in PODs share the same namespace. This allows communicating',
            '    # other containers withing a POD through localhost. Virtual bridge allows',
            '    # a POD to communicate with other PODs through the host. A virtual bridge',
            '    # is created from virtual interface pairs (veth) where one side is in a',
            '    # container and the other in the host root namespace. A virtual bridge',
            '    # uses e.g. Linux bridge or OpenvSwitch (OVS) for connectivity between',
            '    # containers in POD and a external (real) interface.',
            '    #',
            '    # Eeach POD thinks it has a totally normal ethernet device called eth0',
            '    # to make network requests through. But Kubernetes is faking it its',
            '    # just a virtual ethernet connection.',
            '    #',
            '    # When a POD communicates with another POD in the same node, the virtual',
            '    # bridge asks all connected devices (i.e. PODs) if they have destination',
            '    # IP address.',
            '    #',
            '    # When a POD communicates with another POD in another node, a virtual',
            '    # bridge (L2) like cni0 is linked via VXLAN tunnel setup by Flannel to',
            '    # other nodes. When a POD is in another node, the virtual bride will',
            '    # fall to the default GW.',
            '    #',
            '    # Iptables are used to forward IP packets between PODs.',
            '    #',
            '    # Example configuration output',
            '    #',
            '    # [2020-02-03T15:46:25 root@hla-testing] $ nsenter -t 21410 -n ip addr | grep -A3 eth0',
            '    # 3: eth0@if61: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8092 qdisc noqueue state UP group default',
            '    #     link/ether 66:be:4a:6a:56:0b brd ff:ff:ff:ff:ff:ff link-netnsid 0',
            '    #     inet 10.244.0.59/24 scope global eth0',
            '    #        valid_lft forever preferred_lft forever',
            '    # [2020-02-03T15:47:19 root@hla-testing] $ ip link show | grep -A2 "61: "',
            '    # 61: veth71b19139@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8092 qdisc noqueue master cni0 state UP mode DEFAULT group default',  # pylint: disable=line-too-long
            '    #     link/ether e2:b7:f4:a3:da:f6 brd ff:ff:ff:ff:ff:ff link-netnsid 28',
            '    # [2020-02-03T15:51:02 root@hla-testing] $ ip -d l show flannel.1',
            '    # 5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8092 qdisc noqueue state UNKNOWN mode DEFAULT group default',
            '    #     link/ether b6:93:45:98:a3:b7 brd ff:ff:ff:ff:ff:ff promiscuity 0',
            '    #     vxlan id 1 local 192.168.1.11 dev eth1 srcport 0 0 dstport 8472 nolearning ageing 300 noudpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535',  # pylint: disable=line-too-long
            '    #',
            '    # Interface links from the example configuration.',
            '    #',
            '    # eth0@if61 --> veth71b19139@if3 --> master cni0 --> vxlan --> flannel.1',
            '    #',
            '    #            5        61   veth      3',
            '    # flannel.1  x  cni0  x -----------> x eth0',
            '',
            '    # List bridges/links on the host.',
            '    ip link show',
            '    brctl show',
            '',
            '    # Network namespaces can typically be listed using ip netns list.',
            '    # However, if the container runtime is Docker, you will not be able to',
            '    # list namespaces this way because Docker does not sym-link the',
            '    # namespaces under /var/run/netns.',
            '    #',
            '    # You can enable ip netns namespace functionality by creating the',
            '    # necessary sym-link.',
            '    ln -s /var/run/docker/netns /var/run/netns',
            '',
            '    # List iptables.',
            '    sudo iptables -L # there\'s an implicit `-t filter` here,',
            '    sudo iptables -L -t nat',
            '    sudo iptables -L -t mangle',
            '    sudo iptables -L -t raw',
            '    sudo iptables-save',
            '',
            '    # List PODs IP addresses',
            '    kubectl get pod --namespace ucim -o wide',
            '',
            '    # List pods',
            '    crictl pods',
            '    crictl inspectp 680df9452dc61',
            '',
            '    # List interfaces in container and find the corresponding Veth endpont.',
            '    docker ps | grep engine',
            '    docker inspect --format \'{{ .State.Pid }}\' 2080cd573626  # Get pid',
            '    nsenter -t 9135 -n ip addr',
            '    ip link list',
            '',
            '    # Get Flannel configuration',
            '    kubectl -n kube-system get configmap kube-flannel-cfg -o yaml',
            '',
            '    # Show node Veth IP range.',
            '    kubectl get nodes -o jsonpath=\'{range .items[*]} {.metadata.name}{"  "}{.spec.podCIDR}{"\n"}{end}\'',
            '',
            '    # Routing table shows how traffic for the local POD CIDR 10.244.0.0/24',
            '    # is routed to the integration bridge cni0 whereas the POD CIDRs for',
            '    # the other hosts are routed to the flannel.1 port with the other',
            '    # bridges as gateways, hence the container overlay network',
            '    route -n',
            '',
            '    # Flush routing tables',
            '    ip route flush cache',
            '',
            '    # list ARP tables',
            '    arp -a',
            '',
            '### Routes deleted',
            '',
            '    # In order to create cni0 or docker0 routes again, change to interface',
            '    # state down and then up.',
            '    route -n',
            '    ip link set dev docker0 down',
            '    ip link set dev docker0 up',
            '    ip link set dev cni0 down',
            '    ip link set dev cni0 up',
            '    route -n',
            '',
            '## Commands',
            '',
            '    # Versions',
            '    kubectl version',
            '    kubectl version -o yaml',
            '',
            '    # Configuration',
            '    cat ~/.kube/config',
            '',
            '    # Linux kernel parameters.',
            '    sysctl -a | grep ip_forward',
            '',
            '## Configurations',
            '',
            '## References',
            '',
            '### Kubernetes and iptables',
            '',
            '    # [1] Explanation of Kubernetes and iptables.',
            '    > https://msazure.club/kubernetes-services-and-iptables/',
            '',
            '    # [2] Traversing iptables',
            '    > https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html#TRAVERSINGOFTABLES',
            '',
            '    # [3] Kubernetes networking',
            '    > https://www.ciscolive.com/c/dam/r/ciscolive/emea/docs/2018/pdf/BRKDCN-2390.pdf',
            '',
            '## Whiteboard',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2018-02-15T13:49:38.000001+00:00  ',
            'digest   : beb7d5a968d9025b10df2e23cca61b75b307e207630fe223aa52ace4e4851da1  ',
            'filename : howto-debug-kubernetes.md  ',
            'name     :  ',
            'source   :  ',
            'tags     : debug,docker,howto,kubernetes,moby,k8s  ',
            'updated  : 2019-01-27T13:17:51.831220+00:00  ',
            'uuid     : 5d44f0ca-4d92-4736-b913-41ac38503b1d',
            'versions :  ',
            '',
        ))
        data = (
            '## Description',
            '',
            'Debug and configure Kubernetes.',
            '',
            '## Solutions',
            '',
            '### The connection to the server <host>:6443 was refused - did you specify the right host or port?',
            '',
            '    # Delete cache',
            '    ls -al ~/.kube/cache',
            '    rm -drf ~/.kube/cache',
            '',
            '### Kubernetes networking',
            '',
            '    # Flannel based networking',
            '    #',
            '    # Connecting PODs to host',
            '    #',
            '    # Containers in PODs share the same namespace. This allows communicating',
            '    # other containers withing a POD through localhost. Virtual bridge allows',
            '    # a POD to communicate with other PODs through the host. A virtual bridge',
            '    # is created from virtual interface pairs (veth) where one side is in a',
            '    # container and the other in the host root namespace. A virtual bridge',
            '    # uses e.g. Linux bridge or OpenvSwitch (OVS) for connectivity between',
            '    # containers in POD and a external (real) interface.',
            '    #',
            '    # Eeach POD thinks it has a totally normal ethernet device called eth0',
            '    # to make network requests through. But Kubernetes is faking it its',
            '    # just a virtual ethernet connection.',
            '    #',
            '    # When a POD communicates with another POD in the same node, the virtual',
            '    # bridge asks all connected devices (i.e. PODs) if they have destination',
            '    # IP address.',
            '    #',
            '    # When a POD communicates with another POD in another node, a virtual',
            '    # bridge (L2) like cni0 is linked via VXLAN tunnel setup by Flannel to',
            '    # other nodes. When a POD is in another node, the virtual bride will',
            '    # fall to the default GW.',
            '    #',
            '    # Iptables are used to forward IP packets between PODs.',
            '    #',
            '    # Example configuration output',
            '    #',
            '    # [2020-02-03T15:46:25 root@hla-testing] $ nsenter -t 21410 -n ip addr | grep -A3 eth0',
            '    # 3: eth0@if61: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8092 qdisc noqueue state UP group default',
            '    #     link/ether 66:be:4a:6a:56:0b brd ff:ff:ff:ff:ff:ff link-netnsid 0',
            '    #     inet 10.244.0.59/24 scope global eth0',
            '    #        valid_lft forever preferred_lft forever',
            '    # [2020-02-03T15:47:19 root@hla-testing] $ ip link show | grep -A2 "61: "',
            '    # 61: veth71b19139@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8092 qdisc noqueue master cni0 state UP mode DEFAULT group default',  # pylint: disable=line-too-long
            '    #     link/ether e2:b7:f4:a3:da:f6 brd ff:ff:ff:ff:ff:ff link-netnsid 28',
            '    # [2020-02-03T15:51:02 root@hla-testing] $ ip -d l show flannel.1',
            '    # 5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8092 qdisc noqueue state UNKNOWN mode DEFAULT group default',
            '    #     link/ether b6:93:45:98:a3:b7 brd ff:ff:ff:ff:ff:ff promiscuity 0',
            '    #     vxlan id 1 local 192.168.1.11 dev eth1 srcport 0 0 dstport 8472 nolearning ageing 300 noudpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535',  # pylint: disable=line-too-long
            '    #',
            '    # Interface links from the example configuration.',
            '    #',
            '    # eth0@if61 --> veth71b19139@if3 --> master cni0 --> vxlan --> flannel.1',
            '    #',
            '    #            5        61   veth      3',
            '    # flannel.1  x  cni0  x -----------> x eth0',
            '',
            '    # List bridges/links on the host.',
            '    ip link show',
            '    brctl show',
            '',
            '    # Network namespaces can typically be listed using ip netns list.',
            '    # However, if the container runtime is Docker, you will not be able to',
            '    # list namespaces this way because Docker does not sym-link the',
            '    # namespaces under /var/run/netns.',
            '    #',
            '    # You can enable ip netns namespace functionality by creating the',
            '    # necessary sym-link.',
            '    ln -s /var/run/docker/netns /var/run/netns',
            '',
            '    # List iptables.',
            '    sudo iptables -L # there\'s an implicit `-t filter` here,',
            '    sudo iptables -L -t nat',
            '    sudo iptables -L -t mangle',
            '    sudo iptables -L -t raw',
            '    sudo iptables-save',
            '',
            '    # List PODs IP addresses',
            '    kubectl get pod --namespace ucim -o wide',
            '',
            '    # List pods',
            '    crictl pods',
            '    crictl inspectp 680df9452dc61',
            '',
            '    # List interfaces in container and find the corresponding Veth endpont.',
            '    docker ps | grep engine',
            '    docker inspect --format \'{{ .State.Pid }}\' 2080cd573626  # Get pid',
            '    nsenter -t 9135 -n ip addr',
            '    ip link list',
            '',
            '    # Get Flannel configuration',
            '    kubectl -n kube-system get configmap kube-flannel-cfg -o yaml',
            '',
            '    # Show node Veth IP range.',
            '    kubectl get nodes -o jsonpath=\'{range .items[*]} {.metadata.name}{"  "}{.spec.podCIDR}{"',
            '"}{end}\'',
            '',
            '    # Routing table shows how traffic for the local POD CIDR 10.244.0.0/24',
            '    # is routed to the integration bridge cni0 whereas the POD CIDRs for',
            '    # the other hosts are routed to the flannel.1 port with the other',
            '    # bridges as gateways, hence the container overlay network',
            '    route -n',
            '',
            '    # Flush routing tables',
            '    ip route flush cache',
            '',
            '    # list ARP tables',
            '    arp -a',
            '',
            '### Routes deleted',
            '',
            '    # In order to create cni0 or docker0 routes again, change to interface',
            '    # state down and then up.',
            '    route -n',
            '    ip link set dev docker0 down',
            '    ip link set dev docker0 up',
            '    ip link set dev cni0 down',
            '    ip link set dev cni0 up',
            '    route -n',
            '',
            '## Commands',
            '',
            '    # Versions',
            '    kubectl version',
            '    kubectl version -o yaml',
            '',
            '    # Configuration',
            '    cat ~/.kube/config',
            '',
            '    # Linux kernel parameters.',
            '    sysctl -a | grep ip_forward',
            '',
            '## Configurations',
            '',
            '## References',
            '',
            '### Kubernetes and iptables',
            '',
            '    # [1] Explanation of Kubernetes and iptables.',
            '    > https://msazure.club/kubernetes-services-and-iptables/',
            '',
            '    # [2] Traversing iptables',
            '    > https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html#TRAVERSINGOFTABLES',
            '',
            '    # [3] Kubernetes networking',
            '    > https://www.ciscolive.com/c/dam/r/ciscolive/emea/docs/2018/pdf/BRKDCN-2390.pdf',
            '',
            '## Whiteboard',
            ''
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert len(collection) == 1
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'Debug Kubernetes'
        assert resource.description == ('Debug and configure Kubernetes')
        assert resource.name == ''
        assert resource.groups == ('k8s',)
        assert resource.tags == ('debug', 'docker', 'howto', 'k8s', 'kubernetes', 'moby')
        assert resource.links == (
            'https://msazure.club/kubernetes-services-and-iptables/',
            'https://www.ciscolive.com/c/dam/r/ciscolive/emea/docs/2018/pdf/BRKDCN-2390.pdf',
            'https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html#TRAVERSINGOFTABLES',
        )
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == 'howto-debug-kubernetes.md'
        assert resource.created == '2018-02-15T13:49:38.000001+00:00'
        assert resource.updated == '2019-01-27T13:17:51.831220+00:00'
        assert resource.uuid == '5d44f0ca-4d92-4736-b913-41ac38503b1d'

    def test_parser_solution_009(self):
        """Test parsing solution.

        Test case verifies that Markdown content brief description is parsed
        correctly. In this case the solution data contains '@' mark which is
        also used in the Markdown solution header. The parser must read only
        the first line of the solution to parse the header.
        """

        text = Const.NEWLINE.join((
            '# How-to Makefiles @make',
            '',
            '> This solution gives examples how to use Makefiles.',
            '',
            '>',
            '',
            '## Description',
            '',
            'This solution defines how to use Makefiles in various use cases.',
            '',
            '## Solutions',
            '',
            '    # Make sure that the last line of the target is tabbed. If spaces',
            '    # are used, it will break Makefile tab completion by adding extra',
            '    # targets to e.g. \'make docker<tab><tab>\'.',
            '    docker-build:',
            '            $(export-env-conditionally)',
            '            time docker build -t $(REGISTRY)$(IMAGE):$(VERSION) \\',
            '                    --build-arg VERSION=$(VERSION) \\',
            '                    --build-arg COMMIT_SHA=$(BUILD) \\',
            '                    --build-arg BUILD_DATE=$(DATE) \\',
            '                    --build-arg IMAGE_NAME=$(IMAGE):$(VERSION) .',
            '',
            '    docker-test:',
            '            $(export-env-conditionally)',
            '            echo "test ucim image: $(REGISTRY)$(IMAGE):$(VERSION)"',
            '            time docker-compose -f Composefile.tests up --abort-on-container-exit || (docker-compose -f Composefile.tests down; exit 1)',  # pylint: disable=line-too-long
            '            time docker-compose -f Composefile.tests down',
            '',
            '    help:',
            '            set +x;',
            '            @echo \'Cleaning targets:\'',
            '            @echo \'  clean                 - Clean all targets.\'',
            '            @echo \'\'',
            '',
            '## Commands',
            '',
            '## Configurations',
            '',
            '## References',
            '',
            '## Whiteboard',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2019-08-28T07:08:38.284222+00:00  ',
            'digest   : eafc61a6d586384d5453671afba832885cbc082b99037a6e1038e59b7a216aa8  ',
            'filename : howto-makefile.md  ',
            'name     : how-to makefile  ',
            'source   :  ',
            'tags     : bash,make,makefile,howto  ',
            'updated  : 2019-08-28T07:35:32.241764+00:00  ',
            'uuid     : 66e4d19f-3ecc-40bc-941a-f08776395e08  ',
            'versions :  ',
            '',
        ))
        data = (
            '## Description',
            '',
            'This solution defines how to use Makefiles in various use cases.',
            '',
            '## Solutions',
            '',
            '    # Make sure that the last line of the target is tabbed. If spaces',
            '    # are used, it will break Makefile tab completion by adding extra',
            '    # targets to e.g. \'make docker<tab><tab>\'.',
            '    docker-build:',
            '            $(export-env-conditionally)',
            '            time docker build -t $(REGISTRY)$(IMAGE):$(VERSION) \\',
            '                    --build-arg VERSION=$(VERSION) \\',
            '                    --build-arg COMMIT_SHA=$(BUILD) \\',
            '                    --build-arg BUILD_DATE=$(DATE) \\',
            '                    --build-arg IMAGE_NAME=$(IMAGE):$(VERSION) .',
            '',
            '    docker-test:',
            '            $(export-env-conditionally)',
            '            echo "test ucim image: $(REGISTRY)$(IMAGE):$(VERSION)"',
            '            time docker-compose -f Composefile.tests up --abort-on-container-exit || (docker-compose -f Composefile.tests down; exit 1)',  # pylint: disable=line-too-long
            '            time docker-compose -f Composefile.tests down',
            '',
            '    help:',
            '            set +x;',
            '            @echo \'Cleaning targets:\'',
            '            @echo \'  clean                 - Clean all targets.\'',
            '            @echo \'\'',
            '',
            '## Commands',
            '',
            '## Configurations',
            '',
            '## References',
            '',
            '## Whiteboard',
            ''
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert len(collection) == 1
        assert resource.category == Const.SOLUTION
        assert resource.data == data
        assert resource.brief == 'How-to Makefiles'
        assert resource.description == ('This solution gives examples how to use Makefiles.')
        assert resource.name == 'how-to makefile'
        assert resource.groups == ('make',)
        assert resource.tags == ('bash', 'howto', 'make', 'makefile')
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == 'howto-makefile.md'
        assert resource.created == '2019-08-28T07:08:38.284222+00:00'
        assert resource.updated == '2019-08-28T07:35:32.241764+00:00'
        assert resource.uuid == '66e4d19f-3ecc-40bc-941a-f08776395e08'

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
            '> [1] https://docs.docker.com/engine/reference/commandline/images/  ',
            '[2] https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '## Meta',
            '',
            '> category  : reference  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : ec6ff1c1e8c52bc2ca8de76c71cd2eebd4f5ca07e6bdd9bba42ad2154d40503b  ',
            'filename  :   ',
            'languages : python  ',
            'name      :   ',
            'source    :   ',
            'tags      : cleanup, container, python, docker-ce, moby  ',
            'updated   : 2018-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : docker-ce==1.1.1,moby!=2.7.0,moby>2.6.0,docker-ce<1.1.1',
            '',
        ))
        links = (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/'
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == 'Remove all exited containers and dangling images'
        assert resource.description == (
            'Remove all exited containers and dangling images. The command examples ' +
            'first remove all exited containers and the all dangling images.'
        )
        assert resource.name == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker-ce', 'moby', 'python')
        assert resource.links == links
        assert resource.source == ''
        assert resource.versions == ('docker-ce<1.1.1', 'docker-ce==1.1.1', 'moby!=2.7.0', 'moby>2.6.0')
        assert resource.languages == ('python',)
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2018-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == 'dae01bb8ba3cf8c850eabf5ea2abdfe84be14670fc041f6d3ca9c4150c7de1f1'

    def test_parser_reference_002(self):
        """Test parsing reference.

        Test case verifies that optional fields brief, groups and description
        can be ommitted and the content is still parsed correctly.
        """

        text = Const.NEWLINE.join((
            '# @default',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/',
            '',
            '## Meta',
            '',
            '> category  : reference  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0bd50d9035d987a2407b0dfe68aea761fadf1306556bd5fafea3f59bef51c826  ',
            'filename  :   ',
            'languages : shell,python  ',
            'name      :   ',
            'source    :   ',
            'tags      : cleanup, container, python, docker-ce, moby  ',
            'updated   : 2018-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : docker_ce==1.1.1,moby!=2.7.0',
            '',
        ))
        links = ('https://docs.docker.com/engine/reference/commandline/images/',)
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ('default',)
        assert resource.tags == ('cleanup', 'container', 'docker-ce', 'moby', 'python')
        assert resource.links == links
        assert resource.source == ''
        assert resource.versions == ('docker_ce==1.1.1', 'moby!=2.7.0')
        assert resource.languages == ('python', 'shell')
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2018-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '0d1ea43e0200b200175e73b22cb1a9db472251c0250fc2070ea9cc6025ee26f7'

    def test_parser_reference_003(self):
        """Test parsing reference.

        Test case verifies that the default group is added even when the group
        is not defined at all.
        """

        text = Const.NEWLINE.join((
            '# @',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/images/',
            '',
            '## Meta',
            '',
            '> category  : reference  ',
            'created   : 2017-10-12T11:52:11.000001+00:00  ',
            'digest    : 0bd50d9035d987a2407b0dfe68aea761fadf1306556bd5fafea3f59bef51c826  ',
            'filename  :   ',
            'languages :   ',
            'name      :   ',
            'source    :   ',
            'tags      : cleanup, container, python, docker-ce, moby  ',
            'updated   : 2018-10-12T11:52:11.000001+00:00  ',
            'uuid      : f21c6318-8830-11e8-a114-2c4d54508088  ',
            'versions  : docker_ce==1.1.1,moby!=2.7.0',
            '',
        ))
        links = ('https://docs.docker.com/engine/reference/commandline/images/',)
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ('default',)
        assert resource.tags == ('cleanup', 'container', 'docker-ce', 'moby', 'python')
        assert resource.links == links
        assert resource.source == ''
        assert resource.versions == ('docker_ce==1.1.1', 'moby!=2.7.0')
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.created == '2017-10-12T11:52:11.000001+00:00'
        assert resource.updated == '2018-10-12T11:52:11.000001+00:00'
        assert resource.uuid == 'f21c6318-8830-11e8-a114-2c4d54508088'
        assert resource.digest == '0d1ea43e0200b200175e73b22cb1a9db472251c0250fc2070ea9cc6025ee26f7'
