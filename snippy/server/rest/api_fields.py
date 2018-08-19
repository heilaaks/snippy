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

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.base import ApiContentDigestBase
from snippy.server.rest.base import ApiContentDigestFieldBase
from snippy.server.rest.base import ApiContentUuidBase
from snippy.server.rest.base import ApiContentUuidFieldBase


class ApiKeywords(ApiContentBase):
    """Process content based on given keyword list."""

    def __init__(self, fields):
        super(ApiKeywords, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, sall=None, stag=None, sgrp=None):
        """Search content based on given keyword list."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiKeywords, self).on_get(request, response, sall=sall)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, sall=None, stag=None, sgrp=None):
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')


class ApiGroups(ApiContentBase):
    """Process content based on groups field."""

    def __init__(self, fields):
        super(ApiGroups, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, sall=None, stag=None, sgrp=None):
        """Search content based on groups field."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiGroups, self).on_get(request, response, sgrp=sgrp)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, sall=None, stag=None, sgrp=None):
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')


class ApiTags(ApiContentBase):
    """Process content based on tags field."""

    def __init__(self, fields):
        super(ApiTags, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, sall=None, stag=None, sgrp=None):
        """Search content based on tags field."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiTags, self).on_get(request, response, stag=stag)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, sall=None, stag=None, sgrp=None):
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')


class ApiDigest(ApiContentDigestBase):
    """Process content based on unique digest."""

    def __init__(self, fields):
        super(ApiDigest, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, digest):
        """Search content based on digest."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiDigest, self).on_get(request, response, digest)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, digest):  # pylint: disable=unused-argument
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')


class ApiDigestField(ApiContentDigestFieldBase):
    """Process content field based on unique digest and specified field."""

    def __init__(self, fields):
        super(ApiDigestField, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, digest, field):
        """Search content based on uuid."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiDigestField, self).on_get(request, response, digest, field)


class ApiUuid(ApiContentUuidBase):
    """Process content based on unique uuid."""

    def __init__(self, fields):
        super(ApiUuid, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, uuid):
        """Search content based on digest."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiUuid, self).on_get(request, response, uuid)


class ApiUuidField(ApiContentUuidFieldBase):
    """Process content field based on unique uuid and specified field."""

    def __init__(self, fields):
        super(ApiUuidField, self).__init__(fields, Const.ALL_CATEGORIES)

    def on_get(self, request, response, uuid, field):
        """Search content based on uuid."""

        if 'scat' not in request.params:
            request.params['scat'] = [Const.SNIPPET, Const.SOLUTION, Const.REFERENCE]
        super(ApiUuidField, self).on_get(request, response, uuid, field)
