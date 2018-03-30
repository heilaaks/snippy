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

"""base: Base class for configuration sources."""

import re

from snippy.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.logger import Logger
from snippy.meta import __version__


class ConfigSourceBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for configuration sources."""

    # Operations
    CREATE = 'create'
    SEARCH = 'search'
    UPDATE = 'update'
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'
    OPERATIONS = ('create', 'search', 'update', 'delete', 'export', 'import')

    # Fields
    DATA = 'data'
    BRIEF = 'brief'
    GROUP = 'group'
    TAGS = 'tags'
    LINKS = 'links'
    CATEGORY = 'category'
    FILENAME = 'filename'
    RUNALIAS = 'runalias'
    VERSIONS = 'versions'
    CREATED = 'created'
    CREATED = 'updated'
    DIGEST = 'digest'
    KEY = 'key'
    ALL_FIELDS = ('data', 'brief', 'group', 'tags', 'links', 'category', 'filename',
                  'runalias', 'versions', 'created', 'updated', 'digest', 'key')

    # Defaults
    LIMIT_DEFAULT = 20
    BASE_PATH = '/snippy/api/v1/'
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = '8080'

    def __init__(self, parameters=None):
        self._logger = Logger(__name__).logger
        self._repr = self._get_repr()
        self.set_conf(parameters)

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
        attributes = tuple(set(self.__dict__.keys()) - set({'_logger', '_repr'}))
        # Optimization: For some reason using lstrip below to remove the
        # underscore that is always left, causes 2-3% performance penalty.
        # Using strip does not cause same effect.
        attributes = [attribute.strip('_') for attribute in attributes]
        for attribute in sorted(attributes):
            namespace.append('%s=%r' % (attribute, getattr(self, attribute)))
        repr_ = '%s(%s)' % (class_name, ', '.join(namespace))

        return repr_

    def set_conf(self, parameters):
        """Set API configuration parameters."""

        if parameters is None:
            parameters = {}

        # There are few parameters like 'data' and 'digest' where the tool
        # error logic must know if value was defined at all. This kind of
        # parameters must be set to None by default. All other parameters
        # must have default value like empty list or string that makes sense.
        self.base_path = parameters.get('base_path', ConfigSourceBase.BASE_PATH)
        self.brief = parameters.get('brief', Const.EMPTY)
        self.category = parameters.get('category')
        self.data = parameters.get('data', None)
        self.debug = parameters.get('debug', False)
        self.defaults = parameters.get('defaults', False)
        self.digest = parameters.get('digest', None)
        self.editor = parameters.get('editor', False)
        self.failure = parameters.get('failure', False)
        self.filename = parameters.get('filename', Const.EMPTY)
        self.group = parameters.get('group', Const.DEFAULT_GROUP)
        self.server_ip = parameters.get('server_ip', ConfigSourceBase.SERVER_IP)
        self.server_port = parameters.get('server_port', ConfigSourceBase.SERVER_PORT)
        self.storage_path = parameters.get('storage_path', Const.EMPTY)
        self.json_logs = parameters.get('json_logs', False)
        self.limit = parameters.get('limit', self.LIMIT_DEFAULT)
        self.links = parameters.get('links', ())
        self.no_ansi = parameters.get('no_ansi', False)
        self.operation = parameters.get('operation')
        self.profiler = parameters.get('profiler', False)
        self.quiet = parameters.get('quiet', False)
        self.regexp = parameters.get('regexp', Const.EMPTY)
        self.rfields = parameters.get('fields', self.ALL_FIELDS)
        self.sall = parameters.get('sall', None)
        self.server = parameters.get('server', False)
        self.sfields = parameters.get('sort', ('brief'))
        self.sgrp = parameters.get('sgrp', None)
        self.stag = parameters.get('stag', None)
        self.tags = parameters.get('tags', ())
        self.template = parameters.get('template', False)
        self.version = parameters.get('version', __version__)
        self.very_verbose = parameters.get('very_verbose', False)
        self._repr = self._get_repr()

    @property
    def data(self):
        """Get content data."""

        return self._data

    @data.setter
    def data(self, value):
        """Content data is stored as a tuple with one line per element.
        There is a quarantee that each line contains only one newline
        at the end of string in the tuple.

        Any value including empty string is considered valid data."""

        if value is not None:
            string_ = Parser.to_string(value)
            data = tuple(string_.split(Const.DELIMITER_DATA))
        else:
            data = ()

        self._data = data  # pylint: disable=attribute-defined-outside-init

    @property
    def tags(self):
        """Get content tags."""

        return self._tags

    @tags.setter
    def tags(self, value):
        """Content tags are stored as a tuple with one tag per element."""

        self._tags = Parser.keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def links(self):
        """Get content links."""

        return self._links

    @links.setter
    def links(self, value):
        """Content links are stored as a tuple with one link per element."""

        self._links = Parser.links(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def sall(self):
        """Get 'search all' keywords."""

        return self._sall

    @sall.setter
    def sall(self, value):
        """Search all keywords stored as a tuple with one keywords per
        element."""

        self._sall = Parser.search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def stag(self):
        """Get 'search tag' keywords."""

        return self._stag

    @stag.setter
    def stag(self, value):
        """Search tag keywords stored as a tuple with one keywords per
        element."""

        self._stag = Parser.search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def sgrp(self):
        """Get 'search group' keywords."""

        return self._sgrp

    @sgrp.setter
    def sgrp(self, value):
        """Search group keywords stored as a tuple with one keywords per
        element."""

        self._sgrp = Parser.search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def regexp(self):
        """Get search regexp filter."""

        return self._regexp

    @regexp.setter
    def regexp(self, value):
        """Search regexp filter must be Python regexp."""

        try:
            re.compile(value)
            self._regexp = value  # pylint: disable=attribute-defined-outside-init
        except re.error:
            self._regexp = Const.EMPTY  # pylint: disable=attribute-defined-outside-init
            Cause.push(Cause.HTTP_BAD_REQUEST,
                       'listing matching content without filter because it was not syntactically correct regular expression')

    @property
    def limit(self):
        """Get search result limit."""

        return self._limit

    @limit.setter
    def limit(self, value):
        """Search result limit."""

        self._limit = self.LIMIT_DEFAULT  # pylint: disable=attribute-defined-outside-init
        try:
            self._limit = int(value)  # pylint: disable=attribute-defined-outside-init
        except ValueError:
            self._logger.info('search result limit is not a number and thus default used: %d', self._limit)

    @property
    def sfields(self):
        """Get sorted fields in internal presentation."""

        return self._sfields

    @sfields.setter
    def sfields(self, value):
        """Sorted fields are stored in internal presentation from given
        value. The internal format contains field index that matches to
        database column index. The order where the sorted column names
        was received must be persisted. Otherwise the sort does not work
        correctly."""

        sorted_dict = {}
        sorted_dict['order'] = []
        sorted_dict['value'] = {}
        fields = Parser.keywords(value, sort_=False)
        for field in fields:
            try:
                if field[0].startswith('-'):
                    index_ = self.ALL_FIELDS.index(field[1:])
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = True
                else:
                    index_ = self.ALL_FIELDS.index(field)
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = False
            except ValueError:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existent field={}'.format(field))
        self._logger.debug('config source sorted fields: %s', fields)
        self._logger.debug('config source internal format for sorted fields: %s', sorted_dict)
        self._sfields = sorted_dict  # pylint: disable=attribute-defined-outside-init

    @property
    def rfields(self):
        """Get removed fields."""

        return self._rfields

    @rfields.setter
    def rfields(self, value):
        """Removed fields are presented as tuple and they are converted
        from requested fields."""

        requested_fields = Parser.keywords(value)
        self._rfields = tuple(set(self.ALL_FIELDS) - set(requested_fields))  # pylint: disable=attribute-defined-outside-init
        self._logger.debug('config source content fields that are removed from response: %s', self._rfields)

    @property
    def base_path(self):
        """Get server base path."""

        return self._base_path

    @base_path.setter
    def base_path(self, value):
        """Make sure that server base path ends with slash."""

        # Joining base path URL always assumes that the base path starts
        # and ends with slash. The os.path cannot be used because it
        # causes incorrect URL on Windows.
        if not value.startswith('/'):
            value = '/' + value
        if not value.endswith('/'):
            value = value + '/'

        # Checking the base path is far from complete and it is not known
        # how to do it to be absolutely certain that it works without
        # copying all the same checks as used server. Therefore this is
        # just a portion of checks for possible failure cases.
        if '//' in value:
            self._logger.debug('config source uses default base path because invalid configuration: %s', value)
            value = ConfigSourceBase.BASE_PATH

        self._base_path = value  # pylint: disable=attribute-defined-outside-init
