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
from snippy.config.config import Config
from snippy.config.source.api import Api
from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.generate import Generate
from snippy.server.rest.validate import Validate


class ApiGroups(ApiContentBase):
    """Process content based on group field."""

    def __init__(self, fields):
        self._logger = Logger.get_logger(__name__)
        self._category = Const.ALL_CATEGORIES
        self._content = fields

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, sgrp):
        """Search content based on group field."""

        self._logger.debug('run get: %s', request.uri)
        print(request.params)
        request.params['sgrp'] = sgrp
        #self.on_get(request, response)
        super(ApiGroups, self).on_get(request, response)
        #api = Api(None, Api.SEARCH, request.params)
        #Config.load(api)
        #self._fields.run(self._fields.GROUP)
        #if self._fields.collection.empty() and Config.search_limit != 0:
        #    Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resources')
        #if Cause.is_ok():
        #    response.content_type = ApiContentBase.MEDIA_JSON_API
        #    response.body = Generate.collection(self._fields.collection, request, pagination=True)
        #    response.status = Cause.http_status()
        #else:
        #    response.content_type = ApiContentBase.MEDIA_JSON_API
        #    response.body = Generate.error(Cause.json_message())
        #    response.status = Cause.http_status()
        #
        #Cause.reset()
        #self._logger.debug('end get: %s', request.uri)


class ApiId(object):
    """Process content based on unique digest or uuid."""

    def __init__(self, fields):
        self._logger = Logger.get_logger(__name__)
        self._fields = fields

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, field, value):
        """Search content based on digest."""

        self._logger.debug('run get: %s', request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, digest, field):  # pylint: disable=unused-argument
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')


class ApiIdField(object):
    """Process content field based on unique digest or uuid."""

    def __init__(self, fields):
        self._logger = Logger.get_logger(__name__)
        self._fields = fields

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, field, value):
        """Search content based on uuid."""

        self._logger.debug('run get: %s', request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, digest, field):  # pylint: disable=unused-argument
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')


class ApiKeywords(object):
    """Process content based on given keyword list."""

    def __init__(self, fields):
        self._logger = Logger.get_logger(__name__)
        self._fields = fields

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, field, value):
        """Search content based on given keyword list."""

        self._logger.debug('run get: %s', request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, digest, field):  # pylint: disable=unused-argument
        """Respond with allowed methods."""

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET')
