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
        Config.logger = Logger().get()
        Config.args = Arguments()
        Config.__set_config()

    @classmethod
    def __set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['root'] = os.path.realpath(os.path.join(os.getcwd()))
        cls.config['db_path'] = os.path.join(os.environ.get('HOME'), 'devel', 'cuma-db')
        cls.config['db_file'] = 'cuma.db'
        cls.config['db_schema'] = os.path.join(cls.config['root'], 'cuma/database/database.sql')
        cls.config['args'] = {}
        cls.config['args']['snippet'] = Config.__parse_snippet()
        cls.config['args']['tags'] = Config.__parse_tags()
        cls.config['args']['comment'] = Config.__parse_comment()
        cls.config['args']['profiler'] = Arguments.get_profiler()


    @classmethod
    def __parse_snippet(cls):
        """preprocess the user given snippet."""

        arg = Arguments.get_snippet()
        if arg:
            return arg

        return ''

    @classmethod
    def __parse_tags(cls):
        """preprocess the user given tag list."""

        arg = Arguments.get_tags()
        if arg:
            return arg.split(',')

        return []

    @classmethod
    def __parse_comment(cls):
        """preprocess the user given comment."""

        arg = Arguments.get_comment()
        if arg:
            return arg

        return ''

    @classmethod
    def get_storage_path(cls):
        """Get path of the persistent storage."""

        return cls.config['db_path']

    @classmethod
    def get_storage_file(cls):
        """Get path and file of the persistent storage."""

        return os.path.join(cls.config['db_path'], cls.config['db_file'])

    @classmethod
    def get_storage_schema(cls):
        """Get storage schema."""

        return cls.config['db_schema']

    @classmethod
    def get_snippet(cls):
        """Get the snippet."""

        return cls.config['args']['snippet']

    @classmethod
    def get_tags(cls):
        """Get tags for the snippet."""

        return cls.config['args']['tags']

    @classmethod
    def get_comment(cls):
        """Get comment for the snippet."""

        return cls.config['args']['comment']

    @classmethod
    def is_profiled(cls):
        """Check if the code profiler is run."""

        return cls.config['args']['profiler']
