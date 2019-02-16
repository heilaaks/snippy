#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
from signal import signal, getsignal, SIGPIPE, SIG_DFL
import ssl

import falcon
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from snippy.config.config import Config
from snippy.content.fields import Fields
from snippy.content.reference import Reference
from snippy.content.snippet import Snippet
from snippy.content.solution import Solution
from snippy.logger import CustomGunicornLogger
from snippy.logger import Logger
from snippy.server.gunicorn_server import GunicornServer as SnippyServer
from snippy.server.rest.api_fields import ApiDigest
from snippy.server.rest.api_fields import ApiDigestField
from snippy.server.rest.api_fields import ApiGroups
from snippy.server.rest.api_fields import ApiKeywords
from snippy.server.rest.api_fields import ApiTags
from snippy.server.rest.api_fields import ApiUuid
from snippy.server.rest.api_fields import ApiUuidField
from snippy.server.rest.api_hello import ApiHello
from snippy.server.rest.api_references import ApiReferences
from snippy.server.rest.api_references import ApiReferencesDigest
from snippy.server.rest.api_references import ApiReferencesField
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
            'bind': '%s' % (Config.server_host),
            'ca_certs': Config.server_ssl_ca_cert,
            'certfile': Config.server_ssl_cert,
            'ciphers': 'ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA',
            'keyfile': Config.server_ssl_key,
            'logger_class': CustomGunicornLogger,
            'on_exit': SnippyServer.on_exit,
            'post_worker_init': SnippyServer.post_worker_init,
            'pre_request': SnippyServer.pre_request,
            'ssl_version': ssl.PROTOCOL_TLSv1_2,
            'workers': 1
        }
        self._logger.debug('run rest api server application with base path: %s', Config.server_app_base_path)
        try:
            self.api = falcon.API(media_type='application/vnd.api+json')
        except AttributeError:
            raise ImportError
        snippet = Snippet(self.storage, run_cli=False)
        solution = Solution(self.storage, run_cli=False)
        reference = Reference(self.storage, run_cli=False)
        fields = Fields(self.storage)
        self.api.req_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})
        self.api.resp_options.media_handlers.update({'application/vnd.api+json': falcon.media.JSONHandler()})
        self.api.add_route('/snippy', ApiHello())
        self.api.add_route(Config.server_app_base_path.rstrip('/'), ApiHello())
        self.api.add_route(urljoin(Config.server_app_base_path, 'hello'), ApiHello())
        self.api.add_route(urljoin(Config.server_app_base_path, 'snippets'), ApiSnippets(snippet))
        self.api.add_route(urljoin(Config.server_app_base_path, 'snippets/{digest}'), ApiSnippetsDigest(snippet))
        self.api.add_route(urljoin(Config.server_app_base_path, 'snippets/{digest}/{field}'), ApiSnippetsField(snippet))
        self.api.add_route(urljoin(Config.server_app_base_path, 'solutions'), ApiSolutions(solution))
        self.api.add_route(urljoin(Config.server_app_base_path, 'solutions/{digest}'), ApiSolutionsDigest(solution))
        self.api.add_route(urljoin(Config.server_app_base_path, 'solutions/{digest}/{field}'), ApiSolutionsField(solution))
        self.api.add_route(urljoin(Config.server_app_base_path, 'references'), ApiReferences(reference))
        self.api.add_route(urljoin(Config.server_app_base_path, 'references/{digest}'), ApiReferencesDigest(reference))
        self.api.add_route(urljoin(Config.server_app_base_path, 'references/{digest}/{field}'), ApiReferencesField(reference))
        self.api.add_route(urljoin(Config.server_app_base_path, 'groups/{sgrp}'), ApiGroups(fields))
        self.api.add_route(urljoin(Config.server_app_base_path, 'tags/{stag}'), ApiTags(fields))
        self.api.add_route(urljoin(Config.server_app_base_path, 'digest/{digest}'), ApiDigest(fields))
        self.api.add_route(urljoin(Config.server_app_base_path, 'digest/{digest}/{field}'), ApiDigestField(fields))
        self.api.add_route(urljoin(Config.server_app_base_path, 'uuid/{uuid}'), ApiUuid(fields))
        self.api.add_route(urljoin(Config.server_app_base_path, 'uuid/{uuid}/{field}'), ApiUuidField(fields))
        self.api.add_route(urljoin(Config.server_app_base_path, '{sall}'), ApiKeywords(fields))

        # The signal handler manipulation and the flush below prevent the
        # 'broken pipe' error with grep. See more information from Logger
        # print_stdout method. Example command below works because of this.
        #
        # $ snippy --server-host localhost:8080 -vv | grep -A2 -B2 'operation: run :'
        signal_sigpipe = getsignal(SIGPIPE)
        signal(SIGPIPE, SIG_DFL)
        SnippyServer(self.api, options).run()
        sys.stdout.flush()
        signal(SIGPIPE, signal_sigpipe)
