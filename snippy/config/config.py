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
from snippy.cause.cause import Cause
from snippy.config.source.editor import Editor
from snippy.logger.logger import Logger


class Config(object):  # pylint: disable=too-many-public-methods
    """Global configuration management."""

    logger = None
    storage_file = None
    storage_schema = None
    search_all_kws = ()

    def __init__(self):
        if not Config.logger:
            Config.logger = Logger(__name__).get()
        Config.source = None
        Config.server = Config._server()
        Config.debug = Config._debug()
        Config.profiler = Config._profiler()
        Config.quiet = Config._quiet()
        Config.json_logs = Config._json_logs()
        Config.storage_file = Config._storage_file()
        Config.storage_schema = Config._storage_schema()
        Config.snippet_template = Config._content_template('snippet-template.txt')
        Config.solution_template = Config._content_template('solution-template.txt')

    @classmethod
    def _server(cls):
        """Test if service is run as a server."""

        return True if '--server' in sys.argv else False

    @classmethod
    def _debug(cls):
        """Test if service is run in debug mode."""

        return True if '--debug' in sys.argv or '-vv' in sys.argv else False

    @classmethod
    def _profiler(cls):
        """Test if profiler is run."""

        return True if '--profile' in sys.argv else False

    @classmethod
    def _quiet(cls):
        """Test if all output is suppressed."""

        return True if '--quiet' in sys.argv else False

    @classmethod
    def _json_logs(cls):
        """Test if logs are formatted as JSON."""

        return True if '--json-logs' in sys.argv else False

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
    def _content_template(cls, template):
        """Get defined content template installed with the tool."""

        template = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), template)
        if not os.path.isfile(template):
            cls.logger.error('NOK: content template installed with tool does not exist or is not accessible: %s', template)
            sys.exit(1)

        return template

    @classmethod
    def read_source(cls, source):
        """Read configuration source."""

        cls.source = source
        cls.logger.debug('config source: %s', cls.source)

        # Operation
        cls.operation = cls.source.operation
        cls.operation_digest = cls.source.digest

        # Content
        cls.content_category = cls.source.category
        cls.content_data = cls.source.data
        cls.content_brief = cls.source.brief
        cls.content_group = cls.source.group
        cls.content_tags = cls.source.tags
        cls.content_links = cls.source.links
        cls.content_filename = cls.source.filename

        # Search
        cls.search_all_kws = cls.source.sall
        cls.search_tag_kws = cls.source.stag
        cls.search_grp_kws = cls.source.sgrp
        cls.search_filter = cls.source.regexp
        cls.search_limit = cls.source.limit
        cls.remove_fields = cls.source.rfields
        cls.sorted_fields = cls.source.sfields

        # Migrate
        cls.defaults = cls.source.defaults
        cls.template = cls.source.template

        # Options
        cls.editor = cls.source.editor
        cls.use_ansi = not cls.source.no_ansi

        # Parsed from defined configuration.
        cls.is_operation_create = True if cls.operation == 'create' else False
        cls.is_operation_search = True if cls.operation == 'search' else False
        cls.is_operation_update = True if cls.operation == 'update' else False
        cls.is_operation_delete = True if cls.operation == 'delete' else False
        cls.is_operation_export = True if cls.operation == 'export' else False
        cls.is_operation_import = True if cls.operation == 'import' else False
        cls.is_category_snippet = True if cls.content_category == Const.SNIPPET else False
        cls.is_category_solution = True if cls.content_category == Const.SOLUTION else False
        cls.is_category_all = True if cls.content_category == Const.ALL else False
        cls.operation_filename = cls._operation_filename()
        cls.operation_filetype = cls._operation_filetype()
        cls.is_operation_file_json = True if cls.operation_filetype == Const.CONTENT_TYPE_JSON else False
        cls.is_operation_file_text = True if cls.operation_filetype == Const.CONTENT_TYPE_TEXT else False
        cls.is_operation_file_yaml = True if cls.operation_filetype == Const.CONTENT_TYPE_YAML else False
        cls._print_config()

    @classmethod
    def _print_config(cls):
        """Print global configuration."""

        cls.logger.debug('configured storage file: %s', cls.storage_file)
        cls.logger.debug('configured storage schema: %s', cls.storage_schema)
        cls.logger.debug('configured content operation: %s', cls.operation)
        cls.logger.debug('configured content category: %s', cls.content_category)
        cls.logger.debug('configured content data: %s', cls.content_data)
        cls.logger.debug('configured content brief: %s', cls.content_brief)
        cls.logger.debug('configured content group: %s', cls.content_group)
        cls.logger.debug('configured content tags: %s', cls.content_tags)
        cls.logger.debug('configured content links: %s', cls.content_links)
        cls.logger.debug('configured content filename: %s', cls.content_filename)
        cls.logger.debug('configured operation digest: %s', cls.operation_digest)
        cls.logger.debug('configured operation filename: "%s"', cls.operation_filename)
        cls.logger.debug('configured operation file type: "%s"', cls.operation_filetype)
        cls.logger.debug('configured search all keywords: %s', cls.search_all_kws)
        cls.logger.debug('configured search tag keywords: %s', cls.search_tag_kws)
        cls.logger.debug('configured search group keywords: %s', cls.search_grp_kws)
        cls.logger.debug('configured search result filter: %s', cls.search_filter)
        cls.logger.debug('configured search result limit: %s', cls.search_limit)
        cls.logger.debug('configured search result sorted field: %s', cls.sorted_fields)
        cls.logger.debug('configured search result removed fields: %s', cls.remove_fields)
        cls.logger.debug('configured option editor: %s', cls.editor)
        cls.logger.debug('configured option use_ansi: %s', cls.use_ansi)
        cls.logger.debug('configured option defaults: %s', cls.defaults)
        cls.logger.debug('configured option template: %s', cls.template)
        cls.logger.debug('configured option server: %s', cls.server)

    @classmethod
    def _operation_filename(cls):
        """Operation filename is set based user input for content filename,
        operation and content. For some operations like import and export
        with defaults option cause the filename to be updated automatically
        to point into correct location that stores e.g. the default content."""

        filename = Config.source.filename

        defaults = 'snippets.yaml'
        template = 'snippet-template.txt'
        if Config.is_category_solution:
            defaults = 'solutions.yaml'
            template = 'solution-template.txt'

        # Run migrate operation with default content.
        if cls.defaults:
            filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/default'), defaults)

        # Run migrate operation with content template.
        if cls.template:
            filename = os.path.join('./', template)

        # Run export operation with specified content without specifying
        # the operation file.
        if cls.is_operation_export and cls.is_search_criteria():
            if Config.is_category_snippet and not filename:
                filename = 'snippet.' + Const.CONTENT_TYPE_TEXT
            elif Config.is_category_solution and not filename:
                filename = 'solution.' + Const.CONTENT_TYPE_TEXT

        # In case user did not provide filename, set defaults. For example
        # if user defined export or import operation without the file, the
        # default files are used.
        if not filename:
            filename = os.path.join('./', defaults)

        return filename

    @classmethod
    def _operation_filetype(cls):
        """Operation file type is extracted from operation fiel and it makes
        sure that only supported content types can be operated."""

        filetype = Const.CONTENT_TYPE_NONE

        # User defined content to/from user specified file.
        name, extension = os.path.splitext(cls.operation_filename)
        if name and ('yaml' in extension or 'yml' in extension):
            filetype = Const.CONTENT_TYPE_YAML
        elif name and 'json' in extension:
            filetype = Const.CONTENT_TYPE_JSON
        elif name and ('txt' in extension or 'text' in extension):
            filetype = Const.CONTENT_TYPE_TEXT
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot identify file format for file {}'.format(cls.operation_filename))

        return filetype

    @classmethod
    def get_content(cls, content, source=Const.EMPTY):
        """Get content from configuration, editor or from a given
        string that contains newlines."""

        # contents = []
        # if any(source):
        #     contents = Parser.read_content(content, source)
        # elif cls.editor:
        if cls.editor:
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
            if content_copy.is_template(edited=item):
                Cause.push(Cause.HTTP_BAD_REQUEST, 'no content was stored because it matched to empty template')

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
    def validate_search_context(cls, contents, operation):  # pylint: disable=too-many-branches
        """Validate content search context."""

        # Search keys are treated in priority order of 1) digest, 2) content data
        # and 3) search keywords. Search keywords are already validated and invalid
        # keywords are interpreted as 'list all' which is always correct at this
        # point.
        cls.logger.debug('validating search context with %d results', len(contents))
        if cls.is_content_digest():
            if cls.operation_digest:
                if not contents:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with message digest %s' % cls.operation_digest)
                elif len(contents) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'given digest %.16s matches (%d) more than once preventing the operation' %
                               (cls.operation_digest, len(contents)))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty message digest to %s content' % operation)
        elif cls.content_data:
            if any(cls.content_data):
                data = Const.EMPTY.join(cls.content_data)
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
    def is_search_keywords(cls):
        """Test if search is made with any search option."""

        return True if cls.search_all_kws or cls.search_tag_kws or cls.search_grp_kws else False

    @classmethod
    def is_content_digest(cls):
        """Test if content digest was defined from command line."""

        return False if cls.operation_digest is None else True

    @classmethod
    def is_search_criteria(cls):
        """Test if any of the search criterias were used."""

        criteria = False
        if cls.is_search_keywords() or cls.is_content_digest() or cls.content_data:
            criteria = True

        return criteria

    @classmethod
    def get_operation_file(cls, content_filename=Const.EMPTY):
        """Return file for operation."""

        # Use the content filename only in case of export operation and
        # when the user did not define the target file from command line.
        filename = cls.operation_filename
        if cls.is_operation_export and content_filename and not Config.source.filename:
            filename = content_filename

        return filename

    @classmethod
    def is_supported_file_format(cls):
        """Test if file format is supported."""

        return True if cls.is_operation_file_yaml or cls.is_operation_file_json or cls.is_operation_file_text else False

    @staticmethod
    def get_utc_time():
        """Get UTC time."""

        utc = datetime.datetime.utcnow()

        return utc.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def _get_edited_content(cls, content):
        """Read and set the user provided values from editor."""

        editor = Editor(content, Config.get_utc_time())
        editor.read_content()
        if editor.is_content_identified():
            cls.content_data = editor.get_edited_data()
            cls.content_brief = editor.get_edited_brief()
            cls.content_group = editor.get_edited_group()
            cls.content_tags = editor.get_edited_tags()
            cls.content_links = editor.get_edited_links()
            cls.content_filename = editor.get_edited_filename()
            content.set((cls.content_data,
                         cls.content_brief,
                         cls.content_group,
                         cls.content_tags,
                         cls.content_links,
                         content.get_category(),
                         cls.content_filename,
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

        content.set((cls.content_data,
                     cls.content_brief,
                     cls.content_group,
                     cls.content_tags,
                     cls.content_links,
                     content.get_category(),
                     cls.content_filename,
                     content.get_runalias(),
                     content.get_versions(),
                     content.get_utc(),
                     content.get_digest(),
                     content.get_metadata(),
                     content.get_key()))

        return content
