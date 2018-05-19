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

"""api_snippets: JSON REST API for Snippets."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.api import Api
from snippy.content.snippet import Snippet
from snippy.logger import Logger
from snippy.server.rest.base import ContentApiBase
from snippy.server.rest.jsonapiv1 import JsonApiV1
from snippy.server.rest.validate import Validate


class ApiSnippets(ContentApiBase):
    """Process snippet collections."""


class ApiSnippetsDigest(object):
    """Process snippet based on digest resource ID."""

    def __init__(self, storage):
        self._logger = Logger.get_logger(__name__)
        self.storage = storage

    @Logger.timeit
    def on_put(self, request, response, digest):
        """Update whole snippet based on digest."""

        self._logger.debug('run put %ssnippets/%s', Config.base_path_app, digest)
        resource_ = Validate.resource(request, digest)
        if resource_:
            api = Api(Const.SNIPPET, Api.UPDATE, resource_)
            Config.load(api)
            contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SNIPPET, contents, request, digest)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end put %ssnippets/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_patch(self, request, response, digest):
        """Update partial snippet based on digest."""

        self._logger.debug('run patch %ssnippets/%s', Config.base_path_app, digest)
        self.on_put(request, response, digest)
        Cause.reset()
        self._logger.debug('end patch %ssnippets/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_get(self, request, response, digest):
        """Search snippet based on digest."""

        self._logger.debug('run get %ssnippets/%s', Config.base_path_app, digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.SEARCH, local_params)
        Config.load(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if not contents['data']:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SNIPPET, contents, request, digest, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %ssnippets/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_delete(self, _, response, digest):
        """Delete snippet based on digest."""

        self._logger.debug('run delete %ssnippets/%s', Config.base_path_app, digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.DELETE, local_params)
        Config.load(api)
        Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete %ssnippets/%s', Config.base_path_app, digest)

    @Logger.timeit
    def on_post(self, request, response, digest):
        """Update snippet."""

        self._logger.debug('run post %ssnippets/%s', Config.base_path_app, digest)
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
        self._logger.debug('end post %ssnippets/%s', Config.base_path_app, digest)


class ApiSnippetsField(object):  # pylint: disable=too-few-public-methods
    """Process snippet based on digest resource ID and specified field."""

    def __init__(self, storage):
        self._logger = Logger.get_logger(__name__)
        self.storage = storage

    @Logger.timeit
    def on_get(self, request, response, digest, field):
        """Get defined snippet field based on digest."""

        self._logger.debug('run get %ssnippets/%s/field', Config.base_path_app, digest, field)
        local_params = {'digest': digest, 'fields': field}
        api = Api(Const.SNIPPET, Api.SEARCH, local_params)
        Config.load(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if not contents['data']:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SNIPPET, contents, request, digest, field=field, pagination=False)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %ssnippets/%s/field', Config.base_path_app, digest, field)
