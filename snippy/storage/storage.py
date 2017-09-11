#!/usr/bin/env python3

"""storage.py: Storage management."""

import hashlib
from snippy.config import Constants as Const
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

        digest = Storage._calculate_digest(snippet)
        return self.database.insert_snippet(snippet, digest)

    def search(self, keywords=None, digest=None, content=None):
        """Search snippets."""

        rows = self.database.select_snippets(keywords, digest, content)
        snippets = Storage._get_tuple_list(rows)

        return snippets

    def update(self, digest_updated, snippet):
        """Update snippet."""

        digest = Storage._calculate_digest(snippet)

        self.database.update_snippet(snippet, digest_updated, digest)

    def export_snippets(self):
        """Export all snippets."""

        rows = self.database.select_all_snippets()
        snippets = Storage._get_tuple_list(rows)

        return snippets

    def import_snippets(self, snippets):
        """Import all given snippets."""

        for snippet in snippets['snippets']:
            snippet['digest'] = Storage._calculate_digest(snippet)

        return self.database.bulk_insert_snippets(snippets['snippets'])

    def delete(self, digest):
        """Delete snippet."""

        return self.database.delete_snippet(digest)

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def convert_to_dictionary(self, snippets):
        """Convert snippets to dictionary format."""

        snippet_list = []
        self.logger.debug('creating dictionary from snippets')
        for snippet in snippets:
            snippet_list.append(Storage._get_dictionary(snippet))

        return snippet_list

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()

    @staticmethod
    def _calculate_digest(snippet):
        """Calculate digest for the data."""

        data_string = Storage._get_string(snippet)
        digest = hashlib.sha256(data_string.encode('UTF-8')).hexdigest()

        return digest

    @staticmethod
    def _get_tuple_list(rows):
        """Convert snippets from database to list of tuples."""

        snippets = []
        for row in rows:
            snippets.append(Storage._get_tuple(row))

        return snippets

    @staticmethod
    def _get_tuple(row):
        """Convert single row from database to snippet in tuple."""

        snippet = (row[Const.SNIPPET_CONTENT],
                   row[Const.SNIPPET_BRIEF],
                   row[Const.SNIPPET_GROUP],
                   row[Const.SNIPPET_TAGS].split(Const.DELIMITER_TAGS),
                   row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS),
                   row[Const.SNIPPET_DIGEST],
                   row[Const.SNIPPET_METADATA],
                   row[Const.SNIPPET_ID])

        return snippet

    @staticmethod
    def _get_dictionary(snippet):
        """Convert snippet to dictionary format."""

        result = {'content': snippet[Const.SNIPPET_CONTENT],
                  'brief': snippet[Const.SNIPPET_BRIEF],
                  'groups': snippet[Const.SNIPPET_GROUP],
                  'tags': snippet[Const.SNIPPET_TAGS],
                  'links': snippet[Const.SNIPPET_LINKS],
                  'digest': snippet[Const.SNIPPET_DIGEST]}

        return result

    @staticmethod
    def _get_string(snippet):
        """Convert snippet to single string."""

        result = Const.EMPTY.join(snippet[Const.SNIPPET_CONTENT:Const.SNIPPET_TAGS])
        result = result + Const.EMPTY.join(sorted(snippet[Const.SNIPPET_TAGS]))
        result = result + Const.EMPTY.join(sorted(snippet[Const.SNIPPET_LINKS]))

        return result
