#!/usr/bin/env python3

"""storage.py: Storage management."""

from snippy.logger import Logger
from snippy.storage.database import Sqlite3Db as Database


class Storage(object):
    """Storage management for snippets."""

    def __init__(self):
        self.logger = Logger().get()
        self.database = Database()

    def init(self):
        """Initialize storage."""

        self.database.init()

    def store(self, snippet, tags=None, comment=None, link=None, metadata=None):
        """Store snippet."""

        self.database.insert_snippet(snippet, tags, comment, link, metadata)

    def search(self, keywords):
        """Search snippet."""

        self.database.select_snippet(keywords)

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()
