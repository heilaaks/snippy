#!/usr/bin/env python3

"""storage.py: Storage management."""

import hashlib
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

        return self

    def create(self, snippet):
        """Create snippet."""

        snippet['digest'] = Storage._hash(snippet)
        return self.database.insert_snippet(snippet)

    def search(self, keywords=None, digest=None, content=None):
        """Search snippets."""

        return self.database.select_snippets(keywords, digest, content)

    def update(self, digest, snippet):
        """Update snippet."""

        snippet['digest'] = Storage._hash(snippet)

        return self.database.update_snippet(digest, snippet)

    def export_snippets(self):
        """Export all snippets."""

        return self.database.select_all_snippets()

    def import_snippets(self, snippets):
        """Import all given snippets."""

        for snippet in snippets['snippets']:
            snippet['digest'] = Storage._hash(snippet)

        return self.database.bulk_insert_snippets(snippets['snippets'])

    def delete(self, digest):
        """Delete snippet."""

        return self.database.delete_snippet(digest)

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()

    @staticmethod
    def _hash(data_dictionary):
        """Calculate digest for the data."""

        data_string = ''.join(['%s::%s' % (key, value) for (key, value) in sorted(data_dictionary.items())])

        return hashlib.blake2s(data_string.encode('UTF-8')).hexdigest()
