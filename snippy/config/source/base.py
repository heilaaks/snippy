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
    FIELDS = ('data', 'brief', 'group', 'tags', 'links', 'category', 'filename',
              'runalias', 'versions', 'utc', 'digest', 'key')

    # Defaults
    LIMIT_DEFAULT = 20

    def __init__(self):
        self.operation = Const.EMPTY
        self.category = Const.UNKNOWN_CONTENT
        self.editor = None
        self._data = ()
        self.brief = Const.EMPTY,
        self.group = Const.DEFAULT_GROUP
        self._tags = ()
        self._links = ()
        self.digest = Const.EMPTY
        self._sall = None
        self._stag = None
        self._sgrp = None
        self.regexp = None
        self.filename = Const.EMPTY
        self.defaults = None
        self.template = None
        self.help = None
        self.version = None
        self.very_verbose = None
        self.quiet = None
        self.debug = None
        self.profile = None
        self.no_ansi = None
        self.server = None
        self.limit = None
        self.sort = None
        self.fields = None
        self._logger = Logger(__name__).get()
        self._repr = None
        self._parameters = {'editor': False,
                            'regexp': Const.EMPTY,
                            'defaults': False,
                            'template': False,
                            'help': False,
                            'version': __version__,
                            'very_verbose': False,
                            'quiet': False,
                            'debug': False,
                            'profile': False,
                            'no_ansi': False,
                            'server': False,
                            'limit': ConfigSourceBase.LIMIT_DEFAULT,
                            'sort': ConfigSourceBase.BRIEF,
                            'fields': ConfigSourceBase.FIELDS}
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
        self._tags = parameters.get('tags', ())
        self._links = parameters.get('links', ())
        self.digest = parameters.get('digest', None)
        self._sall = parameters.get('sall', ())
        self._stag = parameters.get('stag', ())
        self._sgrp = parameters.get('sgrp', ())

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

    def get_search_filter(self):
        """Return regexp filter for search output."""

        self._logger.debug('config source filter: %s', self.regexp)

        return self.regexp

    def is_editor(self):
        """Test usage of editor for the operation."""

        return self.editor

    def is_no_ansi(self):
        """Return usage of ANSI characters like color codes in terminal output."""

        self._logger.debug('config source no-ansi: %s', self.no_ansi)

        return self.no_ansi

    def is_defaults(self):
        """Return the usage of defaults in migration operation."""

        self._logger.debug('config source defaults: %s', self.defaults)

        return self.defaults

    def is_template(self):
        """Return the usage of template in migration operation."""

        self._logger.debug('config source template: %s', self.template)

        return self.template

    def is_debug(self):
        """Return the usage of debug option."""

        self._logger.debug('config source debug: %s', self.debug)

        return self.debug

    def is_server(self):
        """Test if the service is run as a server."""

        self._logger.debug('config source server: %s', self.server)

        return self.server

    def get_search_limit(self):
        """Return content count limit."""

        limit = ConfigSourceBase.LIMIT_DEFAULT
        try:
            limit = int(self.limit)
        except ValueError:
            self._logger.info('search result limit is not a number and thus default use: %d', limit)

        self._logger.debug('config source limit: %s', limit)

        return limit

    def get_sorted_fields(self):
        """Return fields that are used to sort content."""

        sorted_dict = {}
        field_names = []
        fields = ConfigSourceBase._six_string(self.sort)
        if isinstance(fields, str):
            field_names.append(fields)
            field_names = Parser.keywords(field_names, sort_=False)
        elif isinstance(fields, (list, tuple)):
            field_names.extend(fields)
        else:
            self._logger.debug('search result sorting parameter ignored because of unknown type')
        self._logger.debug('config source sorted fields: %s', field_names)

        # Convert the field names to internal field index that match
        # to database column index.
        sorted_dict['order'] = []
        sorted_dict['value'] = {}
        for field in field_names:
            try:
                if field[0].startswith('-'):
                    index_ = ConfigSourceBase.FIELDS.index(field[1:])
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = True
                else:
                    index_ = ConfigSourceBase.FIELDS.index(field)
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = False
            except ValueError:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existent field={}'.format(field))
        self._logger.debug('config source internal format for sorted fields: %s', sorted_dict)

        return sorted_dict

    def get_removed_fields(self):
        """Return content fields that not used in the search result."""

        requested_fields = ConfigSourceBase.FIELDS
        fields = ConfigSourceBase._six_string(self.fields)
        if isinstance(fields, str):
            requested_fields = (fields,)
            requested_fields = Parser.keywords(requested_fields)
        elif isinstance(fields, (list, tuple)):
            requested_fields = tuple(fields)
        else:
            self._logger.debug('search result selected fields parameter ignored because of unknown type')
        self._logger.debug('config source used fields in search result: %s', requested_fields)

        removed_fields = tuple(set(ConfigSourceBase.FIELDS) - set(requested_fields))
        self._logger.debug('config source removed fields from search response: %s', removed_fields)

        return removed_fields

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
