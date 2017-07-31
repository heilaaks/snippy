#!/usr/bin/env python3

"""sqlite3_db.py: Database management."""

import os
import sys
import sqlite3
from snippy.logger import Logger
from snippy.config import Config


class Sqlite3Db(object):
    """Sqlite3 database management."""

    def __init__(self):
        self.logger = Logger().get()
        self.conn = None
        self.cursor = None

    def init(self):
        """Initialize database."""

        self.conn, self.cursor = self._create_db()

    def disconnect(self):
        """Close database connection."""

        if self.conn:
            try:
                self.cursor.close()
                self.cursor = None
                self.conn.close()
                self.conn = None
                self.logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self.logger.exception('closing sqlite3 database failed with exception "%s"', exception)

    def insert_snippet(self, snippet, tags=None, comment=None, link=None, metadata=None):
        """Insert snippet into database."""

        if self.conn:
            try:
                tags_string = ','.join(map(str, tags))
                query = ('insert into snippet(snippet, tags, comment, link, metadata) values(?,?,?,?,?)')
                self.logger.debug('insert snippet {:s} with tags {:s}'.format(snippet, tags_string))
                self.cursor.execute(query, (snippet, tags_string, comment, link, metadata))
                self.conn.commit()
            except sqlite3.Error as exception:
                self.logger.exception('inserting into sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

    def debug(self):
        """Dump the whole database."""

        if self.conn:
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.logger.debug('sqlite3 dump %s', self.cursor.fetchall())
            except sqlite3.Error as exception:
                self.logger.exception('dumping sqlite3 database failed with exception "%s"', exception)

    def _create_db(self):
        """Create the database."""

        location = self._get_db_location()
        try:
            conn = sqlite3.connect(location, check_same_thread=False, uri=True)
            cursor = conn.cursor()
            with open(Config.get_storage_schema(), 'rt') as schema_file:
                schema = schema_file.read()
                conn.executescript(schema)
            self.logger.debug('initialized sqlite3 database into {:s}'.format(location))
        except sqlite3.Error as exception:
            self.logger.exception('creating sqlite3 database failed with exception "%s"', exception)

        return (conn, cursor)

    def _get_db_location(self):
        """Get the location where there the database is going to be stored."""

        location = ''
        if Config.is_storage_in_memory():
            location = "file::memory:?cache=shared"
        else:
            if os.path.exists(Config.get_storage_path()) and os.access(Config.get_storage_path(), os.W_OK):
                location = Config.get_storage_file()
            else:
                self.logger.error('storage path does not exist or is not accessible: {:s}'.format(Config.get_storage_path()))

                sys.exit('storage path does not exist or is not accessible: {:s}'.format(Config.get_storage_path()))

        return location
