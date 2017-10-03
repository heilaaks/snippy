#!/usr/bin/env python3

"""test_wf_update_snippet.py: Test workflows for updating snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config import Constants as Const
from snippy.config import Editor
from snippy.storage.database import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestWorkflowUpdateSnippet(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Test workflows for updating snippets."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_updating_snippet_with_digest(self, mock_get_db_location, mock_call_editor):
        """Updated snippet from command line based on with digest.

        Workflow:
            @ update snippet
        Execution:
            $ python snip.py update SnippetHelper().get_snippet(0)
        Expected results:
            1 Snippet can be updated based on digest.
            2 Snippet is updated with editor when only digest option is provided.
        """

        initial = Snippet().get_references(0)
        updates = Snippet().get_references(1)
        (message, merged) = Snippet().get_edited_message(initial, updates, (Const.DATA,))
        mock_get_db_location.return_value = Database.get_storage()
        mock_call_editor.return_value = message

        # Create original snippet.
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        snippy.run_cli()
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())[0], initial)
        assert len(snippy.storage.search(Const.SNIPPET, data=initial.get_data())) == 1

        # Update original snippet based on digest. Only content data is updated.
        sys.argv = ['snippy', 'update', '-d', initial.get_digest()]
        snippy.reset()
        snippy.run_cli()
        snippets = snippy.storage.search(Const.SNIPPET, digest=merged.get_digest())
        print(snippets[0])
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=merged.get_digest())[0], merged)
        assert len(snippy.storage.search(Const.SNIPPET, data=merged.get_data())) == 1
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
