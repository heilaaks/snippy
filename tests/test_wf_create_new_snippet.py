#!/usr/bin/env python3

"""test_wf_create_new_snippet.py: Test workflows for creating new snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config import Config
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import
from tests.testlib.snippet_helper import SnippetHelper as Snippet


class TestWorkflowCreateNewSnippet(unittest.TestCase): # pylint: disable=too-few-public-methods
    """Test workflows for creating new snippets."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_creating_new_snippet_from_command_line(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Create snippet from command line with all parameters.

        Workflow:
            @ creating snippet
        Execution:
            $ python snip.py create SnippetHelper().get_snippet(0)
        Expected results:
            1 Long versions from command line options work.
            2 Only one entry is read from storage and it can be read with digest or content.
            3 Content, brief, group, tags and links are read correctly.
            4 Tags and links are presented in a list and they are sorted.
            5 Message digest is corrent and constantly same.
        """

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'

        sys.argv = ['snippy', 'create'] + Snippet().get_command_args(0)
        snippy = Snippy()
        snippy.run()
        references = Snippet().get_references(0)
        Snippet().compare(snippy.storage.search(digest=references[0][DIGEST])[0], references[0])
        Snippet().compare(snippy.storage.search(content=references[0][CONTENT])[0], references[0])
        assert len(snippy.storage.search(digest=references[0][DIGEST])) == 1
        assert len(snippy.storage.search(content=references[0][CONTENT])) == 1
        snippy.release()
