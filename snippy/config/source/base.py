#!/usr/bin/env python3

"""base.py: Base class for configuration sources."""

from snippy.metadata import __version__
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause


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
    COLUMNS = ('data', 'brief', 'group', 'tags', 'links', 'category', 'filename',
               'runalias', 'versions', 'utc', 'digest', 'key')

    # Defaults
    LIMIT_DEFAULT = 20

    def __init__(self):
        # Parameters are assigned dynamically from self.parameters.
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
        self.logger = Logger(__name__).get()
        self.represents = Const.EMPTY
        self.parameters = {'operation': Const.EMPTY,
                           'cat': Const.UNKNOWN_CONTENT,
                           'editor': False,
                           'data': Const.EMPTY,
                           'brief': Const.EMPTY,
                           'group': Const.DEFAULT_GROUP,
                           'tags': [],
                           'links': Const.EMPTY,
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
                           'fields': ConfigSourceBase.COLUMNS}
        self._set_self()
        self._set_repr()

    def _set_conf(self, parameters):
        """Set API configuration parameters."""

        self.parameters.update(parameters)

        # These are special cases where the code logic needs to know
        # if some parameter was provided at all.
        if 'data' not in parameters:
            self.parameters.pop('data')
        if 'digest' not in parameters:
            self.parameters.pop('digest')
        if 'sall' not in parameters:
            self.parameters.pop('sall')
        if 'stag' not in parameters:
            self.parameters.pop('stag')
        if 'sgrp' not in parameters:
            self.parameters.pop('sgrp')
        self._set_repr()

    def _set_self(self):
        """Set instance variables."""

        for parameter in self.parameters:
            setattr(self, parameter, self.parameters[parameter])

    def _set_repr(self):
        """Set object representation."""

        namespace = []
        class_name = type(self).__name__
        for parameter in sorted(self.parameters):
            namespace.append('%s=%r' % (parameter, self.parameters[parameter]))

        self.represents = '%s(%s)' % (class_name, ', '.join(namespace))

    def get_operation(self):
        """Return the requested operation for the content."""

        self.logger.info('parsed positional argument with value "%s"', self.operation)

        return self.operation

    def get_content_category(self):
        """Return content category."""

        self.logger.info('parsed content category with value "%s"', self.cat)

        return self.cat

    def is_content_data(self):
        """Test if content data option was used."""

        return True if 'data' in self.parameters else False

    def get_content_data(self):
        """Return content data."""

        data = None
        if self.is_content_data():
            data = self.data
            self.logger.info('parsed argument --content with value %s', self.data)
        else:
            self.logger.info('argument --content was not used')

        return data

    def get_content_brief(self):
        """Return content brief description."""

        self.logger.info('parsed argument --brief with value "%s"', self.brief)

        return self.brief

    def get_content_group(self):
        """Return content group."""

        self.logger.info('parsed argument --group with value "%s"', self.group)

        return self.group

    def get_content_tags(self):
        """Return content tags."""

        tags = self._to_list(self.tags)
        self.logger.debug('parsed content tags "%s"', tags)

        return tags

    def get_content_links(self):
        """Return content links."""

        links = self._to_list(self.links)
        self.logger.debug('parsed content links "%s"', links)

        return links

    def is_content_digest(self):
        """Test if content digest option was used."""

        return True if 'digest' in self.parameters else False

    def get_content_digest(self):
        """Return digest identifying the content."""

        digest = None
        if self.is_content_digest():
            digest = self.digest
            self.logger.info('parsed argument --digest with value %s', self.digest)
        else:
            self.logger.info('argument --digest was not used')

        return digest

    def is_search_all(self):
        """Test if search all option was used."""

        return True if 'sall' in self.parameters else False

    def get_search_all(self):
        """Return keywords to search from all fields."""

        sall = None
        if self.is_search_all():
            sall = self._to_list(self.sall)
            self.logger.info('parsed argument --sall with value %s', sall)
        else:
            self.logger.info('argument --sall was not used')

        return sall

    def is_search_tag(self):
        """Test if search tag option was used."""

        return True if 'stag' in self.parameters else False

    def get_search_tag(self):
        """Return keywords to search only from tags."""

        stag = None
        if self.is_search_tag():
            stag = self._to_list(self.stag)
            self.logger.info('parsed argument --stag with value %s', stag)
        else:
            self.logger.info('argument --stag was not used')

        return stag

    def is_search_grp(self):
        """Test if search grp option was used."""

        return True if 'sgrp' in self.parameters else False

    def get_search_grp(self):
        """Return keywords to search only from groups."""

        sgrp = None
        if self.is_search_grp():
            sgrp = self._to_list(self.sgrp)
            self.logger.info('parsed argument --sgrp with value %s', sgrp)
        else:
            self.logger.info('argument --sgrp was not used')

        return sgrp

    def get_search_filter(self):
        """Return regexp filter for search output."""

        self.logger.info('parsed argument --filter with value %s', self.regexp)

        return self.regexp

    def is_editor(self):
        """Test usage of editor for the operation."""

        return self.editor

    def get_operation_file(self):
        """Return file for operation."""

        self.logger.info('parsed argument --file with value "%s"', self.filename)

        return self.filename

    def is_no_ansi(self):
        """Return usage of ANSI characters like color codes in terminal output."""

        self.logger.info('parsed argument --no-ansi with value "%s"', self.no_ansi)

        return self.no_ansi

    def is_defaults(self):
        """Return the usage of defaults in migration operation."""

        self.logger.info('parsed argument --defaults with value %s', self.defaults)

        return self.defaults

    def is_template(self):
        """Return the usage of template in migration operation."""

        self.logger.info('parsed argument --template with value %s', self.template)

        return self.template

    def is_debug(self):
        """Return the usage of debug option."""

        self.logger.info('parsed argument --debug with value %s', self.debug)

        return self.debug

    def is_server(self):
        """Test if the service is run as a server."""

        self.logger.info('parsed argument --server with value "%s"', self.server)

        return self.server

    def get_search_limit(self):
        """Return content count limit."""

        limit = ConfigSourceBase.LIMIT_DEFAULT
        try:
            limit = int(self.limit)
        except ValueError:
            self.logger.debug('search limit is not a number and thus the limit is set to default %d', limit)

        self.logger.info('parsed content limit option with value "%s"', limit)

        return limit

    def get_search_sorted_columns(self):
        """Return content sort options."""

        sorted_dict = {}
        column_names = []
        try:
            if isinstance(self.sort, str):
                column_names.append(self.sort)
            elif isinstance(self.sort, (list, tuple)):
                column_names.extend(self.sort)
            else:
                self.logger.info('search sorting attributes ignored because of unknown type')
        except ValueError:
            self.logger.info('search sort option validation failed and thus no sorting is applied')
        self.logger.debug('parsed content sort option with value "%s"', column_names)

        # Convert the column names to internal column index.
        sorted_dict['order'] = []
        sorted_dict['value'] = {}
        for column in column_names:
            try:
                if column[0].startswith('-'):
                    column_index = ConfigSourceBase.COLUMNS.index(column[1:])
                    sorted_dict['order'].append(column_index)
                    sorted_dict['value'][column_index] = True
                else:
                    column_index = ConfigSourceBase.COLUMNS.index(column)
                    sorted_dict['order'].append(column_index)
                    sorted_dict['value'][column_index] = False
            except ValueError:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existing field={}'.format(column))
        self.logger.debug('converted sort parameters to internal format "%s"', sorted_dict)

        return sorted_dict

    def get_search_removed_columns(self):
        """Return columns that used in search result."""

        used_columns = ConfigSourceBase.COLUMNS
        try:
            if isinstance(self.fields, str):
                used_columns = (self.fields,)
            elif isinstance(self.fields, (list, tuple)):
                used_columns = tuple(self.fields)
            else:
                self.logger.info('search result column list attributes ignored because of unknown type')
        except ValueError:
            self.logger.info('search result column list option validation failed and thus all columns are used')
        self.logger.debug('parsed search result column list option with value "%s"', used_columns)

        # To optimize internal logic, list columns that are moved. Column 'key'
        # is never added to content.
        removed_columns = list(set(ConfigSourceBase.COLUMNS) - set(used_columns))
        try:
            removed_columns.remove(ConfigSourceBase.KEY)
        except ValueError:
            pass

        return tuple(removed_columns)

    def _to_list(self, option):
        """Return option as a list if items."""

        item_list = []
        try:
            # In Python2 a string can be str or unicode but in Python3 strings
            # are always unicode strings.
            if Const.PYTHON2 and isinstance(option, unicode):  # noqa: F821 # pylint: disable=undefined-variable
                option = option.encode('utf-8')
            if isinstance(option, str):
                item_list.append(option)
            elif isinstance(option, (list, tuple)):
                item_list = list(option)
            else:
                self.logger.info('content ignored because of unknown type %s', option)
        except ValueError:
            self.logger.info('content validation failed and option ignored %s', option)

        return item_list
