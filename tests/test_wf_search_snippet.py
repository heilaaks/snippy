#!/usr/bin/env python3

"""test_wf_search_snippet.py: Test workflows for searching snippets."""

import sys
import unittest
import mock
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
    def test_searching_snippets_with_sall_option(self, mock_get_db_location): # pylint: disable=too-many-statements
        """Search snippet with --sall option.

        Workflow:
            @ search snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py search --sall redis --no-ansi  # Match only data
            $ python snip.py search --sall all --no-ansi    # Match only brief
            $ python snip.py search --sall docker --no-ansi # Match only group
            $ python snip.py search --sall moby --no-ansi   # Match only tags
            $ python snip.py search --sall 53908d68425c61dc --no-ansi
            $ python snip.py search --sall . --no-ansi
            $ python snip.py search --sall --no-ansi
        Expected results:
            1 Snippet is found from data with --sall option.
            2 Snippet is found from brief with --sall option.
            3 Snippet is found from group with --sall option.
            4 Snippet is found from tags with --sall option
            5 Snippet is found with --sall option based on digest.
            6 All snippets are listed with keyword '.' for --sall option.
            7 All snippets are listed when no keywords are provided for --sall option.
            8 Exit cause is always OK.
        """

        saved_stdout = sys.stdout
        mock_get_db_location.return_value = Database.get_storage()
        snippy = Snippet.add_snippets(self)

        # Find from snippet2 data.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', 'redis', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # Find from snippet1 brief.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', 'all', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]\n' \
                         '   $ docker rm --volumes $(docker ps --all --quiet)\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/'

        # Find from group that results both snippets.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', 'docker', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]\n' \
                         '   $ docker rm --volumes $(docker ps --all --quiet)\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '\n' \
                         '2. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # Find from tags that results both snippets.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', 'moby', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]\n' \
                         '   $ docker rm --volumes $(docker ps --all --quiet)\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '\n' \
                         '2. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # Find based on content digest with --sall option.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', '53908d68425c61dc', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # List all snippets based on '.' keyword.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', '.', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]\n' \
                         '   $ docker rm --volumes $(docker ps --all --quiet)\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '\n' \
                         '2. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # List all snippets when no keywords are provided.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]\n' \
                         '   $ docker rm --volumes $(docker ps --all --quiet)\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '\n' \
                         '2. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # Release all resources
        snippy.release()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_searching_snippet_with_content(self, mock_get_db_location): # pylint: disable=too-many-statements
        """Search snippet with --content option.

        Workflow:
            @ search snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py search -c 'docker rm --volumes $(docker ps --all --quiet)' --no-ansi
        Expected results:
            1 Snippet is found based on content data.
            2 Exit cause is OK.
        """

        saved_stdout = sys.stdout
        mock_get_db_location.return_value = Database.get_storage()
        snippy = Snippet.add_snippets(self)

        # Find snippet based on content data.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]\n' \
                         '   $ docker rm --volumes $(docker ps --all --quiet)\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/'

        # Release all resources
        snippy.release()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_searching_snippet_with_digest(self, mock_get_db_location): # pylint: disable=too-many-statements
        """Search snippet with --digest option.

        Workflow:
            @ search snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py search -d 53908d68425c61dc --no-ansi
        Expected results:
            1 Snippet is found based on content digest.
            2 Exit cause is OK.
        """

        saved_stdout = sys.stdout
        mock_get_db_location.return_value = Database.get_storage()
        snippy = Snippet.add_snippets(self)

        # Find based on content digest with -d|--digest option.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--digest', '53908d68425c61dc', '--no-ansi']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        assert output == '1. Remove docker image with force @docker [53908d68425c61dc]\n' \
                         '   $ docker rm --force redis\n' \
                         '\n' \
                         '   # cleanup,container,docker,docker-ce,moby\n' \
                         '   > https://docs.docker.com/engine/reference/commandline/rm/\n' \
                         '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
