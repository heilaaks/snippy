#!/usr/bin/env python3

"""api.py: Api parameter management."""

from __future__ import print_function
from snippy.version import __version__
from snippy.logger.logger import Logger
from snippy.config.constants import Constants as Const


class Api(object):  # pylint: disable=too-few-public-methods
    """Api parameter management."""

    args = {}
    logger = {}

    CREATE = 'create'
    SEARCH = 'search'
    UPDATE = 'update'
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'
    OPERATIONS = ('create', 'search', 'update', 'delete', 'export', 'import')

    def __init__(self, parameters, operation):
        Api.logger = Logger(__name__).get()

        self.represents = Const.EMPTY
        self.parameters = {'operation': operation,
                           'cat': Const.SNIPPET,
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
                           'limit': 20}

        Api._validate(parameters)
        self._set_conf(parameters)
        self._set_self()
        self._set_repr()

    def __repr__(self):

        return self.represents

    @staticmethod
    def _validate(parameters):
        """Validate API configuration parameters."""

        valid = True
        for key in sorted(parameters):
            if key == 'operation':
                valid = Api._is_valid_operation(parameters[key])

        return valid

    def _set_conf(self, parameters):
        """Set API configuration parameters."""

        self.parameters.update(parameters)

        # Remove suppressed parameters if they are not provided. These are special
        # cases inherit from command line usage where the code logic needs to know
        # if some parameter was provided or not at all.
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

    def _set_self(self):
        """Set self variables dynamically."""

        for parameter in self.parameters:
            setattr(self, parameter, self.parameters[parameter])

    def _set_repr(self):
        """Set object representation."""

        namespace = []
        class_name = type(self).__name__
        for parameter in sorted(self.parameters):
            namespace.append('%s=%r' % (parameter, self.parameters[parameter]))

        self.represents = '%s(%s)' % (class_name, ', '.join(namespace))

    @staticmethod
    def _is_valid_operation(value):
        """Validate operation parameter."""

        is_valid = False
        if any(value in operation for operation in Api.OPERATIONS):
            is_valid = True

        return is_valid
