#!/usr/bin/env python3

"""sqlite3_db.py: Database management."""

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

        self.conn, self.cursor = self.__create_db()

        #if os.path.exists(Config.get_storage_path()):
        #    self.conn, self.cursor = self.__create_db(Config.get_storage_file())
        #else:
        #    self.logger.error('storage path does not exist {:s}'.format(Config.get_storage_path()))

    def disconnect(self):
        """Close database connection."""

        if self.conn is not None:
            try:
                self.cursor.close()
                self.conn.close()
                self.logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self.logger.exception('closing sqlite3 database failed with exception "%s"', exception)

    def debug(self):
        """Dump the whole database."""

        if self.conn is not None:
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.logger.debug('sqlite3 dump %s', self.cursor.fetchall())
            except sqlite3.Error as exception:
                self.logger.exception('dumping sqlite3 database failed with exception "%s"', exception)

    def __create_db(self):
        """Create the database."""

        database = self.__get_database()
        try:
            conn = sqlite3.connect(database, check_same_thread=False, uri=True)
            cursor = conn.cursor()
            with open(Config.get_storage_schema(), 'rt') as schema_file:
                schema = schema_file.read()
                conn.executescript(schema)
            self.logger.debug('initialized sqlite3 database into {:s}'.format(database))
        except sqlite3.Error as exception:
            self.logger.exception('creating sqlite3 database failed with exception "%s"', exception)

        return (conn, cursor)

    @staticmethod
    def __get_database():
        """Get the database connection string."""

        if Config.is_storage_in_memory():
            database = "file::memory:?cache=shared"
        else:
            database = Config.get_storage_file()

        return database
