#!/usr/bin/env python3

"""sqlite3_db_helper.py: Helper methods for Sqlite3 database testing."""

import sqlite3
import os.path
import pkg_resources
from snippy.config import Constants as Const


class Sqlite3DbHelper(object):
    """Helper methods for Sqlite3 database testing."""


    @staticmethod
    def select_all_snippets():
        """Select all snippets."""

        conn, cursor = Sqlite3DbHelper._connect_db()
        cursor.execute('SELECT * FROM snippets')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return rows

    @staticmethod
    def delete_all_snippets():
        """Delete all snippets."""

        # In successful case the database table does not exist anymore
        conn, cursor = Sqlite3DbHelper._connect_db()
        try:
            cursor.execute('DELETE FROM snippets')
            conn.commit()
        except sqlite3.OperationalError:
            pass
        cursor.close()
        conn.close()

    @staticmethod
    def get_schema():
        """Return the file where the database schema is located."""

        return os.path.join(pkg_resources.resource_filename('snippy', 'data/config'), 'database.sql')

    @staticmethod
    def _connect_db():
        """Connect to shared memory database."""

        if not Const.PYTHON2:
            conn = sqlite3.connect('file::memory:?cache=shared', check_same_thread=False, uri=True)
        else:
            conn = sqlite3.connect('file::memory:?cache=shared', check_same_thread=False)
        cursor = conn.cursor()

        return (conn, cursor)
