#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""sqlite3db_helper: Helper methods for Sqlite3 database testing."""

from __future__ import print_function
import sqlite3
import os.path
from contextlib import closing
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.storage.storage import Storage


class Sqlite3DbHelper(object):
    """Helper methods for Sqlite3 database testing."""

    @staticmethod
    def get_contents():
        """Return database as content tuple."""

        rows = ()
        connection = Sqlite3DbHelper._connect()
        with closing(connection.cursor()) as cursor:
            cursor.execute('SELECT * FROM contents')
            rows = cursor.fetchall()
        connection.close()

        return Storage()._get_contents(rows)  # pylint: disable=protected-access

    @staticmethod
    def print_contents():
        """Print database content."""

        rows = ()
        connection = Sqlite3DbHelper._connect()
        with closing(connection.cursor()) as cursor:
            cursor.execute('SELECT * FROM contents')
            rows = cursor.fetchall()
        connection.close()

        for content in Storage()._get_contents(rows):  # pylint: disable=protected-access
            print(content)

    @staticmethod
    def get_content(digest):
        """Return content based on digest."""

        rows = ()
        try:
            query = ('SELECT * FROM contents WHERE digest LIKE ?')
            qargs = [digest+'%']
            connection = Sqlite3DbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                rows = cursor.fetchall()
            connection.close()
        except sqlite3.Error as exception:
            print(exception)

        return Storage()._get_contents(rows)  # pylint: disable=protected-access

    @staticmethod
    def get_category(category):
        """Return content based on category."""

        rows = ()
        try:
            query = ('SELECT * FROM contents WHERE category=?')
            qargs = [category]
            connection = Sqlite3DbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                rows = cursor.fetchall()
            connection.close()
        except sqlite3.Error as exception:
            print(exception)

        return Storage()._get_contents(rows)  # pylint: disable=protected-access

    @staticmethod
    def get_snippets():
        """Return snippets from database as content tuple."""

        return Sqlite3DbHelper.get_category(Const.SNIPPET)

    @staticmethod
    def get_solutions():
        """Return solutions from database as content tuple."""

        return Sqlite3DbHelper.get_category(Const.SOLUTION)

    @staticmethod
    def delete_all_contents():
        """Delete all content from database."""

        # In successful case the database table does not exist anymore
        try:
            connection = Sqlite3DbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute('DELETE FROM contents')
                connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            pass

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
            filename = Sqlite3DbHelper.get_storage()
            if os.path.isfile(filename):
                try:
                    os.remove(filename)
                except OSError:
                    pass

    @staticmethod
    def select_all_snippets():
        """Select all rows from database. DEPRECATED."""

        rows = ()
        connection = Sqlite3DbHelper._connect()
        with closing(connection.cursor()) as cursor:
            cursor.execute('SELECT * FROM contents')
            rows = cursor.fetchall()
        connection.close()

        return rows

    @staticmethod
    def _connect():
        """Connect to database."""

        if not Const.PYTHON2:
            connection = sqlite3.connect(Sqlite3DbHelper.get_storage(), check_same_thread=False, uri=True)
        else:
            connection = sqlite3.connect(Sqlite3DbHelper.get_storage(), check_same_thread=False)

        return connection
