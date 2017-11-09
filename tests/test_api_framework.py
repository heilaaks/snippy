#!/usr/bin/env python3

"""test_wf_import_snippet.py: Test workflows for importing snippets."""

import sys
import unittest
import mock
import pytest
from snippy.snip import Snippy
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiFramework(unittest.TestCase):
    """Test Snippy API framework."""

    @pytest.mark.skip(reason="mocking sys.exit in here stalls all tests with pytest with high cpu load. Why?")
    #@mock.patch('sys.exit')
    #def test_resets(self, mock_exit):
    def test_resets(self):
        """Test Snippy reset."""

        #with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
        #with self.assertRaises(SystemExit): ## Blocks all logging?
        with mock.patch('snippy.config.arguments.sys.exit'):
            snippy = Snippy()
            sys.argv = ['snippy', 'search']
            cause = snippy.run_cli()
            print(cause)
            print("HERE")
            print(snippy.config.is_operation_search())
            print(snippy.config.source.get_operation())
            print(snippy.config.is_operation_search())
            print(snippy.config.source.get_operation())
            print(snippy.config)
            print("HERE-TAIL")
            snippy.release()
            snippy = None
            Database.delete_storage()

        #assert 0

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
