#!/usr/bin/env python3

"""cause.py: Cause code management."""

import sys
import inspect
import json
from snippy.metadata import __version__
from snippy.metadata import __homepage__
from snippy.logger.logger import Logger


class Cause(object):
    """Cause code management."""

    ALL_OK = 'OK'

    HTTP_200 = '200 OK'
    HTTP_201 = '201 Created'
    HTTP_204 = '204 No Content'
    HTTP_400 = '400 Bad Request'
    HTTP_404 = '404 Not Found'
    HTTP_405 = '405 Method Not Allowed'
    HTTP_409 = '409 Conflict'
    HTTP_500 = '500 Internal Server Error'

    HTTP_OK = HTTP_200
    HTTP_CREATED = HTTP_201
    HTTP_NO_CONTENT = HTTP_204
    HTTP_BAD_REQUEST = HTTP_400
    HTTP_NOT_FOUND = HTTP_404
    HTTP_METHOD_NOT_ALLOWED = HTTP_405
    HTTP_CONFLICT = HTTP_409
    HTTP_INTERNAL_SERVER_ERROR = HTTP_500
    OK_STATUS = (HTTP_OK, HTTP_CREATED, HTTP_NO_CONTENT)

    _logger = None
    _list = {'errors': []}

    def __init__(self):
        if not Cause._logger:
            Cause._logger = Logger(__name__).get()

    @classmethod
    def reset(cls):
        """Reset cause to initial value."""

        cause = cls.get_message()
        cls._list = {'errors': []}

        return cause

    @classmethod
    def push(cls, status, message):
        """Append cause to list."""

        caller = cls._caller()
        cls._logger.info('status %s with message %s from %s', status, message, caller)
        cls._list['errors'].append({'code': int(status.split()[0]),
                                    'status': status,
                                    'module': caller,
                                    'message': message})

    @classmethod
    def is_ok(cls):
        """Test if errors were detected."""

        is_ok = False
        if not cls._list['errors']:
            is_ok = True
        elif len(cls._list['errors']) == 1 and cls._list['errors'][0]['status'] in Cause.OK_STATUS:
            is_ok = True
        elif all(error['status'] in Cause.OK_STATUS for error in cls._list['errors']):
            is_ok = True

        # all(item[2] == 0 for item in items)

        return is_ok

    @classmethod
    def http_status(cls):
        """Return the HTTP status."""

        status = Cause.HTTP_OK
        if cls._list['errors']:
            status = cls._list['errors'][0]['status']

        return status

    @classmethod
    def json_message(cls):
        """Return errors in JSON data structure."""

        response = cls._list
        response['metadata'] = {'version': __version__,
                                'homepage': __homepage__}

        return json.dumps(response)

    @classmethod
    def get_message(cls):
        """Return cause message."""

        cause = Cause.ALL_OK
        if not cls.is_ok():
            cause = 'NOK: ' + cls._list['errors'][0]['message']

        return cause

    @staticmethod
    def _caller():
        """Get caller module and code line."""

        # This is optimized: Inspect.stack reads source code file that generates
        # expensive file access. The contenxt loading can be switched off with
        # stack(0) setting /1/. A bit more efficient way is to use sys._getframe
        # that is according to /2/ four times faster the stack(0). Testing shows
        # that there is a noticeable difference but not that much.
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
