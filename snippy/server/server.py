#!/usr/bin/env python3

"""server.py - JSON REST API server."""

import falcon
from snippy.server.api_hello import ApiHello
from snippy.server.api_snippets import ApiSnippets
from snippy.server.api_snippets import ApiSnippetsDigest
from snippy.server.api_snippets import ApiSnippetsDigestData
from snippy.server.gunicorn_server import GunicornServer as SnippyServer


class Server(object):  # pylint: disable=too-few-public-methods
    """REST API Server."""

    def __init__(self, storage):
        self.api = None
        self.config = None
        self.storage = storage

    def run(self):
        """Run Snippy API server."""

        options = {
            'bind': '%s:%s' % ('127.0.0.1', '8080'),
            'workers': 1,
        }
        self.api = falcon.API()
        self.api.add_route('/', ApiHello())
        self.api.add_route('/api/hello', ApiHello())
        self.api.add_route('/api/snippets', ApiSnippets())
        self.api.add_route('/api/snippets/{digest}', ApiSnippetsDigest())
        self.api.add_route('/api/snippets/{digest}/data', ApiSnippetsDigestData())
        SnippyServer(self.api, options).run()
