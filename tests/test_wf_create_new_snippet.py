#!/usr/bin/env python3

"""test_wf_create_new_snippet.py: Test workflows for creating new snippets."""

import sys
import unittest
import mock
from snip import Snippy
from snippy.config import Constants as Const
from snippy.config import Config
from tests.testlib.snippet_helper import SnippetHelper as Helper


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
            2 One entry is read from storage and it can be read with digest or content.
            3 Content, brief, group, tags and links are read correctly.
            4 Tags and links are presented in a list and they are sorted.
            5 Message digest is corrent and constantly same.
        """

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'

        sys.argv = ['snippy', 'create'] + Helper().get_command_args(0)
        snippy = Snippy()
        snippy.run()
        reference = Helper().get_references(0)
        Helper().assert_snippets(snippy.storage.search(digest=reference[0][Const.SNIPPET_DIGEST])[0], reference[0])
        Helper().assert_snippets(snippy.storage.search(content=reference[0][Const.SNIPPET_CONTENT])[0], reference[0])
        snippy.disconnect()
