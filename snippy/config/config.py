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

"""config.py: Global configuration."""

import datetime
import os.path
import sys

import pkg_resources

from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.cli import Cli
from snippy.config.source.editor import Editor
from snippy.config.source.parser import Parser
from snippy.logger import Logger


class Config(object):
    """Global configuration object."""

    _logger = Logger(__name__).logger

    @classmethod
    def init(cls, args):
        """Initialize global configuration."""

        cls.init_args = args

        # Set logging and profiling configuration.
        cls.debug_logs = True if cls.init_args and '--debug' in cls.init_args else False
        cls.very_verbose = True if cls.init_args and '-vv' in cls.init_args else False
        cls.quiet = True if cls.init_args and '-q' in cls.init_args else False
        cls.json_logs = True if cls.init_args and '--json-logs' in cls.init_args else False
        cls.profiler = True if cls.init_args and '--profile' in cls.init_args else False
        Logger.configure({'debug': cls.debug_logs,
                          'very_verbose': cls.very_verbose,
                          'quiet': cls.quiet,
                          'json_logs': cls.json_logs})
        cls._logger.debug('config initial command line arguments: %s', cls.init_args)

        # Set static configuration.
        cls.storage_schema = cls._storage_schema()
        cls.snippet_template = cls._content_template('snippet-template.txt')
        cls.solution_template = cls._content_template('solution-template.txt')

        # Set dynamic configuration.
        cls.load(Cli(args))

    @classmethod
    def load(cls, source):
        """Load dynamic configuration from source."""

        cls.source = source
        cls._logger.debug('config source: %s', cls.source)

        # operation
        cls.operation = cls.source.operation
        cls.operation_digest = cls.source.digest

        # content
        cls.content_category = cls.source.category
        cls.content_data = cls.source.data
        cls.content_brief = cls.source.brief
        cls.content_group = cls.source.group
        cls.content_tags = cls.source.tags
        cls.content_links = cls.source.links
        cls.content_filename = cls.source.filename

        # search
        cls.search_all_kws = cls.source.sall
        cls.search_tag_kws = cls.source.stag
        cls.search_grp_kws = cls.source.sgrp
        cls.search_filter = cls.source.regexp
        cls.search_limit = cls.source.limit
        cls.remove_fields = cls.source.rfields
        cls.sorted_fields = cls.source.sfields

        # migrate
        cls.defaults = cls.source.defaults
        cls.template = cls.source.template

        # options
        cls.editor = cls.source.editor
        cls.use_ansi = not cls.source.no_ansi
        cls.cli = not cls.source.exit

        # server
        cls.base_path = cls.source.base_path
        cls.server = cls.source.server
        cls.server_ip = cls.source.server_ip
        cls.server_port = cls.source.server_port

        # storage
        cls.storage_path = cls.source.storage_path

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
        cls.storage_file = cls._storage_file()

        cls.debug()

    @classmethod
    def get_contents(cls, content, source=None):
        """Get list of contents configured from one of the config sources."""

        if source is not None:
            contents = Parser.read_content(content, source, cls.get_utc_time())
        elif cls.editor:
            contents = Editor.read_content(content)
        else:
            contents = cls._read_content(content)

        return tuple(contents)

    @classmethod
    def _read_content(cls, content):
        """Read content from configuration."""

        contents = []
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
        contents.append(content)

        return contents

    @classmethod
    def _storage_schema(cls):
        """Test that database schema file exist."""

        # The database schema is installed with the tool and it must always exist.
        schema_file = os.path.join(pkg_resources.resource_filename('snippy', 'data/config'), 'database.sql')
        if not os.path.isfile(schema_file):
            cls._logger.error('NOK: database schema file path does not exist or is not accessible: %s', schema_file)
            sys.exit(1)

        return schema_file

    @classmethod
    def _content_template(cls, template):
        """Get defined content template installed with the tool."""

        template = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), template)
        if not os.path.isfile(template):
            cls._logger.error('NOK: content template installed with tool does not exist or is not accessible: %s', template)
            sys.exit(1)

        return template

    @classmethod
    def _storage_file(cls):
        """Test that storage path exist."""

        if Config.storage_path:
            storage_path = Config.storage_path
        else:
            storage_path = pkg_resources.resource_filename('snippy', 'data/storage')

        if os.path.exists(storage_path) and os.access(storage_path, os.W_OK):
            storage_file = os.path.join(storage_path, 'snippy.db')
        else:
            cls._logger.error('NOK: storage path does not exist or is not accessible: %s', storage_path)
            sys.exit(1)

        return storage_file

    @classmethod
    def _operation_filename(cls):
        """Operation filename is set based user input for content filename,
        operation and content. For some operations like import and export
        with defaults option cause the filename to be updated automatically
        to point into correct location that stores e.g. the default content."""

        filename = cls.source.filename

        defaults = 'snippets.yaml'
        template = 'snippet-template.txt'
        if cls.is_category_solution:
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
            if cls.is_category_snippet and not filename:
                filename = 'snippet.' + Const.CONTENT_TYPE_TEXT
            elif cls.is_category_solution and not filename:
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
    def validate_search_context(cls, contents, operation):  # pylint: disable=too-many-branches
        """Validate content search context."""

        # Search keys are treated in priority order of 1) digest, 2) content data
        # and 3) search keywords. Search keywords are already validated and invalid
        # keywords are interpreted as 'list all' which is always correct at this
        # point.
        cls._logger.debug('validating search context with %d results', len(contents))
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
        elif cls._is_search_keywords():
            if not contents:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')
            elif len(contents) > 1:
                Cause.push(Cause.HTTP_CONFLICT,
                           'given search keyword matches (%d) more than once preventing the operation' % len(contents))
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'no message digest, content data or search keywords were provided')

    @classmethod
    def _is_search_keywords(cls):
        """Test if search is made with any of the search option."""

        return True if cls.search_all_kws or cls.search_tag_kws or cls.search_grp_kws else False

    @classmethod
    def is_content_digest(cls):
        """Test if content digest was defined from command line."""

        return False if cls.operation_digest is None else True

    @classmethod
    def is_search_criteria(cls):
        """Test if any of the search criterias were used."""

        criteria = False
        if cls._is_search_keywords() or cls.is_content_digest() or cls.content_data:
            criteria = True

        return criteria

    @classmethod
    def get_operation_file(cls, content_filename=Const.EMPTY):
        """Return file for operation."""

        # Use the content filename only in case of export operation
        # and when user did not define target file from command line.
        filename = cls.operation_filename
        if cls.is_operation_export and content_filename and not cls.source.filename:
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
    def debug(cls):
        """Debug Config."""

        cls._logger.debug('configured storage file: %s', cls.storage_file)
        cls._logger.debug('configured storage schema: %s', cls.storage_schema)
        cls._logger.debug('configured content operation: %s', cls.operation)
        cls._logger.debug('configured content category: %s', cls.content_category)
        cls._logger.debug('configured content data: %s', cls.content_data)
        cls._logger.debug('configured content brief: %s', cls.content_brief)
        cls._logger.debug('configured content group: %s', cls.content_group)
        cls._logger.debug('configured content tags: %s', cls.content_tags)
        cls._logger.debug('configured content links: %s', cls.content_links)
        cls._logger.debug('configured content filename: %s', cls.content_filename)
        cls._logger.debug('configured operation digest: %s', cls.operation_digest)
        cls._logger.debug('configured operation filename: "%s"', cls.operation_filename)
        cls._logger.debug('configured operation file type: "%s"', cls.operation_filetype)
        cls._logger.debug('configured search all keywords: %s', cls.search_all_kws)
        cls._logger.debug('configured search tag keywords: %s', cls.search_tag_kws)
        cls._logger.debug('configured search group keywords: %s', cls.search_grp_kws)
        cls._logger.debug('configured search result filter: %s', cls.search_filter)
        cls._logger.debug('configured search result limit: %s', cls.search_limit)
        cls._logger.debug('configured search result sorted field: %s', cls.sorted_fields)
        cls._logger.debug('configured search result removed fields: %s', cls.remove_fields)
        cls._logger.debug('configured option editor: %s', cls.editor)
        cls._logger.debug('configured option use_ansi: %s', cls.use_ansi)
        cls._logger.debug('configured option defaults: %s', cls.defaults)
        cls._logger.debug('configured option template: %s', cls.template)
        cls._logger.debug('configured option server: %s', cls.server)
        cls._logger.debug('configured option server api base path: %s', cls.base_path)
        cls._logger.debug('configured option server ip %s and port %s', cls.server_ip, cls.server_port)
