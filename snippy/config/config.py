#!/usr/bin/env python3

"""config.py: Configuration management."""

import re
import sys
import os.path
import inspect
import pkg_resources
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Arguments
from snippy.config import Editor
from snippy.format import Format


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
        cls.config['content'] = {}
        cls.config['content']['category'] = cls._parse_content_category()
        cls.config['content']['data'] = cls._parse_content_data()
        cls.config['content']['brief'] = cls._parse_content_brief()
        cls.config['content']['group'] = cls._parse_content_group()
        cls.config['content']['tags'] = cls._parse_content_tags()
        cls.config['content']['links'] = cls._parse_content_links()
        cls.config['operation'] = {}
        cls.config['operation']['task'] = cls._parse_operation()
        cls.config['operation']['file'] = {}
        cls.config['operation']['file']['name'], cls.config['operation']['file']['type'] = cls._parse_operation_file()
        cls.config['digest'] = cls._parse_digest()
        cls.config['search'] = {}
        cls.config['search']['field'], cls.config['search']['keywords'] = cls._parse_search()
        cls.config['search']['filter'] = cls._parse_search_filter()
        cls.config['input'] = {}
        cls.config['input']['editor'] = cls._parse_editor()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = pkg_resources.resource_filename('snippy', 'data/storage')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = {}
        cls.config['storage']['schema']['path'] = pkg_resources.resource_filename('snippy', 'data/config')
        cls.config['storage']['schema']['file'] = 'database.sql'
        cls.config['storage']['in_memory'] = False
        cls.config['exit_code'] = 'OK'

        cls.logger.debug('configured value from positional argument as "%s"', cls.config['operation']['task'])
        cls.logger.debug('configured value from content category as "%s"', cls.config['content']['category'])
        cls.logger.debug('configured value from --content as %s', cls.config['content']['data'])
        cls.logger.debug('configured value from --brief as "%s"', cls.config['content']['brief'])
        cls.logger.debug('configured value from --group as "%s"', cls.config['content']['group'])
        cls.logger.debug('configured value from --tags as %s', cls.config['content']['tags'])
        cls.logger.debug('configured value from --links as %s', cls.config['content']['links'])
        cls.logger.debug('configured value from --digest as "%s"', cls.config['digest'])
        cls.logger.debug('configured value from --editor as %s', cls.config['input']['editor'])
        cls.logger.debug('configured value from --file as "%s"', cls.config['operation']['file']['name'])
        cls.logger.debug('configured value from search field as %s', cls.config['search']['field'])
        cls.logger.debug('configured value from search keywords as %s', cls.config['search']['keywords'])
        cls.logger.debug('configured value from search filter as %s', cls.config['search']['filter'])
        cls.logger.debug('extracted file format from argument --file "%s"', cls.config['operation']['file']['type'])

    @classmethod
    def get_content(cls, content=None, use_editor=None):
        """Return content after it has been optionally edited."""

        # Set the defaults from commmand line for editor. If content is not
        # provided at all, it tells that operation is done with digest only.
        if not content:
            content = (cls.get_content_data(),
                       cls.get_content_brief(),
                       cls.get_content_group(),
                       cls.get_content_tags(),
                       cls.get_content_links(),
                       cls.get_category(),
                       None, # filename
                       None, # utc
                       None, # digest
                       None, # metadata
                       None) # key

        if cls.is_editor() or use_editor:
            content = Config._get_edited_content(content)

        return content

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
    def is_category_snippet(cls):
        """Test if operation is applied to snippet category."""

        return True if cls.config['content']['category'] == Const.SNIPPET else False

    @classmethod
    def is_category_solution(cls):
        """Test if operation is applied to solution category."""

        return True if cls.config['content']['category'] == Const.SOLUTION else False

    @classmethod
    def is_category_all(cls):
        """Test if operation is applied to all content categories."""

        return True if cls.config['content']['category'] == 'all' else False

    @classmethod
    def get_category(cls):
        """Return content category."""

        return cls.config['content']['category']

    @classmethod
    def set_category(cls, category):
        """Set content category."""

        if category == Const.SOLUTION:
            cls.config['content']['category'] = Const.SOLUTION
        else:
            cls.config['content']['category'] = Const.SNIPPET

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
    def get_content_digest(cls):
        """Return digest identifying the content."""

        return cls.config['digest']

    @classmethod
    def is_search_all(cls):
        """Test if all fields are searched."""

        return True if cls.config['search']['field'] == Const.SEARCH_ALL else False

    @classmethod
    def is_search_grp(cls):
        """Test if search is made only from groups."""

        return True if cls.config['search']['field'] == Const.SEARCH_GRP else False

    @classmethod
    def is_search_tag(cls):
        """Test if search is made only from tags."""

        return True if cls.config['search']['field'] == Const.SEARCH_TAG else False

    @classmethod
    def get_search_keywords(cls):
        """Return list of search keywords."""

        return cls.config['search']['keywords']

    @classmethod
    def get_search_filter(cls):
        """Return search filter."""

        return cls.config['search']['filter']

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

        return os.path.join(cls.config['storage']['schema']['path'], cls.config['storage']['schema']['file'])

    @classmethod
    def set_storage_in_memory(cls, in_memory):
        """Set the storage to be in memory."""

        cls.config['storage']['in_memory'] = in_memory

    @classmethod
    def is_storage_in_memory(cls):
        """Test if storage is defined to be run in memory."""

        return cls.config['storage']['in_memory']

    @classmethod
    def set_cause(cls, cause):
        """Set failure cause."""

        cls.logger.info('%s from module %s', cause, cls._caller())

        # Only allow one update to get the original cause.
        if cls.config['exit_code'] == 'OK':
            cls.config['exit_code'] = 'NOK: ' + cause

    @classmethod
    def get_exit_cause(cls):
        """Return exit cause for the tool."""

        return cls.config['exit_code']

    @classmethod
    def _parse_operation(cls):
        """Process the operation for the content."""

        return cls.args.get_operation()

    @classmethod
    def _parse_content_category(cls):
        """Process the content category."""

        return cls.args.get_content_category()

    @classmethod
    def _parse_content_data(cls):
        """Process content data."""

        arg = cls.args.get_content_data()
        if arg:
            content = arg.split(Const.DELIMITER_CONTENT)

            return tuple(content)

        return Const.EMPTY_TUPLE

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

        return Format.get_keywords(arg)

    @classmethod
    def _parse_content_links(cls):
        """Process content reference links."""

        links = cls.args.get_content_links()
        # Examples: Support processing of:
        #           1. -l docker container cleanup # Space separated string of links
        link_list = links.split()
        link_list = sorted(link_list)


        return tuple(link_list)

    @classmethod
    def _parse_digest(cls):
        """Process message digest identifying the operation target."""

        arg = cls.args.get_content_digest()
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

        return (field, Format.get_keywords(arg))

    @classmethod
    def _parse_search_filter(cls):
        """Process the user given search keywords and field."""

        regexp = cls.args.get_search_filter()

        try:
            re.compile(regexp)
        except re.error:
            cls.logger.info('filter is not a valid regexp "%s"', regexp)
            regexp = Const.EMPTY

        return regexp

    @classmethod
    def _parse_editor(cls):
        """Process editor usage."""

        # Implicitly force editor in case of update operation with message digest.
        editor = cls.args.get_editor()
        if cls.is_operation_update() and cls.get_content_digest():
            editor = True

        return editor

    @classmethod
    def _get_edited_content(cls, content):
        """Read and set the user provided values from editor."""

        editor = Editor(content)
        editor.read_content()
        cls.config['content']['data'] = editor.get_edited_data()
        cls.config['content']['brief'] = editor.get_edited_brief()
        cls.config['content']['group'] = editor.get_edited_group()
        cls.config['content']['tags'] = editor.get_edited_tags()
        cls.config['content']['links'] = editor.get_edited_links()
        content = (cls.get_content_data(),
                   cls.get_content_brief(),
                   cls.get_content_group(),
                   cls.get_content_tags(),
                   cls.get_content_links(),
                   cls.get_category(),
                   None, # filename
                   None, # utc
                   None, # digest
                   None, # metadata
                   None) # key

        return content

    @classmethod
    def _parse_operation_file(cls):
        """Process file for operation."""

        return cls._get_file_type(cls.args.get_operation_file())

    @classmethod
    def _get_file_type(cls, filename):
        """Return the file format and file."""

        if not filename:
            return (Const.EMPTY, Const.FILE_TYPE_NONE)

        # Import default content with keyword 'default'.
        default_file = 'snippets.yaml'
        if Config.is_category_solution():
            default_file = 'solutions.yaml'

        if filename == 'defaults':
            filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/default'), default_file)

            return (filename, Const.FILE_TYPE_YAML)

        # Import content from user specified file.
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

    @staticmethod
    def _caller():
        caller = inspect.stack()[2]
        module = inspect.getmodule(caller[0])

        return module.__name__
