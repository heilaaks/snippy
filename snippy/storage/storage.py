#!/usr/bin/env python3

"""storage.py: Storage management."""

import hashlib
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.storage.database import Sqlite3Db as Database


class Storage(object):
    """Storage management for both types of content."""

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.database = Database()

    def init(self):
        """Initialize database."""

        self.database.init()

    def create(self, content, table='snippets'):
        """Create content."""

        digest = Storage._calculate_digest(content)
        cause = self.database.insert_content(table, content, digest)

        return cause

    def search(self, keywords=None, digest=None, content=None, table='snippets'):
        """Search content."""

        rows = self.database.select_content(table, keywords, digest, content)
        entries = Storage._get_tuple_list(rows)

        return entries

    def update(self, content, digest_updated, table='snippets'):
        """Update content."""

        digest = Storage._calculate_digest(content)
        self.database.update_content(table, content, digest_updated, digest)

    def export_content(self, table='snippets'):
        """Export content."""

        rows = self.database.select_all_content(table)
        content = Storage._get_tuple_list(rows)

        return content

    def import_content(self, contents, table='snippets'):
        """Import contents."""

        return self.database.bulk_insert_content(table, contents)

    def delete(self, digest, table='snippets'):
        """Delete content."""

        cause = self.database.delete_content(table, digest)

        return cause

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    @staticmethod
    def convert_to_dictionary(contents):
        """Convert content to dictionary format."""

        content_list = []
        for entry in contents:
            content_list.append(Storage._get_dictionary(entry))

        return content_list

    @staticmethod
    def convert_from_dictionary(contents):
        """Convert content from dictionary format."""

        content_list = []
        for entry in contents:
            content_list.append(Storage._get_tuple_from_dictionary(entry))

        return content_list

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

    @staticmethod
    def _get_tuple_from_dictionary(dictionary):
        """Convert single dictionary entry into tuple."""

        content = [dictionary['content'],
                   dictionary['brief'],
                   dictionary['group'],
                   dictionary['tags'],
                   dictionary['links']]
        digest = Storage._calculate_digest(content)
        content.append(digest)

        return tuple(content)

    @staticmethod
    def _get_dictionary(content):
        """Convert content into dictionary."""

        dictionary = {'content': content[Const.CONTENT],
                      'brief': content[Const.BRIEF],
                      'group': content[Const.GROUP],
                      'tags': content[Const.TAGS],
                      'links': content[Const.LINKS],
                      'digest': content[Const.DIGEST],
                      'utc': content[Const.UTC]}

        return dictionary

    @staticmethod
    def _calculate_digest(content):
        """Calculate digest for the data."""

        data_string = Storage._get_string(content)
        digest = hashlib.sha256(data_string.encode('UTF-8')).hexdigest()

        return digest

    @staticmethod
    def _get_string(content):
        """Convert content into one string."""

        content_str = Const.EMPTY.join(map(str, content[Const.CONTENT]))
        content_str = content_str + Const.EMPTY.join(content[Const.BRIEF:Const.TAGS])
        content_str = content_str + Const.EMPTY.join(sorted(content[Const.TAGS]))
        content_str = content_str + Const.EMPTY.join(sorted(content[Const.LINKS]))

        return content_str
