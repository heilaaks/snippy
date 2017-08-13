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
        cls.config['args']['brief'] = cls.__parse_brief()
        cls.config['args']['tags'] = cls.__parse_tags()
        cls.config['args']['link'] = cls.__parse_link()
        cls.config['args']['find'] = cls.__parse_find()
        cls.config['args']['delete'] = cls.__parse_delete()
        cls.config['args']['export'], cls.config['args']['export_format'] = cls.__parse_export()
        cls.config['args']['profiler'] = cls.args.get_profiler()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = os.path.join(os.environ.get('HOME'), 'devel/snippy-db')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = os.path.join(cls.config['root'], 'snippy/storage/database/database.sql')
        cls.config['storage']['in_memory'] = False

        cls.logger.info('configured argument --snippet as "%s"', cls.config['args']['snippet'])
        cls.logger.info('configured argument --tags as "%s"', cls.config['args']['tags'])
        cls.logger.info('configured argument --brief as "%s"', cls.config['args']['brief'])
        cls.logger.info('configured argument --link as "%s"', cls.config['args']['link'])
        cls.logger.info('configured argument --find as "%s"', cls.config['args']['find'])
        cls.logger.info('configured argument --delete as "%s"', cls.config['args']['delete'])
        cls.logger.info('configured argument --export as "%s"', cls.config['args']['export'])
        cls.logger.info('configured argument --profiler as "%s"', cls.config['args']['profiler'])
        cls.logger.info('extracted export file format as "%s"', cls.config['args']['export_format'])

    @classmethod
    def is_snippet_task(cls):
        """Test if the user action was for a snippet."""

        if cls.get_snippet() or cls.get_find_keywords() or cls.get_delete() or cls.get_export():
            return True

        return False

    @classmethod
    def is_resolve_task(cls):
        """Test if the user action was for a resolution."""

        if cls.get_resolve() or cls.get_find_keywords():
            return True

        return False

    @classmethod
    def get_snippet(cls):
        """Get the snippet."""

        return cls.config['args']['snippet']

    @classmethod
    def get_resolve(cls):
        """Get the resolution."""

        return cls.config['args']['resolve']

    @classmethod
    def get_brief(cls):
        """Get brief description for the snippet or resolution."""

        return cls.config['args']['brief']

    @classmethod
    def get_tags(cls):
        """Get tags for the snippet or resolution."""

        return cls.config['args']['tags']

    @classmethod
    def get_link(cls):
        """Get link for the snippet or resolution."""

        return cls.config['args']['link']

    @classmethod
    def get_find_keywords(cls):
        """Get find keywords for the snippet or resolution."""

        return cls.config['args']['find']

    @classmethod
    def get_delete(cls):
        """Get deleted snippet index."""

        return cls.config['args']['delete']

    @classmethod
    def get_export(cls):
        """Get export file."""

        return cls.config['args']['export']

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
    def __parse_brief(cls):
        """Preprocess the user given brief description."""

        arg = cls.args.get_brief()
        if arg:
            return arg

        return ''

    @classmethod
    def __parse_tags(cls):
        """Process the user given tag keywords."""

        arg = cls.args.get_tags()

        return cls.__parse_keywords(arg)

    @classmethod
    def __parse_link(cls):
        """Preprocess the user given link."""

        arg = cls.args.get_link()
        if arg:
            return arg

        return ''

    @classmethod
    def __parse_find(cls):
        """Process the user given find keywords."""

        arg = cls.args.get_find()

        return cls.__parse_keywords(arg)

    @classmethod
    def __parse_delete(cls):
        """Process the user given delete keywords to remove snippet."""

        arg = cls.args.get_delete()
        if arg:
            return arg

        return 0

    @classmethod
    def __parse_export(cls):
        """Preprocess the user given export file."""

        export_file = cls.args.get_export()
        filename, file_extension = os.path.splitext(export_file)
        print("filename %s and extension %s" % (filename, file_extension))
        if filename and ('yaml' in file_extension or 'yml' in file_extension):
            export_file = filename + '.yaml'

            return (export_file, 'yaml')

        cls.logger.info('unsupported export file format "%s"', file_extension)

        return ('', 'yaml')

    @classmethod
    def __parse_keywords(cls, keywords):
        """Preprocess the user given keyword list. The keywords are for example the
        user provided tags or the find keywords. The keywords are returned as a list
        from the Argument. The user may use various formats so each item in a list may
        be for example a string of comma separated tags."""

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t dockertesting', container-managemenet', cleanup_testing
        kw_list = []
        for tag in keywords:
            kw_list = kw_list + re.findall(r"[\w\-]+", tag)

        return sorted(kw_list)
