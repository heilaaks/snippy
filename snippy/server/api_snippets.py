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

"""api_snippets.py - JSON REST API for Snippets."""

from __future__ import print_function
import json
import falcon
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.source.api import Api
from snippy.config.config import Config
from snippy.content.snippet import Snippet
from snippy.server.validate import Validate


class ApiSnippets(object):
    """Process snippet collections."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage
        self.validate = Validate()

    def on_post(self, request, response):
        """Create new snippets."""

        contents = []
        self.logger.debug('run post /api/v1/snippets')
        collection = Validate.collection(request.media)
        for member in collection:
            api = Api(Const.SNIPPET, Api.CREATE, member)
            Config.read_source(api)
            contents = contents + json.loads(Snippet(self.storage, Const.CONTENT_TYPE_JSON).run())
        if Cause.is_ok():
            response.content_type = falcon.MEDIA_JSON
            response.body = json.dumps(contents)
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

        Cause.reset()
        Logger.set_new_oid()

    def on_get(self, request, response):
        """Search snippets based on query parameters."""

        self.logger.debug('run get /api/v1/snippets')
        api = Api(Const.SNIPPET, Api.SEARCH, request.params)
        Config.read_source(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.content_type = falcon.MEDIA_JSON
            response.body = contents
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

        Cause.reset()
        Logger.set_new_oid()

    def on_delete(self, request, response):
        """Delete snippet based on query parameters."""

        self.logger.debug('run delete /api/v1/snippets')
        api = Api(Const.SNIPPET, Api.DELETE, request.params)
        Config.read_source(api)
        Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

        Cause.reset()
        Logger.set_new_oid()


class ApiSnippetsDigest(object):
    """Process snippet based on digest resource ID."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def on_put(self, request, response, digest):
        """Update snippet based on digest."""

        self.logger.debug('run put /api/v1/snippets/{digest} = %s', digest)
        local_params = request.media
        local_params['digest'] = digest
        api = Api(Const.SNIPPET, Api.UPDATE, local_params)
        Config.read_source(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.content_type = falcon.MEDIA_JSON
            response.body = contents
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

        Cause.reset()
        Logger.set_new_oid()

    def on_get(self, _, response, digest):
        """Search snippet based on digest."""

        self.logger.debug('run get /api/v1/snippets/{digest} = %s', digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.SEARCH, local_params)
        Config.read_source(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.content_type = falcon.MEDIA_JSON
            response.body = contents
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

        Cause.reset()
        Logger.set_new_oid()

    def on_delete(self, _, response, digest):
        """Delete snippet based on digest."""

        self.logger.debug('run delete /api/v1/snippets/{digest} = %s', digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.DELETE, local_params)
        Config.read_source(api)
        Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

        Cause.reset()
        Logger.set_new_oid()
