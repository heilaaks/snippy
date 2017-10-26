#!/usr/bin/env python3

"""test_wf_export_snippet.py: Test workflows for exporting snippets."""

import sys
import unittest
import mock
import yaml
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfExportSnippet(unittest.TestCase):
    """Test workflows for exporting snippets."""

    @mock.patch.object(yaml, 'safe_dump')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_all_snippets_yaml(self, mock_get_db_location, mock_get_utc_time, mock_safe_dump):
        """Export snippets to defined yaml file.

        Workflow:
            @ export snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py export
            $ python snip.py export -f ./defined-snippets.yaml
            $ python snip.py export --snippet -f ./defined-snippets.yaml
        Expected results:
            1 Two snippets are exported.
            2 Filename defined from command line will be honored when the whole content is exported.
            3 Default filename will be used when user does not defined exported filename.
            4 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
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
        snippy = Snippet.add_snippets(self)

        ## Brief: Export all snippets without defining target file name from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./snippets.yaml', 'w')

        ## Brief: Export all snippets into yaml file defined from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '-f', './defined-snippets.yaml']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./defined-snippets.yaml', 'w')

        ## Brief: Export all snippets into yaml file defined from command line by explicitly defining
        ##        the content category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '-f', './defined-snippets.yaml', '--snippet']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./defined-snippets.yaml', 'w')

        # Release all resources
        snippy.release()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_defined_snippet(self, mock_get_db_location, mock_get_utc_time):
        """Export defined snippets.

        Workflow:
            @ export snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py export -d 53908d68425c61dc
            $ python snip.py export -d 53908d68425c61dc -f defined-snippet.txt
        Expected results:
            1 Only defined snippet is exported.
            2 Default filename snippet.text will be created with correct content when file is not defined.
            3 Filename defined from command line will be honored when defined content is exported.
            4 Exit cause is always OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        export = ('# Commented lines will be ignored.',
                  '#',
                  '# Add mandatory snippet below.',
                  'docker rm --force redis',
                  '',
                  '# Add optional brief description below.',
                  'Remove docker image with force',
                  '',
                  '# Add optional single group below.',
                  'docker',
                  '',
                  '# Add optional comma separated list of tags below.',
                  'cleanup,container,docker,docker-ce,moby',
                  '',
                  '# Add optional links below one link per line.',
                  'https://docs.docker.com/engine/reference/commandline/rm/',
                  'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                  '',
                  '')
        snippy = Snippet.add_snippets(self)

        # Export defined snippet into default text file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '-d', '53908d68425c61dc']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(export))

        # Export defined snippet into specified file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(export))

        # Release all resources
        snippy.release()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_snippet_template(self, mock_get_db_location, mock_get_utc_time):
        """Export snippet template.

        Workflow:
            @ export snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py export --template
            $ python snip.py export --snippet --template
        Expected results:
            1 Snippet template is created to default file.
            2 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        export = ('# Commented lines will be ignored.',
                  '#',
                  '# Add mandatory snippet below.',
                  '',
                  '',
                  '# Add optional brief description below.',
                  '',
                  '',
                  '# Add optional single group below.',
                  'default',
                  '',
                  '# Add optional comma separated list of tags below.',
                  '',
                  '',
                  '# Add optional links below one link per line.',
                  '',
                  '',
                  '')
        snippy = Snippet.add_snippets(self)

        # Export snippet template.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--template']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(export))

        # Export snippet template and explicitly define content category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--snippet', '--template']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(export))

        # Release all resources
        snippy.release()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_snippet_unsupported_file_format(self, mock_get_db_location, mock_get_utc_time):
        """Export snippet defining unsupported file format.

        Workflow:
            @ export snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py create SnippetHelper().get_snippet(1)
            $ python snip.py export --snippet -f foo.bar
        Expected results:
            1 No file is created and no exporting is done.
            2 Exit cause is NOK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        snippy = Snippet.add_snippets(self)

        # Export snippet template.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '-f', 'foo.bar']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
