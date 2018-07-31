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

"""api_fields: JSON REST API for content fields."""

from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.base import ApiContentDigestBase
from snippy.server.rest.base import ApiContentDigestFieldBase


class ApiKeywords(ApiContentBase):
    """Process content based on given keyword list."""

    def __init__(self, fields):
        super(ApiKeywords, self).__init__(fields, Const.ALL_CATEGORIES)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, sall=None, stag=None, sgrp=None, uuid=None, digest=None):
        """Search content based on given keyword list."""

        self._logger.debug('run get: %s', request.uri)
        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiKeywords, self).on_get(request, response, sall=sall)


class ApiGroups(ApiContentBase):
    """Process content based on group field."""

    def __init__(self, fields):
        super(ApiGroups, self).__init__(fields, Const.ALL_CATEGORIES)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, sall=None, stag=None, sgrp=None, uuid=None, digest=None):
        """Search content based on group field."""

        self._logger.debug('run get: %s', request.uri)
        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiGroups, self).on_get(request, response, sgrp=sgrp)


class ApiTags(ApiContentBase):
    """Process content based on tags field."""

    def __init__(self, fields):
        super(ApiTags, self).__init__(fields, Const.ALL_CATEGORIES)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, sall=None, stag=None, sgrp=None, uuid=None, digest=None):
        """Search content based on tags field."""

        self._logger.debug('run get: %s', request.uri)
        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiTags, self).on_get(request, response, stag=stag)


class ApiDigest(ApiContentDigestBase):
    """Process content based on unique digest."""

    def __init__(self, fields):
        super(ApiDigest, self).__init__(fields, Const.ALL_CATEGORIES)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, digest):
        """Search content based on digest."""

        self._logger.debug('run get: %s', request.uri)
        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiDigest, self).on_get(request, response, digest)


class ApiDigestField(ApiContentDigestFieldBase):
    """Process content field based on unique digest or uuid and specified field."""

    def __init__(self, fields):
        super(ApiDigestField, self).__init__(fields, Const.ALL_CATEGORIES)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, digest, field):
        """Search content based on uuid."""

        self._logger.debug('run get: %s', request.uri)
        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiDigestField, self).on_get(request, response, digest, field)
