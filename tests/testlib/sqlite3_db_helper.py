#!/usr/bin/env python3

"""sqlite3_db_helper.py: Helper methods for Sqlite3 database testing."""

import sqlite3
from snippy.logger import Logger


class Sqlite3DbHelper(object): # pylint: disable=too-few-public-methods
    """Helper methods for Sqlite3 database testing."""

    def __init__(self):
        self.logger = Logger().get()
        self.conn, self.cursor = self._connect_db()

    def select_snippet(self, snippet_id):
        """Select requested snippet with unique ID."""

        self.logger.debug('select snippet with id {:d}'.format(snippet_id))
        self.cursor.execute('select * from snippets')
        rows = self.cursor.fetchall()
        for row in rows:
            self.logger.debug("fetched row %s", row)

    def select_all_snippets(self):
        """Select all snippets."""

        self.cursor.execute('select * from snippets')
        rows = self.cursor.fetchall()
        for row in rows:
            self.logger.debug("fetched row %s", row)

        return rows

    def _connect_db(self):
        """Connect to shared memory database."""

        self.logger.debug("connect to sqlite3 database")
        conn = sqlite3.connect('file::memory:?cache=shared', check_same_thread=False, uri=True)
        cursor = conn.cursor()

        return (conn, cursor)
