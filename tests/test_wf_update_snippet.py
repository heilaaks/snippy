#!/usr/bin/env python3

"""test_wf_update_snippet.py: Test workflows for updating snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.editor import Editor
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfUpdateSnippet(unittest.TestCase):
    """Test workflows for updating snippets."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_updating_snippet_with_digest(self, mock_get_db_location, mock_call_editor):
        """Update snippet from command line based on digest.

        Expected results:
            1 Snippet can be updated based on digest.
            2 Snippet is updated with editor when only digest option is provided.
            3 Only content data gets updated and remaining fields are not changed.
            4 Updated content can be found with new digest in long format.
            5 Updated content can be found with new digest in short format.
            6 Updated content can be found with new data.
            7 Two entries are still stored after update operation.
            8 Exit cause is OK.
        """

        initial = Snippet().get_references(0)
        updates = Snippet().get_references(1)
        (message, merged) = Snippet().get_edited_message(initial, updates, (Const.DATA,))
        mock_call_editor.return_value = message
        mock_get_db_location.return_value = Database.get_storage()
        snippy = self.add_snippets()

        # Update original snippet based on digest. Only content data is updated.
        sys.argv = ['snippy', 'update', '-d', initial.get_digest()]
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 2
        Snippet.compare(self, Database.get_content(merged.get_digest())[0], merged)

        # Release all resources
        snippy.release()

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_updating_snippet_using_solution_category(self, mock_get_db_location, mock_call_editor):
        """Update snippet but accidentally defining solution category from command line.

        Expected results:
            1 Category is not changed from snippet to solution.
            2 Snippet is updated normally.
            3 Exit cause is OK.
        """

        initial = Snippet().get_references(0)
        updates = Snippet().get_references(1)
        (message, merged) = Snippet().get_edited_message(initial, updates, (Const.DATA,))
        mock_call_editor.return_value = message
        mock_get_db_location.return_value = Database.get_storage()
        snippy = self.add_snippets()

        # Accidentally define the category to be solution
        sys.argv = ['snippy', 'update', '--solution', '-d', initial.get_digest()]
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet.compare(self, Database.get_content(merged.get_digest())[0], merged)

        # Release all resources
        snippy.release()

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_updating_snippet_with_unknown_digest(self, mock_get_db_location, mock_call_editor):
        """Updating snippet with misspelled message digest.

        Expected results:
            1 Original snippet is not updated.
            2 Original snippet can be found with original digest short and long versions.
            3 Original snippet can be found with original data.
            4 Exit cause is NOK and indicates the failure.
        """

        initial = Snippet().get_references(0)
        updates = Snippet().get_references(1)
        (message, _) = Snippet().get_edited_message(initial, updates, (Const.DATA,))
        mock_call_editor.return_value = message
        mock_get_db_location.return_value = Database.get_storage()
        snippy = self.add_snippets()

        ## Brief: Try to update digest with misspelled message digest.
        sys.argv = ['snippy', 'update', '-d', '123456789abcdef0']  ## workflow
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == 'NOK: cannot find snippet to be updated with digest 123456789abcdef0'
        Snippet.compare(self, Database.get_content(initial.get_digest())[0], initial)

        # Release all resources
        snippy.release()

    def add_snippets(self):
        """Add snippets that are being updated in tests."""

        snippet1 = Snippet().get_references(0)
        snippet3 = Snippet().get_references(2)

        # Create two snippets that are updated in tests.
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet.compare(self, Database.get_content(snippet1.get_digest())[0], snippet1)
        assert len(Database.get_content(snippet1.get_digest())) == 1
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(2)
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet.compare(self, Database.get_content(snippet3.get_digest())[0], snippet3)
        assert len(Database.get_content(snippet3.get_digest())) == 1
        assert len(Database.select_all_snippets()) == 2

        return snippy

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
