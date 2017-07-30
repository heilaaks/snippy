#!/usr/bin/env python3

"""test_storage_snippet.py: Test snippet storage."""

import mock
from snippy.config import Config

class TestStorageAddNewSnippet(object): # pylint: disable=too-few-public-methods
    """Testing storing new snippets."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_add_new_with_all_parameters(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Test that snippet without tags, comment or links is stored."""

        from snippy.storage import Storage

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'
        obj = Storage()
        obj.init()
        obj.debug()
