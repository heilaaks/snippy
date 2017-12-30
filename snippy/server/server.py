#!/usr/bin/env python3

"""server.py - JSON REST API server."""

import falcon
from snippy.logger.logger import Logger
from snippy.server.api_hello import ApiHello
from snippy.server.api_snippets import ApiSnippets
from snippy.server.api_snippets import ApiSnippetsDigest
from snippy.server.gunicorn_server import GunicornServer as SnippyServer


class Server(object):  # pylint: disable=too-few-public-methods
    """REST API Server."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.api = None
        self.storage = storage

    def run(self):
        """Run Snippy API server."""

        options = {
            'bind': '%s:%s' % ('127.0.0.1', '8080'),
            'workers': 1,
        }
        self.api = falcon.API()
        self.api.add_route('/', ApiHello())
        self.api.add_route('/api/v1/hello', ApiHello())
        self.api.add_route('/api/v1/snippets', ApiSnippets(self.storage))
        self.api.add_route('/api/v1/snippets/{digest}', ApiSnippetsDigest(self.storage))
        SnippyServer(self.api, options).run()
