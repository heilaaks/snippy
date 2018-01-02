#!/usr/bin/env python3

"""api.py: API parameter management."""

from __future__ import print_function
from snippy.config.source.base import ConfigSourceBase


class Api(ConfigSourceBase):
    """API parameter management."""

    def __init__(self, category, operation, parameters):
        super(Api, self).__init__()
        parameters['cat'] = category
        parameters['operation'] = operation

        Api._validate(parameters)
        self._set_sall(parameters)
        self._set_conf(parameters)

    @staticmethod
    def _set_sall(parameters):
        """Set 'match any' if search is made without any search criterias."""

        if parameters['operation'] == Api.SEARCH:
            if 'sall' not in parameters and \
               'stag' not in parameters and \
               'sgrp' not in parameters and \
               'data' not in parameters and \
               'digest' not in parameters:
                parameters['sall'] = ('.')

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

    def is_editor(self):
        """Api configuration source never uses text editor."""

        return False
