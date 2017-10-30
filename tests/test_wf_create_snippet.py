#!/usr/bin/env python3

"""test_wf_create_snippet.py: Test workflows for creating snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfCreateSnippet(unittest.TestCase):
    """Test workflows for creating snippets."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_creating_new_snippet_from_command_line(self, mock__get_db_location):
        """Create snippet from command line with all parameters.

        Expected results:
            1 Long versions from command line options work.
            2 Only one entry is read from storage and it can be read with digest or content.
            3 Content, brief, group, tags and links are read correctly.
            4 Tags and links are presented in a list and they are sorted.
            5 Message digest is corrent and constantly same.
            6 Exit cause is OK.
        """

        initial = Snippet().get_references(0)
        mock__get_db_location.return_value = Database.get_storage()

        ## Brief: Create new snippet by defining all content parameters from command line.
        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)  ## workflow
        snippy = Snippy()
        cause = snippy.run_cli()
        assert cause == Cause.ALL_OK
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())[0], initial)
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, data=initial.get_data())[0], initial)
        assert len(snippy.storage.search(Const.SNIPPET, digest=initial.get_digest())) == 1
        assert len(snippy.storage.search(Const.SNIPPET, data=initial.get_data())) == 1

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
