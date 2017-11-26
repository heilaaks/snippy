#!/usr/bin/env python3

"""api_snippets.py - JSON REST API for Snippets."""

from snippy.version import __version__
from snippy.logger.logger import Logger


class ApiSnippets(object):  # pylint: disable=too-few-public-methods
    """Snippets API."""

    def __init__(self):
        self.logger = Logger(__name__).get()

    def on_get(self, request, response):
        """Request snippets based on search parameters."""

        self.logger.debug('ApiSnippets')
        print(request)
        print("path %s" % request.path)
        print("query %s" % request.query_string)
        print("query params %s" % request.params)
        print("accept %s" % request.accept)
        print("accept bool %s" % request.client_accepts_json)

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
