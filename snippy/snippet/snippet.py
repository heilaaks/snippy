#!/usr/bin/env python3

"""snippet.py: Snippet management."""

from snippy.logger import Logger


class Snippet(object):
    """Snippet management."""

    def __init__(self):
        self.logger = Logger().get()
        self.storage = None

    def add(self):
        """Add new snippet."""

        self.logger.info('add new snippet')

    def run(self, storage):
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        self.storage = storage
