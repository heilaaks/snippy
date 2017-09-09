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
        cls.config['operation'] = {}
        cls.config['operation']['task'] = cls._parse_operation()
        cls.config['operation']['file'] = {}
        cls.config['operation']['file']['name'], cls.config['operation']['file']['type'] = cls._parse_operation_file()
        cls.config['content'] = {}
        cls.config['content']['type'] = cls._parse_content_type()
        cls.config['content']['data'] = cls._parse_content_data()
        cls.config['content']['brief'] = cls._parse_content_brief()
        cls.config['content']['group'] = cls._parse_content_group()
        cls.config['content']['tags'] = cls._parse_content_tags()
        cls.config['content']['links'] = cls._parse_content_links()
        cls.config['digest'] = cls._parse_digest()
        cls.config['search'] = {}
        cls.config['search']['field'], cls.config['search']['keywords'] = cls._parse_search()
        cls.config['input'] = {}
        cls.config['input']['editor'] = cls._parse_editor()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = os.path.join(os.environ.get('HOME'), 'devel/snippy-db')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = os.path.join(cls.config['root'], 'snippy/storage/database/database.sql')
        cls.config['storage']['in_memory'] = False # Enabled only for testing.
        cls.config['exit_code'] = 'OK'

        cls.logger.debug('configured value from positional argument as "%s"', cls.config['operation'])
        cls.logger.debug('configured value from content type as "%s"', cls.config['content']['type'])
        cls.logger.debug('configured value from --content as "%s"', cls.config['content']['data'])
        cls.logger.debug('configured value from --brief as "%s"', cls.config['content']['brief'])
        cls.logger.debug('configured value from --group as "%s"', cls.config['content']['group'])
        cls.logger.debug('configured value from --tags as %s', cls.config['content']['tags'])
        cls.logger.debug('configured value from --links as %s', cls.config['content']['links'])
        cls.logger.debug('configured value from --digest as "%s"', cls.config['digest'])
        cls.logger.debug('configured value from --editor as %s', cls.config['input']['editor'])
        cls.logger.debug('configured value from --file as "%s"', cls.config['operation']['file']['name'])
        cls.logger.debug('configured value from search field as %s', cls.config['search']['field'])
        cls.logger.debug('configured value from search keywords as %s', cls.config['search']['keywords'])
        cls.logger.debug('extracted file format from argument --file "%s"', cls.config['operation']['file']['type'])

    @classmethod
    def get_snippet(cls, snippet=None, use_editor=None):
        """Return snippet after it has been optionally edited."""

        # Set the defaults from commmand line to editing window. If the
        # snippet is not provided, it indicates update with digest only.
        if not snippet:
            snippet = {'content': cls.get_content_data(), 'brief': cls.get_content_brief(),
                       'group': cls.get_content_group(), 'tags': cls.get_content_tags(),
                       'links': cls.get_content_links()}

        if cls.is_editor() or use_editor:
            snippet = cls._set_editor_content(snippet)

        return snippet

    @classmethod
    def is_operation_create(cls):
        """Test if operation was create."""

        return True if cls.config['operation']['task'] == 'create' else False

    @classmethod
    def is_operation_search(cls):
        """Test if operation was search."""

        return True if cls.config['operation']['task'] == 'search' else False

    @classmethod
    def is_operation_update(cls):
        """Test if operation was update."""

        return True if cls.config['operation']['task'] == 'update' else False

    @classmethod
    def is_operation_delete(cls):
        """Test if operation was delete."""

        return True if cls.config['operation']['task'] == 'delete' else False

    @classmethod
    def is_operation_export(cls):
        """Test if operation was export."""

        return True if cls.config['operation']['task'] == 'export' else False

    @classmethod
    def is_operation_import(cls):
        """Test if operation was import."""

        return True if cls.config['operation']['task'] == 'import' else False

    @classmethod
    def is_content_snippet(cls):
        """Test if content was snippet."""

        return True if cls.config['content']['type'] == 'snippet' else False

    @classmethod
    def is_content_solution(cls):
        """Test if content was solution."""

        return True if cls.config['content']['type'] == 'solution' else False

    @classmethod
    def get_content_data(cls):
        """Return content data."""

        return cls.config['content']['data']

    @classmethod
    def get_content_brief(cls):
        """Return content brief description."""

        return cls.config['content']['brief']

    @classmethod
    def get_content_group(cls):
        """Return content group."""

        return cls.config['content']['group']

    @classmethod
    def get_content_tags(cls):
        """Return content tags."""

        return cls.config['content']['tags']

    @classmethod
    def get_content_links(cls):
        """Return content reference links."""

        return cls.config['content']['links']

    @classmethod
    def get_operation_digest(cls):
        """Return digest identifying the operation target."""

        return cls.config['digest']

    @classmethod
    def is_search_all(cls):
        """Test if all fields are searched."""

        return True if cls.config['search']['field'] == Const.SEARCH_ALL else False

    @classmethod
    def get_search_keywords(cls):
        """Return list of search keywords."""

        return cls.config['search']['keywords']

    @classmethod
    def is_editor(cls):
        """Test if editor is used to input content."""

        return cls.config['input']['editor']

    @classmethod
    def get_operation_file(cls):
        """Return file for operation."""

        return cls.config['operation']['file']['name']

    @classmethod
    def is_file_type_yaml(cls):
        """Test if file format is yaml."""

        return True if cls.config['operation']['file']['type'] == Const.FILE_TYPE_YAML else False

    @classmethod
    def is_file_type_json(cls):
        """Test if file format is json."""

        return True if cls.config['operation']['file']['type'] == Const.FILE_TYPE_JSON else False

    @classmethod
    def is_file_type_text(cls):
        """Test if file format is text."""

        return True if cls.config['operation']['file']['type'] == Const.FILE_TYPE_TEXT else False

    @classmethod
    def get_storage_path(cls):
        """Return path of the persistent storage."""

        return cls.config['storage']['path']

    @classmethod
    def get_storage_file(cls):
        """Return path and file of the persistent storage."""

        return os.path.join(cls.config['storage']['path'], cls.config['storage']['file'])

    @classmethod
    def get_storage_schema(cls):
        """Return storage schema."""

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
    def set_exit_cause(cls, code):
        """Set exit cause for the tool."""

        # Only allow one update to get the original cause.
        if cls.config['exit_code'] == 'OK':
            cls.config['exit_code'] = 'NOK: ' + code

    @classmethod
    def get_exit_cause(cls):
        """Return exit cause for the tool."""

        return cls.config['exit_code']

    @classmethod
    def _parse_operation(cls):
        """Process the operation for the content."""

        return cls.args.get_operation()

    @classmethod
    def _parse_content_type(cls):
        """Process the content type."""

        return cls.args.get_content_type()

    @classmethod
    def _parse_content_data(cls):
        """Process content data."""

        arg = cls.args.get_content_data()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_brief(cls):
        """Process content brief description."""

        arg = cls.args.get_content_brief()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_group(cls):
        """Process content group."""

        arg = cls.args.get_content_group()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_tags(cls):
        """Process content tags."""

        arg = cls.args.get_content_tags()

        return cls._get_keywords(arg)

    @classmethod
    def _parse_content_links(cls):
        """Process content reference links."""

        links = cls.args.get_content_links()
        # Examples: Support processing of:
        #           1. -l docker container cleanup # Space separated string of links
        link_list = links.split()

        return sorted(link_list)

    @classmethod
    def _parse_digest(cls):
        """Process message digest identifying the operation target."""

        arg = cls.args.get_operation_digest()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_search(cls):
        """Process the user given search keywords and field."""

        arg = ()
        field = Const.SEARCH_ALL
        if cls.args.get_search_all():
            arg = cls.args.get_search_all()
        elif cls.args.get_search_tag():
            arg = cls.args.get_search_tag()
            field = Const.SEARCH_TAG
        elif cls.args.get_search_grp():
            arg = cls.args.get_search_grp()
            field = Const.SEARCH_GRP

        return (field, cls._get_keywords(arg))

    @classmethod
    def _parse_editor(cls):
        """Process editor usage."""

        # Implicitly force editor in case of update operation with message digest.
        editor = cls.args.get_editor()
        if cls.is_operation_update() and cls.get_operation_digest():
            editor = True

        return editor

    @classmethod
    def _set_editor_content(cls, snippet=None):
        """Read and set the user provided values from editor."""

        if not snippet:
            snippet = {'content': Const.EMPTY, 'brief': Const.EMPTY, 'group': Const.EMPTY, 'tags': Const.EMPTY,
                       'links': Const.EMPTY}

        edited_input = cls.args.get_editor_content(snippet)
        if edited_input:
            cls.logger.debug('using parameters from editor')
            cls.config['content']['data'] = Config._get_user_string(edited_input, Const.EDITED_SNIPPET)
            cls.config['content']['brief'] = Config._get_user_string(edited_input, Const.EDITED_BRIEF)
            cls.config['content']['group'] = Config._get_user_string(edited_input, Const.EDITED_GROUP)
            cls.config['content']['tags'] = Config._get_user_list(edited_input, Const.EDITED_TAGS)
            cls.config['content']['links'] = Config._get_user_list(edited_input, Const.EDITED_LINKS)
            cls.logger.debug('configured value from editor for content as "%s"', cls.config['content']['data'])
            cls.logger.debug('configured value from editor for brief as "%s"', cls.config['content']['brief'])
            cls.logger.debug('configured value from editor for group as "%s"', cls.config['content']['group'])
            cls.logger.debug('configured value from editor for tags as %s', cls.config['content']['tags'])
            cls.logger.debug('configured value from editor for links as %s', cls.config['content']['links'])

        snippet = {'content': cls.get_content_data(), 'brief': cls.get_content_brief(),
                   'group': cls.get_content_group(), 'tags': cls.get_content_tags(),
                   'links': cls.get_content_links()}

        return snippet

    @classmethod
    def _get_user_string(cls, edited_string, constants):
        """Parse string type value from editor input."""

        value_list = cls._get_user_list(edited_string, constants)

        return constants['delimiter'].join(value_list)

    @classmethod
    def _get_user_list(cls, edited_string, constants):
        """Parse list type value from editor input."""

        user_answer = re.search('%s(.*)%s' % (constants['head'], constants['tail']), edited_string, re.DOTALL)
        if user_answer and not user_answer.group(1).isspace():
            value_list = list(map(lambda s: s.strip(), user_answer.group(1).rstrip().split(constants['delimiter'])))

            return value_list

        return []

    @classmethod
    def _parse_operation_file(cls):
        """Process file for operation."""

        return cls._get_file_type(cls.args.get_operation_file())

    @classmethod
    def _get_file_type(cls, filename):
        """Return the file format and file."""

        if not filename:
            return (Const.EMPTY, Const.FILE_TYPE_NONE)

        filename, file_extension = os.path.splitext(filename)
        if filename and ('yaml' in file_extension or 'yml' in file_extension):
            filename = filename + '.yaml'

            return (filename, Const.FILE_TYPE_YAML)
        elif filename and 'json' in file_extension:
            filename = filename + '.json'

            return (filename, Const.FILE_TYPE_JSON)

        elif filename and ('txt' in file_extension or 'text' in file_extension):
            filename = filename + '.txt'
            if cls.is_operation_import():
                cls.logger.error('unsupported file format for import "%s"', file_extension)
                sys.exit(1)

            return (filename, Const.FILE_TYPE_TEXT)
        else:
            cls.logger.info('unsupported export file format "%s"', file_extension)

        return (Const.EMPTY, Const.FILE_TYPE_YAML)

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
