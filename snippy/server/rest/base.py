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

"""base: Base class for content APIs."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.api import Api
from snippy.logger import Logger
from snippy.server.rest.jsonapiv1 import JsonApiV1
from snippy.server.rest.validate import Validate


class ContentApiBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for content APIs."""

    def __init__(self, content):
        self._logger = Logger.get_logger(__name__)
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response):
        """Create new content."""

        contents = self._content.storage.get_contents(None)
        self._logger.debug('run post %s', request.uri)
        collection = Validate.collection(request)
        for member in collection:
            api = Api(self._content.category, Api.CREATE, member)
            Config.load(api)
            content = self._content.run()
            contents['data'].extend(content['data'])
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.collection(self._content.category, contents, request)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end post %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response):
        """Search content based on query parameters."""

        self._logger.debug('run get %s', request.uri)
        api = Api(self._content.category, Api.SEARCH, request.params)
        Config.load(api)
        contents = self._content.run()
        if not contents['data'] and Config.search_limit != 0:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resources')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.collection(self._content.category, contents, request, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response):
        """Deleting content without resource is not supported."""

        self._logger.debug('run delete %s', request.uri)
        Cause.push(Cause.HTTP_NOT_FOUND, 'cannot delete content without identified resource')
        response.content_type = Const.MEDIA_JSON_API
        response.body = JsonApiV1.error(Cause.json_message())
        response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete %s', request.uri)
