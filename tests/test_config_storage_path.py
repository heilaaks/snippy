#!/usr/bin/env python3

"""test_config_storage_path.py: Testing storage path configuration."""

import os
import sys
from snippy.config import Config


class TestConfigStoragePath(object):
    """Testing storage path configuration. As of now, these just very that
    there are no accidents hapening for the configured database path. This
    may not be the best test since this just relies on copying the path"""

    def test_storage_path(self):
        """Test that storage path is configured correctly."""

        sys.argv = ['snippy', 'create']
        obj = Config()
        path = os.path.join(os.environ['HOME'], 'devel/snippy-db')
        assert obj.get_storage_path() == path

    def test_storage_snippy(self):
        """Test that storage file is configured correctly."""

        sys.argv = ['snippy', 'create']
        obj = Config()
        db_file = os.path.join(os.environ['HOME'], 'devel/snippy-db', 'snippy.db')
        assert obj.get_storage_file() == db_file
