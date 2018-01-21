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

from snippy.logger.logger import CustomGunicornLogger
from snippy.logger.logger import Logger
from snippy.server.api_hello import ApiHello
from snippy.server.api_snippets import ApiSnippets
from snippy.server.api_snippets import ApiSnippetsDigest
from snippy.server.api_solutions import ApiSolutions
from snippy.server.gunicorn_server import GunicornServer as SnippyServer
import falcon


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
            'logger_class': CustomGunicornLogger
        }
        self.api = falcon.API()
        self.api.add_route('/', ApiHello())
        self.api.add_route('/api/hello', ApiHello())
        self.api.add_route('/api/v1/hello', ApiHello())
        self.api.add_route('/api/v1/snippets', ApiSnippets(self.storage))
        self.api.add_route('/api/v1/snippets/{digest}', ApiSnippetsDigest(self.storage))
        self.api.add_route('/api/v1/solutions', ApiSolutions(self.storage))
        SnippyServer(self.api, options).run()
