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

"""test_cli_search_snippet: Test workflows for searching snippets."""

import pytest

from snippy.cause import Cause
from snippy.config.constants import Constants as Const
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliSearchSnippet(object):  # pylint: disable=too-many-public-methods
    """Test workflows for searching snippets."""

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_001(self, snippy, capsys):
        """Search snippet from all fields.

        Search snippets from all fields. The match is made from one
        snippet content data.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'redis', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_002(self, snippy, capsys):
        """Search snippet from all fields.

        Search snippets from all fields. The match is made from one snippet
        brief description.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'all', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_003(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Search snippets from all fields. The match is made from two
        ##        snippets group metadata.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'docker', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_004(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Search snippets from all fields. The match is made from two
        ##        snippets tags metadata.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'moby', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_005(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Search snippets from all fields. The match is made from one
        ##        snippet links metadata.
        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'tutorials', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_006(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Search snippets from all fields. The match is made from one
        ##        snippet digest.
        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '53908d68425c61dc', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_007(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Search snippets from all fields with two keywords. The match
        ##        is made from two different snippets. In this search keywords
        ##        are separated by comma.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'redis,--quiet', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_008(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Search snippets from all fields with three keywords. The
        ##        match is made two different snippts. In this case search
        ##        keywords are separated by spaces.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'netcat --quiet all', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_009(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: List all snippets by defining search criteria of search all
        ##        to 'match any'.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_010(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: List all snippets by leaving search criteria for 'search
        ##        all fields' out completely. This is translated to 'match
        ##        any'.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_011(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: List all snippets by leaving search criteria of search all as empty. This is
        ##        translated to 'match any'.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('snippy')
    def test_cli_search_snippet_012(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Try to search snippets when there are no content stored.
        ##        The used search keyword matches to 'match any' that tries
        ##        to list all the content.
        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_013(self, snippy, capsys):
        """Search snippet from all fields."""

        ## Brief: Try to search snippets with keyword that cannot be found.
        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sall', 'not-found', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_014(self, snippy, capsys):
        """Search snippet from tag field."""

        ## Brief: Search snippets from tag field. The match is made from one
        ##        snippet.
        output = (
            '1. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'netcat', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_015(self, snippy, capsys):
        """Search snippet from tag field."""

        ## Brief: Search snippets from tag field. No matches are made.
        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--stag', 'not-found', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_016(self, snippy, capsys):
        """Search snippet from tag field."""

        ## Brief: List all snippets by leaving search criteria for 'search
        ##        tags' out completely. This is translated to 'match any'.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err


    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_017(self, snippy, capsys):
        """Search snippet from group field."""

        ## Brief: Search snippets from group field. The match is made from one snippet.
        output = (
            '1. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sgrp', 'linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_018(self, snippy, capsys):
        """Search snippet from group field."""

        ## Brief: Search snippets from group field. No matches are made.
        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sgrp', 'not-found', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_019(self, snippy, capsys):
        """Search snippet from group field."""

        ## Brief: List all snippets by leaving search criteria for 'search
        ##        groups' out completely. This is translated to 'match any'.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sgrp', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'default-solutions', 'import-netcat')
    def test_cli_search_snippet_020(self, snippy, capsys):
        """Search snippet with regexp."""

        ## Brief: Search all content with regexp filter. The ansi characters
        ##        must be automatically disabled in when the --filter option
        ##        is used.
        output = (
            '$ docker rm --volumes $(docker ps --all --quiet)',
            '$ docker rm --force redis',
            '$ nc -v 10.183.19.189 443',
            '$ nmap 10.183.19.189',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--filter', '.*(\\$\\s.*)'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'default-solutions', 'import-netcat')
    def test_cli_search_snippet_021(self, snippy, capsys):
        """Search snippet with regexp."""

        ## Brief: Search all content with regexp filter. The ansi characters
        ##        must be automatically disabled in when the --filter option
        ##        is used. This must match to snippet and solution commands.
        output = (
            '$ docker rm --volumes $(docker ps --all --quiet)',
            '$ docker rm --force redis',
            '$ nc -v 10.183.19.189 443',
            '$ nmap 10.183.19.189',
            '',
            '$ ./filebeat -e -c config/filebeat.yml -d "*"',
            '$ nginx -V 2>&1 | grep -- \'--with-debug\'',
            '$ ls -al /var/log/nginx/',
            '$ unlink /var/log/nginx/access.log',
            '$ unlink /var/log/nginx/error.log',
            '$ nginx -s reload',
            '$ vi conf.d/default.conf',
            '$ docker exec -i -t $(docker ps | egrep -m 1 \'petelk/nginx\' | awk \'{print $1}\') /bin/bash',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--all', '--sall', '.', '--filter', '\\.*(\\$\\s.*)'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'default-solutions', 'import-netcat')
    def test_cli_search_snippet_022(self, snippy, capsys):
        """Search snippet with regexp."""

        ## Brief: Search all content with regexp filter. There are no matches.
        output = 'OK\n'
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--filter', 'not-found'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'default-solutions')
    def test_cli_search_snippet_023(self, snippy, capsys):
        """Search snippet with regexp."""

        ## Brief: Try to search all snippets with filter that is not
        ##        syntactically correct regular expression.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'NOK: listing matching content without filter because it was not syntactically correct regular expression',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--filter', '[invalid(regexp', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: listing matching content without filter because it was not syntactically correct regular expression'
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_024(self, snippy, capsys):
        """Search snippets with --content option."""

        ## Brief: Search snippets based on content data.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--content', 'docker rm --volumes $(docker ps --all --quiet)', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_025(self, snippy, capsys):
        """Search snippets with --content option."""

        ## Brief: Search snippets based on content data that matches to
        ##        beginnging of the content.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--content', 'docker rm --volumes', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_026(self, snippy, capsys):
        """Search snippets with --content option."""

        ## Brief: Search snippets based on content data that matches to a
        ##        string in the middle of a content.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--content', 'volumes', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_027(self, snippy, capsys):
        """Search snippet with --digest option."""

        ## Brief: Search snippet by explicitly defining short message digest.
        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '53908d68425c61dc', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_028(self, snippy, capsys):
        """Search snippet with --digest option."""

        ## Brief: Search snippet by explicitly defining long message digest.
        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5', '--no-ansi'])  # pylint: disable=line-too-long
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_029(self, snippy, capsys):
        """Search snippet with --digest option."""

        ## Brief: Search snippets by defining one digit message digest. In
        ##        this case the searched digit matches to two snippets.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '5', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_030(self, snippy, capsys):
        """Search snippet with --digest option."""

        ## Brief: Search snippets by defining empty string as message digest.
        ##        This matches to all content in all categories.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_031(self, snippy, capsys):
        """Search snippet from all fields and limit the search within specific group."""

        ## Brief: Search snippets from all fields of specific group. The match must
        ##        not be made from other than defined group. In this case the list
        ##        all must print the content of defined group.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--sgrp', 'docker', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_032(self, snippy, capsys):
        """Search snippet from all fields and limit the search within specific group."""

        ## Brief: Search snippets from all fields of from two different groups.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            '3. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--sgrp', 'docker,linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_033(self, snippy, capsys):
        """Search snippet from tag fields and limit the search within specific group."""

        ## Brief: Search snippets from tag fields of specific group. The match
        ##        must not be made from other than defined group. In this case
        ##        the list all must print the content of defined group.
        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'docker', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_034(self, snippy, capsys):
        """Search snippet from tag fields and limit the search within specific group."""

        ## Brief: Try to search snippets based on tag fields of specific
        ##        group. In this case there are no matches made.
        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_035(self, snippy, capsys):
        """Search snippets with special failures."""

        ## Brief: Try to search snippets without defining any search criteria.
        output = 'NOK: please define keyword, digest or content data as search criteria\n'
        cause = snippy.run(['snippy', 'search'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: please define keyword, digest or content data as search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_036(self, snippy, capsys):
        """Search snippets with special failures."""

        ## Brief: Try to search snippets defining filter but not any search
        ##        criteria. In this case the filter cannot be applied because
        ##        no search criteria is applied.
        output = 'NOK: please define keyword, digest or content data as search criteria\n'
        cause = snippy.run(['snippy', 'search', '--filter', '.*(\\$\\s.*)'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: please define keyword, digest or content data as search criteria'
        assert out == output
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
