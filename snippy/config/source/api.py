#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""api: API based content management."""

from __future__ import print_function
from snippy.config.source.base import ConfigSourceBase


class Api(ConfigSourceBase):
    """API parameter management."""

    def __init__(self, category, operation, parameters):
        super(Api, self).__init__()
        params = dict(parameters)
        params['category'] = category
        params['operation'] = operation
        params['editor'] = False  # Never use text editor with API server.

        Api._validate(params)
        self._set_sall(params)
        self.set_conf(params)

    @staticmethod
    def _set_sall(parameters):
        """Set 'match any' if search is made without any search criteria."""

        if parameters['operation'] == Api.SEARCH:
            if not any(field in parameters for field in ('sall', 'stag', 'sgrp', 'data', 'uuid', 'digest')):
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
