#!/usr/bin/env python3

"""config.py: Configuration management."""

import re
import os.path
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Arguments


class Config(object):
    """Global configuration management."""

    args = {}
    config = {}
    logger = None

    def __init__(self):
        Config.logger = Logger().get()
        Config.args = Arguments()
        Config._set_config()

    @classmethod
    def _set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['root'] = os.path.realpath(os.path.join(os.getcwd()))
        cls.config['args'] = {}
        cls.config['args']['snippet'] = cls._parse_snippet()
        cls.config['args']['resolve'] = cls._parse_resolve()
        cls.config['args']['brief'] = cls._parse_brief()
        cls.config['args']['tags'] = cls._parse_tags()
        cls.config['args']['links'] = cls._parse_links()
        cls.config['args']['find'] = cls._parse_find()
        cls.config['args']['write'] = cls._parse_write()
        cls.config['args']['delete'] = cls._parse_delete()
        cls.config['args']['export'], cls.config['args']['export_format'] = cls._parse_export()
        cls.config['args']['profiler'] = cls.args.get_profiler()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = os.path.join(os.environ.get('HOME'), 'devel/snippy-db')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = os.path.join(cls.config['root'], 'snippy/storage/database/database.sql')
        cls.config['storage']['in_memory'] = False # Enabled only for testing.

        cls._set_editor_input()

        cls.logger.debug('configured argument --snippet as "%s"', cls.config['args']['snippet'])
        cls.logger.debug('configured argument --tags as %s', cls.config['args']['tags'])
        cls.logger.debug('configured argument --brief as "%s"', cls.config['args']['brief'])
        cls.logger.debug('configured argument --links as %s', cls.config['args']['links'])
        cls.logger.debug('configured argument --find as %s', cls.config['args']['find'])
        cls.logger.debug('configured argument --delete as %d', cls.config['args']['delete'])
        cls.logger.debug('configured argument --export as "%s"', cls.config['args']['export'])
        cls.logger.debug('configured argument --profiler as %s', cls.config['args']['profiler'])
        cls.logger.debug('extracted export file format as "%s"', cls.config['args']['export_format'])

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
    def get_links(cls):
        """Get links for the snippet or resolution."""

        return cls.config['args']['links']

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
    def is_export_format_yaml(cls):
        """Test if export format is yaml."""

        if cls.config['args']['export_format'] == Const.EXPORT_YAML:
            return True

        return False

    @classmethod
    def is_export_format_json(cls):
        """Test if export format is json."""

        if cls.config['args']['export_format'] == Const.EXPORT_JSON:
            return True

        return False

    @classmethod
    def is_export_format_text(cls):
        """Test if export format is text."""

        if cls.config['args']['export_format'] == Const.EXPORT_TEXT:
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
    def is_profiled(cls):
        """Check if the code profiler is run."""

        return cls.config['args']['profiler']

    @classmethod
    def _parse_snippet(cls):
        """Preprocess the user given snippet."""

        arg = cls.args.get_snippet()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_resolve(cls):
        """Preprocess the user given resolution."""

        arg = cls.args.get_resolve()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_brief(cls):
        """Preprocess the user given brief description."""

        arg = cls.args.get_brief()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_tags(cls):
        """Process the user given tag keywords."""

        arg = cls.args.get_tags()

        return cls._parse_keywords(arg)

    @classmethod
    def _parse_links(cls):
        """Preprocess the user given links."""

        links = cls.args.get_links()
        # Examples: Support processing of:
        #           1. -l docker container cleanup # Space separated string of links
        link_list = links.split()

        return sorted(link_list)

    @classmethod
    def _parse_find(cls):
        """Process the user given find keywords."""

        arg = cls.args.get_find()

        return cls._parse_keywords(arg)

    @classmethod
    def _parse_write(cls):
        """Process the user given input from editor."""

        return cls.args.get_write()

    @classmethod
    def _parse_delete(cls):
        """Process the user given delete keywords to remove snippet."""

        arg = cls.args.get_delete()
        if arg:
            return arg

        return 0

    @classmethod
    def _parse_export(cls):
        """Preprocess the user given export file."""

        export_file = cls.args.get_export()
        filename, file_extension = os.path.splitext(export_file)
        if filename and ('yaml' in file_extension or 'yml' in file_extension):
            export_file = filename + '.yaml'

            return (export_file, Const.EXPORT_YAML)
        elif filename and 'json' in file_extension:
            export_file = filename + '.json'

            return (export_file, Const.EXPORT_JSON)

        elif filename and ('txt' in file_extension or 'text' in file_extension):
            export_file = filename + '.txt'

            return (export_file, Const.EXPORT_TEXT)

        cls.logger.info('unsupported export file format "%s"', file_extension)

        return ('', Const.EXPORT_YAML)

    @classmethod
    def _parse_keywords(cls, keywords):
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

    @classmethod
    def _set_editor_input(cls):
        """Read and set the user provided values from the editor."""

        if cls.config['args']['write']:
            cls.logger.debug('using parameters from editor')
            snippet = re.search('%s(.*)%s' % (Const.EDITOR_SNIPPET_HEAD, Const.EDITOR_SNIPPET_TAIL), \
                                 cls.config['args']['write'], re.DOTALL)
            if snippet:
                line_list = list(map(lambda s: s.strip(), snippet.group(1).rstrip().split(Const.NEWLINE)))
                cls.config['args']['snippet'] = Const.NEWLINE.join(line_list)

            brief = re.search('%s(.*)%s' % (Const.EDITOR_BRIEF_HEAD, Const.EDITOR_BRIEF_TAIL), \
                               cls.config['args']['write'], re.DOTALL)
            if brief:
                line_list = list(map(lambda s: s.strip(), brief.group(1).rstrip().split(Const.NEWLINE)))
                cls.config['args']['brief'] = Const.NEWLINE.join(line_list)

            tags = re.search('%s(.*)%s' % (Const.EDITOR_TAGS_HEAD, Const.EDITOR_TAGS_TAIL), \
                              cls.config['args']['write'], re.DOTALL)
            if tags:
                line_list = list(map(lambda s: s.strip(), tags.group(1).rstrip().split(Const.NEWLINE)))
                cls.config['args']['tags'] = cls._parse_keywords(line_list)

            links = re.search('%s(.*)%s' % (Const.EDITOR_LINKS_HEAD, Const.EDITOR_LINKS_TAIL), \
                               cls.config['args']['write'], re.DOTALL)
            if links:
                line_list = list(map(lambda s: s.strip(), links.group(1).rstrip().split(Const.NEWLINE)))
                cls.config['args']['links'] = sorted(line_list)
