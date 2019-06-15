# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""base: Base class for configuration sources."""

import os
import re
import sys
import traceback
from collections import OrderedDict

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.parser import Parser
from snippy.logger import Logger
from snippy.meta import __version__


class ConfigSourceBase(object):  # pylint: disable=too-many-instance-attributes, too-many-public-methods, too-many-lines
    """Base class for configuration sources."""

    CREATE = 'create'
    SEARCH = 'search'
    UPDATE = 'update'
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'
    UNIQUE = 'unique'
    OPERATIONS = ('create', 'search', 'update', 'delete', 'export', 'import')

    ATTRIBUTES = ('category', 'data', 'brief', 'description', 'name', 'groups', 'tags',
                  'links', 'source', 'versions', 'languages', 'filename', 'created',
                  'updated', 'uuid', 'digest')

    # Defaults
    DEFAULT_LOG_MSG_MAX = Logger.DEFAULT_LOG_MSG_MAX
    LIMIT_DEFAULT_API = 20
    LIMIT_DEFAULT_CLI = 99
    OFFSET_DEFAULT = 0
    SERVER_BASE_PATH_REST = '/api/snippy/rest'

    RE_MATCH_OPT_LEADING_HYPHENS = re.compile(r'''
        ^[-]{0,2}    # Match leading hyphens used to indicate command line option.
        ''', re.VERBOSE)

    def __init__(self, derived):
        self._logger = Logger.get_logger(__name__)
        self._logger.debug('config source: {}'.format(derived))
        self._derived = derived
        self._reset_fields = {}
        self._repr = self._get_repr()
        self.complete = Const.EMPTY
        self.debug = False
        self.defaults = False
        self.digest = None
        self.editor = False
        self.failure = False
        self.failure_message = Const.EMPTY
        self.template_format = Const.CONTENT_FORMAT_MKDN
        self.template_format_used = False
        self.languages = ()
        self.log_json = False
        self.log_msg_max = self.DEFAULT_LOG_MSG_MAX
        self.merge = False
        self.no_ansi = False
        self.no_editor = False
        self.operation = None
        self.operation_file = Const.EMPTY
        self.plugin = []  # Plugin from configuration source.
        self.plugin_used = False  # Plugin used in configuration source.
        self.plugins = {}  # All plugins.
        self.profiler = False
        self.quiet = False
        self.run_healthcheck = False
        self.server_minify_json = False
        self.server_readonly = False
        self.server_ssl_ca_cert = None
        self.server_ssl_cert = None
        self.server_ssl_key = None
        self.storage_path = Const.EMPTY
        self.storage_type = Const.DB_SQLITE
        self.storage_host = Const.EMPTY
        self.storage_user = Const.EMPTY
        self.storage_password = Const.EMPTY
        self.storage_database = Const.EMPTY
        self.storage_ssl_cert = None
        self.storage_ssl_key = None
        self.storage_ssl_ca_cert = None
        self.template = False
        self.import_hook = None
        self.uuid = None
        self.version = __version__
        self.very_verbose = False

    def __str__(self):  # pylint: disable=too-many-statements
        """Print class attributes in a controlled manner.

        This is intended to limit printing of sensitive configuration values
        by accident. This method should return only configuration values that
        can be printed without revealing configuration that is considered
        sensitive.

        See LOGGING security rules.
        """

        namespace = []
        if not hasattr(self, '_repr'):
            return str('%s(%s)' % ('ConfigSourceBase', ', '.join(namespace)))

        namespace.append('brief={}'.format(self.brief))
        namespace.append('category={}'.format(self.category))
        namespace.append('complete={}'.format(self.complete))
        namespace.append('data={}'.format(self.data))
        namespace.append('debug={}'.format(self.debug))
        namespace.append('defaults={}'.format(self.defaults))
        namespace.append('description={}'.format(self.description))
        namespace.append('digest={}'.format(self.digest))
        namespace.append('editor={}'.format(self.editor))
        namespace.append('failure={}'.format(self.failure))
        namespace.append('failure_message={}'.format(self.failure_message))
        namespace.append('filename={}'.format(self.filename))
        namespace.append('groups={}'.format(self.groups))
        namespace.append('identity={}'.format(self.identity))
        namespace.append('languages={}'.format(self.languages))
        namespace.append('links={}'.format(self.links))
        namespace.append('log_json={}'.format(self.log_json))
        namespace.append('log_msg_max={}'.format(self.log_msg_max))
        namespace.append('merge={}'.format(self.merge))
        namespace.append('name={}'.format(self.name))
        namespace.append('no_ansi={}'.format(self.no_ansi))
        namespace.append('no_editor={}'.format(self.no_editor))
        namespace.append('operation={}'.format(self.operation))
        namespace.append('operation_file={}'.format(self.operation_file))
        namespace.append('plugin={}'.format(self.plugin))
        namespace.append('profiler={}'.format(self.profiler))
        namespace.append('quiet={}'.format(self.quiet))
        namespace.append('remove_fields={}'.format(self.remove_fields))
        namespace.append('reset_fields={}'.format(self.reset_fields))
        namespace.append('run_healthcheck={}'.format(self.run_healthcheck))
        namespace.append('run_server={}'.format(self.run_server))
        namespace.append('sall={}'.format(self.sall))
        namespace.append('scat={}'.format(self.scat))
        namespace.append('search_filter={}'.format(self.search_filter))
        namespace.append('search_limit={}'.format(self.search_limit))
        namespace.append('search_offset={}'.format(self.search_offset))
        namespace.append('server_base_path_rest={}'.format(self.server_base_path_rest))
        namespace.append('server_host={}'.format(self.server_host))
        namespace.append('server_minify_json={}'.format(self.server_minify_json))
        namespace.append('server_readonly={}'.format(self.server_readonly))
        namespace.append('sgrp={}'.format(self.sgrp))
        namespace.append('sort_fields={}'.format(self.sort_fields))
        namespace.append('source={}'.format(self.source))
        namespace.append('stag={}'.format(self.stag))
        namespace.append('storage_type={}'.format(self.storage_type))
        namespace.append('tags={}'.format(self.tags))
        namespace.append('template={}'.format(self.template))
        namespace.append('uuid={}'.format(self.uuid))
        namespace.append('version={}'.format(self.version))
        namespace.append('versions={}'.format(self.versions))
        namespace.append('very_verbose={}'.format(self.very_verbose))

        return str('%s(%s)' % (self._derived, ', '.join(namespace)))

    def __repr__(self):
        if hasattr(self, '_repr'):
            repr_ = self._repr
        else:
            repr_ = self._get_repr()

        return repr_

    def _get_repr(self):
        """Get object representation."""

        namespace = []
        class_name = type(self).__name__
        attributes = tuple(set(self.__dict__.keys()) - set({'_logger', '_repr', '_derived'}))
        # Optimization: For some reason using lstrip below to remove the
        # underscore that is always left, causes 2-3% performance penalty.
        # Using strip does not cause same effect.
        attributes = [attribute.strip('_') for attribute in attributes]
        for attribute in sorted(attributes):
            namespace.append('%s=%r' % (attribute, getattr(self, attribute)))
        repr_ = '%s(%s)' % (class_name, ', '.join(namespace))

        return repr_

    def init_conf(self, parameters):  # pylint: disable=too-many-statements
        """Initialize configuration parameters.

        Configuration can be read from command line interface or received
        from API query. It is also possible to configure for example server
        and storage parameters with environment variables. The precedence
        of configuration is:

          1. Command line option.
          2. Environment variable.
          3. Hard coded default.

        Args:
            parameters (dict): Parameters from configuration source.
        """

        if parameters is None:
            parameters = {}

        # Content category aware parsing requires the category to be defined
        # as early as possible. The content category requires knowledge of the
        # operation.
        self.operation = parameters.get('operation')
        self.category = parameters.get('category', Const.SNIPPET)
        self.scat = parameters.get('scat', self.category)

        # There are few parameters like 'data' and 'digest' where the tool
        # error logic must know if value was defined at all by the CLI user.
        # This kind of parameters must be set to None by default. All other
        # parameters must have default value like empty list or string that
        # make sense.
        self.brief = parameters.get('brief', Const.EMPTY)
        self.complete = parameters.get('complete', Const.EMPTY)
        self.data = parameters.get('data', None)
        self.debug = parameters.get(*self.read_env('debug', False))
        self.defaults = parameters.get('defaults', False)
        self.description = parameters.get('description', Const.EMPTY)
        self.digest = parameters.get('digest', None)
        self.editor = parameters.get('editor', False)
        self.failure = parameters.get('failure', False)
        self.failure_message = parameters.get('failure_message', Const.EMPTY)
        self.filename = parameters.get('filename', Const.EMPTY)
        self.template_format = parameters.get('format', Const.CONTENT_FORMAT_MKDN)
        self.template_format_used = parameters.get('format_used', False)
        self.groups = parameters.get('groups', Const.DEFAULT_GROUPS)
        self.identity = parameters.get('identity', None)
        self.languages = parameters.get('languages', ())
        self.links = parameters.get('links', ())
        self.log_json = parameters.get(*self.read_env('log_json', False))
        self.log_msg_max = parameters.get(*self.read_env('log_msg_max', self.DEFAULT_LOG_MSG_MAX))
        self.merge = parameters.get('merge', False)
        self.name = parameters.get('name', Const.EMPTY)
        self.no_ansi = parameters.get(*self.read_env('no_ansi', False))
        self.no_editor = parameters.get('no_editor', False)
        self.operation_file = parameters.get('operation_file', Const.EMPTY)
        self.plugin = parameters.get('plugin', [])
        self.plugin_used = bool('plugin' in parameters)
        self.profiler = parameters.get(*self.read_env('profile', False))
        self.quiet = parameters.get(*self.read_env('q', False))
        self.remove_fields = parameters.get('fields', self.ATTRIBUTES)
        self.run_healthcheck = parameters.get('server_healthcheck', False)
        self.sall = parameters.get('sall', None)
        self.search_filter = parameters.get('search_filter', None)
        self.search_limit = parameters.get('limit', self.LIMIT_DEFAULT_API)
        self.search_offset = parameters.get('offset', self.OFFSET_DEFAULT)
        self.server_base_path_rest = parameters.get(*self.read_env('server_base_path_rest', self.SERVER_BASE_PATH_REST))
        self.server_host = parameters.get(*self.read_env('server_host', Const.EMPTY))
        self.server_minify_json = parameters.get(*self.read_env('server_minify_json', False))
        self.server_readonly = parameters.get('server_readonly', False)
        self.server_ssl_ca_cert = parameters.get(*self.read_env('server_ssl_ca_cert', None))
        self.server_ssl_cert = parameters.get(*self.read_env('server_ssl_cert', None))
        self.server_ssl_key = parameters.get(*self.read_env('server_ssl_key', None))
        self.sgrp = parameters.get('sgrp', None)
        self.sort_fields = parameters.get('sort', ('brief'))
        self.source = parameters.get('source', Const.EMPTY)
        self.stag = parameters.get('stag', None)
        self.storage_path = parameters.get(*self.read_env('storage_path', Const.EMPTY))
        self.storage_type = parameters.get(*self.read_env('storage_type', Const.DB_SQLITE))
        self.storage_host = parameters.get(*self.read_env('storage_host', Const.EMPTY))
        self.storage_user = parameters.get(*self.read_env('storage_user', Const.EMPTY))
        self.storage_password = parameters.get(*self.read_env('storage_password', Const.EMPTY))
        self.storage_database = parameters.get(*self.read_env('storage_database', Const.EMPTY))
        self.storage_ssl_cert = parameters.get(*self.read_env('storage_ssl_cert', None))
        self.storage_ssl_key = parameters.get(*self.read_env('storage_ssl_key', None))
        self.storage_ssl_ca_cert = parameters.get(*self.read_env('storage_ssl_ca_cert', None))
        self.tags = parameters.get('tags', ())
        self.template = parameters.get('template', False)
        self.uuid = parameters.get('uuid', None)
        self.version = parameters.get('version', __version__)
        self.versions = parameters.get('versions', ())
        self.very_verbose = parameters.get(*self.read_env('vv', False))
        self._repr = self._get_repr()

        self._set_import_hook()

        # The flag that tells if Snippy server is run is set after the
        # command line arguments and environment variables are parsed.
        self.run_server = bool(self.server_host)

    @property
    def category(self):
        """Get content category."""

        return self._category

    @category.setter
    def category(self, value):
        """Set content or field category.

        The content category is important when content is created. In case of
        the ``create`` operation, there must be only one category.
        """

        value = Parser.format_list(value)
        if len(value) == 1 and set(value).issubset(Const.CATEGORIES) or set(value).issubset(Const.FIELD_CATEGORIES):
            value = value[0]
        else:
            value = Const.UNKNOWN_CATEGORY

        self._category = value  # pylint: disable=attribute-defined-outside-init

    @property
    def data(self):
        """Get content data."""

        return self._data

    @data.setter
    def data(self, value):
        """Convert content data to tuple of utf-8 encoded unicode strings.

        The tool must be able to idenfity if the value was given at all. This
        case is idenfigied with value None. With empty value from user, there
        will be a single element in tuple which is empty string. By doing this,
        there is no need to check value None each time when accessed.
        """

        if value is not None:
            data = Parser.format_data(self.category, value)
        else:
            data = ()

        self._data = data  # pylint: disable=attribute-defined-outside-init

    @property
    def brief(self):
        """Get content brief."""

        return self._brief

    @brief.setter
    def brief(self, value):
        """Convert content brief to utf-8 encoded unicode string."""

        if value is None:
            self._reset_fields['brief'] = 'brief'

        self._brief = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def description(self):
        """Get content description."""

        return self._description

    @description.setter
    def description(self, value):
        """Convert content description to utf-8 encoded unicode string."""

        if value is None:
            self._reset_fields['description'] = 'description'

        self._description = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def name(self):
        """Get content name."""

        return self._name

    @name.setter
    def name(self, value):
        """Convert content name to utf-8 encoded unicode string."""

        if value is None:
            self._reset_fields['name'] = 'name'

        self._name = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def groups(self):
        """Get content groups."""

        return self._groups

    @groups.setter
    def groups(self, value):
        """Convert content groups to tuple of utf-8 encoded unicode strings."""

        if value is None:
            self._reset_fields['groups'] = 'groups'

        self._groups = Parser.format_list(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def tags(self):
        """Get content tags."""

        return self._tags

    @tags.setter
    def tags(self, value):
        """Convert content tags to tuple of utf-8 encoded unicode strings."""

        if value is None:
            self._reset_fields['tags'] = 'tags'

        self._tags = Parser.format_list(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def links(self):
        """Get content links."""

        return self._links

    @links.setter
    def links(self, value):
        """Convert content links to tuple of utf-8 encoded unicode strings."""

        if value is None:
            self._reset_fields['links'] = 'links'

        self._links = Parser.format_links(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def source(self):
        """Get content source."""

        return self._source

    @source.setter
    def source(self, value):
        """Convert content source to utf-8 encoded unicode string."""

        if value is None:
            self._reset_fields['source'] = 'source'

        self._source = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def versions(self):
        """Get content versions."""

        return self._versions

    @versions.setter
    def versions(self, value):
        """Convert content versions to tuple of utf-8 encoded unicode strings."""

        if value is None:
            self._reset_fields['versions'] = 'versions'

        self._versions = Parser.format_versions(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def languages(self):
        """Get content languages."""

        return self._languages

    @languages.setter
    def languages(self, value):
        """Convert content languages to tuple of utf-8 encoded unicode strings."""

        if value is None:
            self._reset_fields['languages'] = 'languages'

        self._languages = Parser.format_list(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def filename(self):
        """Get content filename attribute."""

        return self._filename

    @filename.setter
    def filename(self, value):
        """Convert content filename to utf-8 encoded unicode string."""

        if value is None:
            self._reset_fields['filename'] = 'filename'

        self._filename = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def operation_file(self):
        """Get operation filename from the ``--file`` option."""

        return self._operation_file

    @operation_file.setter
    def operation_file(self, value):
        """Convert operation filename to utf-8 encoded unicode string."""

        self._operation_file = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def sall(self):
        """Get 'search all' keywords."""

        return self._sall

    @sall.setter
    def sall(self, value):
        """Store 'search all' keywords.

        The keywords are stored in tuple with one keywords per element."""

        self._sall = Parser.format_search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def scat(self):
        """Get content categories."""

        return self._scat

    @scat.setter
    def scat(self, value):
        """Store content categories.

        The ``scat`` option defines the content category or categories for
        the operation. If operation is ``create``, there must be only one
        category. If the operation is ``search`` or the operation requires
        searching content, there can be multiple values.

        The keywords are stored in tuple with one keywords per element.

        If any of the given categories is incorrect, an error is set. This
        is a simple error handling that fails the operation instead of trying
        to recover it. An unknown value is set to the ``scat`` option in case
        of a failure because it minimizes the search results in the error
        scenario. If all categories would be searched with errors, it could
        lead to a large search results sets in case of failures.
        """

        scat = Parser.format_search_keywords(value)
        if not scat:
            scat = (Const.SNIPPET,)
        if Const.ALL_CATEGORIES in scat:
            scat = Const.CATEGORIES

        if not set(scat).issubset(Const.CATEGORIES):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content categories: {} :are not a subset of: {}'.format(self._format_scat(scat), Const.CATEGORIES))  # noqa pylint: disable=line-too-long
            scat = (Const.UNKNOWN_CATEGORY,)

        if self.operation == self.CREATE and (Const.UNKNOWN_CATEGORY in scat or len(scat) != 1):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content category must be unique when content is created: {}'.format(self._format_scat(scat)))  # noqa pylint: disable=line-too-long

        self._scat = scat  # pylint: disable=attribute-defined-outside-init

    @property
    def stag(self):
        """Get 'search tag' keywords."""

        return self._stag

    @stag.setter
    def stag(self, value):
        """Store 'search tag' keywords.

        The keywords are stored in tuple with one keywords per element."""

        self._stag = Parser.format_search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def sgrp(self):
        """Get 'search groups' keywords."""

        return self._sgrp

    @sgrp.setter
    def sgrp(self, value):
        """Store 'search groups' keywords.

        The keywords are stored in tuple with one keywords per element.
        """

        self._sgrp = Parser.format_search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def search_filter(self):
        """Get search regexp filter."""

        return self._search_filter

    @search_filter.setter
    def search_filter(self, value):
        """Search regexp filter must be Python regexp.

        Value ``None`` means that the value was not set at all by caller.
        """

        if value is None:
            self._search_filter = None  # pylint: disable=attribute-defined-outside-init

            return

        try:
            self._search_filter = re.compile(value)  # pylint: disable=attribute-defined-outside-init
        except (re.error, TypeError):
            self._search_filter = None  # pylint: disable=attribute-defined-outside-init
            Cause.push(Cause.HTTP_BAD_REQUEST,
                       'listing matching content without filter because it was not syntactically correct regular expression')

    @property
    def search_limit(self):
        """Get search result limit."""

        return self._search_limit

    @search_limit.setter
    def search_limit(self, value):
        """Search result limit defines maximum amount of search results."""

        self._search_limit = self.LIMIT_DEFAULT_API  # pylint: disable=attribute-defined-outside-init
        try:
            value = int(value)
            if value >= 0:
                self._search_limit = value  # pylint: disable=attribute-defined-outside-init
            else:
                raise ValueError
        except ValueError:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'search result limit is not a positive integer: {}'.format(value))

    @property
    def search_offset(self):
        """Get search offset from start."""

        return self._search_offset

    @search_offset.setter
    def search_offset(self, value):
        """Store 'search offset'.

        The search offset defines how many entries are skippet from the
        beginning of search results."""

        self._search_offset = self.OFFSET_DEFAULT  # pylint: disable=attribute-defined-outside-init
        try:
            value = int(value)
            if value >= 0:
                self._search_offset = value  # pylint: disable=attribute-defined-outside-init
            else:
                raise ValueError
        except ValueError:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'search offset is not a positive integer: {}'.format(value))

    @property
    def sort_fields(self):
        """Get sorted fields."""

        return self._sort_fields

    @sort_fields.setter
    def sort_fields(self, value):
        """Sorted fields are stored in internal presentation."""

        parsed = OrderedDict()
        fields = Parser.format_list(value, sort_=False)
        for field in fields:
            match = re.match(r'''
            (?P<direction>-?)   # Catch sort direction sign (+/-).
            (?P<field>\S+)      # Catch fields.
            ''', field, re.IGNORECASE | re.VERBOSE)
            if match.group('field') and match.group('field') in self.ATTRIBUTES:
                parsed[match.group('field')] = 'DESC' if match.group('direction') == '-' else 'ASC'
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existent field={}'.format(field))
        self._logger.debug('{}: content attribute sort order from user: {}'.format(self._derived, fields))
        self._logger.debug('{}: content attribute internal sort structure: {}'.format(self._derived, parsed))
        self._sort_fields = parsed  # pylint: disable=attribute-defined-outside-init

    @property
    def remove_fields(self):
        """Get removed fields."""

        return self._remove_fields

    @remove_fields.setter
    def remove_fields(self, value):
        """Store 'removed fields'.

        The removed fields are presented as tuple and they are converted from
        requested 'fields' parameter."""

        remove_fields = ()
        requested_fields = Parser.format_list(value)
        valid = True
        for field in requested_fields:
            if field not in self.ATTRIBUTES:
                valid = False
                Cause.push(Cause.HTTP_BAD_REQUEST, 'resource field does not exist: {}'.format(field))

        if valid:
            remove_fields = tuple(set(self.ATTRIBUTES) - set(requested_fields))  # pylint: disable=attribute-defined-outside-init

        self._logger.debug('{}: content attributes that are removed: {}'.format(self._derived, remove_fields))
        self._remove_fields = remove_fields  # pylint: disable=attribute-defined-outside-init

    @property
    def reset_fields(self):
        """Get reset fields."""

        return tuple(self._reset_fields.keys())

    @property
    def run_server(self):
        """Get bool value that tells if Snippy server is run."""

        return self._run_server

    @run_server.setter
    def run_server(self, value):
        """Store flag that tells if server is run.

        This flag is set after all command line options have been parsed.

        If content operations are used from the command line, the server
        is not started. Using content operations tell that user wants to
        operate content from command line, not run the server. This is a
        special for Docker acontainer which always has the ``server-host``
        environment variable set.

        If healthcheck operation for the server is made, server is never
        run. User may give the server host address with the healthcheck,
        but the server itself is not started. This is related to a Docker
        container healthcheck.

        Args:
            value (bool): Bool value that tells if server is run.
        """

        if self.operation in self.OPERATIONS:
            self._logger.debug('override server startup because of operation: {}'.format(self.operation))
            value = False

        if self.run_healthcheck:
            value = False

        self._run_server = value  # pylint: disable=attribute-defined-outside-init

    @property
    def server_base_path_rest(self):
        """Get REST API base path."""

        return self._server_base_path_rest

    @server_base_path_rest.setter
    def server_base_path_rest(self, value):
        """Validate server REST API base path.

        Checking the base path is far from complete and it is not known how
        to do it to be absolutely certain that it works without copying all
        the same checks as used server. Therefore this is just a portion of
        checks for possible failure cases.

        Make sure that REST API base path ends with slash.

        Args:
            value (str): REST API base path.
        """

        # Joining base path URL always assumes that the base path starts
        # and ends with slash. The os.path cannot be used because it
        # causes incorrect URL on Windows.
        if not value.startswith('/'):
            value = '/' + value
        if not value.endswith('/'):
            value = value + '/'

        if '//' in value:
            self._logger.debug('{}: use default base path because invalid configuration: {}'.format(self._derived, value))
            value = self.SERVER_BASE_PATH_REST

        self._server_base_path_rest = value  # pylint: disable=attribute-defined-outside-init

    @property
    def server_host(self):
        """Get server host IP and port"""

        return self._server_host

    @server_host.setter
    def server_host(self, value):
        """Validate server host IP and port.

        Validating against special case of server host 'container.hostname'
        should never happen. There is a startup script that is setting the
        ``SNIPPY_SERVER_HOST`` environment parameter correctly.

        Args:
            value (str): Server host that contains IP address and port.
        """

        if 'container.hostname' in value:
            import socket
            try:
                host = socket.gethostbyname(socket.gethostname())
                value = value.replace('container.hostname', host)
                os.environ['SNIPPY_SERVER_HOST'] = value
            except socket.error:
                value = value.replace('container.hostname', '0.0.0.0')
                self._logger.security('running container server on 0.0.0.0: {}'.format(value))

        self._server_host = value  # pylint: disable=attribute-defined-outside-init

    @property
    def identity(self):
        """Get content identity."""

        return self._identity

    @identity.setter
    def identity(self, value):
        """Convert content identity to utf-8 encoded unicode string.

        The identity attribute is used when the content identity type is not
        known. The identity can be either a message digest or UUID.

        There is no failure proof way to tell if the identity string is a
        Digest or UUID. By creating a third identity field for unidentidied
        identity type, it quarantees that the digest and UUID attributes
        always have correctly matching identity against the type.
        """

        if value is None:
            self._identity = None  # pylint: disable=attribute-defined-outside-init
        else:
            self._identity = Parser.format_string(value)  # pylint: disable=attribute-defined-outside-init

    @classmethod
    def read_env(cls, option, default):
        """Read parameter from optional environment variable.

        Read parameter value from environment variable or return given default
        value. Environment variable names follow the same command line option
        naming convesion with modifications:

          1. Leading hyphens are removed.
          2. Option casing is converted to full upper case.
          3. Hyphens are replaced with underscores.
          4. ``SNIPPY_`` prefix is added,

        For example corresponding environment variable for the ``--server-host``
        command line option is ``SNIPPY_SERVER_HOST``.

        Args:
            option (str): Command line option.
            default: Default value.

        Returns:
            tuple: Same command line option name as received with value.
        """

        # Remove leading hyphens to allow calling the method with the name
        # of command line parameter. This helps finding related code.
        option = cls.RE_MATCH_OPT_LEADING_HYPHENS.sub('', option)

        # The getenv returns None if parameter was not set.
        value = os.getenv('SNIPPY_' + option.replace('-', '_').upper(), default)
        if value is None:
            return (option, default)

        # There is no need to convert string variables because they can be
        # returned directly. The bool typed environment variable gets True
        # only if the value is read as expected.
        #
        # The environment variables are strings so value '0' will convert
        # to boolean True because the string is not empty.
        if isinstance(default, bool):
            try:
                value = int(value)
                value = bool(value)
            except ValueError:
                if value.lower() == 'true':
                    value = True
                else:
                    value = default
        elif isinstance(default, int):
            try:
                value = int(value)
            except ValueError:
                value = default

        if option == 'storage_type' and value not in Const.STORAGES:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'incorrect storage type: {} :is not a subset of: {}'.format(value, Const.STORAGES))
            value = Const.DB_SQLITE

        return (option, value)

    @classmethod
    def read_arg(cls, option, default, args):
        """Read command line argument directly from sys.argv.

        This is intenden to be used only in special cases that are related to
        debug options. The debug options are required for example to print logs
        before parsing command line arguments.

        This function supports only bool and integer values because there are
        currently no other use cases.

        This follows the standard command option parsing precedence:

          1. Command line option.
          2. Environment variable.
          3. Hard coded default.

        Args:
            option (string): Command line option.
            default: Default value if option is not configured.
            args (list): Argument list received from command line.

        Returns:
            int,bool: Value for the command line option.
        """

        value = Const.EMPTY
        parameter = cls.RE_MATCH_OPT_LEADING_HYPHENS.sub('', option)
        if isinstance(default, bool):
            value = bool(option in args) or cls.read_env(parameter, default)[1]
        elif isinstance(default, int):
            try:
                if bool(option in args):
                    value = int(args[args.index(option) + 1])
                else:
                    value = int(cls.read_env(parameter, default)[1])
                if value < 0:
                    value = default
            except (IndexError, ValueError):
                value = default
        else:
            value = default

        return value

    @staticmethod
    def _format_scat(scat):
        """Format ``scat`` option for Python 2 and Python 3.

        The formatting removes unicode string prefix u'' in case of Python 2.
        The formatting also prints a beautified list of invalid categories in
        the same format as the valid categories.

        Args
            scat (tuple): Content categories
        """

        return '({})'.format(', '.join('\'{0}\''.format(w) for w in scat))

    def get_plugin_short_names(self):
        """Get plugin short names.

        The short names are used when user or client identifies a plugin.

        The plugins are idenfied with prefix ``snippy-`` in the plugin name.
        The plugins are stored and operated without the ``snippy-`` prefix.

        Returns:
            tuple: List of plugin names.
        """

        return tuple(self.plugins.keys())

    def read_plugins(self, args):
        """Read all plugins.

        Reading of plugins all the time is too slow. This is a problem with
        tests that slow down too much in case this would be read always.

        Returns:
            dict: ``Distribution`` objects from importlib_metadata.
        """

        plugins = {}
        if '--plugin' not in args:
            return

        try:
            import importlib_metadata
            for distribution in importlib_metadata.distributions():
                if distribution.metadata['Name'].startswith('snippy-'):
                    name = distribution.metadata['Name'].replace('snippy-', Const.EMPTY)
                    plugins[name] = distribution
        except ImportError:
            self._logger.debug('failed to read plugins: {}'.format(traceback.format_exc()))

        self.plugins = plugins

    def _set_import_hook(self):
        """Set import plugin.

        This methods tests if user provided a plugin for import operation
        and sets the import specific plugin variable.
        """

        self.import_hook = None
        if self.plugin and self.operation == self.IMPORT:
            self._logger.debug('import plugin used: {}'.format(self.plugin))
            module = self.plugins[self.plugin].entry_points[0].value
            try:
                __import__(module)
                try:
                    modulespecs = sys.modules[module]
                    import_hook = getattr(modulespecs, 'snippy_import_hook', None)
                    if callable(import_hook):
                        self.import_hook = import_hook
                except KeyError:
                    self._logger.debug('failed use plugin: {}'.format(traceback.format_exc()))
            except ModuleNotFoundError:
                self._logger.debug('failed to import plugin: {}'.format(traceback.format_exc()))
