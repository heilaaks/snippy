#!/usr/bin/env python3

"""api_snippets.py - JSON REST API for Snippets."""

from __future__ import print_function
import falcon
from snippy.metadata import __version__
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.source.api import Api
from snippy.config.config import Config
from snippy.content.snippet import Snippet


class ApiSnippets(object):  # pylint: disable=too-few-public-methods
    """Process snippet collections"""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def on_post(self, request, response):
        """Create new snippet."""

        self.logger.debug('run post /api/snippets')
        api = Api(Const.SNIPPET, Api.CREATE, request.media)
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

    def on_get(self, request, response):
        """Search snippets based on query parameters."""

        self.logger.debug('run get /api/snippets')
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

    def on_delete(self, request, response):
        """Delete snippet based on query parameters."""

        self.logger.debug('run delete /api/snippets')
        api = Api(Const.SNIPPET, Api.DELETE, request.params)
        Config.read_source(api)
        Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()


class ApiSnippetsDigest(object):  # pylint: disable=too-few-public-methods
    """Process snippet based on digest resource ID."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    @staticmethod
    def on_put(request, response, digest):
        """Handle PUT reguest."""

        print("ApiSnippetsDigest")
        print(request)
        print("path %s" % request.path)
        print("query %s" % request.query_string)
        print("query params %s" % request.params)
        print("accept %s" % request.accept)
        print("accept bool %s" % request.client_accepts_json)
        print("digest %s" % digest)

        hello = __version__
        response.media = hello

    def on_get(self, request, response, digest):
        """Search snippet based on digest."""

        self.logger.debug('run get /api/snippets/{digest} = %s', digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.SEARCH, local_params)
        Config.read_source(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        print(contents)
        if Cause.is_ok():
            response.content_type = falcon.MEDIA_JSON
            response.body = contents
            response.status = Cause.http_status()
        else:
            response.content_type = falcon.MEDIA_JSON
            response.body = Cause.json_message()
            response.status = Cause.http_status()

    def on_delete(self, _, response, digest):
        """Delete snippet based on digest."""

        self.logger.debug('run delete /api/snippets/{digest} = %s', digest)
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
