#!/usr/bin/env python3

"""storage.py: Storage management."""

from snippy.logger import Logger
from snippy.storage.database import Sqlite3Db as Database


class Storage(object):
    """Storage management for snippets."""

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.database = Database()

    def init(self):
        """Initialize storage."""

        self.database.init()

    def store(self, snippet, brief=None, category=None, tags=None, links=None, metadata=None):
        """Store snippet."""

        self.database.insert_snippet(snippet, brief, category, tags, links, metadata)

    def search(self, keywords):
        """Search snippets."""

        return self.database.select_snippets(keywords)

    def export_snippets(self):
        """Export all snippets."""

        return self.database.select_all_snippets()

    def import_snippets(self, snippets):
        """Import all given snippets."""

        return self.database.bulk_insert_snippets(snippets['snippets'])

    def delete(self, db_index):
        """Delete snippet."""

        return self.database.delete_snippet(db_index)

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()
