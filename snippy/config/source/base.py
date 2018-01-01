#!/usr/bin/env python3

"""base.py: Base class for configuration sources."""

from snippy.metadata import __version__
from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
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

    # Columns
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
        # Parameters are assigned dynamically from self._parameters.
        self.operation = None
        self.cat = None
        self.editor = None
        self.data = None
        self.brief = None
        self.group = None
        self.tags = None
        self.links = None
        self.digest = None
        self.sall = None
        self.stag = None
        self.sgrp = None
        self.regexp = None
        self.filename = None
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
        self._represents = Const.EMPTY
        self._parameters = {'operation': Const.EMPTY,
                            'cat': Const.UNKNOWN_CONTENT,
                            'editor': False,
                            'data': Const.EMPTY,
                            'brief': Const.EMPTY,
                            'group': Const.DEFAULT_GROUP,
                            'tags': [],
                            'links': [],
                            'digest': Const.EMPTY,
                            'sall': [],
                            'stag': [],
                            'sgrp': [],
                            'regexp': Const.EMPTY,
                            'filename': Const.EMPTY,
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

    def _set_conf(self, parameters):
        """Set API configuration parameters."""

        self._parameters.update(parameters)

        # These are special cases where the code logic needs to know
        # if some parameter was provided at all.
        if 'data' not in parameters:
            self._parameters.pop('data')
        if 'digest' not in parameters:
            self._parameters.pop('digest')
        if 'sall' not in parameters:
            self._parameters.pop('sall')
        if 'stag' not in parameters:
            self._parameters.pop('stag')
        if 'sgrp' not in parameters:
            self._parameters.pop('sgrp')
        self._set_repr()

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

        self._represents = '%s(%s)' % (class_name, ', '.join(namespace))

    def get_operation(self):
        """Return the requested operation for the content."""

        self._logger.debug('config source operation: %s', self.operation)

        return self.operation

    def get_content_category(self):
        """Return content category."""

        self._logger.debug('config source category: %s', self.cat)

        return self.cat

    def is_content_data(self):
        """Test if content data option was used."""

        return True if 'data' in self._parameters else False

    def get_content_data(self):
        """Return content data."""

        data = None
        if self.is_content_data():
            data = self._to_string(self.data)
            self._logger.debug('config source data: %s', data)
        else:
            self._logger.debug('config source data was not used')

        return data

    def get_content_brief(self):
        """Return content brief description."""

        self._logger.debug('config source brief: %s', self.brief)

        return self.brief

    def get_content_group(self):
        """Return content group."""

        self._logger.debug('config source group: %s', self.group)

        return self.group

    def get_content_tags(self):
        """Return content tags."""

        tags = self._to_list(self.tags)
        self._logger.debug('config source tags: %s', tags)

        return tags

    def get_content_links(self):
        """Return content links."""

        links = self._to_list(self.links)
        self._logger.debug('config source links: %s', links)

        return links

    def is_content_digest(self):
        """Test if content digest option was used."""

        return True if 'digest' in self._parameters else False

    def get_content_digest(self):
        """Return digest identifying the content."""

        digest = None
        if self.is_content_digest():
            digest = self.digest
            self._logger.debug('config source digest: %s', self.digest)
        else:
            self._logger.debug('config source digest was not used')

        return digest

    def is_search_all(self):
        """Test if search all option was used."""

        return True if 'sall' in self._parameters else False

    def get_search_all(self):
        """Return keywords to search from all fields."""

        sall = None
        if self.is_search_all():
            sall = self._to_list(self.sall)
            self._logger.debug('config source sall: %s', sall)
        else:
            self._logger.debug('config source sall was not used')

        return sall

    def is_search_tag(self):
        """Test if search tag option was used."""

        return True if 'stag' in self._parameters else False

    def get_search_tag(self):
        """Return keywords to search only from tags."""

        stag = None
        if self.is_search_tag():
            stag = self._to_list(self.stag)
            self._logger.debug('config source stag: %s', stag)
        else:
            self._logger.debug('config source stag was not used')

        return stag

    def is_search_grp(self):
        """Test if search grp option was used."""

        return True if 'sgrp' in self._parameters else False

    def get_search_grp(self):
        """Return keywords to search only from groups."""

        sgrp = None
        if self.is_search_grp():
            sgrp = self._to_list(self.sgrp)
            self._logger.debug('config source sgrp: %s', sgrp)
        else:
            self._logger.debug('config source sgrp was not used')

        return sgrp

    def get_search_filter(self):
        """Return regexp filter for search output."""

        self._logger.debug('config source filter: %s', self.regexp)

        return self.regexp

    def is_editor(self):
        """Test usage of editor for the operation."""

        return self.editor

    def get_operation_file(self):
        """Return file for operation."""

        self._logger.debug('config source filename: %s', self.filename)

        return self.filename

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
        column_names = []
        try:
            if isinstance(self.sort, str):
                column_names.append(self.sort)
            elif isinstance(self.sort, (list, tuple)):
                column_names.extend(self.sort)
            else:
                self._logger.debug('search result sorting parameter ignored because of unknown type')
        except ValueError:
            self._logger.info('search result sort validation failed and thus no sorting is applied')
        self._logger.debug('config source sorted fields: %s', column_names)

        # Convert the column names to internal column index.
        sorted_dict['order'] = []
        sorted_dict['value'] = {}
        for column in column_names:
            try:
                if column[0].startswith('-'):
                    column_index = ConfigSourceBase.FIELDS.index(column[1:])
                    sorted_dict['order'].append(column_index)
                    sorted_dict['value'][column_index] = True
                else:
                    column_index = ConfigSourceBase.FIELDS.index(column)
                    sorted_dict['order'].append(column_index)
                    sorted_dict['value'][column_index] = False
            except ValueError:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existing field={}'.format(column))
        self._logger.debug('config source internal format for sorted fields: %s', sorted_dict)

        return sorted_dict

    def get_removed_fields(self):
        """Return content fields that not used in the search result."""

        requested_fields = ConfigSourceBase.FIELDS
        try:
            if isinstance(self.fields, str):
                requested_fields = (self.fields,)
            elif isinstance(self.fields, (list, tuple)):
                requested_fields = tuple(self.fields)
            else:
                self._logger.debug('search result selected fields parameter ignored because of unknown type')
        except ValueError:
            self._logger.info('search result selected fields parameter validation failed and thus all fields are used')
        self._logger.debug('config source used fields in search result: %s', requested_fields)

        removed_fields = tuple(set(ConfigSourceBase.FIELDS) - set(requested_fields))
        self._logger.debug('config source removed fields from search response: %s', removed_fields)

        return removed_fields

    def _to_list(self, option):
        """Return option as list of items."""

        item_list = []
        try:
            # In Python 2 a string can be str or unicode but in Python 3 strings
            # are always unicode strings.
            if Const.PYTHON2 and isinstance(option, unicode):  # noqa: F821 # pylint: disable=undefined-variable
                option = option.encode('utf-8')
            if isinstance(option, str):
                item_list.append(option)
            elif isinstance(option, (list, tuple)):
                item_list = list(option)
            else:
                self._logger.debug('config source list parameter ignored because of unknown type %s', option)
        except ValueError:
            self._logger.info('config source list parameter validation failed and option ignored %s', option)

        return item_list

    def _to_string(self, option):
        """Return option as string by joining list items with newlines."""

        item_string = Const.EMPTY
        try:
            # In Python 2 a string can be str or unicode but in Python 3 strings
            # are always unicode strings.
            if Const.PYTHON2 and isinstance(option, unicode):  # noqa: F821 # pylint: disable=undefined-variable
                item_string = option.encode('utf-8')
            if isinstance(option, str):
                item_string = option
            elif isinstance(option, (list, tuple)):
                item_string = Const.NEWLINE.join([x.strip() for x in option])  # Enforce only one newline at the end.
            else:
                self._logger.debug('config source string parameter ignored because of unknown type %s', option)
        except ValueError:
            self._logger.info('config source string parameter validation failed and option ignored %s', option)

        return item_string
