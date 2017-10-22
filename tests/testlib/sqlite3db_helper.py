#!/usr/bin/env python3

"""sqlite3db_helper.py: Helper methods for Sqlite3 database testing."""

import sqlite3
import os.path
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.storage.storage import Storage


class Sqlite3DbHelper(object):
    """Helper methods for Sqlite3 database testing."""


    @staticmethod
    def select_all_snippets():
        """Select all snippets."""

        conn, cursor = Sqlite3DbHelper._connect_db()
        cursor.execute('SELECT * FROM contents')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return rows

    @staticmethod
    def get_contents():
        """Return database as content tuple."""

        conn, cursor = Sqlite3DbHelper._connect_db()
        cursor.execute('SELECT * FROM contents')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return Storage()._get_contents(rows)  # pylint: disable=protected-access

    @staticmethod
    def get_solutions():
        """Return solutions from database as content tuple."""

        conn, cursor = Sqlite3DbHelper._connect_db()
        query = ('SELECT * FROM contents WHERE category=?')
        qargs = ['solution']
        try:
            cursor.execute(query, qargs)
            rows = cursor.fetchall()
        except sqlite3.Error as exception:
            print(exception)
        cursor.close()
        conn.close()

        return Storage()._get_contents(rows)  # pylint: disable=protected-access

    @staticmethod
    def delete_all_snippets():
        """Delete all snippets."""

        # In successful case the database table does not exist anymore
        conn, cursor = Sqlite3DbHelper._connect_db()
        try:
            cursor.execute('DELETE FROM contents')
            conn.commit()
        except sqlite3.OperationalError:
            pass
        cursor.close()
        conn.close()

    @staticmethod
    def get_schema():
        """Return the file where the database schema is located."""

        schema = os.path.join(pkg_resources.resource_filename('snippy', 'data/config'), 'database.sql')

        return  schema

    @staticmethod
    def get_storage():
        """Return the file where the database is located."""

        # Sqlite3 in Python2 does not support shared memory databases.
        # Because of this, the database is stored on disk.
        if not Const.PYTHON2:
            storage = 'file::memory:?cache=shared'
        else:
            storage = os.path.join(pkg_resources.resource_filename('snippy', 'data/storage'), 'snippy-test.db')

        return storage

    @staticmethod
    def delete_storage():
        """Delete the database file created for the test."""

        # The file based database is used in testing only in case of Python2.
        if Const.PYTHON2:
            os.remove(Sqlite3DbHelper.get_storage())

    @staticmethod
    def _connect_db():
        """Connect to shared memory database."""

        if not Const.PYTHON2:
            conn = sqlite3.connect(Sqlite3DbHelper.get_storage(), check_same_thread=False, uri=True)
        else:
            conn = sqlite3.connect(Sqlite3DbHelper.get_storage(), check_same_thread=False)
        cursor = conn.cursor()

        return (conn, cursor)
