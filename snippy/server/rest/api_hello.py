# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""api_hello: JSON REST API for hello API endpoint."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.logger import Logger
from snippy.server.rest.base import ApiResource
from snippy.server.rest.generate import Generate
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__


class ApiHello(ApiResource):
    """Hello API."""

    def on_get(self, request, response):
        """Get server /hello API endpoint.

        The route is not measured and logs must not be printed from here if
        request came from the server healthcheck from the same host. This is
        the case when Docker container hosts the server and the healtcheck in
        the same container but in different processes.

        If the server in Docker container uses the ``--net=host`` option, it
        prevents the logs from HTTP request to this API endpoints because the
        server and host use the same network. This is accepted behaviour.

        As of now, it is considered that constant server healthcheck must not
        flood the logs with successful healthcheck. This would lose important
        logs for troubleshooting.

        For the normal /hello API call the logs must be printed in order to
        trace calls and problems with the /hello API. It is considered that
        external clients will use the /hello instead of the server base path.

        The logs are disabled based on local IP address to generate logs for
        remote healtchecks. External clients may try to flood the server so
        it is important to log the external events.
        """

        hello = {
            'meta': {
                'version': __version__,
                'homepage': __homepage__,
                'docs': __docs__,
                'openapi': __openapi__
            }
        }
        if request.netloc != Config.server_host:
            self._logger.debug('run: %s %s', request.method, request.uri)
        response.content_type = ApiResource.MEDIA_JSON_API
        response.body = Generate.dumps(hello)
        response.status = Cause.http_status()
        if request.netloc != Config.server_host:
            self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_options(self, request, response):
        """Respond with allowed methods for Hello!"""

        self._logger.debug('run: %s %s', request.method, request.uri)
        response.status = Cause.http_status()
        response.set_header('Allow', 'GET')
        self._logger.debug('end: %s %s', request.method, request.uri)
