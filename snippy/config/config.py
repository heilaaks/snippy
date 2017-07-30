#!/usr/bin/env python3

"""config.py: Configuration management."""

import re
import os.path
from snippy.config import Arguments
from snippy.logger import Logger


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
        cls.config['db_path'] = os.path.join(os.environ.get('HOME'), 'devel/snippy-db')
        cls.config['db_file'] = 'snippy.db'
        cls.config['db_schema'] = os.path.join(cls.config['root'], 'snippy/storage/database/database.sql')
        cls.config['args'] = {}
        cls.config['args']['snippet'] = cls.__parse_snippet()
        cls.config['args']['resolve'] = cls.__parse_resolve()
        cls.config['args']['tags'] = cls.__parse_tags()
        cls.config['args']['comment'] = cls.__parse_comment()
        cls.config['args']['profiler'] = cls.args.get_profiler()

        cls.logger.info('configured argument --snippet as "%s"', cls.config['args']['snippet'])
        cls.logger.info('configured argument --tags as "%s"', cls.config['args']['tags'])
        cls.logger.info('configured argument --comment as "%s"', cls.config['args']['comment'])
        cls.logger.info('configured argument --profiler as "%s"', cls.config['args']['profiler'])

    @classmethod
    def is_snippet(cls):
        """Test if the user action was to add new snippet."""

        if cls.get_snippet():
            return True

        return False

    @classmethod
    def is_resolve(cls):
        """Test if the user action was to add new resolution."""

        if cls.get_resolve():
            return True

        return False

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
    def get_resolve(cls):
        """Get the resolution."""

        return cls.config['args']['resolve']

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

    @classmethod
    def __parse_snippet(cls):
        """Preprocess the user given snippet."""

        arg = cls.args.get_snippet()
        if arg:
            return arg

        return ''

    @classmethod
    def __parse_resolve(cls):
        """Preprocess the user given resolution."""

        arg = cls.args.get_resolve()
        if arg:
            return arg

        return ''

    @classmethod
    def __parse_tags(cls):
        """Preprocess the user given tag list. The tags are returned as a list from
        the Argument. The user may use various formats so each item in a list may be
        a string of comma separated tags."""

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t dockertesting', container-managemenet', cleanup_testing
        arg = cls.args.get_tags()
        tags = []

        for tag in arg:
            tags = tags + re.findall(r"[\w\-]+", tag)

        return sorted(tags)

    @classmethod
    def __parse_comment(cls):
        """Preprocess the user given comment."""

        arg = cls.args.get_comment()
        if arg:
            return arg

        return ''
