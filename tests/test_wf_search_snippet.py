#!/usr/bin/env python3

"""test_wf_search_snippet.py: Test workflows for searching snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error


class TestWfSearchSnippet(unittest.TestCase):
    """Test workflows for searching snippets."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_sall(self, mock_isfile, mock_get_db_location):
        """Search snippet from all fields."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets from all fields. The match is made from one snippet
        ##        content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', 'redis', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
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
                      '   > https://docs.docker.com/engine/reference/commandline/rm/')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', 'all', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
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
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', 'docker', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
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
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', 'moby', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Search snippets from all fields. The match is made from one snippet
        ##        digest data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', '53908d68425c61dc', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
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
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', '.', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: List all snippets by leaving search criteria of search all oout completely.
        ##        This is translated to 'match any'.
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
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
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
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sall', '', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_stag(self, mock_isfile, mock_get_db_location):
        """Search snippet from tag field."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets from tag field. The match is made from one snippet
        ##        content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Test if specific port is open @linux [f3fd167c64b6f97e]',
                      '   $ nc -v 10.183.19.189 443',
                      '   $ nmap 10.183.19.189',
                      '',
                      '   # linux,netcat,networking,port',
                      '   > https://www.commandlinux.com/man-page/man1/nc.1.html')
            snippy = Snippet.add_defaults(Snippy())
            Snippet.add_one(snippy, Snippet.NETCAT)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--stag', 'netcat', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_sgrp(self, mock_isfile, mock_get_db_location):
        """Search snippet from group field."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets from tag field. The match is made from one snippet
        ##        content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Test if specific port is open @linux [f3fd167c64b6f97e]',
                      '   $ nc -v 10.183.19.189 443',
                      '   $ nmap 10.183.19.189',
                      '',
                      '   # linux,netcat,networking,port',
                      '   > https://www.commandlinux.com/man-page/man1/nc.1.html')
            snippy = Snippet.add_defaults(Snippy())
            Snippet.add_one(snippy, Snippet.NETCAT)
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--sgrp', 'linux', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_snippet_with_data(self, mock_isfile, mock_get_db_location):
        """Search snippets with --content option."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippets based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                      '   $ docker rm --volumes $(docker ps --all --quiet)',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/')
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'search', '--content', 'docker rm --volumes $(docker ps --all --quiet)', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_searching_snippet_with_digest(self, mock_isfile, mock_get_db_location):
        """Search snippet with --digest option."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search snippet by explicitly defining short message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Remove docker image with force @docker [53908d68425c61dc]',
                      '   $ docker rm --force redis',
                      '',
                      '   # cleanup,container,docker,docker-ce,moby',
                      '   > https://docs.docker.com/engine/reference/commandline/rm/',
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'search', '--digest', '53908d68425c61dc', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
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
                      '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes')
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'search', '--digest', '5', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
