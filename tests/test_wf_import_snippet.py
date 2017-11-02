#!/usr/bin/env python3

"""test_wf_import_snippet.py: Test workflows for importing snippets."""

import sys
import unittest
import json
import yaml
import mock
import pkg_resources
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSnippet(unittest.TestCase):
    """Test workflows for importing snippets."""

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_all_snippets(self, mock_isfile, mock_get_db_location, mock_yaml_load, mock_json_load):
        """Import all snippets."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [{'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
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
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict
        compare_content = {'54e41e9b52a02b63': import_dict['content'][0],
                           'f3fd167c64b6f97e': import_dict['content'][1]}

        ## Brief: Import all snippets. File name is not defined in commmand line. This should
        ##        result tool internal default file name ./snippets.yaml being used by default.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./snippets.yaml', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from yaml file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.yaml', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from json file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.json']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.json', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from txt file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]) +
                                     Const.NEWLINE +
                                     Snippet.get_template(import_dict['content'][1]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from text file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]) +
                                     Const.NEWLINE +
                                     Snippet.get_template(import_dict['content'][1]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.text']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.text', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import snippet from file which file format is not supported. This
        ##        should result error text for end user and no files should be read.
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './foo.bar']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_contents()
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_snippet_defaults(self, mock_isfile, mock_get_db_location, mock_yaml_load):
        """Import snippet defaults."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [{'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
                                    'brief': 'Remove all docker containers with volumes',
                                    'group': 'docker',
                                    'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                                    'links': ('https://docs.docker.com/engine/reference/commandline/rm/', ),
                                    'category': 'snippet',
                                    'filename': '',
                                    'utc': '2017-10-14 22:22:22',
                                    'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'},
                                   {'data': ('docker rm --force redis', ),
                                    'brief': 'Remove docker image with force',
                                    'group': 'docker',
                                    'tags': ('docker-ce', 'docker', 'moby', 'container', 'cleanup'),
                                    'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                                              'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-' +
                                              'images-containers-and-volumes'),
                                    'category': 'snippet',
                                    'filename': '',
                                    'utc': '2017-10-20 07:08:45',
                                    'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'}]}
        mock_yaml_load.return_value = import_dict
        compare_content = {'54e41e9b52a02b63': import_dict['content'][0],
                           '53908d68425c61dc': import_dict['content'][1]}

        ## Brief: Import snippet defaults. All snippets should be imported from predefined file
        ##        location under tool data folder from yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--defaults']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import snippet defaults again. The second import should fail with an error
        ##        because the content already exist.  The error text must be the same for all content
        ##        categories.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'import', '--defaults']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: no content was inserted because content data already existed'
            assert len(Database.get_snippets()) == 2
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_existing_snippets(self, mock_isfile, mock_get_db_location, mock_yaml_load):
        """Import snippets already existing."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [{'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
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
        mock_yaml_load.return_value = import_dict

        ## Brief: Import snippets from yaml file that is defined from command line. In this case
        ##        one of the two snippets is already existing. Because the content existing is
        ##        not considered as an error and another snippet is imported successfully, the
        ##        result cause is OK.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(None)
            sys.argv = ['snippy', 'import', '-f', './snippets.yaml']   ## workflow
            assert len(Database.get_contents()) == 2
            content_before = snippy.storage.search(Const.SNIPPET, data=import_dict['content'][0]['data'])
            cause = snippy.run_cli()
            content_after = snippy.storage.search(Const.SNIPPET, data=import_dict['content'][0]['data'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippets.yaml', 'r')
            Snippet().compare(self, content_after[0], content_before[0])
            assert len(Database.get_contents()) == 3
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': import_dict['content'][0],
                                                     'f3fd167c64b6f97e': import_dict['content'][1]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
