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

"""server.py - JSON REST API server."""

import falcon
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from snippy.config.config import Config
from snippy.logger.logger import CustomGunicornLogger
from snippy.logger.logger import Logger
from snippy.server.gunicorn_server import GunicornServer as SnippyServer
from snippy.server.rest.api_hello import ApiHello
from snippy.server.rest.api_snippets import ApiSnippets
from snippy.server.rest.api_snippets import ApiSnippetsDigest
from snippy.server.rest.api_solutions import ApiSolutions
from snippy.server.rest.api_solutions import ApiSolutionsDigest


class Server(object):  # pylint: disable=too-few-public-methods
    """REST API Server."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.api = None
        self.storage = storage

    def run(self):
        """Run Snippy API server."""

        options = {
            'bind': '%s:%s' % (Config.server_ip, Config.server_port),
            'workers': 1,
            'logger_class': CustomGunicornLogger
        }
        self.logger.debug('run server with base path: %s', Config.base_path)
        self.api = falcon.API()
        self.api.add_route('/snippy', ApiHello())
        self.api.add_route(Config.base_path.rstrip('/'), ApiHello())
        self.api.add_route(urljoin(Config.base_path, 'hello'), ApiHello())
        self.api.add_route(urljoin(Config.base_path, 'snippets'), ApiSnippets(self.storage))
        self.api.add_route(urljoin(Config.base_path, 'snippets/{digest}'), ApiSnippetsDigest(self.storage))
        self.api.add_route(urljoin(Config.base_path, 'solutions'), ApiSolutions(self.storage))
        self.api.add_route(urljoin(Config.base_path, 'solutions/{digest}'), ApiSolutionsDigest(self.storage))
        SnippyServer(self.api, options).run()
