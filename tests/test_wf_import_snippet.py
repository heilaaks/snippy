#!/usr/bin/env python3

"""test_wf_import_snippet.py: Test workflows for importing snippets."""

import sys
import unittest
import mock
import yaml
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSnippet(unittest.TestCase):
    """Test workflows for importing snippets."""

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_importing_snippets(self, mock_isfile, mock_get_db_location, mock_safe_load):
        """Import snippets from defined yaml file.

        Workflow:
            @ import snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py import -f ./snippets.yaml
        Expected results:
            1 One snippet is imported.
            2 One imported snippet data already exist and the existing one is not updated.
            3 Two existing snippets are not changed when one new snippet is imported.
            4 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        snippets = {'content': [{'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
                                 'brief': 'Remove all docker containers with volumes',
                                 'group': 'docker',
                                 'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/', ),
                                 'category': 'snippet',
                                 'filename': '',
                                 'utc': '2017-10-14 22:22:22',
                                 'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'},
                                {'data': ('nc -v 10.183.19.189 443',
                                          'nmap 10.183.19.189'),
                                 'brief': 'Test if specific port is open',
                                 'group': 'linux',
                                 'tags': ('linux', 'netcat', 'networking', 'port'),
                                 'links': ('https://www.commandlinux.com/man-page/man1/nc.1.html',),
                                 'category': 'snippet',
                                 'filename': '',
                                 'utc': '2017-10-20 07:08:45',
                                 'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'}]}
        mock_safe_load.return_value = snippets
        snippy = Snippet.add_snippets(self)

        # Import snippets from yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'import', '-f', './snippets.yaml']
            snippy.reset()
            assert len(Database.get_contents()) == 2
            content_before = snippy.storage.search(Const.SNIPPET, data=snippets['content'][0]['data'])
            cause = snippy.run_cli()
            content_after = snippy.storage.search(Const.SNIPPET, data=snippets['content'][0]['data'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippets.yaml', 'r')
            Snippet().compare(self, content_after[0], content_before[0])
            assert len(Database.get_contents()) == 3

            # Verify the imported snippet by exporting it again to text file.
            content = snippy.storage.search(Const.SNIPPET, digest='53908d68425c61dc')
            (message, _) = Snippet().get_edited_message(content[0], content[0], ())
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(message)

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
