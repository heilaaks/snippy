#!/usr/bin/env python3

"""sqlite3_db_helper.py: Helper methods for Sqlite3 database testing."""

import sqlite3


class Sqlite3DbHelper(object): # pylint: disable=too-few-public-methods
    """Helper methods for Sqlite3 database testing."""

    def __init__(self):
        self.conn, self.cursor = Sqlite3DbHelper._connect_db()

    def select_all_snippets(self):
        """Select all snippets."""

        self.cursor.execute('select * from snippets')
        rows = self.cursor.fetchall()

        return rows

    @staticmethod
    def _connect_db():
        """Connect to shared memory database."""

        conn = sqlite3.connect('file::memory:?cache=shared', check_same_thread=False, uri=True)
        cursor = conn.cursor()

        return (conn, cursor)
