#!/usr/bin/env python3

"""test_wf_update_snippet.py: Test workflows for updating snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.editor import Editor
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfUpdateSnippet(unittest.TestCase):
    """Test workflows for updating snippets."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_update_snippet_with_digest(self, mock_get_db_location, mock_call_editor):
        """Update snippet with digest."""

        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Update snippet based on short message digest. Only the content data is updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'af8c89629dc1a531': Snippet.get_dictionary(template),
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-d', '54e41e9b52a02b63']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update snippet based on very short message digest. This must match to a single
        ##        snippet that must be updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'af8c89629dc1a531': Snippet.get_dictionary(template),
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-d', '54e41']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update snippet based on long message digest. Only the content data is updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'af8c89629dc1a531': Snippet.get_dictionary(template),
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update snippet based on message digest and accidentally define solution
        ##        category. In this case the snippet is updated properly regardless of
        ##        incorrect category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'af8c89629dc1a531': Snippet.get_dictionary(template),
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '--solution', '-d', '54e41e9b52a02b63']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with message digest that cannot be found. No changes must
        ##        be made to stored content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-d', '123456789abcdef0']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with empty message digest. Nothing should be updated
        ##        in this case because the empty digest matches to more than one snippet. Only
        ##        one content can be updated at the time.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-d', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty message digest to update content'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with one digit digest that matches two snippets. Note!
        ##        not change the snippets because this case is produced with real message digests
        ##        that just happen to have same digit starting both of the cases.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-d', '5']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: given digest 5 matches (2) more than once preventing the operation'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_update_snippet_with_data(self, mock_get_db_location, mock_call_editor):
        """Update snippet with data."""

        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Update snippet based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'af8c89629dc1a531': Snippet.get_dictionary(template),
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-c', 'docker rm --volumes $(docker ps --all --quiet)']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with empty content data. Nothing should be update
        ##        in this case because there is more than one content left.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                               '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]}
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'update', '-c', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty content data to update content'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
