#!/usr/bin/env python3

"""config.py: Configuration management."""

import re
import sys
import os.path
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Arguments


class Config(object): # pylint: disable=too-many-public-methods
    """Global configuration management."""

    args = {}
    config = {}
    logger = None

    def __init__(self):
        Config.logger = Logger(__name__).get()
        Config.args = Arguments()
        Config._set_config()

    @classmethod
    def _set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['root'] = os.path.realpath(os.path.join(os.getcwd()))
        cls.config['args'] = {}
        cls.config['args']['job'] = cls._parse_job()
        cls.config['args']['role'] = cls._parse_job_role()
        cls.config['args']['editor'] = cls._parse_editor()
        cls.config['args']['file'] = {}
        cls.config['args']['file']['name'], cls.config['args']['file']['type'] = cls._parse_file()
        cls.config['args']['id'] = cls._parse_id()
        cls.config['args']['content'] = cls._parse_content()
        cls.config['args']['brief'] = cls._parse_brief()
        cls.config['args']['category'] = cls._parse_category()
        cls.config['args']['tags'] = cls._parse_tags()
        cls.config['args']['links'] = cls._parse_links()
        cls.config['args']['search'] = cls._parse_search()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = os.path.join(os.environ.get('HOME'), 'devel/snippy-db')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = os.path.join(cls.config['root'], 'snippy/storage/database/database.sql')
        cls.config['storage']['in_memory'] = False # Enabled only for testing.

        cls._set_editor_input()

        cls.logger.debug('configured argument --job as "%s"', cls.config['args']['job'])
        cls.logger.debug('configured argument --role as "%s"', cls.config['args']['role'])
        cls.logger.debug('configured argument --editor as "%s"', cls.config['args']['editor'])
        cls.logger.debug('configured argument --file as "%s"', cls.config['args']['file']['name'])
        cls.logger.debug('configured argument --id as "%s"', cls.config['args']['id'])
        cls.logger.debug('configured argument --content as "%s"', cls.config['args']['content'])
        cls.logger.debug('configured argument --brief as "%s"', cls.config['args']['brief'])
        cls.logger.debug('configured argument --category as "%s"', cls.config['args']['category'])
        cls.logger.debug('configured argument --tags as %s', cls.config['args']['tags'])
        cls.logger.debug('configured argument --links as %s', cls.config['args']['links'])
        cls.logger.debug('configured argument --search as %s', cls.config['args']['search'])
        cls.logger.debug('extracted file format from argument --file "%s"', cls.config['args']['file']['type'])

    @classmethod
    def is_role_snippet(cls):
        """Test if defined role was snippet."""

        if cls.config['args']['role'] == 'snippet':
            return True

        return False

    @classmethod
    def is_role_resolve(cls):
        """Test if defined role was resolve."""

        if cls.config['args']['role'] == 'resolve':
            return True

        return False

    @classmethod
    def is_job_create(cls):
        """Test if defined job was create."""

        return True if cls.config['args']['job'] == 'create' else False

    @classmethod
    def is_job_search(cls):
        """Test if defined job was search."""

        return True if cls.config['args']['job'] == 'search' else False

    @classmethod
    def is_job_delete(cls):
        """Test if defined job was delete."""

        return True if cls.config['args']['job'] == 'delete' else False

    @classmethod
    def is_job_export(cls):
        """Test if defined job was export."""

        return True if cls.config['args']['job'] == 'export' else False

    @classmethod
    def is_job_import(cls):
        """Test if defined job was import."""

        return True if cls.config['args']['job'] == 'import' else False

    @classmethod
    def get_file(cls):
        """Get job supplementary filename."""

        return cls.config['args']['file']['name']

    @classmethod
    def get_target_id(cls):
        """Get job supplementary target identity."""

        return cls.config['args']['id']

    @classmethod
    def get_job_content(cls):
        """Get content for the job."""

        return cls.config['args']['content']

    @classmethod
    def get_job_brief(cls):
        """Get brief description for the job."""

        return cls.config['args']['brief']

    @classmethod
    def get_job_category(cls):
        """Get category for the job."""

        return cls.config['args']['category']

    @classmethod
    def get_job_tags(cls):
        """Get tags for the job."""

        return cls.config['args']['tags']

    @classmethod
    def get_job_links(cls):
        """Get links for the job."""

        return cls.config['args']['links']

    @classmethod
    def get_search_keywords(cls):
        """Get user provided list of search keywords."""

        return cls.config['args']['search']


    @classmethod
    def is_file_type_yaml(cls):
        """Test if supplementary file format is yaml."""

        if cls.config['args']['file']['type'] == Const.FILE_TYPE_YAML:
            return True

        return False

    @classmethod
    def is_file_type_json(cls):
        """Test if supplementary file format is json."""

        if cls.config['args']['file']['type'] == Const.FILE_TYPE_JSON:
            return True

        return False

    @classmethod
    def is_file_type_text(cls):
        """Test if supplementary file format is text."""

        if cls.config['args']['file']['type'] == Const.FILE_TYPE_TEXT:
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
    def _parse_job(cls):
        """Process the job."""

        return cls.args.get_job()

    @classmethod
    def _parse_job_role(cls):
        """Process the job role."""

        return cls.args.get_job_role()

    @classmethod
    def _parse_editor(cls):
        """Process the input from editor."""

        return cls.args.get_editor()

    @classmethod
    def _parse_file(cls):
        """Process supplementary file the job."""

        return cls._get_file_type(cls.args.get_file())

    @classmethod
    def _parse_id(cls):
        """Process supplementary id for the job."""

        arg = cls.args.get_id()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_content(cls):
        """Process the job content."""

        arg = cls.args.get_content()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_brief(cls):
        """Process the brief description for the job."""

        arg = cls.args.get_brief()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_category(cls):
        """Process the job category."""

        arg = cls.args.get_category()
        if arg:
            return arg

        return ''

    @classmethod
    def _parse_tags(cls):
        """Process the job tags."""

        arg = cls.args.get_tags()

        return cls._get_keywords(arg)

    @classmethod
    def _parse_links(cls):
        """Process the links of the job."""

        links = cls.args.get_links()
        # Examples: Support processing of:
        #           1. -l docker container cleanup # Space separated string of links
        link_list = links.split()

        return sorted(link_list)

    @classmethod
    def _parse_search(cls):
        """Process the user given search keywords."""

        arg = cls.args.get_search()
        if arg:
            cls.config['args']['job'] = 'search'

        return cls._get_keywords(arg)

    @classmethod
    def _get_file_type(cls, filename):
        """Get the file format and file."""

        filename, file_extension = os.path.splitext(filename)
        if filename and ('yaml' in file_extension or 'yml' in file_extension):
            filename = filename + '.yaml'

            return (filename, Const.FILE_TYPE_YAML)
        elif filename and 'json' in file_extension:
            filename = filename + '.json'

            return (filename, Const.FILE_TYPE_JSON)

        elif filename and ('txt' in file_extension or 'text' in file_extension):
            filename = filename + '.txt'
            if cls.is_job_import():
                cls.logger.error('unsupported file format for import "%s"', file_extension)
                sys.exit(1)

            return (filename, Const.FILE_TYPE_TEXT)
        else:
            cls.logger.info('unsupported export file format "%s"', file_extension)

        return ('', Const.FILE_TYPE_YAML)

    @classmethod
    def _get_keywords(cls, keywords):
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

        edited_input = cls.config['args']['editor']
        if edited_input:
            cls.logger.debug('using parameters from editor')
            cls.config['args']['content'] = Config._get_user_string(edited_input, Const.EDITED_SNIPPET)
            cls.config['args']['brief'] = Config._get_user_string(edited_input, Const.EDITED_BRIEF)
            cls.config['args']['category'] = Config._get_user_string(edited_input, Const.EDITED_CATEGORY)
            cls.config['args']['tags'] = Config._get_user_list(edited_input, Const.EDITED_TAGS)
            cls.config['args']['links'] = Config._get_user_list(edited_input, Const.EDITED_LINKS)

    @classmethod
    def _get_user_list(cls, edited_string, constants):
        """Parse list type value from editor input."""

        user_answer = re.search('%s(.*)%s' % (constants['head'], constants['tail']), edited_string, re.DOTALL)
        if user_answer:
            value_list = list(map(lambda s: s.strip(), user_answer.group(1).rstrip().split(Const.NEWLINE)))

            return value_list

        return []

    @classmethod
    def _get_user_string(cls, edited_string, constants):
        """Parse string type value from editor input."""

        value_list = cls._get_user_list(edited_string, constants)

        return constants['delimiter'].join(value_list)
