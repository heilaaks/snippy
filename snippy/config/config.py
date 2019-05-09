#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""config: Global configuration."""

import datetime
import io
import json
import os.path
import sys

import pkg_resources

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.config.source.cli import Cli
from snippy.config.source.editor import Editor
from snippy.content.collection import Collection
from snippy.devel.profiler import Profiler
from snippy.logger import Logger


class Config(object):
    """Global configuration object."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def __str__(cls):
        """Print class attributes in a controlled manner.

        This is intended to limit printing of sensitive configuration values
        by accident. This method should return only configuration values that
        can be printed without revealing configuration that is considered
        sensitive like:

        - User names and passwords.

        - SSL certificate paths and certificate names.

        - IP addresses, host names and service ports.

        - Full file paths. File paths are truncated to prevent revealing
          installation location in the server.

        - Database table names.

        - Internal database keys like the UUID primary key.

        - Direct printing of command line arguments.

        No sensitive information listed here must be printed. The data is not
        printed with any log level. The thought is that if sensitive data would
        be printed on any level, there would be accidental leak of information
        at some point. The server would be first run with highest debug setting
        and then left running with those.
        """

        namespace = []
        if not hasattr(cls, 'source'):
            return str('%s(%s)' % ('Config', ', '.join(namespace)))

        namespace.append('operation={}'.format(cls.operation))
        namespace.append('operation_uuid={}'.format(cls.operation_uuid))
        namespace.append('operation_digest={}'.format(cls.operation_digest))
        namespace.append('operation_identity={}'.format(cls.operation_identity))
        namespace.append('operation_filename={}'.format(cls.operation_filename))
        namespace.append('operation_file_format={}'.format(cls.operation_file_format))
        namespace.append('content_category={}'.format(cls.content_category))
        namespace.append('content_data={}'.format(cls.content_data))
        namespace.append('content_brief={}'.format(cls.content_brief.encode('utf-8')))
        namespace.append('content_description={}'.format(cls.content_description.encode('utf-8')))
        namespace.append('content_groups={}'.format(cls.content_groups))
        namespace.append('content_tags={}'.format(cls.content_tags))
        namespace.append('content_links={}'.format(cls.content_links))
        namespace.append('content_name={}'.format(cls.content_name.encode('utf-8')))
        namespace.append('content_filename={}'.format(cls.content_filename))
        namespace.append('content_versions={}'.format(cls.content_versions))
        namespace.append('content_source={}'.format(cls.content_source))
        namespace.append('run_healthcheck={}'.format(cls.run_healthcheck))
        namespace.append('search_all_kws={}'.format(cls.search_all_kws))
        namespace.append('search_cat_kws={}'.format(cls.search_cat_kws))
        namespace.append('search_tag_kws={}'.format(cls.search_tag_kws))
        namespace.append('search_grp_kws={}'.format(cls.search_grp_kws))
        namespace.append('search_filter={}'.format(cls.search_filter))
        namespace.append('search_limit={}'.format(cls.search_limit))
        namespace.append('search_offset={}'.format(cls.search_offset))
        namespace.append('sort_fields={}'.format(cls.sort_fields))
        namespace.append('storage_type={}'.format(cls.storage_type))
        namespace.append('storage_file=...{}'.format(os.sep.join(os.path.normpath(cls.storage_file).split(os.sep)[5:])))
        namespace.append('storage_schema=..{}'.format(os.sep.join(os.path.normpath(cls.storage_schema).split(os.sep)[5:])))
        namespace.append('server_host={}'.format(cls.server_host))
        namespace.append('server_base_path_rest={}'.format(cls.server_base_path_rest))
        namespace.append('server_minify_json={}'.format(cls.server_minify_json))
        namespace.append('server_readonly={}'.format(cls.server_readonly))
        namespace.append('editor={}'.format(cls.editor))
        namespace.append('use_ansi={}'.format(cls.use_ansi))

        return str('%s(%s)' % ('Config', ', '.join(namespace)))

    @classmethod
    def init(cls, args):
        """Initialize global configuration."""

        if args is None:
            args = []

        # Set logger and development configuration.
        cls._init_logs(args)

        cls.source = Cli(args)

        # Static storage and template configurations.
        cls.storage_type = cls.source.storage_type
        cls.storage_schema = cls._test_resource('data/storage', 'database.sql')
        cls.storage_path = cls.source.storage_path
        cls.storage_file = cls._storage_file()
        cls.storage_host = cls.source.storage_host
        cls.storage_user = cls.source.storage_user
        cls.storage_password = cls.source.storage_password
        cls.storage_database = cls.source.storage_database
        cls.storage_ssl_cert = cls.source.storage_ssl_cert
        cls.storage_ssl_key = cls.source.storage_ssl_key
        cls.storage_ssl_ca_cert = cls.source.storage_ssl_ca_cert
        cls.templates = {
            'text': {
                'snippet': cls._read_resource('data/templates', 'snippet.txt'),
                'solution': cls._read_resource('data/templates', 'solution.txt'),
                'reference': cls._read_resource('data/templates', 'reference.txt')
            },
            'mkdn': {
                'snippet': cls._read_resource('data/templates', 'snippet.md'),
                'solution': cls._read_resource('data/templates', 'solution.md'),
                'reference': cls._read_resource('data/templates', 'reference.md')
            }
        }
        cls.completion = {
            'bash': cls._read_resource('data/completion', 'snippy.bash-completion')
        }

        # Static server configurations.
        cls.server_readonly = cls.source.server_readonly
        cls.server_base_path_rest = cls.source.server_base_path_rest
        cls.server_minify_json = cls.source.server_minify_json
        cls.server_host = cls.source.server_host
        cls.server_ssl_cert = cls._ssl_file(cls.source.server_ssl_cert)
        cls.server_ssl_key = cls._ssl_file(cls.source.server_ssl_key)
        cls.server_ssl_ca_cert = cls._ssl_file(cls.source.server_ssl_ca_cert)

        # Server and healthchecks are started only once.
        cls.run_server = cls.source.run_server
        cls.run_healthcheck = cls.source.run_healthcheck

        # Dynamic configuration.
        cls.load(cls.source)

    @classmethod
    def load(cls, source):  # pylint: disable=too-many-statements
        """Load dynamic configuration from source."""

        cls.source = source

        # logger: Only quiet flag is updated. If all logging configuration
        # would be updated, the server would print logs only from the first
        # operation. The reason to update quiet flag is to be able to prevent
        # test cases to print unnecessary help dialog when test creates the
        # Snippy() object. This allows the first creation to be silent but
        # allows further configuration from tests with snippy.run().
        cls.quiet = bool(cls.source.quiet)
        cls._update_logger()
        cls._logger.debug('config source: %s', cls.source)

        # operation
        cls.operation = cls.source.operation
        cls.operation_digest = cls.source.digest
        cls.operation_uuid = cls.source.uuid
        cls.operation_identity = cls.source.identity
        cls.merge = cls.source.merge

        # content
        cls.content_category = cls.source.category
        cls.content_data = cls.source.data
        cls.content_brief = cls.source.brief
        cls.content_description = cls.source.description
        cls.content_name = cls.source.name
        cls.content_groups = cls.source.groups
        cls.content_tags = cls.source.tags
        cls.content_links = cls.source.links
        cls.content_source = cls.source.source
        cls.content_versions = cls.source.versions
        cls.content_filename = cls.source.filename

        # search
        cls.search_cat_kws = cls.source.scat
        cls.search_all_kws = cls.source.sall
        cls.search_tag_kws = cls.source.stag
        cls.search_grp_kws = cls.source.sgrp
        cls.search_filter = cls.source.search_filter
        cls.search_limit = cls.source.search_limit
        cls.search_offset = cls.source.search_offset
        cls.remove_fields = cls.source.remove_fields
        cls.reset_fields = cls.source.reset_fields
        cls.sort_fields = cls.source.sort_fields

        # migrate
        cls.defaults = cls.source.defaults
        cls.template = cls.source.template
        cls.complete = cls.source.complete

        # options
        cls.editor = cls.source.editor
        cls.template_format = cls.source.template_format
        cls.use_ansi = not cls.source.no_ansi
        cls.failure = cls.source.failure
        cls.failure_message = cls.source.failure_message

        # Parsed from defined configuration.
        cls.is_operation_create = bool(cls.operation == 'create')
        cls.is_operation_search = bool(cls.operation == 'search')
        cls.is_operation_update = bool(cls.operation == 'update')
        cls.is_operation_delete = bool(cls.operation == 'delete')
        cls.is_operation_export = bool(cls.operation == 'export')
        cls.is_operation_import = bool(cls.operation == 'import')
        cls.is_category_snippet = bool(cls.content_category == Const.SNIPPET)
        cls.is_category_solution = bool(cls.content_category == Const.SOLUTION)
        cls.is_category_reference = bool(cls.content_category == Const.REFERENCE)
        cls.is_multi_category = bool(len(cls.search_cat_kws) > 1)
        cls.operation_filename = cls._operation_filename((cls.content_category,))
        cls.operation_file_format = cls._operation_file_format(cls.operation_filename)
        cls.is_operation_file_json = bool(cls.operation_file_format == Const.CONTENT_FORMAT_JSON)
        cls.is_operation_file_mkdn = bool(cls.operation_file_format == Const.CONTENT_FORMAT_MKDN)
        cls.is_operation_file_text = bool(cls.operation_file_format == Const.CONTENT_FORMAT_TEXT)
        cls.is_operation_file_yaml = bool(cls.operation_file_format == Const.CONTENT_FORMAT_YAML)

        cls.debug()

    @classmethod
    def reset(cls):
        """Reset configuration."""

        if cls.source.failure:
            cls._logger.debug('configuration failure: {}'.format(cls.source.failure_message))

        Profiler.disable()

    @classmethod
    def get_collection(cls, update=None):
        """Get collection of resources.

        Read collection of resources from the used configuration source. If a
        resource update is provided on top of configured content, the update
        is merged or migrated on top of the configuration.

        Args:
            update (obj): Content updates on top of configured content in Resource().

        Returns:
            obj: Configured content in a Collection() object.
        """

        collection = Collection()
        timestamp = Config.utcnow()
        update = cls._get_config(timestamp, collection, update, merge=Config.merge)
        if cls.editor:
            template = update.get_template(
                cls.content_category,
                cls.template_format,
                cls.templates
            )
            Editor.read(timestamp, cls.template_format, template, collection)
        else:
            collection.migrate(update)

        return collection

    @classmethod
    def get_resource(cls, update):
        """Get resource.

        Read a resource from the used configuration source. If an update is
        provided on top of configured content, the update is merged or
        migrated on top of configuration.

        Args:
            update (obj): Resource() to be used on top of the configuration.

        Returns:
            obj: Updated Resource().
        """

        collection = cls.get_collection(update)
        if len(collection) == 1:
            resource = next(collection.resources())
        else:
            cls._logger.debug('updating resource from configuration source failed: %d', len(collection))
            resource = None

        return resource

    @classmethod
    def _get_config(cls, timestamp, collection, updates, merge):
        """Read configured content fields.

        Read content fields read from one of the configuration sources. The
        configuration is migrated or merged to updates if they exist.

        Args:
            timestamp (str): IS8601 timestamp to be used with created collection.
            collection (obj): Collection() to store configured content.
            updates (obj): Resource() from existing content.
            merge (bool): Defines if content is merged or not.

        Returns:
            obj: Configured content with updates in Resource().
        """

        config = collection.get_resource(cls.content_category, timestamp)
        config.data = cls.content_data
        config.brief = cls.content_brief
        config.description = cls.content_description
        config.name = cls.content_name
        config.groups = cls.content_groups
        config.tags = cls.content_tags
        config.links = cls.content_links
        config.source = cls.content_source
        config.versions = cls.content_versions
        config.filename = cls.content_filename

        if updates:
            if merge:
                for field in Config.reset_fields:
                    setattr(updates, field, None)
                updates.merge(config, validate=False)
            else:
                updates.migrate(config, validate=False)
        else:
            updates = config
        updates.seal(validate=False)

        return updates

    @classmethod
    def _init_logs(cls, args):
        """Init logger and development configuration.

        Parse log configuration manually from sys.argv in order to initialize
        logger as early as possible. The same parameters are read eventually
        by the Cli class parser.

        Args:
            args (list): Command line arguments from sys.argv.
        """

        cls.debug_logs = Cli.read_arg('--debug', False, args)
        cls.log_json = Cli.read_arg('--log-json', False, args)
        cls.log_msg_max = Cli.read_arg('--log-msg-max', Logger.DEFAULT_LOG_MSG_MAX, args)
        cls.profiler = Cli.read_arg('--profile', False, args)
        cls.quiet = Cli.read_arg('-q', False, args)
        cls.very_verbose = Cli.read_arg('-vv', False, args)

        # Profile code.
        Profiler.enable(cls.profiler)

        cls._update_logger()

    @classmethod
    def _update_logger(cls):
        """Update logger configuration."""

        Logger.configure({
            'debug': cls.debug_logs,
            'log_json': cls.log_json,
            'log_msg_max': cls.log_msg_max,
            'quiet': cls.quiet,
            'very_verbose': cls.very_verbose
        })

        cls._logger.debug(
            'config log settings debug: {} :very verbose: {} :quiet: {} :json logs: {} :log msg max: {}'.format(
                cls.debug_logs,
                cls.very_verbose,
                cls.quiet,
                cls.log_json,
                cls.log_msg_max
            )
        )

    @classmethod
    def _read_resource(cls, path, filename):
        """Read Snippy resource file.

        Args:
            path (str): Relative path under the snippy project.
            filename (str): Resource filename.

        Returns:
            str: File read into a string.
        """

        resource_file = ''
        filename = cls._test_resource(path, filename)
        with io.open(filename, encoding='utf-8') as infile:
            resource_file = infile.read()

        return resource_file

    @staticmethod
    def _test_resource(path, filename):
        """Test if Snippy resource exists.

        Args:
            path (str): Relative path under the snippy project.
            filename (str): Resource filename.

        Returns:
            str: File if the resource exists.
        """

        filename = os.path.join(pkg_resources.resource_filename('snippy', path), filename)
        if not os.path.isfile(filename):
            Logger.print_status('NOK: cannot run because snippy resource file is not accessible: {}'.format(filename))
            sys.exit(1)

        return filename

    @classmethod
    def server_schema(cls):
        """Get REST API JSON validation schema.

        Returns:
            str: Server API schema to validate incoming HTTP requests.
        """

        request_resource = json.loads(cls._read_resource('data/server/openapi/schema', 'requestresource.json'))
        request_collection = json.loads(cls._read_resource('data/server/openapi/schema', 'requestcollection.json'))
        schema = Const.EMPTY
        schema = {
            'oneOf': [request_resource, request_collection]
        }

        return schema

    @classmethod
    def server_schema_base_uri(cls):
        """Get server API schema base URI.

        Returns:
            str: Path where the API schema is stored in URI format.
        """

        filepath = pkg_resources.resource_filename('snippy', 'data/server/openapi/schema/')
        if not os.path.isdir(filepath):
            Logger.print_status('NOK: cannot run because server api schema base uri is not accessible: {}'.format(filepath))
            sys.exit(1)

        return 'file:' + filepath

    @classmethod
    def _storage_file(cls):
        """Construct store file with absolute path.

        The in-memory database is supported only in Python 3. The Sqlite, which
        is used as a in-memory database, supports this feature only in Python 3.

        Returns:
            str: Path or URI to the storage.
        """

        if cls.source.run_healthcheck:
            return Const.EMPTY

        if Config.storage_type == Const.DB_IN_MEMORY and not Const.PYTHON2:
            return 'file::memory:?cache=shared'

        if Config.storage_path:
            storage_path = Config.storage_path
        else:
            storage_path = pkg_resources.resource_filename('snippy', 'data/storage')

        if os.path.exists(storage_path) and os.access(storage_path, os.W_OK):
            storage_file = os.path.join(storage_path, 'snippy.db')
        elif cls.source.server_readonly and os.path.exists(storage_path) and os.access(storage_path, os.R_OK):
            cls._logger.debug('running server in readonly mode')
            storage_file = os.path.join(storage_path, 'snippy.db')
        else:
            # This is a special case which prevents additional error log after
            # tool is already about to exit with help text from the CLI parser.
            if not cls.source.failure:
                Logger.print_status('NOK: cannot run because content storage path is not writable: {}'.format(storage_path))
            sys.exit(1)

        return storage_file

    @classmethod
    def _ssl_file(cls, filename):
        """Test that given SSL/TLS certificate or key file exist."""

        if filename is not None and not os.path.isfile(filename):
            Logger.print_status('NOK: cannot run secured server because ssl/tls certificate file cannot be read: {}'.format(filename))
            sys.exit(1)

        return filename

    @classmethod
    def get_operation_file(cls, collection=None):
        """Return filename for the operation.

        Use the resource ``filename`` attribute only in case of an export
        operation when there is a single resource in collection and when
        user did not define ``--file`` option.

        If collection is provided with more than one resource, the operation
        file is still updated. The collection might be a search result from
        different category than originally defined.

        Args:
            collection (obj): Resources in Collection() container.

        Returns:
            str: Operation filename.
        """

        filename = cls.operation_filename
        if cls.is_operation_export and collection and not cls.source.operation_file:
            if len(collection) == 1 and next(collection.resources()).filename:
                filename = next(collection.resources()).filename
            else:
                categories = collection.category_list()
                filename = cls._operation_filename(categories)
            cls.operation_filename = filename
            cls.operation_file_format = cls._operation_file_format(filename)
            cls.is_operation_file_json = bool(cls.operation_file_format == Const.CONTENT_FORMAT_JSON)
            cls.is_operation_file_mkdn = bool(cls.operation_file_format == Const.CONTENT_FORMAT_MKDN)
            cls.is_operation_file_text = bool(cls.operation_file_format == Const.CONTENT_FORMAT_TEXT)
            cls.is_operation_file_yaml = bool(cls.operation_file_format == Const.CONTENT_FORMAT_YAML)

        return filename

    @classmethod
    def is_supported_file_format(cls):
        """Test if file format is supported."""

        return bool(cls.is_operation_file_json or
                    cls.is_operation_file_mkdn or
                    cls.is_operation_file_text or
                    cls.is_operation_file_yaml)

    @classmethod
    def default_content_file(cls, category):
        """Return default content file.

        Args:
            category (str): User defined content category.

        Returns:
            str: Filename with absolute path.
        """

        filename = category + 's.yaml'
        filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/defaults'), filename)

        return filename

    @classmethod
    def _operation_filename(cls, categories):
        """Return operation default filename

        Filename is set based on priority order of
          1) command line input
          2) content defaults operations, content template or shell completion
          3) content category specific defaults

        Args:
            categories (tuple): List of categories related to operation.

        Returns:
            str: Operation filename.
        """

        filename = None
        if cls.source.operation_file:
            filename = cls.source.operation_file

        if cls.defaults:
            filename = cls.default_content_file(cls.content_category)

        if cls.template:
            filename = os.path.join('./', cls.content_category + '-template.' + cls.template_format.lower())

        if cls.complete and not filename:
            filename = os.path.join('./snippy.' + cls.complete + '-completion')

        if not filename:
            if len(categories) == 1:
                defaults = categories[0] + 's.mkdn'
            else:
                defaults = 'content.mkdn'
            filename = os.path.join('./', defaults)

        return filename

    @classmethod
    def _operation_file_format(cls, filename):
        """Extract operation file format.

        The file format must be exactly as defined for supported file formats.
        In case of shell completion, there is no file extension and the check
        passes.

        Args:
            filename (str): Filename with file extension defining the format.

        Returns:
            str: Operation file format.
        """

        file_format = Const.CONTENT_FORMAT_NONE
        name, extension = os.path.splitext(filename)
        if name and extension == '.json':
            file_format = Const.CONTENT_FORMAT_JSON
        elif name and extension in ('.md', '.mkdn'):
            file_format = Const.CONTENT_FORMAT_MKDN
        elif name and extension in ('.text', '.txt'):
            file_format = Const.CONTENT_FORMAT_TEXT
        elif name and extension in ('.yaml', '.yml'):
            file_format = Const.CONTENT_FORMAT_YAML
        elif not cls.complete:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot identify file format for file: {}'.format(filename))

        return file_format

    @classmethod
    def validate_search_context(cls, collection, operation):  # pylint: disable=too-many-branches
        """Validate content search context."""

        # Search keys are treated in priority order of 1) digest, 2) uuid, 3)
        # unknown identity, 4) content data and 5) search keywords. Search
        # keywords are already validated and invalid keywords are interpreted
        # as 'list all' which is always correct at this point.
        cls._logger.debug('validating search context with %d results', len(collection))
        if cls._is_content_digest():
            if cls.operation_digest:
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with message digest: %s' % cls.operation_digest)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content digest: %.16s :matched: %d :times preventing: %s :operation' %
                               (cls.operation_digest, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty message digest for: %s :operation' % operation)
        elif cls._is_content_uuid():
            if cls.operation_uuid:
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with content uuid: %s' % cls.operation_uuid)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content uuid: %.16s :matched: %d :times preventing: %s :operation' %
                               (cls.operation_uuid, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty content uuid for: %s :operation' % operation)
        elif cls._is_content_identity():
            if cls.operation_identity:
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with content identity: %s' % cls.operation_identity)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content identity: %.16s :matched: %d :times preventing: %s :operation' %
                               (cls.operation_identity, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty content identity for: %s :operation' % operation)
        elif cls.content_data:
            if any(cls.content_data):
                data = Const.EMPTY.join(cls.content_data)
                data = data[:30] + (data[30:] and '...')
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with content data: %s' % data)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content data: %s :matched: %d :times preventing: %s :operation' %
                               (data, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty content data for: %s :operation' % operation)
        elif cls._is_search_keywords():
            if not collection:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')
            elif len(collection) > 1:
                Cause.push(Cause.HTTP_CONFLICT,
                           'search keywords matched: %d :times preventing: %s :operation' % (len(collection), operation))
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'no message digest, content data or search keywords were provided')

    @classmethod
    def _is_search_keywords(cls):
        """Test if search is made with any of the search option.

        The seach categories (search_cat_kws) is not considered optional search
        keywords because this category is set always implicitly if not provided
        by the user.
        """

        return bool(cls.search_all_kws or cls.search_tag_kws or cls.search_grp_kws)

    @classmethod
    def _is_content_digest(cls):
        """Test if content digest was defined."""

        return bool(cls.operation_digest is not None)

    @classmethod
    def _is_content_uuid(cls):
        """Test if content uuid was defined."""

        return bool(cls.operation_uuid is not None)

    @classmethod
    def _is_content_identity(cls):
        """Test if content identity was defined."""

        return bool(cls.operation_identity is not None)

    @classmethod
    def is_search_criteria(cls):
        """Test if any of the search criterias were used."""

        criteria = False
        if cls._is_search_keywords()     \
           or cls._is_content_digest()   \
           or cls._is_content_uuid()     \
           or cls._is_content_identity() \
           or cls.content_data:
            criteria = True

        return criteria

    @staticmethod
    def utcnow():
        """Get UTC time stamp in ISO8601 format."""

        utc = datetime.datetime.utcnow()

        return utc.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

    @classmethod
    def debug(cls):
        """Debug Config.

        Do not print any configuration attrubutes from here. Use only the
        string presentation of the Config class to print attributes. This
        is because of security reasons.
        """

        cls._logger.debug('config parsed: {}'.format(Config()))
