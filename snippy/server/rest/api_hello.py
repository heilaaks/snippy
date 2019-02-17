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

"""api_hello: JSON REST API for hello endpoint."""

import falcon

from snippy.logger import Logger
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.generate import Generate
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__


class ApiHello(ApiContentBase):  # pylint: disable=too-few-public-methods
    """Hello API."""

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, _sall=None, _stag=None, _sgrp=None):
        """Get Hello!"""

        hello = {
            'meta': {
                'version': __version__,
                'homepage': __homepage__,
                'docs': __docs__,
                'openapi': __openapi__
            }
        }
        self._logger.debug('run: %s %s', request.method, request.uri)
        response.content_type = ApiContentBase.MEDIA_JSON_API
        response.body = Generate.dumps(hello)
        response.status = falcon.HTTP_200
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_options(self, request, response, _sall=None, _stag=None, _sgrp=None):
        """Respond with allowed methods for Hello!"""

        self._logger.debug('run: %s %s', request.method, request.uri)
        response.status = falcon.HTTP_200
        response.set_header('Allow', 'GET')
        self._logger.debug('end: %s %s', request.method, request.uri)
