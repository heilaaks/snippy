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
        cls.config['args'] = {}
        cls.config['args']['snippet'] = cls.__parse_snippet()
        cls.config['args']['resolve'] = cls.__parse_resolve()
        cls.config['args']['tags'] = cls.__parse_tags()
        cls.config['args']['comment'] = cls.__parse_comment()
        cls.config['args']['link'] = cls.__parse_link()
        cls.config['args']['profiler'] = cls.args.get_profiler()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = os.path.join(os.environ.get('HOME'), 'devel/snippy-db')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = os.path.join(cls.config['root'], 'snippy/storage/database/database.sql')
        cls.config['storage']['in_memory'] = False

        cls.logger.info('configured argument --snippet as "%s"', cls.config['args']['snippet'])
        cls.logger.info('configured argument --tags as "%s"', cls.config['args']['tags'])
        cls.logger.info('configured argument --comment as "%s"', cls.config['args']['comment'])
        cls.logger.info('configured argument --link as "%s"', cls.config['args']['link'])
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

        return cls.config['storage']['path']

    @classmethod
    def get_storage_file(cls):
        """Get path and file of the persistent storage."""

        return os.path.join(cls.config['storage']['path'], cls.config['storage']['file'])

    @classmethod
    def get_storage_schema(cls):
        """Get storage schema."""

        return cls.config['storage']['schema']

    @classmethod
    def set_storage_in_memory(cls, in_memory):
        """Set the storage to be in memory."""

        cls.config['storage']['in_memory'] = in_memory

    @classmethod
    def is_storage_in_memory(cls):
        """Test if storage is defined to be run in memory."""

        return cls.config['storage']['in_memory']

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
        """Get tags for the snippet or resolution."""

        return cls.config['args']['tags']

    @classmethod
    def get_comment(cls):
        """Get comment for the snippet or resolution."""

        return cls.config['args']['comment']

    @classmethod
    def get_link(cls):
        """Get link for the snippet or resolution."""

        return cls.config['args']['link']

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

    @classmethod
    def __parse_link(cls):
        """Preprocess the user given link."""

        arg = cls.args.get_link()
        if arg:
            return arg

        return ''
