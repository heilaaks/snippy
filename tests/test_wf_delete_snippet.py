#!/usr/bin/env python3

"""test_wf_delete_snippet.py: Test workflows for deleting snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfDeleteSnippet(unittest.TestCase):
    """Test workflows for deleting snippets."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_delete_snippet_with_digest(self, mock_get_db_location):
        """Delete snippet with digest."""

        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Delete snippet with short 16 byte version of message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '53908d68425c61dc']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()


        ## Brief: Delete snippet with very short version of digest that matches to one snippet.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '54e41']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete snippet with long 16 byte version of message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with message digest that cannot be found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '123456789abcdef0']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with empty message digest. Nothing should be deleted
        ##        in this case because there is more than one content left.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty message digest to delete content'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete snippet with empty message digest when there is only one content.
        ##        left. In this case the last content can be deleted with empty digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'delete', '-d', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert not Database.get_snippets()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with short version of digest that does not match
        ##        to any existing message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '123456']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with message digest 123456'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_delete_snippet_with_data(self, mock_get_db_location):
        """Delete snippet with data."""

        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Delete snippet based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all --quiet)']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with content data that does not exist. In this case the
        ##        content data is not truncated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all)']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with content data \'docker rm --volumes $(docker ps --all)\''
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with empty content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--content', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty content data to delete content'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
