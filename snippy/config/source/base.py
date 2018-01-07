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

"""base.py: Base class for configuration sources."""

import re
from snippy.metadata import __version__
from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.logger.logger import Logger


class ConfigSourceBase(object):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
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
    UTC = 'utc'
    DIGEST = 'digest'
    KEY = 'key'
    ALL_FIELDS = ('data', 'brief', 'group', 'tags', 'links', 'category', 'filename',
                  'runalias', 'versions', 'utc', 'digest', 'key')

    # Defaults
    LIMIT_DEFAULT = 20

    def __init__(self):
        self.operation = Const.EMPTY
        self.category = Const.UNKNOWN_CONTENT
        self.editor = False
        self._data = ()
        self.brief = Const.EMPTY,
        self.group = Const.DEFAULT_GROUP
        self._tags = ()
        self._links = ()
        self.digest = None
        self._sall = ()
        self._stag = ()
        self._sgrp = ()
        self._regexp = Const.EMPTY,
        self._limit = ConfigSourceBase.LIMIT_DEFAULT
        self.filename = Const.EMPTY
        self.defaults = False
        self.template = False
        self.version = __version__
        self.very_verbose = False
        self.quiet = False
        self.debug = False
        self.profile = False
        self.no_ansi = False
        self.server = False
        self._sfields = {}
        self._rfields = ()
        self._logger = Logger(__name__).get()
        self._repr = None
        self._parameters = {}
        self._set_self()
        self._set_repr()

    def __repr__(self):

        return self._repr

    def _set_self(self):
        """Set instance variables."""

        for parameter in self._parameters:
            setattr(self, parameter, self._parameters[parameter])

    def _set_repr(self):
        """Set object representation."""

        namespace = []
        class_name = type(self).__name__
        for parameter in sorted(self._parameters):
            namespace.append('%s=%r' % (parameter, self._parameters[parameter]))

        self._repr = '%s(%s)' % (class_name, ', '.join(namespace))

    def _set_conf(self, parameters):
        """Set API configuration parameters."""

        self._parameters.update(parameters)
        self.operation = parameters.get('operation')
        self.category = parameters.get('category')
        self._data = parameters.get('data', ())
        self.brief = parameters.get('brief', Const.EMPTY)
        self.group = parameters.get('group', Const.DEFAULT_GROUP)
        self.tags = parameters.get('tags', ())
        self.links = parameters.get('links', ())
        self.digest = parameters.get('digest', None)
        self._sall = parameters.get('sall', ())
        self._stag = parameters.get('stag', ())
        self._sgrp = parameters.get('sgrp', ())
        self.regexp = parameters.get('regexp', Const.EMPTY)
        self.limit = parameters.get('limit', ConfigSourceBase.LIMIT_DEFAULT)
        self.sfields = parameters.get('sort', ('brief'))
        self.rfields = parameters.get('fields', ConfigSourceBase.ALL_FIELDS)
        self.no_ansi = parameters.get('no_ansi', False)
        self.defaults = parameters.get('defaults', False)
        self.template = parameters.get('template', False)
        self.editor = parameters.get('editor', False)
        self.server = parameters.get('server', False)
        self.debug = parameters.get('debug', False)
        self.very_verbose = parameters.get('very_verbose', False)
        self.quiet = parameters.get('quiet', False)
        self.profile = parameters.get('profile', False)

        self._set_self()
        self._set_repr()

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
            string_ = self._to_string(value)
            self._data = tuple(string_.split(Const.DELIMITER_DATA))
        else:
            self._data = ()

    @property
    def tags(self):
        """Get content tags."""

        return self._tags

    @tags.setter
    def tags(self, value):
        """Content tags are stored as a tuple with one tag per element."""

        self._tags = Parser.keywords(self._to_list(value))

    @property
    def links(self):
        """Get content links."""

        return self._links

    @links.setter
    def links(self, value):
        """Content links are stored as a tuple with one link per element."""

        self._links = Parser.links(self._to_list(value))

    @property
    def sall(self):
        """Get 'search all' keywords."""

        return self._sall

    @sall.setter
    def sall(self, value):
        """Search all keywords stored as a tuple with one keywords per
        element."""

        self._sall = self._to_keywords(value)

    @property
    def stag(self):
        """Get 'search tag' keywords."""

        return self._stag

    @stag.setter
    def stag(self, value):
        """Search tag keywords stored as a tuple with one keywords per
        element."""

        self._stag = self._to_keywords(value)

    @property
    def sgrp(self):
        """Get 'search group' keywords."""

        return self._sgrp

    @sgrp.setter
    def sgrp(self, value):
        """Search group keywords stored as a tuple with one keywords per
        element."""

        self._sgrp = self._to_keywords(value)

    @property
    def regexp(self):
        """Get search regexp filter."""

        return self._regexp

    @regexp.setter
    def regexp(self, value):
        """Search regexp filter must be Python regexp."""

        try:
            re.compile(value)
            self._regexp = value
        except re.error:
            self._regexp = Const.EMPTY
            Cause.push(Cause.HTTP_BAD_REQUEST,
                       'listing matching content without filter because it was not syntactically correct regular expression')

    @property
    def limit(self):
        """Get search result limit."""

        return self._limit

    @limit.setter
    def limit(self, value):
        """Search result limit."""

        self._limit = ConfigSourceBase.LIMIT_DEFAULT
        try:
            self._limit = int(value)
        except ValueError:
            self._logger.info('search result limit is not a number and thus default use: %d', self._limit)

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
        field_names = Parser.keywords(self._to_list(value), sort_=False)
        for field in field_names:
            try:
                if field[0].startswith('-'):
                    index_ = ConfigSourceBase.ALL_FIELDS.index(field[1:])
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = True
                else:
                    index_ = ConfigSourceBase.ALL_FIELDS.index(field)
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = False
            except ValueError:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existent field={}'.format(field))
        self._logger.debug('config source internal format for sorted fields: %s', sorted_dict)
        self._sfields = sorted_dict

    @property
    def rfields(self):
        """Get removed fields."""

        return self._rfields

    @rfields.setter
    def rfields(self, value):
        """Removed fields are presented as tuple and they are converted from
        requested fields."""

        requested_fields = Parser.keywords(self._to_list(value))
        self._rfields = tuple(set(ConfigSourceBase.ALL_FIELDS) - set(requested_fields))
        self._logger.debug('config source converted removed fields from requested fields: %s', self._rfields)

    def _to_string(self, value):
        """Return value as string by joining list items with newlines."""

        string_ = Const.EMPTY
        value = ConfigSourceBase._six_string(value)
        if isinstance(value, str):
            string_ = value
        elif isinstance(value, (list, tuple)):
            string_ = Const.NEWLINE.join([x.strip() for x in value])  # Enforce only one newline at the end.
        else:
            self._logger.debug('config source string parameter ignored because of unknown type %s', value)

        return string_

    def _to_list(self, option):
        """Return option as list of items."""

        list_ = []
        option = ConfigSourceBase._six_string(option)
        if isinstance(option, str):
            list_.append(option)
        elif isinstance(option, (list, tuple)):
            list_ = list(option)
        else:
            self._logger.debug('config source list parameter ignored because of unknown type: %s', type(option))

        return list_

    def _to_keywords(self, value):
        """Convert value to list of search keywrods."""

        # The keyword list may be empty or it can contain empty string.
        # Both cases must be evaluated to 'match any'.
        keywords = ()
        if value is not None:
            keywords = Parser.keywords(self._to_list(value))
            if not any(keywords):
                self._logger.debug('all content listed because keywords were not provided')
                keywords = ('.')
        else:
            keywords = ()

        return keywords

    @staticmethod
    def _six_string(parameter):
        """Take care of converting Python 2 unicode string to str."""

        # In Python 2 a string can be str or unicode but in Python 3 strings
        # are always unicode strings. This makes sure that a string is always
        # str for Python 2 and python 3.
        if Const.PYTHON2 and isinstance(parameter, unicode):  # noqa: F821 # pylint: disable=undefined-variable
            parameter = parameter.encode('utf-8')

        return parameter
