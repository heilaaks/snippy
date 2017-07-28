#!/usr/bin/env python3

"""database.py: Database management."""

import os
import sqlite3
from snippy.logger import Logger
from snippy.config import Config


class Database(object):
    """Database management."""

    def __init__(self):
        self.logger = Logger().get()
        self.conn = None
        self.cursor = None

    def init(self):
        """Initialize database."""

        if os.path.exists(Config.get_storage_path()):
            self.conn, self.cursor = self.__create_db(Config.get_storage_file())
        else:
            self.logger.error('storage path does not exist {:s}'.format(Config.get_storage_path()))

    def __create_db(self, snippy_db):
        """Create the database."""

        try:
            conn = sqlite3.connect(snippy_db, check_same_thread=False)
            cursor = conn.cursor()
            with open(Config().get_storage_schema(), 'rt') as schema:
                schema = schema.read()
                conn.executescript(schema)
            self.logger.debug('initialized sqlite3 database into {:s}'.format(snippy_db))
        except sqlite3.Error as exception:
            self.logger.error('creating sqlite3 database failed with exception {}'.format(exception))

        return (conn, cursor)

    def disconnect(self):
        """Close database connection."""

        if self.conn is not None:
            try:
                self.cursor.close()
                self.conn.close()
                self.logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self.logger.error('closing sqlite3 database failed with exception {:s}'.format(exception))

    def debug(self):
        """Dump the whole databse."""

        if self.conn is not None:
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.logger.debug('sqlite3 dump {}'.format(self.cursor.fetchall()))
            except sqlite3.Error as exception:
                self.logger.error('dumping sqlite3 database failed with exception {}'.format(exception))
