#!/usr/bin/env python3

"""config.py: Read configuration."""

import os.path
from cuma.config import Arguments
from cuma.logger import Logger


class Config(object):
    """Global configuration management."""

    args = {}
    config = {}
    logger = None

    def __init__(self):
        if not Config.config:
            Config.logger = Logger().get()
            Config.args = Arguments()
            Config.__set_config()

    @classmethod
    def __set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['path'] = os.path.join(os.environ.get('HOME'), 'devel', 'cuma-db')
        cls.config['file'] = 'cuma.db'
        cls.config['args'] = {}
        cls.config['args']['snippet'] = Arguments.get_argument('snippet')
        cls.config['args']['tags'] = cls.args.get_argument('tags')
        cls.config['args']['comment'] = Arguments.get_argument('comment')

    @classmethod
    def get_storage_path(cls):
        """Get path of the persistent storage"""

        return cls.config['path']

    @classmethod
    def get_storage_file(cls):
        """Get path and file of the persistent storage"""

        return os.path.join(cls.config['path'], cls.config['file'])
