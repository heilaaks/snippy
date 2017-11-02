#!/usr/bin/env python3

"""test_wf_export_snippet.py: Test workflows for exporting snippets."""

import sys
import unittest
import mock
import yaml
from snippy.snip import Snippy
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
    def test_export_all_snippets(self, mock_get_db_location, mock_get_utc_time, mock_safe_dump):
        """Export all snippets."""

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

        ## Brief: Export all snippets without defining target file name from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'export']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./snippets.yaml', 'w')
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all snippets into yaml file defined from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'export', '-f', './defined-snippets.yaml']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./defined-snippets.yaml', 'w')
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export all snippets into yaml file defined from command line by explicitly defining
        ##        the content category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'export', '-f', './defined-snippets.yaml', '--snippet']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_safe_dump.assert_called_with(export, mock.ANY, default_flow_style=mock.ANY)
            mock_file.assert_called_once_with('./defined-snippets.yaml', 'w')
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to export all snippets into file format that is not supported. This should
        ##        result error text for end user and no files should be created.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'export', '-f', 'foo.bar']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file foo.bar'
            mock_file.assert_not_called()
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_defined_snippet(self, mock_get_db_location, mock_get_utc_time):
        """Export defined snippet."""

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
                  '')

        ## Brief: Export defined snippet based on message digest. File name is not defined in command
        ##        line -f|--file option. This should result usage of default file name and format
        ##        snippet.text.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'export', '-d', '53908d68425c61dc']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('snippet.text', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(export)), mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export defined snippet based on message digest. File name is  defined in command
        ##        line. This should result file and format defined by command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'export', '-d', '53908d68425c61dc', '-f', 'defined-snippet.txt']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-snippet.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(export)), mock.call(Const.NEWLINE)])
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_export_snippet_template(self, mock_get_db_location, mock_get_utc_time):
        """Export snippet template."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_get_utc_time.return_value = '2017-10-14 19:56:31'
        template = Snippet.TEMPLATE

        ## Brief: Export snippet template. This should result file name and format based on
        ##        tool internal settings.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--template']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(template))
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Export snippet template by explicitly defining content category. This should
        ##        result file name and format based on tool internal settings.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'export', '--snippet', '--template']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippet-template.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Const.NEWLINE.join(template))
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
