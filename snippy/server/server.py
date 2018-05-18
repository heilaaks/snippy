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

"""server: JSON REST API server."""

import falcon
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from snippy.config.config import Config
from snippy.logger import CustomGunicornLogger
from snippy.logger import Logger
from snippy.server.gunicorn_server import GunicornServer as SnippyServer
from snippy.server.rest.api_hello import ApiHello
from snippy.server.rest.api_snippets import ApiSnippets
from snippy.server.rest.api_snippets import ApiSnippetsDigest
from snippy.server.rest.api_solutions import ApiSolutions
from snippy.server.rest.api_solutions import ApiSolutionsDigest


class Server(object):  # pylint: disable=too-few-public-methods
    """REST API Server."""

    def __init__(self, storage):
        self._logger = Logger(__name__).get_logger()
        self.api = None
        self.storage = storage

    def run(self):
        """Run Snippy API server."""

        options = {
            'bind': '%s:%s' % (Config.server_ip, Config.server_port),
            'workers': 1,
            'logger_class': CustomGunicornLogger
        }
        self._logger.debug('run rest api server application with base path: %s', Config.base_path_app)
        try:
            self.api = falcon.API(media_type='application/vnd.api+json')
        except AttributeError:
            raise ImportError
        self.api.req_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})
        self.api.resp_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})
        self.api.add_route('/snippy', ApiHello())
        self.api.add_route(Config.base_path_app.rstrip('/'), ApiHello())
        self.api.add_route(urljoin(Config.base_path_app, 'hello'), ApiHello())
        self.api.add_route(urljoin(Config.base_path_app, 'snippets'), ApiSnippets(self.storage))
        self.api.add_route(urljoin(Config.base_path_app, 'snippets/{digest}'), ApiSnippetsDigest(self.storage))
        self.api.add_route(urljoin(Config.base_path_app, 'solutions'), ApiSolutions(self.storage))
        self.api.add_route(urljoin(Config.base_path_app, 'solutions/{digest}'), ApiSolutionsDigest(self.storage))
        SnippyServer(self.api, options).run()
