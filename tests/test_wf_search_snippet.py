#!/usr/bin/env python3

"""test_wf_search_snippet.py: Test workflows for searching snippets."""

from __future__ import print_function
import sys
import unittest
from io import StringIO
import mock
from snippy.snip import Snippy
from snippy.cause import Cause
from snippy.config import Constants as Const
from snippy.storage.database import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestWfDeleteSnippet(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Test workflows for searching snippets."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_deleting_snippet_with_digest_short_version(self, mock_get_db_location): # pylint: disable=too-many-statements
        """Search snippet with --sall option from all fields.

        Workflow:
            @ search snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py search --sall redis --no-color
            $ python snip.py search --sall all --no-color
            $ python snip.py search --sall docker --no-color
            $ python snip.py search -c 'docker rm --volumes $(docker ps --all --quiet)' --no-color
            $ python snip.py search --sall 53908d68425c61dc
        Expected results:
            1 Snippet is found from data with --sall option.
            2 Snippet is found from brief with --sall option.
            3 Snippet is found from group with --sall option.
            4 Snippet is found based on content data.
            5 Snippet is found based on content digest.
            6 Exit cause is always OK.
        """

        saved_stdout = sys.stdout
        snippet1 = Snippet().get_references(0)
        snippet2 = Snippet().get_references(1)
        mock_get_db_location.return_value = Database.get_storage()

        # Create two snippets where search is made.
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=snippet1.get_digest())[0], snippet1)
        assert len(snippy.storage.search(Const.SNIPPET, data=snippet1.get_data())) == 1
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(1)
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=snippet2.get_digest())[0], snippet2)
        assert len(snippy.storage.search(Const.SNIPPET, data=snippet2.get_data())) == 1
        assert len(Database.select_all_snippets()) == 2


        # Find from snippet2 data.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', 'redis', '--no-colors']
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
        sys.argv = ['snippy', 'search', '--sall', 'all', '--no-colors']
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
        sys.argv = ['snippy', 'search', '--sall', 'docker', '--no-colors']
        snippy.reset()
        cause = snippy.run_cli()
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        assert cause == Cause.ALL_OK
        print(output)
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

        # Find based on content data.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '--no-colors']
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

        # Find based on content digest.
        out = StringIO()
        sys.stdout = out
        sys.argv = ['snippy', 'search', '--sall', '53908d68425c61dc', '--no-colors']
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
