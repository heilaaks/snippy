#!/usr/bin/env python3

"""api_snippets.py - JSON REST API for Snippets."""

from __future__ import print_function
from snippy.version import __version__
from snippy.logger.logger import Logger
from snippy.config.source.api import Api
from snippy.config.config import Config
from snippy.content.snippet import Snippet


class ApiSnippets(object):  # pylint: disable=too-few-public-methods
    """Snippets API."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def on_get(self, request, response):
        """Request snippets based on search parameters."""

        self.logger.debug('ApiSnippets')
        print(request)
        print("path %s" % request.path)
        print("query %s" % request.query_string)
        print("query params %s" % request.params)
        print("accept %s" % request.accept)
        print("accept bool %s" % request.client_accepts_json)

        api = Api(request.params, Api.SEARCH)
        Config.read_source(api)
        snippet = Snippet(self.storage)
        snippet.run()

        hello = __version__
        response.media = hello


class ApiSnippetsDigest(object):  # pylint: disable=too-few-public-methods
    """Request snippet based on digest."""

    def __init__(self):
        self.logger = Logger(__name__).get()

    @staticmethod
    def on_get(request, response, digest):
        """Handle GET reguest."""

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


class ApiSnippetsDigestData(object):  # pylint: disable=too-few-public-methods
    """Request snnippet content data based on mdigest"""

    def __init__(self):
        self.logger = Logger(__name__).get()

    @staticmethod
    def on_get(request, response, digest):
        """Handle GET reguest."""

        print("ApiSnippetsDigestData")
        print(request)
        print("path %s" % request.path)
        print("query %s" % request.query_string)
        print("query params %s" % request.params)
        print("accept %s" % request.accept)
        print("accept bool %s" % request.client_accepts_json)
        print("digest %s" % digest)

        hello = __version__
        response.media = hello