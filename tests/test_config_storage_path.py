
"""test_config_storage_path.py: Testing storage path configuration."""

class TestConfigStoragePath(object):
    """Testing storage path configuration."""

    def test_storage_path(self):
        """Test that storage path is configured correctly."""
        from cuma.config import Config
        obj = Config()
        path = '/home/heilaaks/devel/cuma-db'
        assert obj.get_storage_path() == path

    def test_storage_cuma(self):
        """Test that storage file is configured correctly."""
        from cuma.config import Config
        obj = Config()
        db_file = '/home/heilaaks/devel/cuma-db/cuma.db'
        assert obj.get_storage_file() == db_file
