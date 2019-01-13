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

"""cause: Cause code services."""

from __future__ import print_function

import inspect
import sys

from snippy.logger import Logger
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__


class Cause(object):
    """Cause code services."""

    ALL_OK = 'OK'

    # HTTP status codes.
    HTTP_200 = '200 OK'
    HTTP_201 = '201 Created'
    HTTP_204 = '204 No Content'
    HTTP_400 = '400 Bad Request'
    HTTP_403 = '403 Forbidden'
    HTTP_405 = '405 Method Not Allowed'
    HTTP_404 = '404 Not Found'
    HTTP_409 = '409 Conflict'
    HTTP_500 = '500 Internal Server Error'

    HTTP_OK = HTTP_200
    HTTP_CREATED = HTTP_201
    HTTP_NO_CONTENT = HTTP_204
    HTTP_BAD_REQUEST = HTTP_400
    HTTP_FORBIDDEN = HTTP_403
    HTTP_NOT_FOUND = HTTP_404
    HTTP_METHOD_NOT_ALLOWED = HTTP_405
    HTTP_CONFLICT = HTTP_409
    HTTP_INTERNAL_SERVER_ERROR = HTTP_500
    OK_STATUS_LIST = (HTTP_OK, HTTP_CREATED, HTTP_NO_CONTENT)

    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_404_NOT_FOUND = 404

    _list = {'errors': []}
    _logger = Logger.get_logger(__name__)

    @classmethod
    def reset(cls):
        """Reset cause to initial value."""

        cause = cls.get_message()
        cls._list = {'errors': []}

        return cause

    @classmethod
    def push(cls, status, message):
        """Append cause to list.

        Message will always contain only the string till the first newline.
        The reason is that the message may be coming from an exception which
        message may contain multiple lines. In this case it is always assumed
        that the first line contains the actual exception message. The whole
        message is always printed into log.

        Args:
            status (str): One of the predefined HTTP status codes.
            message (str): Description of the cause.

        Examples
        --------
        >>> Cause.push(Cause.HTTP_CREATED, 'content created')
        """

        # Optimization: Prevent setting the caller module and line number in case
        # of success causes. Reading of the line number requires file access that
        # is expensive and avoided in successful cases.
        caller = 'snippy.cause.cause.optimize:1'
        if status not in Cause.OK_STATUS_LIST:
            caller = cls._caller()
        cls._logger.debug('cause %s with message %s from %s', status, message, caller)
        cls._list['errors'].append({
            'status': int(status.split()[0]),
            'status_string': status,
            'module': caller,
            'title': message.splitlines()[0]
        })

    @classmethod
    def insert(cls, status, message):
        """Insert cause as a first cause.

        Args:
            status (str): One of the predefined HTTP status codes.
            message (str): Description of the cause.

        Examples
        --------
        >>> Cause.insert(Cause.HTTP_CREATED, 'content created')
        """

        cls.push(status, message)
        cls._list['errors'].insert(0, cls._list['errors'].pop())

    @classmethod
    def is_ok(cls):
        """Test if errors were detected.

        The status is considered ok in following cases:

          1. There are no errors at all.
          2. There are only accepted error codes.
          3. Content has been created without internal errors.

        The last case is a special case. The problem is that currently the case
        where multiple contents are imported when some of them fail due to data
        already existing is considered successful. That is, user should get OK
        when importing a list of data when some of them are already imported.
        For this reason, the Created is searched without internal error.

        The UUID collision is considered internal error because that field is
        set by the application.

        Returns:
            bool: Define if the cause list can be considered ok.
        """

        is_ok = False
        if not cls._list['errors']:
            is_ok = True
        elif len(cls._list['errors']) == 1 and cls._list['errors'][0]['status_string'] in Cause.OK_STATUS_LIST:
            is_ok = True
        elif all(error['status_string'] in Cause.OK_STATUS_LIST for error in cls._list['errors']):
            is_ok = True
        elif not cls._is_internal_error() and any(error['status_string'] == cls.HTTP_CREATED for error in cls._list['errors']):
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
        response['meta'] = {
            'version': __version__,
            'homepage': __homepage__,
            'docs': __docs__,
            'openapi': __openapi__
        }

        return response

    @classmethod
    def get_message(cls):
        """Return cause message.

        Cause codes follow the same rules as the logs with the title or
        message. If there are variables within the message, the variables
        are separated with colon. The end user message is beautified so
        that if there is more than one colon, it indicates that variable
        is in the middle of the message. This is not considered good layout
        for command line interface messages.

        How ever, if there is only one colon, it is used to sepatate the
        last part which is considered clear for user.

        Because of these rules, the colon delimiters are removed only if
        there is more than one.

        Examples:

            1. cannot use empty content uuid for: delete :operation
            2. cannot find content with content uuid: 1234567
        """

        cause = Cause.ALL_OK
        if not cls.is_ok():
            message = cls._list['errors'][0]['title']
            if message.count(':') > 1:
                message = cls._list['errors'][0]['title'].replace(':', '')
            cause = 'NOK: ' + message

        return cause

    @classmethod
    def print_message(cls):
        """Print cause message."""

        Logger.print_status(cls.get_message())

    @classmethod
    def print_failure(cls):
        """Print only failure message."""

        if not cls.is_ok():
            Logger.print_status(cls.get_message())

    @classmethod
    def debug(cls):
        """Debug Cause."""

        for idx, cause in enumerate(cls._list['errors']):
            print('cause[%d]:' % idx)
            print('  status : %s\n'
                  '  string : %s\n'
                  '  module : %s\n'
                  '  title  : %s\n' % (cause['status'], cause['status_string'], cause['module'], cause['title']))

    @classmethod
    def _is_internal_error(cls):
        """Test if internal error was detected."""

        if any(error['status_string'] == cls.HTTP_INTERNAL_SERVER_ERROR for error in cls._list['errors']):
            return True

        return False

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
