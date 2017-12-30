#!/usr/bin/env python3
# flake8: noqa # pylint: skip-file

"""api_solutions.py - JSON REST API for Solutions."""

from __future__ import print_function
import falcon
from snippy.metadata import __version__
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.source.api import Api
from snippy.config.config import Config
from snippy.content.solution import Solution


class ApiSoultions(object):
    """Process solution collections"""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    @staticmethod
    def on_get(request, response):
        """Search solutions based on query parameters."""

        print("ApiSolutions")
        print(request)
        print("path %s" % request.path)
        print("query %s" % request.query_string)
        print("query params %s" % request.params)
        print("accept %s" % request.accept)
        print("accept bool %s" % request.client_accepts_json)

        hello = __version__
        response.media = hello
        response.content_type = falcon.MEDIA_JSON

class ApiSolutionsDigest(object):
    """Process solution based on digest resource ID."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    @staticmethod
    def on_put(request, response, digest):
        """Handle PUT reguest."""

        print("ApiSolutionsDigest")
        print(request)
        print("path %s" % request.path)
        print("query %s" % request.query_string)
        print("query params %s" % request.params)
        print("accept %s" % request.accept)
        print("accept bool %s" % request.client_accepts_json)
        print("digest %s" % digest)

        hello = __version__
        response.media = hello
