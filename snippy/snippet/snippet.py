#!/usr/bin/env python3

"""snippet.py: Snippet management."""

from snippy.logger import Logger
from snippy.config import Config


class Snippet(object):
    """Snippet management."""

    def __init__(self):
        self.logger = Logger().get()
        self.storage = None

    def add(self):
        """Add new snippet."""

        self.logger.info('add new snippet')
        self.storage.store(Config.get_snippet(), Config.get_tags(), Config.get_comment(), Config.get_link())

    def find_keywords(self):
        """Find snippets based on keywords."""

        self.logger.info('find snippet based on keywords')
        self.storage.search(Config.get_find_keywords())

    def run(self, storage):
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        self.storage = storage
        if Config.has_snippet():
            self.add()
        elif Config.has_find_keywords():
            self.find_keywords()
        else:
            self.logger.error('unknown action for snippet')
