#!/usr/bin/env python3

"""api.py: Api parameter management."""

from __future__ import print_function
from snippy.logger.logger import Logger


class Api(object):  # pylint: disable=too-few-public-methods
    """Api parameter management."""

    args = {}
    logger = {}

    def __init__(self):
        Api.logger = Logger(__name__).get()
