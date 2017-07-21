import sys


class TestConfigStoragePath(object):

    def test_storage_path(self):
        from cuma.config import Config
        obj = Config()
        path = '/home/heilaaks/devel/cuma-db'
        assert obj.get_storage_path() == path

    def test_storage_cuma(self):
        from cuma.config import Config
        obj = Config()
        db_file = '/home/heilaaks/devel/cuma-db/cuma.db'
        assert obj.get_storage_file() == db_file
