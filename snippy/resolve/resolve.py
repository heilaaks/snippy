#!/usr/bin/env python3

"""resolve.py: Resolve management."""

from snippy.logger import Logger


class Resolve(object):
    """Resolve management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def add(self):
        """Add new resolution."""

        self.logger.info('add new resolution')

    def run(self):
        """Run the snippet management task."""

        self.logger.info('managing resolution')
