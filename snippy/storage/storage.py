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

    def store(self, snippet, brief=None, tags=None, link=None, metadata=None):
        """Store snippet."""

        self.database.insert_snippet(snippet, brief, tags, link, metadata)

    def search(self, keywords):
        """Search snippets."""

        return self.database.select_snippets(keywords)

    def export(self):
        """Export all snippets."""

        return self.database.select_all_snippets()

    def delete(self, db_index):
        """Delete snippet."""

        return self.database.delete_snippet(db_index)

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()
