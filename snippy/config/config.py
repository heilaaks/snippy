#!/usr/bin/env python3

"""config.py: Configuration management."""

import re
import copy
import os.path
import datetime
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.editor import Editor


class Config(object):  # pylint: disable=too-many-public-methods
    """Global configuration management."""

    source = None
    logger = None
    config = {}

    def __init__(self, source=None):
        Config.logger = Logger(__name__).get()
        Config.source = source
        Config._set_config()

    @classmethod
    def _set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['root'] = os.path.realpath(os.path.join(os.getcwd()))
        cls.config['content'] = {}
        cls.config['content']['category'] = Config.source.get_content_category()
        cls.config['content']['data'] = cls._parse_content_data()
        cls.config['content']['brief'] = cls._parse_content_brief()
        cls.config['content']['group'] = cls._parse_content_group()
        cls.config['content']['tags'] = cls._parse_content_tags()
        cls.config['content']['links'] = cls._parse_content_links()
        cls.config['content']['filename'] = Const.EMPTY
        cls.config['options'] = {}
        cls.config['options']['no_ansi'] = Config.source.is_no_ansi()
        cls.config['options']['migrate_defaults'] = Config.source.is_defaults()
        cls.config['options']['migrate_template'] = Config.source.is_template()
        cls.config['options']['debug'] = Config.source.is_debug()
        cls.config['digest'] = cls._parse_digest()
        cls.config['operation'] = {}
        cls.config['operation']['task'] = Config.source.get_operation()
        cls.config['operation']['file'] = {}
        cls.config['operation']['file']['name'], cls.config['operation']['file']['type'] = cls._parse_operation_file()
        cls.config['search'] = {}
        cls.config['search']['field'], cls.config['search']['keywords'] = cls._parse_search()
        cls.config['search']['filter'] = cls._parse_search_filter()
        cls.config['input'] = {}
        cls.config['input']['editor'] = Config.source.is_editor()
        cls.config['input']['digest'] = Config.source.is_content_digest()
        cls.config['input']['data'] = Config.source.is_content_data()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = pkg_resources.resource_filename('snippy', 'data/storage')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = {}
        cls.config['storage']['schema']['path'] = pkg_resources.resource_filename('snippy', 'data/config')
        cls.config['storage']['schema']['file'] = 'database.sql'
        cls.config['storage']['in_memory'] = False

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
    def get_content(cls, content, use_editor=False):
        """Return content after it has been optionally edited."""

        if cls.is_editor() or use_editor:
            content = Config._get_edited_content(content)

        return content

    @classmethod
    def get_text_contents(cls, content, edited):
        """Return contents from specified text file."""

        data = []
        contents = []
        editor = Editor(content, Config.get_utc_time(), edited)
        if editor.get_edited_category() == Const.SNIPPET:
            data = Config.split_text_content(edited, '# Add mandatory snippet below', 2)
        elif editor.get_edited_category() == Const.SOLUTION:
            data = Config.split_text_content(edited, '## BRIEF :', 1)
        else:
            Cause.set_text('could not identify text template content category')

        editor = None
        for item in data:
            content_copy = copy.copy(content)
            editor = Editor(content_copy, Config.get_utc_time(), item)
            content_copy.set((editor.get_edited_data(),
                              editor.get_edited_brief(),
                              editor.get_edited_group(),
                              editor.get_edited_tags(),
                              editor.get_edited_links(),
                              editor.get_edited_category(),
                              editor.get_edited_filename(),
                              editor.get_edited_date(),
                              content_copy.get_digest(),
                              content_copy.get_metadata(),
                              content_copy.get_key()))
            content_copy.update_digest()
            if content_copy.is_data_template(edited=item):
                Cause.set_text('no content was stored because the content data is matching to empty template')

            contents.append(content_copy)

        return contents

    @classmethod
    def split_text_content(cls, edited, split, offset):
        """Split solution content from a text file."""

        # Find line numbers that are identified by split tag and offset. The matching
        # line numbers are substracted with offset to get the first line of the solution.
        # The first item from the list is popped and used as a head and following items
        # are treated as as line numbers where the next solution starts.
        edited_list = edited.split(Const.NEWLINE)
        solutions = []
        line_numbers = [i for i, line in enumerate(edited_list) if line.startswith(split)]
        line_numbers[:] = [x-offset for x in line_numbers]
        if line_numbers:
            head = line_numbers.pop(0)
            for line in line_numbers:
                solutions.append(Const.NEWLINE.join(edited_list[head:line]))
                head = line
            solutions.append(Const.NEWLINE.join(edited_list[head:]))

        return solutions

    @classmethod
    def get_content_template(cls, content):
        """Return content in text template."""

        editor = Editor(content, Config.get_utc_time())
        template = editor.get_template()

        return template

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
    def is_migrate_defaults(cls):
        """Test if migrate operation was related to content defaults."""

        return True if cls.config['options']['migrate_defaults'] else False

    @classmethod
    def is_migrate_template(cls):
        """Test if migrate operation was related to content template."""

        return True if cls.config['options']['migrate_template'] else False

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
    def get_content_valid_digest(cls):
        """Return digest identifying the content."""

        digest = Const.EMPTY
        if len(cls.config['digest']) >= Const.DIGEST_MIN_LENGTH:
            digest = cls.config['digest']
        else:
            cls.logger.info('too short digest %d, minimum length is %d', len(cls.config['digest']), Const.DIGEST_MIN_LENGTH)

        return digest

    @classmethod
    def validate_search_context(cls, contents, operation):  # pylint: disable=too-many-branches
        """Validate content search context."""

        # Search keys are treated in priority order of 1) digest, 2) content data
        # and 3) search keywords. Search keywords are already validated and invalid
        # keywords are interpreted as 'list all' which is always correct at this
        # point.
        text = Const.EMPTY
        cls.logger.info('validating search context with %d results', len(contents))
        if cls.is_content_digest():
            if cls.get_content_digest():
                if not contents:
                    text = 'cannot find content with message digest %s' % cls.get_content_digest()
                elif len(contents) > 1:
                    text = ('given digest %.16s matches (%d) more than once preventing ' +
                            'the operation') % (cls.get_content_digest(), len(contents))
            else:
                text = 'cannot use empty message digest to %s content' % operation
        elif cls.is_content_data():
            if cls.get_content_data():
                data = Const.EMPTY.join(cls.get_content_data())
                data = data[:30] + (data[30:] and '...')
                if not contents:
                    text = 'cannot find content with content data \'%s\'' % data
                elif len(contents) > 1:
                    text = ('given content data %s matches (%d) more than once preventing the ' +
                            'operation') % (data, len(contents))
            else:
                text = 'cannot use empty content data to %s content' % operation
        elif cls.is_search_keywords():
            if len(contents) > 1:
                text = ('given search keyword matches (%d) more than once preventing ' +
                        'the operation') % len(contents)
        else:
            text = 'no message digest, content data or search keywords were provided'

        return text

    @classmethod
    def get_filename(cls):
        """Return content filename."""

        return cls.config['content']['filename']

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
    def is_search_keywords(cls):
        """Test if search is made with any keyword field."""

        return True if cls.config['search']['field'] != Const.NO_SEARCH else False

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
    def is_content_data(cls):
        """Test if content data was defined from command line."""

        return cls.config['input']['data']

    @classmethod
    def is_content_digest(cls):
        """Test if content digest was defined from command line."""

        return cls.config['input']['digest']

    @classmethod
    def get_operation_file(cls, content_filename=Const.EMPTY):
        """Return file for operation."""

        # Use the content filename only in case of export operation and
        # when the user did not define the target file from command line.
        filename = cls.config['operation']['file']['name']
        if cls.is_operation_export() and content_filename and not Config.source.get_operation_file():
            filename = content_filename

        return filename

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
    def is_supported_file_format(cls):
        """Test if file format is supported."""

        return True if cls.is_file_type_yaml() or cls.is_file_type_json() or cls.is_file_type_text() else False

    @classmethod
    def use_ansi(cls):
        """Test if ANSI characters like colors are disabled in the command output."""

        return False if cls.config['options']['no_ansi'] else True

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

    @staticmethod
    def get_utc_time():
        """Get UTC time."""

        utc = datetime.datetime.utcnow()

        return utc.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def is_debug(cls):
        """Test if debug option was used."""

        return True if cls.config['options']['debug'] else False

    @classmethod
    def _parse_content_data(cls):
        """Process content data."""

        arg = Config.source.get_content_data()
        if arg:
            content = arg.split(Const.DELIMITER_DATA)

            return tuple(content)

        return Const.EMPTY_TUPLE

    @classmethod
    def _parse_content_brief(cls):
        """Process content brief description."""

        arg = Config.source.get_content_brief()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_group(cls):
        """Process content group."""

        arg = Config.source.get_content_group()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_tags(cls):
        """Process content tags."""

        arg = Config.source.get_content_tags()

        return Editor.get_keywords(arg)

    @classmethod
    def _parse_content_links(cls):
        """Process content reference links."""

        links = Config.source.get_content_links()
        # Examples: Support processing of:
        #           1. -l docker container cleanup # Space separated string of links
        link_list = links.split()
        link_list = sorted(link_list)

        return tuple(link_list)

    @classmethod
    def _parse_digest(cls):
        """Process message digest identifying the operation target."""

        arg = Config.source.get_content_digest()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_search(cls):
        """Process the user given search keywords and field."""

        args = ()
        field = Const.NO_SEARCH
        if Config.source.is_search_all():
            args = Config.source.get_search_all()
            field = Const.SEARCH_ALL
        elif Config.source.is_search_tag():
            args = Config.source.get_search_tag()
            field = Const.SEARCH_TAG
        elif Config.source.is_search_grp():
            args = Config.source.get_search_grp()
            field = Const.SEARCH_GRP

        # The args list may be empty or it can contain empty string. Both cases
        # must be evaluated to 'match all'.
        if not any(args) and (field != Const.NO_SEARCH):
            cls.logger.info('listing all content from category because no keywords were provided')
            args = ('.')

        return (field, Editor.get_keywords(args))

    @classmethod
    def _parse_search_filter(cls):
        """Process the user given search filter."""

        regexp = Config.source.get_search_filter()

        try:
            re.compile(regexp)
        except re.error:
            Cause.set_text('listed matching content without filter because it was not syntactically ' +
                           'correct regular expression')
            regexp = Const.EMPTY

        return regexp

    @classmethod
    def _get_edited_content(cls, content):
        """Read and set the user provided values from editor."""

        editor = Editor(content, Config.get_utc_time())
        editor.read_content()
        if editor.is_content_identified():
            cls.config['content']['data'] = editor.get_edited_data()
            cls.config['content']['brief'] = editor.get_edited_brief()
            cls.config['content']['group'] = editor.get_edited_group()
            cls.config['content']['tags'] = editor.get_edited_tags()
            cls.config['content']['links'] = editor.get_edited_links()
            cls.config['content']['filename'] = editor.get_edited_filename()
            content.set((cls.get_content_data(),
                         cls.get_content_brief(),
                         cls.get_content_group(),
                         cls.get_content_tags(),
                         cls.get_content_links(),
                         content.get_category(),
                         cls.get_filename(),
                         content.get_utc(),
                         content.get_digest(),
                         content.get_metadata(),
                         content.get_key()))
        else:
            Cause.set_text('could not identify edited content category - please keep tags in place')

        return content

    @classmethod
    def _parse_operation_file(cls):
        """Return the filename and the format of the file."""

        filename = Config.source.get_operation_file()
        filetype = Const.FILE_TYPE_NONE

        defaults = 'snippets.yaml'
        template = 'snippet-template.txt'
        if Config.is_category_solution():
            defaults = 'solutions.yaml'
            template = 'solution-template.txt'

        # Run migrate operation with default content.
        if cls.is_migrate_defaults():
            filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/default'), defaults)

        # Run migrate operation with content template.
        if cls.is_migrate_template():
            filename = os.path.join('./', template)

        # Run export operation with specified content without specifying
        # the operation file.
        if cls.is_operation_export() and cls.get_content_digest():
            if Config.is_category_snippet() and not filename:
                filename = 'snippet.' + Const.FILE_TYPE_TEXT
            elif Config.is_category_solution() and not filename:
                filename = 'solution.' + Const.FILE_TYPE_TEXT

        # In case user did not provide filename, set defaults. For example
        # if user defined export or import operation without the file, the
        # default files are used.
        if not filename:
            filename = os.path.join('./', defaults)

        # User defined content to/from user specified file.
        name, extension = os.path.splitext(filename)
        if name and ('yaml' in extension or 'yml' in extension):
            filetype = Const.FILE_TYPE_YAML
        elif name and 'json' in extension:
            filetype = Const.FILE_TYPE_JSON
        elif name and ('txt' in extension or 'text' in extension):
            filetype = Const.FILE_TYPE_TEXT
        else:
            Cause.set_text('cannot identify file format for file {}'.format(filename))

        return (filename, filetype)
