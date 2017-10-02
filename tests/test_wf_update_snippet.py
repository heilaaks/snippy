#!/usr/bin/env python3

"""test_wf_update_snippet.py: Test workflows for updating snippets."""

import sys
import unittest
import tempfile
import subprocess
import mock
from snippy.snip import Snippy
from snippy.config import Constants as Const
#from snippy.config import Editor
from snippy.storage.database import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestWorkflowUpdateSnippet(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Test workflows for updating snippets."""

    @mock.patch.object(subprocess, 'call')
    @mock.patch.object(tempfile, 'NamedTemporaryFile')
    #@mock.patch.object(Editor.tempfile, "NamedTemporaryFile")
    #@mock.patch.object(Editor, 'read_content')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_updating_snippet_with_digest(self, mock__get_db_location, mock_namedtemporaryfile, mock_subprocess_call):
        """Updated snippet from command line based on with digest.

        Workflow:
            @ update snippet
        Execution:
            $ python snip.py update SnippetHelper().get_snippet(0)
        Expected results:
            1 Snippet can be updated based on digest.
            2 Snippet is updated with editor when only digest option is provided.
        """

        mock__get_db_location.return_value = Database.get_storage()
        #mock_read_content.return_value.edited = 'test'
        mock_subprocess_call.return_value = ''
        mock_namedtemporaryfile.return_value.__enter__.return_value.name = 'testoing'
        #mock_namedtemporaryfile.return_value.read.call_args == mock.call('some data')
        #mock_namedtemporaryfile.return_value.read.call_args = 'test'

        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        snippy.run_cli()
        references = Snippet().get_references(0)
        Snippet().compare(self, snippy.storage.search(Const.SNIPPET, digest=references[0].get_digest())[0], references[0])
        ##sys.argv = ['snippy', 'update', '-d', '54e41e9b52a02b6']
        ##snippy.reset()
        ##snippy.run_cli()
        ##snippets = snippy.storage.search(Const.SNIPPET, digest=references[0].get_digest())
        ##print(snippets)
        #Snippet().compare(self, snippets, references)
        #assert len(snippy.storage.search(Const.SNIPPET, digest=references[0].get_digest())) == 1

        #assert len(snippy.storage.search(Const.SNIPPET, data=references[0].get_data())) == 1
        ##assert 0
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        Database.delete_storage()
