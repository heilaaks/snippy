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
from snippy.config.source.api import Api
from snippy.logger import Logger
from snippy.server.rest.generate import Generate
from snippy.server.rest.validate import Validate


class ApiContentBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for content APIs."""

    # JSON API v1.0 media header. The character set is deviation from the
    # specification but it was considered very useful so that user always
    # knows how to decode the characters.
    MEDIA_JSON_API = 'application/vnd.api+json; charset=UTF-8'

    def __init__(self, content=None, category=None):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response):
        """Create new content."""

        self._logger.debug('run post %s', request.uri)
        collection = Validate.collection(request)
        for resource in collection:
            api = Api(self._category, Api.CREATE, resource)
            Config.load(api)
            self._content.run()
        if Cause.is_ok():
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.collection(self._content.collection, request)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end post %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response):
        """Search content based on query parameters."""

        self._logger.debug('run get %s', request.uri)
        api = Api(self._category, Api.SEARCH, request.params)
        Config.load(api)
        self._content.run()
        if not self._content.collection.size() and Config.search_limit != 0:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resources')
        if Cause.is_ok():
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.collection(self._content.collection, request, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response):
        """Deleting content without resource is not supported."""

        self._logger.debug('run delete %s', request.uri)
        Cause.push(Cause.HTTP_NOT_FOUND, 'cannot delete content without identified resource')
        response.content_type = ApiContentBase.MEDIA_JSON_API
        response.body = Generate.error(Cause.json_message())
        response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete %s', request.uri)


class ApiContentDigestBase(object):
    """Process content based on digest."""

    def __init__(self, content, category):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response, digest):
        """Update content."""

        self._logger.debug('run post %', request.uri)
        if request.get_header('x-http-method-override', default='post').lower() == 'put':
            self.on_put(request, response, digest)
        elif request.get_header('x-http-method-override', default='post').lower() == 'patch':
            self.on_patch(request, response, digest)
        elif request.get_header('x-http-method-override', default='post').lower() == 'delete':
            self.on_delete(request, response, digest)
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot create resource with id, use x-http-method-override to override the request')
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end post %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, digest):
        """Search content based on digest."""

        self._logger.debug('run get %s', request.uri)
        local_params = {'digest': digest}
        api = Api(self._category, Api.SEARCH, local_params)
        Config.load(api)
        self._content.run()
        if not self._content.collection.size():
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.resource(self._content.collection, request, digest, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response, digest):
        """Delete content based on digest."""

        self._logger.debug('run delete %s', request.uri)
        local_params = {'digest': digest}
        api = Api(self._category, Api.DELETE, local_params)
        Config.load(api)
        self._content.run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_put(self, request, response, digest):
        """Update whole content based on digest."""

        self._logger.debug('run put %s', request.uri)
        resource = Validate.resource(request, digest)
        if resource:
            api = Api(self._category, Api.UPDATE, resource)
            Config.load(api)
            self._content.run()
        if Cause.is_ok():
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.resource(self._content.collection, request, digest)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end put %s', request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_patch(self, request, response, digest):
        """Update partial content based on digest."""

        self._logger.debug('run patch %s', request.uri)
        self.on_put(request, response, digest)
        Cause.reset()
        self._logger.debug('end patch %s', request.uri)


class ApiContentFieldBase(object):  # pylint: disable=too-few-public-methods
    """Process content based on digest resource ID and specified field."""

    def __init__(self, content, category):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, digest, field):
        """Get defined content field based on digest."""

        self._logger.debug('run get %s', request.uri)
        local_params = {'digest': digest, 'fields': field}
        api = Api(self._category, Api.SEARCH, local_params)
        Config.load(api)
        self._content.run()
        if not self._content.collection.size():
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.resource(self._content.collection, request, digest, field=field, pagination=False)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiContentBase.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get %s', request.uri)
