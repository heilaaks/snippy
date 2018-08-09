#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""api_hello: JSON REST API hello."""

import json

import falcon

from snippy.logger import Logger
from snippy.server.rest.base import ApiContentBase
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__


class ApiHello(ApiContentBase):  # pylint: disable=too-few-public-methods
    """Hello API."""

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_get(_request, response, _sall=None, _stag=None, _sgrp=None):
        """Get Hello!"""

        hello = {
            'meta': {
                'version': __version__,
                'homepage': __homepage__,
                'docs': __docs__,
                'openapi': __openapi__
            }
        }
        response.content_type = ApiContentBase.MEDIA_JSON_API
        response.body = json.dumps(hello)
        response.status = falcon.HTTP_200

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_request, response):
        """Respond with allowed methods for Hello!"""

        response.status = falcon.HTTP_200
        response.set_header('Allow', 'GET')
