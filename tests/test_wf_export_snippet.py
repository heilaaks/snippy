#!/usr/bin/env python3

"""test_wf_export_snippet.py: Test workflows for exporting snippets."""

import sys
import unittest
import mock
import yaml
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSnippet(unittest.TestCase):
    """Test workflows for exporting snippets."""

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.open', new_callable=mock.mock_open, create=True)
    def test_exporting_snippets(self, mock_file, mock_get_db_location, mock_get_utc_time, mock_safe_dump): # pylint: disable=unused-argument
        """Export snippets to defaults file.

        Workflow:
            @ export snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py export -f ./snippets.yaml
        Expected results:
            1 Two snippets are exported.
            2 Correct file is created and it is only for write.
            3 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        snippy = Snippet.add_snippets(self)
        export = {'content': [{'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
                               'brief': 'Remove all docker containers with volumes',
                               'group': 'docker',
                               'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                               'links': ('https://docs.docker.com/engine/reference/commandline/rm/', ),
                               'category': 'snippet',
                               'filename': '',
                               'utc': '2017-10-14 19:56:31',
                               'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'},
                              {'data': ('docker rm --force redis', ),
                               'brief': 'Remove docker image with force',
                               'group': 'docker',
                               'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                               'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                                         'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-' +
                                         'images-containers-and-volumes'),
                               'category': 'snippet',
                               'filename': '',
                               'utc': '2017-10-14 19:56:31',
                               'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'}]}

        # Export snippets.
        sys.argv = ['snippy', 'export', '-f', './snippets.yaml']
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
        mock_file.assert_called_once_with('./snippets.yaml', 'w')

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
