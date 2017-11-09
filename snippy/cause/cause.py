#!/usr/bin/env python3

"""cause.py: Cause code management."""

import inspect
from snippy.logger.logger import Logger


class Cause(object):
    """Cause code management."""

    ALL_OK = 'OK'

    cause_text = ALL_OK
    logger = Logger(__name__).get()

    @classmethod
    def reset(cls):
        """Reset the cause to initial state."""

        cause = cls.cause_text
        cls.cause_text = Cause.ALL_OK

        return cause

    @classmethod
    def set_text(cls, cause_text):
        """Set failure cause."""

        cls.logger.info('%s from module %s', cause_text, cls._caller())

        # Only allow one update to get the original cause.
        if cls.cause_text == Cause.ALL_OK:
            cls.cause_text = 'NOK: ' + cause_text

    @classmethod
    def get_text(cls):
        """Return cause in text format."""

        return cls.cause_text

    @staticmethod
    def _caller():
        caller = inspect.stack()[2]
        module = inspect.getmodule(caller[0])

        return module.__name__
