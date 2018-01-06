#!/usr/bin/env python3

"""test_wf_delete_snippet.py: Test workflows for deleting snippets."""

import sys
import unittest
import mock
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error


class TestWfDeleteSnippet(unittest.TestCase):
    """Test workflows for deleting snippets."""

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_delete_snippet_with_digest(self, mock_isfile, mock_storage_file):
        """Delete snippet with digest."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
#
#        ## Brief: Delete snippet with short 16 byte version of message digest.
#        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
#            snippy = Snippet.add_defaults(Snippy())
#            sys.argv = ['snippy', 'delete', '-d', '53908d68425c61dc']  ## workflow
#            cause = snippy.run_cli()
#            assert cause == 'OK'
#            assert len(Database.get_snippets()) == 1
#            snippy.release()
#            snippy = None
#            Database.delete_storage()
#
#        ## Brief: Delete snippet with very short version of digest that matches to one snippet.
#        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
#            snippy = Snippet.add_defaults(Snippy())
#            sys.argv = ['snippy', 'delete', '-d', '54e41']  ## workflow
#            cause = snippy.run_cli()
#            assert cause == 'OK'
#            assert len(Database.get_snippets()) == 1
#            snippy.release()
#            snippy = None
#            Database.delete_storage()
#
#        ## Brief: Delete snippet with long 16 byte version of message digest.
#        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
#            snippy = Snippet.add_defaults(Snippy())
#            sys.argv = ['snippy', 'delete', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319']  ## workflow
#            cause = snippy.run_cli()
#            assert cause == 'OK'
#            assert len(Database.get_snippets()) == 1
#            snippy.release()
#            snippy = None
#            Database.delete_storage()
#
#        ## Brief: Try to delete snippet with message digest that cannot be found.
#        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
#            snippy = Snippet.add_defaults(Snippy())
#            sys.argv = ['snippy', 'delete', '-d', '123456789abcdef0']  ## workflow
#            cause = snippy.run_cli()
#            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
#            assert len(Database.get_snippets()) == 2
#            snippy.release()
#            snippy = None
#            Database.delete_storage()

        ## Brief: Try to delete snippet with empty message digest. Nothing should be deleted
        ##        in this case because there is more than one content stored.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty message digest to delete content'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete snippet with empty message digest when there is only one content
        ##        stored. In this case the last content can be deleted with empty digest.
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

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_delete_snippet_with_data(self, mock_isfile, mock_storage_file):
        """Delete snippet with data."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

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
            sys.argv = ['snippy', 'delete', '--content', 'not found content']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with content data \'not found content\''
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with content data that does not exist. In this case the
        ##        content data is truncated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all)']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with content data \'docker rm --volumes $(docker p...\''
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete snippet with empty content data. Nothing should be deleted
        ##        in this case because there is more than one content left.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--content', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty content data to delete content'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_delete_snippet_with_search_keyword(self, mock_isfile, mock_storage_file):
        """Delete snippet with search."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Delete snippet based on search keyword that results one hit. In this
        ##        case the content is deleted.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--sall', 'redis']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete snippet based on search keyword that results more than one hit.
        ##        In this case the content must not be deleted.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--sall', 'docker']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: given search keyword matches (2) more than once preventing the operation'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_delete_snippet_failure_stdout(self, mock_isfile, mock_storage_file):
        """Delete snippet with data."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Delete snippet based on search keyword that results more than one hit.
        ##        In this case the error text is read from stdout and it must contain
        ##        the error string.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Snippet.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'delete', '--sall', 'docker']  ## workflow
            cause = snippy.run_cli()
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == 'NOK: given search keyword matches (2) more than once preventing the operation'
            assert result == 'NOK: given search keyword matches (2) more than once preventing the operation'
            assert len(Database.get_snippets()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
