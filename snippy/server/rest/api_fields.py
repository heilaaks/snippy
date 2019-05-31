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

"""api_fields: JSON REST API for resource attributes."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.source.api import Api
from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.server.rest.base import ApiResource
from snippy.server.rest.base import ApiNotImplemented
from snippy.server.rest.generate import Generate


class ApiAttributes(object):
    """Access unique resource attributes."""

    def __init__(self, content):
        self._logger = Logger.get_logger(__name__)
        self._category = content.category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response):
        """Search unique resource attributes.

        Search is made from all content categories by default.

        Args:
            request (obj): Falcon Request().
            response (obj): Falcon Response().
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        if 'scat' not in request.params:
            request.params['scat'] = Const.CATEGORIES
        api = Api(self._category, Api.UNIQUE, request.params)
        Config.load(api)
        self._content.run()
        if not self._content.uniques:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find unique fields for %s attribute' % self._category)
        if Cause.is_ok():
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.fields(self._category, self._content.uniques, request, response)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_post(request, response):
        """Create new field."""

        ApiNotImplemented.send(request, response)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_put(request, response):
        """Change field."""

        ApiNotImplemented.send(request, response)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_delete(request, response):
        """Delete field."""

        ApiNotImplemented.send(request, response)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response):
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET,OPTIONS')
