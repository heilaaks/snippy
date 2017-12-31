#!/usr/bin/env python3

"""validate.py - Validate REST API input."""

from snippy.logger.logger import Logger


class Validate(object):  # pylint: disable=too-few-public-methods
    """Validate REST API input."""

    _logger = None

    def __init__(self):
        if not Validate._logger:
            Validate._logger = Logger(__name__).get()

    @classmethod
    def collection(cls, media):
        """Return media as collection of contents."""

        collection = []
        try:
            if isinstance(media, dict):
                collection.append(media)
                collection = tuple(collection)
            elif isinstance(media, (list, tuple)):
                collection = tuple(media)
            else:
                cls._logger.info('media ignored because of unknown type %s', media)
        except ValueError:
            cls._logger.info('media validation failed and it was ignored %s', media)

        return collection
