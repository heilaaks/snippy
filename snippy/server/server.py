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

"""server: JSON RESTish API server."""

import ssl

import falcon
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from snippy.config.config import Config
from snippy.content.snippet import Snippet
from snippy.content.solution import Solution
from snippy.logger import CustomGunicornLogger
from snippy.logger import Logger
from snippy.server.gunicorn_server import GunicornServer as SnippyServer
from snippy.server.rest.api_hello import ApiHello
from snippy.server.rest.api_snippets import ApiSnippets
from snippy.server.rest.api_snippets import ApiSnippetsDigest
from snippy.server.rest.api_snippets import ApiSnippetsField
from snippy.server.rest.api_solutions import ApiSolutions
from snippy.server.rest.api_solutions import ApiSolutionsDigest
from snippy.server.rest.api_solutions import ApiSolutionsField


class Server(object):  # pylint: disable=too-few-public-methods
    """RESTish API Server."""

    def __init__(self, storage):
        self._logger = Logger.get_logger(__name__)
        self.api = None
        self.storage = storage

    def run(self):
        """Run Snippy API server."""

        options = {
            'bind': '%s:%s' % (Config.server_ip, Config.server_port),
            'ca_certs': Config.ssl_ca_cert,
            'certfile': Config.ssl_cert,
            'ciphers': 'ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA',
            'keyfile': Config.ssl_key,
            'logger_class': CustomGunicornLogger,
            'on_exit': SnippyServer.on_exit,
            'post_worker_init': SnippyServer.post_worker_init,
            'pre_request': SnippyServer.pre_request,
            'ssl_version': ssl.PROTOCOL_TLSv1_2,
            'workers': 1
        }
        self._logger.debug('run rest api server application with base path: %s', Config.base_path_app)
        try:
            self.api = falcon.API(media_type='application/vnd.api+json')
        except AttributeError:
            raise ImportError
        snippet = Snippet(self.storage, run_cli=False)
        solution = Solution(self.storage, run_cli=False)
        self.api.req_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})
        self.api.resp_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})
        self.api.add_route('/snippy', ApiHello())
        self.api.add_route(Config.base_path_app.rstrip('/'), ApiHello())
        self.api.add_route(urljoin(Config.base_path_app, 'hello'), ApiHello())
        self.api.add_route(urljoin(Config.base_path_app, 'snippets'), ApiSnippets(snippet))
        self.api.add_route(urljoin(Config.base_path_app, 'snippets/{digest}'), ApiSnippetsDigest(snippet))
        self.api.add_route(urljoin(Config.base_path_app, 'snippets/{digest}/{field}'), ApiSnippetsField(snippet))
        self.api.add_route(urljoin(Config.base_path_app, 'solutions'), ApiSolutions(solution))
        self.api.add_route(urljoin(Config.base_path_app, 'solutions/{digest}'), ApiSolutionsDigest(solution))
        self.api.add_route(urljoin(Config.base_path_app, 'solutions/{digest}/{field}'), ApiSolutionsField(solution))
        SnippyServer(self.api, options).run()
