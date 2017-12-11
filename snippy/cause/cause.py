#!/usr/bin/env python3

"""cause.py: Cause code management."""

import inspect
import json
from snippy.metadata import __version__
from snippy.metadata import __homepage__
from snippy.logger.logger import Logger


class Cause(object):
    """Cause code management."""

    ALL_OK = 'OK'

    HTTP_OK = '200 OK'
    HTTP_CREATED = '201 Created'
    HTTP_NO_CONTENT = '204 No Content'
    HTTP_BAD_REQUEST = '400 Bad Request'
    HTTP_NOT_FOUND = '404 Not Found'
    HTTP_METHOD_NOT_ALLOWED = '405 Method Not Allowed'
    HTTP_INTERNAL_SERVER_ERROR = '500 Internal Server Error'
    OK_STATUS = (HTTP_OK, HTTP_CREATED, HTTP_NO_CONTENT)

    _logger = None
    _text = ALL_OK
    _list = {'errors': []}

    def __init__(self):
        if not Cause._logger:
            Cause._logger = Logger(__name__).get()

    @classmethod
    def reset(cls):
        """Reset cause to initial value."""

        cause = cls._text
        cls._text = Cause.ALL_OK

        return cause

    @classmethod
    def push(cls, status, message):
        """Append cause to list."""

        cls._logger.info('status %s with message %s from %s', status, message, cls._caller())
        cls._list['errors'].append({'code': int(status.split()[0]),
                                    'status': status,
                                    'module': cls._caller(),
                                    'message': message})

    @classmethod
    def shift(cls):
        """Return the first cause in the list."""

        if cls._list['errors']:
            cause = cls._list['errors'][0]['message']
        else:
            cause = Cause.ALL_OK

        return cause

    @classmethod
    def is_ok(cls):
        """Test if errors were detected."""

        is_ok = True
        if cls._list['errors']:
            is_ok = False
        elif len(cls._list['errors']) == 1 and cls._list['errors'][0]['status'] not in Cause.OK_STATUS:
            is_ok = False

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
    def set_text(cls, cause_text):
        """Set cause text."""

        cls._logger.info('%s from module %s', cause_text, cls._caller())

        # Only allow one update to get the original cause.
        if cls._text == Cause.ALL_OK:
            cls._text = 'NOK: ' + cause_text

    @classmethod
    def get_text(cls):
        """Return cause text."""

        return cls._text

    @staticmethod
    def _caller():
        caller = inspect.stack()[2]
        info = inspect.getframeinfo(caller[0])
        module = inspect.getmodule(caller[0])
        location = module.__name__ + ':' + str(info.lineno)

        return location
