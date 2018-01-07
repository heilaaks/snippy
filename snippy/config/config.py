#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""config.py: Configuration management."""

import sys
import copy
import os.path
import datetime
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.source.editor import Editor


class Config(object):  # pylint: disable=too-many-public-methods
    """Global configuration management."""

    source = None
    logger = None
    config = {}

    def __init__(self):
        if not Config.logger:
            Config.logger = Logger(__name__).get()
        Config.source = None
        Config.config = {}

    @classmethod
    def init(cls):
        """Initialize configuration."""

        # Separated from __init__ to ease mocking in tests.
        cls.logger.debug('initialize storage config')
        cls.storage_file = Config._storage_file()
        cls.db_schema_file = Config._storage_schema()
        cls.server = Config._server()
        cls.debug = Config._debug()

    def reset(self):
        """Reset configuration."""

        self.__init__()
        self.init()

    @classmethod
    def _storage_file(cls):
        """Test that storage path exist."""

        storage_path = pkg_resources.resource_filename('snippy', 'data/storage')
        if os.path.exists(storage_path) and os.access(storage_path, os.W_OK):
            storage_file = os.path.join(storage_path, 'snippy.db')
        else:
            cls.logger.error('NOK: storage path does not exist or is not accessible: %s', storage_path)
            sys.exit(1)

        return storage_file

    @classmethod
    def _storage_schema(cls):
        """Test that database schema file exist."""

        # The database schema is installed with the tool and it must always exist.
        schema_file = os.path.join(pkg_resources.resource_filename('snippy', 'data/config'), 'database.sql')
        if not os.path.isfile(schema_file):
            cls.logger.error('NOK: database schema file path does not exist or is not accessible: %s', schema_file)
            sys.exit(1)

        return schema_file

    @classmethod
    def _server(cls):
        """Test if service is run as a server."""

        return True if '--server' in sys.argv else False

    @classmethod
    def _debug(cls):
        """Test if service is run in debug mode."""

        return True if '--debug' in sys.argv or '-vv' in sys.argv else False

    @classmethod
    def read_source(cls, source):
        """Read configuration source."""

        cls.logger.debug('config source: %s', source)
        Config.source = source
        cls.category = Config.source.category
        cls.operation = Config.source.operation
        cls.content = {}
        cls.content['data'] = Config.source.data
        cls.content['brief'] = Config.source.brief
        cls.content['group'] = Config.source.group
        cls.content['tags'] = Config.source.tags
        cls.content['links'] = Config.source.links
        cls.content['filename'] = Config.source.filename
        cls.digest = Config.source.digest
        cls.search = {}
        cls.search['sall'] = Config.source.sall
        cls.search['stag'] = Config.source.stag
        cls.search['sgrp'] = Config.source.sgrp
        cls.search['regexp'] = Config.source.regexp
        cls.no_ansi = Config.source.no_ansi
        cls.defaults = Config.source.defaults
        cls.template = Config.source.template

        cls.config['search'] = {}
        cls.config['search']['limit'] = cls._parse_search_limit()
        cls.config['search']['sorted_fields'] = cls._parse_sorted_fields()
        cls.config['search']['removed_fields'] = cls._parse_removed_fields()
        cls.config['input'] = {}
        cls.config['input']['editor'] = Config.source.is_editor()
        cls.config['operation'] = {}
        cls.config['operation']['file'] = {}
        cls.config['operation']['file']['name'], cls.config['operation']['file']['type'] = cls._parse_operation_file()

        cls.print_config()

    @classmethod
    def print_config(cls):
        """Print configuration."""

        cls.logger.debug('configured storage file: %s', cls.storage_file)
        cls.logger.debug('configured db schema file: %s', cls.db_schema_file)
        cls.logger.debug('configured server: %s', cls.server)
        cls.logger.debug('configured content operation: %s', cls.operation)
        cls.logger.debug('configured content category: %s', cls.category)
        cls.logger.debug('configured content data: %s', cls.content['data'])
        cls.logger.debug('configured content brief: %s', cls.content['brief'])
        cls.logger.debug('configured content group: %s', cls.content['group'])
        cls.logger.debug('configured content tags: %s', cls.content['tags'])
        cls.logger.debug('configured content links: %s', cls.content['links'])
        cls.logger.debug('configured digest: %s', cls.digest)
        cls.logger.debug('configured value from --editor as %s', cls.config['input']['editor'])
        cls.logger.debug('configured value from --file as "%s"', cls.config['operation']['file']['name'])
        cls.logger.debug('configured search all keywords: %s', cls.search['sall'])
        cls.logger.debug('configured search tag keywords: %s', cls.search['stag'])
        cls.logger.debug('configured search group keywords: %s', cls.search['sgrp'])
        cls.logger.debug('configured search filter regexp: %s', cls.search['regexp'])
        cls.logger.debug('configured option no_ansi: %s', cls.no_ansi)
        cls.logger.debug('configured option defaults: %s', cls.source.defaults)
        cls.logger.debug('configured option template: %s', cls.source.template)
        cls.logger.debug('configured value from limit as %d', cls.config['search']['limit'])
        cls.logger.debug('configured value from sorted fields as %s', cls.config['search']['sorted_fields'])
        cls.logger.debug('configured value from removed fields as %s', cls.config['search']['removed_fields'])
        cls.logger.debug('extracted file format from argument --file "%s"', cls.config['operation']['file']['type'])

    @classmethod
    def get_content(cls, content):
        """Return content after it has been optionally edited."""

        if cls.is_editor():
            content = Config._get_edited_content(content)
        else:
            content = Config._get_config_content(content)

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
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not identify text template content category')

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
                              content_copy.get_runalias(),
                              content_copy.get_versions(),
                              editor.get_edited_date(),
                              content_copy.get_digest(),
                              content_copy.get_metadata(),
                              content_copy.get_key()))
            content_copy.update_digest()
            if content_copy.is_data_template(edited=item):
                Cause.push(Cause.HTTP_BAD_REQUEST, 'content was stored because it matched to empty template')

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

        return True if cls.operation == 'create' else False

    @classmethod
    def is_operation_search(cls):
        """Test if operation was search."""

        return True if cls.operation == 'search' else False

    @classmethod
    def is_operation_update(cls):
        """Test if operation was update."""

        return True if cls.operation == 'update' else False

    @classmethod
    def is_operation_delete(cls):
        """Test if operation was delete."""

        return True if cls.operation == 'delete' else False

    @classmethod
    def is_operation_export(cls):
        """Test if operation was export."""

        return True if cls.operation == 'export' else False

    @classmethod
    def is_operation_import(cls):
        """Test if operation was import."""

        return True if cls.operation == 'import' else False

    @classmethod
    def is_migrate_defaults(cls):
        """Test if migrate operation was related to content defaults."""

        return cls.source.defaults

    @classmethod
    def is_migrate_template(cls):
        """Test if migrate operation was related to content template."""

        return cls.source.template

    @classmethod
    def is_category_snippet(cls):
        """Test if operation is applied to snippet category."""

        return True if cls.category == Const.SNIPPET else False

    @classmethod
    def is_category_solution(cls):
        """Test if operation is applied to solution category."""

        return True if cls.category == Const.SOLUTION else False

    @classmethod
    def is_category_all(cls):
        """Test if operation is applied to all content categories."""

        return True if cls.category == 'all' else False

    @classmethod
    def set_category(cls, category):
        """Set content category."""

        if category == Const.SOLUTION:
            cls.category = Const.SOLUTION
        else:
            cls.category = Const.SNIPPET

    @classmethod
    def get_content_data(cls):
        """Return content data."""

        return cls.content['data']

    @classmethod
    def get_content_brief(cls):
        """Return content brief description."""

        return cls.content['brief']

    @classmethod
    def get_content_group(cls):
        """Return content group."""

        return cls.content['group']

    @classmethod
    def get_content_tags(cls):
        """Return content tags."""

        return cls.content['tags']

    @classmethod
    def get_content_links(cls):
        """Return content reference links."""

        return cls.content['links']

    @classmethod
    def get_content_digest(cls):
        """Return digest identifying the content."""

        return cls.digest

    @classmethod
    def validate_search_context(cls, contents, operation):  # pylint: disable=too-many-branches
        """Validate content search context."""

        # Search keys are treated in priority order of 1) digest, 2) content data
        # and 3) search keywords. Search keywords are already validated and invalid
        # keywords are interpreted as 'list all' which is always correct at this
        # point.
        cls.logger.debug('validating search context with %d results', len(contents))
        if cls.is_content_digest():
            if cls.get_content_digest():
                if not contents:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with message digest %s' % cls.get_content_digest())
                elif len(contents) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'given digest %.16s matches (%d) more than once preventing the operation' %
                               (cls.get_content_digest(), len(contents)))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty message digest to %s content' % operation)
        elif cls.get_content_data():
            if any(cls.get_content_data()):
                data = Const.EMPTY.join(cls.get_content_data())
                data = data[:30] + (data[30:] and '...')
                if not contents:
                    Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with content data \'%s\'' % data)
                elif len(contents) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'given content data %s matches (%d) more than once preventing the operation' %
                               (data, len(contents)))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty content data to %s content' % operation)
        elif cls.is_search_keywords():
            if not contents:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')
            elif len(contents) > 1:
                Cause.push(Cause.HTTP_CONFLICT,
                           'given search keyword matches (%d) more than once preventing the operation' % len(contents))
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'no message digest, content data or search keywords were provided')

    @classmethod
    def get_filename(cls):
        """Return content filename."""

        return cls.content['filename']

    @classmethod
    def is_search_all(cls):
        """Test if all fields are searched."""

        return True if cls.search['sall'] else False

    @classmethod
    def is_search_tag(cls):
        """Test if search is made from tags."""

        return True if cls.search['stag'] else False

    @classmethod
    def is_search_grp(cls):
        """Test if search is made from groups."""

        return True if cls.search['sgrp'] else False

    @classmethod
    def is_search_keywords(cls):
        """Test if search is made with any search option."""

        return True if cls.is_search_all() or cls.is_search_tag() or cls.is_search_grp() else False

    @classmethod
    def get_search_all(cls):
        """Return list of search keywords for search all."""

        return cls.search['sall']

    @classmethod
    def get_search_tag(cls):
        """Return list of search keywords for search tags."""

        return cls.search['stag']

    @classmethod
    def get_search_grp(cls):
        """Return list of search keywords for search groups."""

        return cls.search['sgrp']

    @classmethod
    def get_search_filter(cls):
        """Return search filter."""

        return cls.search['regexp']

    @classmethod
    def get_search_limit(cls):
        """Return search limit."""

        return cls.config['search']['limit']

    @classmethod
    def get_sorted_fields(cls):
        """Return fields that are used to sort content."""

        return cls.config['search']['sorted_fields']

    @classmethod
    def get_removed_fields(cls):
        """Return fields that are removed from content."""

        return cls.config['search']['removed_fields']

    @classmethod
    def is_editor(cls):
        """Test if editor is used to input content."""

        return cls.config['input']['editor']

    @classmethod
    def is_content_digest(cls):
        """Test if content digest was defined from command line."""

        return False if cls.digest is None else True

    @classmethod
    def is_search_criteria(cls):
        """Test if any of the search criterias were used."""

        criteria = False
        if cls.is_search_keywords() or cls.is_content_digest() or cls.get_content_data():
            criteria = True

        return criteria

    @classmethod
    def get_operation_file(cls, content_filename=Const.EMPTY):
        """Return file for operation."""

        # Use the content filename only in case of export operation and
        # when the user did not define the target file from command line.
        filename = cls.config['operation']['file']['name']
        if cls.is_operation_export() and content_filename and not Config.source.filename:
            filename = content_filename

        return filename

    @classmethod
    def is_file_type_yaml(cls):
        """Test if file format is yaml."""

        return True if cls.config['operation']['file']['type'] == Const.CONTENT_TYPE_YAML else False

    @classmethod
    def is_file_type_json(cls):
        """Test if file format is json."""

        return True if cls.config['operation']['file']['type'] == Const.CONTENT_TYPE_JSON else False

    @classmethod
    def is_file_type_text(cls):
        """Test if file format is text."""

        return True if cls.config['operation']['file']['type'] == Const.CONTENT_TYPE_TEXT else False

    @classmethod
    def is_supported_file_format(cls):
        """Test if file format is supported."""

        return True if cls.is_file_type_yaml() or cls.is_file_type_json() or cls.is_file_type_text() else False

    @classmethod
    def use_ansi(cls):
        """Test if ANSI characters like colors are disabled in the command output."""

        return not cls.no_ansi

    @staticmethod
    def get_utc_time():
        """Get UTC time."""

        utc = datetime.datetime.utcnow()

        return utc.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def _parse_search_limit(cls):
        """Process the user given search limit."""

        limit = Config.source.get_search_limit()

        return limit

    @classmethod
    def _parse_sorted_fields(cls):
        """Process the fields that are used to sort content."""

        return Config.source.get_sorted_fields()

    @classmethod
    def _parse_removed_fields(cls):
        """Process the fields that are removed from content."""

        return Config.source.get_removed_fields()

    @classmethod
    def _get_edited_content(cls, content):
        """Read and set the user provided values from editor."""

        editor = Editor(content, Config.get_utc_time())
        editor.read_content()
        if editor.is_content_identified():
            cls.content['data'] = editor.get_edited_data()
            cls.content['brief'] = editor.get_edited_brief()
            cls.content['group'] = editor.get_edited_group()
            cls.content['tags'] = editor.get_edited_tags()
            cls.content['links'] = editor.get_edited_links()
            cls.content['filename'] = editor.get_edited_filename()
            content.set((cls.get_content_data(),
                         cls.get_content_brief(),
                         cls.get_content_group(),
                         cls.get_content_tags(),
                         cls.get_content_links(),
                         content.get_category(),
                         cls.get_filename(),
                         content.get_runalias(),
                         content.get_versions(),
                         content.get_utc(),
                         content.get_digest(),
                         content.get_metadata(),
                         content.get_key()))
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'could not identify edited content category - please keep tags in place')

        return content

    @classmethod
    def _get_config_content(cls, content):
        """Read and set the user provided values from configuration."""

        content.set((cls.get_content_data(),
                     cls.get_content_brief(),
                     cls.get_content_group(),
                     cls.get_content_tags(),
                     cls.get_content_links(),
                     content.get_category(),
                     cls.get_filename(),
                     content.get_runalias(),
                     content.get_versions(),
                     content.get_utc(),
                     content.get_digest(),
                     content.get_metadata(),
                     content.get_key()))

        return content

    @classmethod
    def _parse_operation_file(cls):
        """Return the filename and the format of the file."""

        filename = Config.source.filename
        filetype = Const.CONTENT_TYPE_NONE

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
        if cls.is_operation_export() and cls.is_search_criteria():
            if Config.is_category_snippet() and not filename:
                filename = 'snippet.' + Const.CONTENT_TYPE_TEXT
            elif Config.is_category_solution() and not filename:
                filename = 'solution.' + Const.CONTENT_TYPE_TEXT

        # In case user did not provide filename, set defaults. For example
        # if user defined export or import operation without the file, the
        # default files are used.
        if not filename:
            filename = os.path.join('./', defaults)

        # User defined content to/from user specified file.
        name, extension = os.path.splitext(filename)
        if name and ('yaml' in extension or 'yml' in extension):
            filetype = Const.CONTENT_TYPE_YAML
        elif name and 'json' in extension:
            filetype = Const.CONTENT_TYPE_JSON
        elif name and ('txt' in extension or 'text' in extension):
            filetype = Const.CONTENT_TYPE_TEXT
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot identify file format for file {}'.format(filename))

        return (filename, filetype)
