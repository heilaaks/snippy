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

"""cause.py: Cause code management."""

import inspect
import sys

from snippy.logger.logger import Logger
from snippy.metadata import __docs__
from snippy.metadata import __homepage__
from snippy.metadata import __openapi__
from snippy.metadata import __version__


class Cause(object):
    """Cause code management."""

    ALL_OK = 'OK'

    HTTP_200 = '200 OK'
    HTTP_201 = '201 Created'
    HTTP_204 = '204 No Content'
    HTTP_400 = '400 Bad Request'
    HTTP_403 = '403 Forbidden'
    HTTP_404 = '404 Not Found'
    HTTP_409 = '409 Conflict'
    HTTP_500 = '500 Internal Server Error'

    HTTP_OK = HTTP_200
    HTTP_CREATED = HTTP_201
    HTTP_NO_CONTENT = HTTP_204
    HTTP_BAD_REQUEST = HTTP_400
    HTTP_FORBIDDEN = HTTP_403
    HTTP_NOT_FOUND = HTTP_404
    HTTP_CONFLICT = HTTP_409
    HTTP_INTERNAL_SERVER_ERROR = HTTP_500
    OK_STATUS_LIST = (HTTP_OK, HTTP_CREATED, HTTP_NO_CONTENT)

    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_404_NOT_FOUND = 404

    _list = {'errors': []}
    _logger = Logger(__name__).get()

    @classmethod
    def reset(cls):
        """Reset cause to initial value."""

        cause = cls.get_message()
        cls._list = {'errors': []}

        return cause

    @classmethod
    def push(cls, status, message):
        """Append cause to list."""

        # Optimization: Prevent setting the caller module and line number in case
        # of success causes. Reading of the line number requires file access that
        # is expensive and avoided in successful cases.
        caller = 'snippy.cause.cause.optimize:1'
        if status not in Cause.OK_STATUS_LIST:
            caller = cls._caller()
        cls._logger.info('status %s with message %s from %s', status, message, caller)
        cls._list['errors'].append({'status': int(status.split()[0]),
                                    'status_string': status,
                                    'module': caller,
                                    'title': message})

    @classmethod
    def is_ok(cls):
        """Test if errors were detected."""

        is_ok = False
        if not cls._list['errors']:
            is_ok = True
        elif len(cls._list['errors']) == 1 and cls._list['errors'][0]['status_string'] in Cause.OK_STATUS_LIST:
            is_ok = True
        elif all(error['status_string'] in Cause.OK_STATUS_LIST for error in cls._list['errors']):
            is_ok = True

        return is_ok

    @classmethod
    def http_status(cls):
        """Return the HTTP status."""

        status = Cause.HTTP_OK
        if cls._list['errors']:
            status = cls._list['errors'][0]['status_string']

        return status

    @classmethod
    def json_message(cls):
        """Return errors in JSON data structure."""

        response = cls._list
        response['meta'] = {'version': __version__,
                            'homepage': __homepage__,
                            'docs': __docs__,
                            'openapi': __openapi__}

        return response

    @classmethod
    def get_message(cls):
        """Return cause message."""

        cause = Cause.ALL_OK
        if not cls.is_ok():
            cause = 'NOK: ' + cls._list['errors'][0]['title']

        return cause

    @staticmethod
    def _caller():
        """Get caller module and code line."""

        # Optimization: Inspect.stack reads source code file that generates
        # expensive file access. The contenxt loading can be switched off
        # with stack(0) setting /1/. A bit more efficient way is to use
        # sys._getframe that is according to /2/ four times faster the
        # stack(0). Testing shows that there is a noticeable difference
        # but not that much.
        #
        # Try to avoid calling this method for performance reasons.
        #
        # /1/ https://stackoverflow.com/a/17407257
        # /2/ https://stackoverflow.com/a/45196608
        frame = sys._getframe(2)  # pylint: disable=protected-access
        info = inspect.getframeinfo(frame)
        module = inspect.getmodule(frame)
        location = module.__name__ + ':' + str(info.lineno)

        return location
