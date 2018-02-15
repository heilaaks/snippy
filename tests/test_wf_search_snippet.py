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

"""test_wf_search_snippet.py: Test workflows for searching snippets."""

import sys

import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
    from StringIO import StringIO  # pylint: disable=import-error


class TestWfSearchSnippet(object):
    """Test workflows for searching snippets."""

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_sall(self, mock_isfile, mock_storage_file):
        """Search snippet from all fields."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Search snippets from all fields. The match is made from one snippet
        ##        content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'redis', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields. The match is made from one snippet
        ##        brief description.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                      '   $ docker rm --volumes $(docker ps --all --quiet)',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'all', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields. The match is made from two snippets
        ##        group metadata.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'docker', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields. The match is made from two snippets
        ##        tags metadata.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'moby', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields. The match is made from one snippet
        ##        links metadata.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'tutorials', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields. The match is made from one snippet
        ##        digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '53908d68425c61dc', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields with two keywords. The match is made
        ##        from two different snippets. In this search keywords are separated by
        ##        comma.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'redis,--quiet', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields with three keywords. The match is made two
        ##        different snippts. In this case search keywords are separated by spaces.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'netcat --quiet all', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: List all snippets by defining search criteria of search all to 'match any'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: List all snippets by leaving search criteria for 'search all fields' out
        ##        completely. This is translated to 'match any'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: List all snippets by leaving search criteria of search all as empty. This is
        ##        translated to 'match any'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to search snippets when there are no content stored. The used search
        ##        keyword matches to 'match any' that tries to list all the content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('NOK: cannot find content with given search criteria')
            snippy = Snippy()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--no-ansi'])  ## workflow
            assert cause == 'NOK: cannot find content with given search criteria'
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to search snippets with keyword that cannot be found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('NOK: cannot find content with given search criteria')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', 'not-found', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == 'NOK: cannot find content with given search criteria'
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_stag(self, mock_isfile, mock_storage_file):
        """Search snippet from tag field."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets from tag field. The match is made from one snippet.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Test if specific port is open @linux [f3fd167c64b6f97e]',
                      '   $ nc -v 10.183.19.189 443',
                      '   $ nmap 10.183.19.189',
                      '',
                      '   # linux,netcat,networking,port',
                      '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--stag', 'netcat', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from tag field. No matches are made.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('NOK: cannot find content with given search criteria')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--stag', 'not-found', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == 'NOK: cannot find content with given search criteria'
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: List all snippets by leaving search criteria for 'search tags' out
        ##        completely. This is translated to 'match any'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--stag', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_sgrp(self, mock_isfile, mock_storage_file):
        """Search snippet from group field."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets from group field. The match is made from one snippet.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Test if specific port is open @linux [f3fd167c64b6f97e]',
                      '   $ nc -v 10.183.19.189 443',
                      '   $ nmap 10.183.19.189',
                      '',
                      '   # linux,netcat,networking,port',
                      '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sgrp', 'linux', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from group field. No matches are made.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('NOK: cannot find content with given search criteria')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sgrp', 'not-found', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == 'NOK: cannot find content with given search criteria'
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: List all snippets by leaving search criteria for 'search groups' out
        ##        completely. This is translated to 'match any'.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sgrp', '', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_regxp(self, mock_isfile, mock_storage_file):
        """Search snippet with regexp."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search all content with regexp filter. The ansi characters must be
        ##        automatically disabled in when the --filter option is used.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('$ docker rm --volumes $(docker ps --all --quiet)',
                      '$ docker rm --force redis',
                      '$ nc -v 10.183.19.189 443',
                      '$ nmap 10.183.19.189',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            Solution.add_defaults(snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--filter', '.*(\\$\\s.*)'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search all content with regexp filter. The ansi characters must be
        ##        automatically disabled in when the --filter option is used. This
        ##        must match to snippet and solution commands.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('$ docker rm --volumes $(docker ps --all --quiet)',
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
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            Solution.add_defaults(snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--all', '--sall', '.', '--filter', '\\.*(\\$\\s.*)'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search all content with regexp filter. There are no matches.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            Solution.add_defaults(snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--filter', 'not-found'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to search all snippets with filter that is not syntactically correct
        ##        regular expression.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'NOK: listing matching content without filter because it was not syntactically correct regular expression')
            snippy = Snippet.add_defaults()
            Solution.add_defaults(snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--filter', '[invalid(regexp', '--no-ansi'])  ## workflow
            assert cause == 'NOK: listing matching content without filter because it was not syntactically correct regular expression'
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_data(self, mock_isfile, mock_storage_file):
        """Search snippets with --content option."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                      '   $ docker rm --volumes $(docker ps --all --quiet)',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--content', 'docker rm --volumes $(docker ps --all --quiet)', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets based on content data that matches to beginnging of the content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                      '   $ docker rm --volumes $(docker ps --all --quiet)',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--content', 'docker rm --volumes', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets based on content data that matches to a string in the middle
        ##        of a content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                      '   $ docker rm --volumes $(docker ps --all --quiet)',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--content', 'volumes', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_searching_snippet_with_digest(self, mock_isfile, mock_storage_file):
        """Search snippet with --digest option."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippet by explicitly defining short message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--digest', '53908d68425c61dc', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippet by explicitly defining long message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                      '',
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--digest', '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5', '--no-ansi'])  ## workflow  pylint: disable=line-too-long
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets by defining one digit message digest. In this case the
        ##        searched digit matches to two snippets.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--digest', '5', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets by defining empty string as message digest. This matches
        ##        to all content in all categories.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--digest', '', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_sall_sgrp(self, mock_isfile, mock_storage_file):
        """Search snippet from all fields and limit the search within specific group."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Search snippets from all fields of specific group. The match must
        ##        not be made from other than defined group. In this case the list
        ##        all must print the content of defined group.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--sgrp', 'docker', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields of from two different groups.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--sgrp', 'docker,linux', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_stag_sgrp(self, mock_isfile, mock_storage_file):
        """Search snippet from tag fields and limit the search within specific group."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Search snippets from tag fields of specific group. The match must
        ##        not be made from other than defined group. In this case the list
        ##        all must print the content of defined group.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
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
                      'OK')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'docker', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to search snippets based on tag fields of specific group. In this
        ##        case there are no matches made.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('NOK: cannot find content with given search criteria')
            snippy = Snippet.add_defaults()
            Snippet.add_one(Snippet.NETCAT, snippy)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'linux', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == 'NOK: cannot find content with given search criteria'
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_special_cases(self, mock_isfile, mock_storage_file):
        """Search snippets with special failures."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Try to search snippets without defining any search criteria.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = 'NOK: please define keyword, digest or content data as search criteria'
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search'])  ## workflow
            assert cause == 'NOK: please define keyword, digest or content data as search criteria'
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to search snippets defining filter but not any search criteria.
        ##        In this case the filter cannot be applied because no search criteria
        ##        is applied.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = 'NOK: please define keyword, digest or content data as search criteria'
            snippy = Snippet.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--filter', '.*(\\$\\s.*)'])  ## workflow
            assert cause == 'NOK: please define keyword, digest or content data as search criteria'
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
