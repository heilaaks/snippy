#!/usr/bin/env python3

"""cause.py: Cause code management."""

import inspect
from snippy.logger import Logger


class Cause(object):
    """Cause code management."""

    # Cause: ok
    ALL_OK = 'OK'

    # Cause: Database
    DB_INSERT_OK = 'insert-ok'
    DB_UPDATE_OK = 'update-ok'
    DB_DELETE_OK = 'delete-ok'
    DB_DUPLICATE = 'unique-constraint-violation'
    DB_FAILURE = 'internal-failure'
    DB_ENTRY_NOT_FOUND = 'not-found'

    # Cause: Editor
    EDITOR_FAILURE = 'editor-internal-failure'
    EDITOR_NOT_SUPPORTED = 'editor-not-supported'

    cause = ALL_OK
    logger = Logger(__name__).get()

    @classmethod
    def set(cls, cause):
        """Set failure cause."""

        cls.logger.info('%s from module %s', cause, cls._caller())

        # Only allow one update to get the original cause.
        if cls.cause == Cause.ALL_OK:
            cls.cause = 'NOK: ' + cause

    @classmethod
    def get(cls):
        """Return exit cause for the tool."""

        return cls.cause

    @staticmethod
    def _caller():
        caller = inspect.stack()[2]
        module = inspect.getmodule(caller[0])

        return module.__name__
