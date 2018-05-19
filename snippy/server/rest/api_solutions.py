#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""api_solutions: JSON REST API for Solutions."""

from __future__ import print_function

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.api import Api
from snippy.content.solution import Solution
from snippy.logger import Logger
from snippy.server.rest.base import ContentApiBase
from snippy.server.rest.jsonapiv1 import JsonApiV1
from snippy.server.rest.validate import Validate


class ApiSolutions(ContentApiBase):
    """Process solution collections"""


class ApiSolutionsDigest(object):
    """Process solutions based on digest resource ID."""

    def __init__(self, storage):
        self._logger = Logger.get_logger(__name__)
        self.storage = storage

    @Logger.timeit
    def on_put(self, request, response, digest):
        """Update whole solution based on digest."""

        self._logger.debug('run put %ssolutions/%s', Config.base_path_app, digest)
        resource_ = Validate.resource(request, digest)
        if resource_:
            api = Api(Const.SOLUTION, Api.UPDATE, resource_)
            Config.load(api)
            contents = Solution(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SOLUTION, contents, request, digest)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end put %ssolutions/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_patch(self, request, response, digest):
        """Update partial solution based on digest."""

        self._logger.debug('run patch %ssolutions/%s', Config.base_path_app, digest)
        self.on_put(request, response, digest)
        Cause.reset()
        self._logger.debug('end patch %ssolutions/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_get(self, request, response, digest):
        """Search solutions based on digest."""

        self._logger.debug('run get %ssolutions/%s', Config.base_path_app, digest)
        local_params = {'digest': digest}
        api = Api(Const.SOLUTION, Api.SEARCH, local_params)
        Config.load(api)
        contents = Solution(self.storage, Const.CONTENT_TYPE_JSON).run()
        if not contents['data']:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SOLUTION, contents, request, digest, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %ssolutions/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_delete(self, _, response, digest):
        """Delete solution based on digest."""

        self._logger.debug('run delete %ssolutions/%s', Config.base_path_app, digest)
        local_params = {'digest': digest}
        api = Api(Const.SOLUTION, Api.DELETE, local_params)
        Config.load(api)
        Solution(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete %ssolutions/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_post(self, request, response, digest):
        """Update solution."""

        self._logger.debug('run post %ssolutions/%s', Config.base_path_app, digest)
        if request.get_header('x-http-method-override', default='post').lower() == 'put':
            self.on_put(request, response, digest)
        elif request.get_header('x-http-method-override', default='post').lower() == 'patch':
            self.on_patch(request, response, digest)
        elif request.get_header('x-http-method-override', default='post').lower() == 'delete':
            self.on_delete(request, response, digest)
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot create resource with id, use x-http-method-override to override the request')
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end post %ssolutions/%s', Config.base_path_app, digest)


class ApiSolutionsField(object):  # pylint: disable=too-few-public-methods
    """Process solution based on digest resource ID and specified field."""

    def __init__(self, storage):
        self._logger = Logger.get_logger(__name__)
        self.storage = storage

    @Logger.timeit
    def on_get(self, request, response, digest, field):
        """Get defined solution field based on digest."""

        self._logger.debug('run get %ssolutions/%s/field', Config.base_path_app, digest, field)
        local_params = {'digest': digest, 'fields': field}
        api = Api(Const.SOLUTION, Api.SEARCH, local_params)
        Config.load(api)
        contents = Solution(self.storage, Const.CONTENT_TYPE_JSON).run()
        if not contents['data']:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SOLUTION, contents, request, digest, field=field, pagination=False)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %ssolutions/%s/field', Config.base_path_app, digest, field)
