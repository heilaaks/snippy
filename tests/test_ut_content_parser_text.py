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

"""test_ut_parser: Test ContentParserText() class."""

from snippy.constants import Constants as Const
from snippy.content.parsers.text import ContentParserText as Parser
from snippy.content.collection import Collection


class TestUtContentParserText(object):  # pylint: disable=too-many-public-methods
    """Test ContentParserText() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+00:00'

    def test_parser_snippet_001(self):
        """Test parsing snippet.

        Test case verifies that links are parsed from snippet template where
        the links are the last item in the template. There is no newline at the
        end of the last link.

        Test case verifies that tags are parsed correctly when there is no
        newline after the next item. Also tags must be sorted after parsing.

        Test case verifies that the trailing whitespaces are removed from each
        tag and link. Also links must be sorted after parsing.

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
            '  moby,cleanup,  container,docker,docker-ce,image  ',
            '# Add optional links below one link per line.',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            '  https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rmi/  '
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        assert resource.brief == 'Remove docker image with force'
        assert resource.description == 'Remove all hanging docker images.'
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_snippet_002(self):
        """Test parsing snippet.

        Test case verifies that groups are parsed correctly if there is a list
        of groups. The groups must be sorted after parsing.

        This case has also multiline description with multiple sequential
        spaces. In this case there is empty line after the description before
        the next content tag.
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        assert resource.brief == 'Remove docker image with force'
        assert resource.description == 'Remove all hanging docker images. This uses force command and it removes all with force.'
        assert resource.groups == ('docker', 'moby')
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'docker rm $(docker ps --all -q -f status=exited)',
            'docker images -q --filter dangling=true | xargs docker rm'
        )
        assert resource.brief == 'Remove docker image with force'
        assert resource.description == 'Remove all hanging docker images. This uses force command and it removes all with force.'
        assert resource.groups == ('docker', 'moby')
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        assert not collection

    def test_parser_snippet_005(self):
        """Test parsing snippet.

        Try to match snippet content where the second snippet content does not
        match to any of the snippet tags. In this case the description field is
        missing totally.
        """

        text = '\n'.join((
            '# Add mandatory snippet below.',
            '# Remove docker image with.',
            'docker rm $(docker ps --all -q -f status=exited)',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        assert len(collection) == 1
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            '# Remove docker image with.',
            'docker rm $(docker ps --all -q -f status=exited)'
        )
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.groups == ()
        assert resource.tags == ()
        assert resource.links == ()
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_snippet_006(self):
        """Test parsing snippet.

        Test case verifies that snippet data with links is parsed correctly.
        This case also verifies that the aligned comments are parsed correctly
        to internal format.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory snippet below.',
            'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./  #  Compress folder excluding the tar.',
            'tar tvf mytar.tar.gz                               #  List content of compressed tar.',
            'tar xfO mytar.tar.gz manifest.json                 #  Cat file in compressed tar.',
            'tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"  #  Extract and exclude one file.',
            'tar -xf mytar.tar.gz manifest.json                 #  Extract only one file.',
            '',
            '# Add optional brief description below.',
            'Manipulate compressed tar files',
            '',
            '# Add optional description below.',
            '',
            '',
            '# Add optional comma separated list of groups below.',
            'linux',
            '',
            '# Add optional comma separated list of tags below.',
            'howto,linux,tar,untar',
            '',
            '# Add optional links below one link per line.',
            '',
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
            'tar -xf mytar.tar.gz manifest.json  #  Extract only one file.',
        )
        assert resource.brief == 'Manipulate compressed tar files'
        assert resource.description == ''
        assert resource.groups == ('linux',)
        assert resource.tags == ('howto', 'linux', 'tar', 'untar')
        assert resource.links == ()
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_snippet_007(self):
        """Test parsing snippet.

        Test case verifies that snippet data with explaining comments is parsed
        correctly. In this case the comments are not aligned.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory snippet below.',
            'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./ # Compress folder excluding the tar.',
            'tar tvf mytar.tar.gz # List content of compressed tar.',
            'tar xfO mytar.tar.gz manifest.json # Cat file in compressed tar.',
            'tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"  #  Extract and exclude one file.',
            'tar -xf mytar.tar.gz manifest.json # Extract only one file.',
            '',
            '# Add optional brief description below.',
            'Manipulate compressed tar files',
            '',
            '# Add optional description below.',
            '',
            '',
            '# Add optional comma separated list of groups below.',
            'linux',
            '',
            '# Add optional comma separated list of tags below.',
            'howto,linux,tar,untar',
            '',
            '# Add optional links below one link per line.',
            '',
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
            'tar -xf mytar.tar.gz manifest.json  #  Extract only one file.',
        )
        assert resource.brief == 'Manipulate compressed tar files'
        assert resource.description == ''
        assert resource.groups == ('linux',)
        assert resource.tags == ('howto', 'linux', 'tar', 'untar')
        assert resource.links == ()
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_snippet_008(self):
        """Test parsing snippet.

        Test case verifies that snippet with versions, name, filename and
        source fields is parsed correctly. In this case template tags are
        not removed when the snippet is parsed.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory snippet below.',
            'tar tvf mytar.tar.gz',
            '',
            '# Add optional brief description below.',
            'Manipulate compressed tar files',
            '',
            '# Add optional description below.',
            '<description>',
            '',
            '# Add optional comma separated list of groups below.',
            'linux',
            '',
            '# Add optional comma separated list of tags below.',
            'howto,linux,tar,untar',
            '',
            '# Add optional links below one link per line.',
            '',
            '# Add optional comma separated list of key=value versions below.',
            '<versions>',
            '',
            '# Add optional name below.',
            '<name>',
            '',
            '# Add optional filename below.',
            '<filename>',
            '',
            '# Add optional source reference below.',
            '<source>',
            '',
            ''
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == ('tar tvf mytar.tar.gz',)
        assert resource.brief == 'Manipulate compressed tar files'
        assert resource.description == ''
        assert resource.groups == ('linux',)
        assert resource.tags == ('howto', 'linux', 'tar', 'untar')
        assert resource.links == ()
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_snippet_009(self):
        """Test parsing snippet.

        Test case verifies that snippet with versions, name, filename and
        source fields is parsed correctly. In this case each field contains
        a valid value.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory snippet below.',
            'tar tvf mytar.tar.gz',
            '',
            '# Add optional brief description below.',
            'Manipulate compressed tar files',
            '',
            '# Add optional description below.',
            'short description',
            '',
            '# Add optional comma separated list of groups below.',
            'linux',
            '',
            '# Add optional comma separated list of tags below.',
            'howto,linux,tar,untar',
            '',
            '# Add optional links below one link per line.',
            'https://alpinelinux.org/',
            '',
            '# Add optional comma separated list of key=value versions below.',
            'python=3.7.0,alpine=3.9',
            '',
            '# Add optional name below.',
            'manage tar files',
            '',
            '# Add optional filename below.',
            'tar-file-operations.mkdn',
            '',
            '# Add optional source reference below.',
            'https://github.com/tldr-pages/tldr/blob/master/pages/linux/alpine.md',
            '',
            ''
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == ('tar tvf mytar.tar.gz',)
        assert resource.brief == 'Manipulate compressed tar files'
        assert resource.description == 'short description'
        assert resource.groups == ('linux',)
        assert resource.tags == ('howto', 'linux', 'tar', 'untar')
        assert resource.links == ('https://alpinelinux.org/',)
        assert resource.versions == ('alpine=3.9', 'python=3.7.0')
        assert resource.name == 'manage tar files'
        assert resource.filename == 'tar-file-operations.mkdn'
        assert resource.source == 'https://github.com/tldr-pages/tldr/blob/master/pages/linux/alpine.md'

    def test_parser_snippet_010(self):
        """Test parsing snippet.

        Try to parse snippet which version does not follow required syntax. In
        This case there is one version that has correct syntax which must be
        stored in the content.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory snippet below.',
            'tar tvf mytar.tar.gz',
            '',
            '# Add optional brief description below.',
            '',
            '# Add optional description below.',
            '',
            '# Add optional comma separated list of groups below.',
            '',
            '# Add optional comma separated list of tags below.',
            '',
            '# Add optional links below one link per line.',
            '',
            '# Add optional comma separated list of key=value versions below.',
            'python=^3.7.0,alpine!=3.9,kafka',
            '',
            '# Add optional name below.',
            '',
            '# Add optional filename below.',
            '',
            '# Add optional source reference below.',
            '',
            ''
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == ('tar tvf mytar.tar.gz',)
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.groups == () #('default',)
        assert resource.tags == ()
        assert resource.links == ()
        assert resource.versions == ('alpine!=3.9',)
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_solution_001(self):
        """Test parsing solution.

        Test case verifies that a solution content can be parsed.

        Links that are not starting with tag '> ' must not be read to resource
        links. Links must be sorted after parsing.

        Tags must be sorted after parsing.
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
            '    # Fake links below with incorrect preceding tags that must not be read.',
            '    >  https://github.com/garo/logs2kafka',
            '    #  https://github.com/garo/logs2kafka',
            '    #  https://github.com/garo/logs2kafka',
            '  https://github.com/garo/logs2kafka',
            '    >  http://github.com/garo/logs2kafka',
            '    >> http://github.com/garo/logs2kafka',
            '    >>http://github.com/garo/logs2kafka',
            '',
            '    # /1/ https://github.com/elastic/kibana/issues/5230#issuecomment-288737969'
            '    $ vi kibana.yaml'
            '      server.basePath: "/kibana"'
            '      xpack.reporting.kibanaApp: "/kibana/app/kibana"'
            '    $ vi default.conf'
            '      server {'
            '          location /kibana/ {'
            '              proxy_pass  http://kibana:5601;'
            '              proxy_http_version 1.1;'
            '              proxy_set_header Upgrade $http_upgrade;'
            '              proxy_set_header Connection "upgrade";'
            '              proxy_set_header Host $host;'
            '              rewrite /kibana/(.*)$ /$1 break;'
            '          }'
            '          # Handle landing url without trailing slash.'
            '          location = /kibana {'
            '             return 302 /kibana/;'
            '          }'
            '      }'
            ''
            '################################################################################',
            '## commands',
            '################################################################################',
            '',
            '################################################################################',
            '## solutions',
            '################################################################################',
            '',
            '    # Passing query parameter',
            '    # =======================',
            '    #',
            '    # Pass query parameters from nginx location by adding $is_args$args:',
            '    location ~ /elastic(/|$)(.*) {',
            '        set $elasticsearch_servers elasticsearch;',
            '        proxy_pass                 http://$elasticsearch_servers:9200/$2$is_args$args;',
            '    }',
            '',
            '    # Configure Kibana behind specific base path',
            '    # ==========================================',
            '    #',
            '    # It may be that the Kibana does not working correctly with base',
            '    # path. Because of this /1/, a rewrite is currently needed. It',
            '    # may be because of reroute below, the forwarding with 302 does',
            '    # not work. It is left as an example here.',
            '    # /1/  https://github.com/elastic/kibana/issues/5230#issuecomment-288737969',
            '    $ vi kibana.yaml',
            '      server.basePath: "/kibana"',
            '      xpack.reporting.kibanaApp: "/kibana/app/kibana"',
            '    $ vi default.conf',
            '      server {',
            '          location /kibana/ {',
            '              proxy_pass http://kibana:5601;',
            '              proxy_http_version 1.1;',
            '              proxy_set_header Upgrade $http_upgrade;',
            '              proxy_set_header Connection "upgrade";',
            '              proxy_set_header Host $host;',
            '              rewrite /kibana/(.*)$ /$1 break;',
            '          }',
            '          # Handle landing url without trailing slash.',
            '          location = /kibana {',
            '             return 302 /kibana/;',
            '          }',
            '      }',
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == 'This is a one line solution description.'
        assert resource.groups == ('docker',)
        assert resource.tags == ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        assert resource.links == (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == 'kubernetes-docker-log-driver-kafka.txt'
        assert resource.source == ''

    def test_parser_solution_002(self):
        """Test parsing solution.

        Test case verifies that multiline solution description can be parsed.
        In this case there is an empty line after the description.
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == 'This is two line solution description.'
        assert resource.groups == ('docker',)
        assert resource.tags == ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        assert resource.links == (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == 'kubernetes-docker-log-driver-kafka.txt'
        assert resource.source == ''

    def test_parser_solution_003(self):
        """Test parsing solution.

        Test case verifies that multiline solution description can be parsed.
        In this case there is no empty line after the description.
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == 'This is two line solution description without newline before next header.'
        assert resource.groups == ('docker',)
        assert resource.tags == ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        assert resource.links == (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == 'kubernetes-docker-log-driver-kafka.txt'
        assert resource.source == ''

    def test_parser_solution_004(self):
        """Test parsing solution.

        Test case verifies that solution is parsed correctly when the
        description is not defined.this case the description is not defined.
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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SOLUTION
        assert resource.data == tuple(text.split(Const.DELIMITER_DATA))
        assert resource.brief == 'Testing docker log drivers'
        assert resource.description == ''
        assert resource.groups == ('docker',)
        assert resource.tags == ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin')
        assert resource.links == (
            'https://github.com/MickayG/moby-kafka-logdriver',
            'https://github.com/garo/logs2kafka',
            'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == 'kubernetes-docker-log-driver-kafka.txt'
        assert resource.source == ''

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        assert not collection

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == 'How to write commit messages'
        assert resource.description == 'How to write git commit.'
        assert resource.groups == ('git',)
        assert resource.tags == ('commit', 'git', 'howto', 'message', 'scm')
        assert resource.links == links
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_reference_002(self):
        """Test parsing reference.

        Test case verifies that links are parsed from reference template where
        the links are the first item in the template. There is no newline after
        the links before the next section.

        Tags must be sorted after parsing.
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
            'git,howto,message,scm,commit'
        ))
        links = (
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/'
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == 'How to write commit messages'
        assert resource.description == 'How to write git commit.'
        assert resource.groups == ('git',)
        assert resource.tags == ('commit', 'git', 'howto', 'message', 'scm')
        assert resource.links == links
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == 'How to write commit messages'
        assert resource.description == 'How to write git commit.'
        assert resource.groups == ('git', 'moby')
        assert resource.tags == ('commit', 'git', 'howto', 'message', 'scm')
        assert resource.links == links
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        assert not collection

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
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == data
        assert resource.brief == 'Remove docker image with force'
        assert resource.description == 'Remove docker image.'
        assert resource.groups == ('docker',)
        assert resource.tags == ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby')
        assert resource.links == (
            'https://docs.docker.com/engine/reference/commandline/images/',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            'https://docs.docker.com/engine/reference/commandline/rmi/'
        )
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_reference_006(self):
        """Test parsing reference.

        Test case verifies that reference with versions, name, filename and
        source fields is parsed correctly. In this case template tags are
        not removed when the reference is parsed.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '',
            '# Add optional brief description below.',
            'How to write commit messages',
            '',
            '# Add optional description below.',
            'How to write git commit',
            '',
            '# Add optional comma separated list of groups below.',
            'git',
            '',
            '# Add optional comma separated list of tags below.',
            'commit,git,howto,message,scm'
            '',
            '# Add optional comma separated list of key=value versions below.',
            '<versions>',
            '',
            '# Add optional name below.',
            '<name>',
            '',
            '# Add optional filename below.',
            '<filename>',
            '',
            '# Add optional source reference below.',
            '<source>',
            '',
            ''
        ))
        links = (
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/'
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == 'How to write commit messages'
        assert resource.description == 'How to write git commit'
        assert resource.groups == ('git',)
        assert resource.tags == ('commit', 'git', 'howto', 'message', 'scm')
        assert resource.links == links
        assert resource.versions == ()
        assert resource.name == ''
        assert resource.filename == ''
        assert resource.source == ''

    def test_parser_reference_007(self):
        """Test parsing reference.

        Test case verifies that reference with versions, name, filename and
        source fields is parsed correctly. In this case each field contains
        a valid value.
        """

        text = '\n'.join((
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory links below one link per line.',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/',
            '',
            '# Add optional brief description below.',
            'How to write commit messages',
            '',
            '# Add optional description below.',
            'How to write git commit',
            '',
            '# Add optional comma separated list of groups below.',
            'git',
            '',
            '# Add optional comma separated list of tags below.',
            'commit,git,howto,message,scm'
            '',
            '# Add optional comma separated list of key=value versions below.',
            'git<=1.1.1,python>=2.7.0,python==3.7.0',
            '',
            '# Add optional name below.',
            'git-help-text',
            '',
            '# Add optional filename below.',
            'git.mkdn',
            '',
            '# Add optional source reference below.',
            'https://github.com/',
            '',
            ''
        ))
        links = (
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages',
            'https://chris.beams.io/posts/git-commit/'
        )
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.REFERENCE
        assert resource.data == links
        assert resource.brief == 'How to write commit messages'
        assert resource.description == 'How to write git commit'
        assert resource.groups == ('git',)
        assert resource.tags == ('commit', 'git', 'howto', 'message', 'scm')
        assert resource.links == links
        assert resource.versions == ('git<=1.1.1', 'python>=2.7.0')
        assert resource.name == 'git-help-text'
        assert resource.filename == 'git.mkdn'
        assert resource.source == 'https://github.com/'

    def test_parser_unknown_001(self):
        """Test parsing unidentified content.

        Try to parse content which category is not identified.
        """

        text = '\n'.join((
            'git, moby',
            '# unknown 1.',
            'commit,git,howto,message,scm'
        ))
        collection = Collection()
        Parser(self.TIMESTAMP, text, collection).read_collection()
        assert not collection
