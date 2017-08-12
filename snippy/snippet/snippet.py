#!/usr/bin/env python3

"""snippet.py: Snippet management."""

from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config


class Snippet(object):
    """Snippet management."""

    def __init__(self):
        self.logger = Logger().get()
        self.storage = None

    def add(self):
        """Add new snippet."""

        self.logger.debug('adding new snippet')
        self.storage.store(Config.get_snippet(), Config.get_brief(), Config.get_tags(), Config.get_link())

    def find_keywords(self):
        """Find snippets based on keywords."""

        self.logger.info('finding snippet based on keywords')

        return self.storage.search(Config.get_find_keywords())

    def delete_snippet(self):
        """Delete new snippet."""

        self.logger.debug('deleting snippet')

        return self.storage.delete(Config.get_delete_snippet())

    def format_hits(self, hits):
        """Format hits."""

        self.logger.debug('format search hits')

        console = ''
        for idx, row in enumerate(hits):
            console = console + Const.SNIPPET_HEADER_STR % (idx+1, row[Const.SNIPPET_BRIEF], row[Const.SNIPPET_ID])
            console = Const.SNIPPET_SNIPPET_STR % (console, row[Const.SNIPPET_SNIPPET]) + Const.NEWLINE
            console = Const.SNIPPET_LINK_STR % (console, row[Const.SNIPPET_LINK])
            console = Const.SNIPPET_TAGS_STR % (console, row[Const.SNIPPET_TAGS])
            console = console + Const.NEWLINE

        return console

    def print_hits(self, hits):
        """Print hits."""

        self.logger.debug('printing search results')
        print(hits)

    def run(self, storage):
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        self.storage = storage
        if Config.get_snippet():
            self.add()
        elif Config.get_find_keywords():
            hits = self.find_keywords()
            hits = self.format_hits(hits)
            self.print_hits(hits)
        elif Config.get_delete_snippet():
            self.delete_snippet()
        else:
            self.logger.error('unknown action for snippet')
