#!/usr/bin/env python3

"""api.py: Api parameter management."""

from __future__ import print_function
from snippy.config.constants import Constants as Const
from snippy.config.source.base import ConfigSourceBase


class Api(ConfigSourceBase):
    """Api parameter management."""

    def __init__(self, parameters, operation):
        super(Api, self).__init__()
        self.parameters['operation'] = operation
        self.parameters['cat'] = Const.SNIPPET

        Api._validate(parameters)
        self._set_conf(parameters)
        self._set_self()

    @staticmethod
    def _validate(parameters):
        """Validate API configuration parameters."""

        valid = True
        for key in sorted(parameters):
            if key == 'operation':
                valid = Api._is_valid_operation(parameters[key])

        return valid

    @staticmethod
    def _is_valid_operation(value):
        """Validate operation parameter."""

        is_valid = False
        if any(value in operation for operation in Api.OPERATIONS):
            is_valid = True

        return is_valid
