#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""api_fields: JSON REST API for content attributes."""

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.server.rest.base import ApiResource
from snippy.server.rest.base import ApiNotImplemented


class ApiGroups(ApiResource):
    """Access content ``groups`` attributes."""

    def __init__(self, fields):
        super(ApiGroups, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, sall=None, stag=None, sgrp=None):
        """Search content based on groups field."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiGroups, self).on_get(request, response, sgrp=sgrp)

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response, **kwargs):
        """Create new field."""

        ApiNotImplemented.send(request, response)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response, **kwargs):
        """Delete field."""

        ApiNotImplemented.send(request, response)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, sall=None, stag=None, sgrp=None):
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET,OPTIONS')


class ApiTags(ApiResource):
    """Access content ``tags`` attributes."""

    def __init__(self, fields):
        super(ApiTags, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, sall=None, stag=None, sgrp=None):
        """Search content based on tags field."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiTags, self).on_get(request, response, stag=stag)

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response, **kwargs):
        """Create new field."""

        ApiNotImplemented.send(request, response)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response, **kwargs):
        """Delete field."""

        ApiNotImplemented.send(request, response)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, sall=None, stag=None, sgrp=None):
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET,OPTIONS')
