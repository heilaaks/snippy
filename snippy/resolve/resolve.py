#!/usr/bin/env python3

"""resolve.py: Resolve management."""

from snippy.logger import Logger


class Resolve(object):
    """Resolve management."""

    def __init__(self):
        self.logger = Logger().get()
        self.storage = None

    def add(self):
        """Add new resolution."""

        self.logger.info('add new resolution')

    def run(self, storage):
        """Run the snippet management task."""

        self.logger.info('managing resolution')
        self.storage = storage
