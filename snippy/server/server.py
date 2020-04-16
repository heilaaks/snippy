# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

import sys
from signal import signal, getsignal, SIG_DFL
try:
    from signal import SIGPIPE
except ImportError:
    pass  # SIGPIPE is not available in Windows.
import ssl

import falcon
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.content import Content
from snippy.content.fields import Fields
from snippy.logger import CustomGunicornLogger
from snippy.logger import Logger
from snippy.server.gunicorn_server import GunicornServer as SnippyServer
from snippy.server.rest.api_fields import ApiAttributes
from snippy.server.rest.api_hello import ApiHello
from snippy.server.rest.api_content import ApiContent
from snippy.server.rest.api_content import ApiContentId
from snippy.server.rest.api_content import ApiContentIdField


class Server(object):  # pylint: disable=too-few-public-methods
    """RESTish API Server."""

    def __init__(self, storage):
        self._logger = Logger.get_logger(__name__)
        self.api = None
        self.storage = storage

    def run(self):
        """Run Snippy API server."""

        options = {
            'bind': Config.server_host,
            'ca_certs': Config.server_ssl_ca_cert,
            'certfile': Config.server_ssl_cert,
            'ciphers': 'ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA',
            'keyfile': Config.server_ssl_key,
            'logger_class': CustomGunicornLogger,
            'on_exit': SnippyServer.on_exit,
            'post_worker_init': SnippyServer.post_worker_init,
            'pre_fork': SnippyServer.pre_fork,
            'pre_request': SnippyServer.pre_request,
            'ssl_version': ssl.PROTOCOL_TLSv1_2,
            'workers': 1
        }
        self._logger.debug('run rest api server application with base path: %s', Config.server_base_path_rest)
        try:
            self.api = falcon.API(media_type='application/vnd.api+json')
        except AttributeError:
            raise ImportError
        snippet = Content(self.storage, Const.SNIPPET, run_cli=False)
        solution = Content(self.storage, Const.SOLUTION, run_cli=False)
        reference = Content(self.storage, Const.REFERENCE, run_cli=False)
        groups = Fields(self.storage, Const.GROUPS, run_cli=False)
        tags = Fields(self.storage, Const.TAGS, run_cli=False)
        self.api.req_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})  # noqa pylint: disable=no-member, line-too-long
        self.api.resp_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})  # noqa pylint: disable=no-member, line-too-long
        self.api.add_route(Config.server_base_path_rest.rstrip('/'), ApiHello())
        self.api.add_route(urljoin(Config.server_base_path_rest, 'hello'), ApiHello())
        self.api.add_route(urljoin(Config.server_base_path_rest, 'snippets'), ApiContent(snippet))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'snippets/{identity}'), ApiContentId(snippet))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'snippets/{identity}/{field}'), ApiContentIdField(snippet))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'solutions'), ApiContent(solution))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'solutions/{identity}'), ApiContentId(solution))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'solutions/{identity}/{field}'), ApiContentIdField(solution))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'references'), ApiContent(reference))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'references/{identity}'), ApiContentId(reference))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'references/{identity}/{field}'), ApiContentIdField(reference))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'groups'), ApiAttributes(groups))
        self.api.add_route(urljoin(Config.server_base_path_rest, 'tags'), ApiAttributes(tags))

        # Reset cause just before starting the server. If there were any
        # failures during the server statup phase, they are still stored
        # in the Cause object when the server runs. If this is the case,
        # the first response sent by the server will be error response
        # even when the HTTP request was processed successfully.
        Cause.reset()

        # The signal handler manipulation and the flush below prevent the
        # 'broken pipe' error with grep. See more information from Logger
        # print_stdout method. Example command below works because of this.
        #
        # $ snippy --server-host localhost:8080 -vv --defaults | grep -E -A2 -B2 'run method|end method'
        try:
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
        except (NameError, ValueError):
            pass  # SIGPIPE is not available in Windows.
        SnippyServer(self.api, options).run()
        sys.stdout.flush()
        try:
            signal(SIGPIPE, signal_sigpipe)
        except (NameError, UnboundLocalError, ValueError):
            pass  # SIGPIPE is not available in Windows.
