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
        self.database.init()

    def create(self, snippet):
        """Create snippet."""

        digest = Storage._calculate_digest(snippet)
        cause = self.database.insert_snippet(snippet, digest)

        return cause

    def search(self, keywords=None, digest=None, content=None):
        """Search snippets."""

        rows = self.database.select_snippets(keywords, digest, content)
        snippets = Storage._get_tuple_list(rows)

        return snippets

    def update(self, snippet, digest_updated):
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

        return self.database.bulk_insert_snippets(snippets)

    def delete(self, digest):
        """Delete snippet."""

        cause = self.database.delete_snippet(digest)

        return cause

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    @staticmethod
    def convert_to_dictionary(snippets):
        """Convert snippets to dictionary format."""

        snippet_list = []
        for snippet in snippets:
            snippet_list.append(Storage._get_dictionary(snippet))

        return snippet_list

    @staticmethod
    def convert_from_dictionary(snippets):
        """Convert snippets from dictionary format."""

        snippet_list = []
        for snippet in snippets:
            snippet_list.append(Storage._get_tuple_from_dictionary(snippet))

        return snippet_list

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()

    @staticmethod
    def _get_tuple_list(rows):
        """Convert snippets from database to list of tuples."""

        snippets = []
        for row in rows:
            snippets.append(Storage._get_tuple_from_db_row(row))

        return snippets

    @staticmethod
    def _get_tuple_from_db_row(row):
        """Convert single row from database to snippet in tuple."""

        snippet = (row[Const.SNIPPET_CONTENT],
                   row[Const.SNIPPET_BRIEF],
                   row[Const.SNIPPET_GROUP],
                   row[Const.SNIPPET_TAGS].split(Const.DELIMITER_TAGS),
                   row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS),
                   row[Const.SNIPPET_DIGEST],
                   row[Const.SNIPPET_UTC],
                   row[Const.SNIPPET_METADATA],
                   row[Const.SNIPPET_ID])

        return snippet

    @staticmethod
    def _get_tuple_from_dictionary(dictionary):
        """Convert single dictionary entry into tuple."""

        snippet = [dictionary['content'],
                   dictionary['brief'],
                   dictionary['group'],
                   dictionary['tags'],
                   dictionary['links']]
        digest = Storage._calculate_digest(snippet)
        snippet.append(digest)

        return tuple(snippet)

    @staticmethod
    def _get_dictionary(snippet):
        """Convert snippet to dictionary."""

        dictionary = {'content': snippet[Const.SNIPPET_CONTENT],
                      'brief': snippet[Const.SNIPPET_BRIEF],
                      'group': snippet[Const.SNIPPET_GROUP],
                      'tags': snippet[Const.SNIPPET_TAGS],
                      'links': snippet[Const.SNIPPET_LINKS],
                      'digest': snippet[Const.SNIPPET_DIGEST],
                      'utc': snippet[Const.SNIPPET_UTC]}

        return dictionary

    @staticmethod
    def _calculate_digest(snippet):
        """Calculate digest for the data."""

        data_string = Storage._get_string(snippet)
        digest = hashlib.sha256(data_string.encode('UTF-8')).hexdigest()

        return digest

    @staticmethod
    def _get_string(snippet):
        """Convert snippet to one string."""

        snippet_str = Const.EMPTY.join(snippet[Const.SNIPPET_CONTENT:Const.SNIPPET_TAGS])
        snippet_str = snippet_str + Const.EMPTY.join(sorted(snippet[Const.SNIPPET_TAGS]))
        snippet_str = snippet_str + Const.EMPTY.join(sorted(snippet[Const.SNIPPET_LINKS]))

        return snippet_str
