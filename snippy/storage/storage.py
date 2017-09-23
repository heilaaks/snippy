#!/usr/bin/env python3

"""storage.py: Storage management."""

from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.format import Format
from snippy.storage.database import Sqlite3Db as Database


class Storage(object):
    """Storage management for both types of content."""

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.database = Database()

    def init(self):
        """Initialize database."""

        self.database.init()

    def create(self, category, content):
        """Create content."""

        digest = Format.calculate_digest(content)
        cause = self.database.insert_content(category, content, digest)

        return cause

    def search(self, category, keywords=None, digest=None, content=None):
        """Search content."""

        rows = self.database.select_content(category, keywords, digest, content)
        entries = Storage._get_tuple_list(rows)

        return entries

    def update(self, category, content, digest_updated):
        """Update content."""

        digest = Format.calculate_digest(content)
        self.database.update_content(category, content, digest_updated, digest)

    def delete(self, category, digest):
        """Delete content."""

        cause = self.database.delete_content(category, digest)

        return cause

    def export_content(self, category):
        """Export content."""

        rows = self.database.select_all_content(category)
        content = Storage._get_tuple_list(rows)

        return content

    def import_content(self, category, contents):
        """Import contents."""

        return self.database.bulk_insert_content(category, contents)

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()

    @staticmethod
    def _get_tuple_list(rows):
        """Convert entries from database to list of tuples."""

        contents = []
        for row in rows:
            contents.append(Storage._get_tuple_from_db_row(row))

        return contents

    @staticmethod
    def _get_tuple_from_db_row(row):
        """Convert single row from database into content in a tuple."""

        content = (tuple(row[Const.CONTENT].split(Const.DELIMITER_CONTENT)),
                   row[Const.BRIEF],
                   row[Const.GROUP],
                   tuple(row[Const.TAGS].split(Const.DELIMITER_TAGS)),
                   tuple(row[Const.LINKS].split(Const.DELIMITER_LINKS)),
                   row[Const.DIGEST],
                   row[Const.UTC],
                   row[Const.METADATA],
                   row[Const.KEY])

        return content
