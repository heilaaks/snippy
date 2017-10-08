#!/usr/bin/env python3

"""test_wf_delete_snippet.py: Test workflows for deleting snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.cause import Cause
from snippy.config import Constants as Const
from snippy.storage.database import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfDeleteSnippet(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Test workflows for deleting snippets."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_deleting_snippet_with_digest_short_version(self, mock_get_db_location):
        """Delete snippet from command line based on digest short version.

        Workflow:
            @ delete snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py delete -d 54e41e9b52a02b63
        Expected results:
            1 Snippet can be deleted based on digest short version.
            2 There is no content in database after the snippet is deleted.
            3 Exit cause is OK.
        """

        initial = Snippet().get_references(0)
        mock_get_db_location.return_value = Database.get_storage()

        # Create original snippet.
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())[0], initial)
        assert len(snippy.storage.search(Const.SNIPPET, data=initial.get_data())) == 1

        # Delete snippet with digest short version.
        sys.argv = ['snippy', 'delete', '-d', '%.16s' % initial.get_digest()]
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        assert not snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())
        assert not Database.get_contents()

        # Release all resources
        snippy.release()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_deleting_snippet_with_digest_log_version(self, mock_get_db_location):
        """Delete snippet from command line based on digest short version.

        Workflow:
            @ delete snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
            $ python snip.py delete -d 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319
        Expected results:
            1 Snippet can be deleted based on digest long version.
            2 There is no content in database after the snippet is deleted.
            3 Exit cause is OK.
        """

        initial = Snippet().get_references(0)
        mock_get_db_location.return_value = Database.get_storage()

        # Create original snippet.
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())[0], initial)
        assert len(snippy.storage.search(Const.SNIPPET, data=initial.get_data())) == 1

        # Delete snippet with digest long version.
        sys.argv = ['snippy', 'delete', '-d', initial.get_digest()]
        snippy.reset()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        assert not snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())
        assert not Database.get_contents()

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
