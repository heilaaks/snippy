#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""sqlitedb_helper: Helper methods for Sqlite database testing."""

from __future__ import print_function

import os.path
import sqlite3
import uuid
from contextlib import closing

import pkg_resources

from snippy.constants import Constants as Const
from snippy.content.collection import Collection


class SqliteDbHelper(object):
    """Helper methods for Sqlite database testing."""

    VALID_UUID = '11cd5827-b6ef-4067-b5ac-3ceac07dde9f'
    TEST_UUIDS = (
        uuid.UUID(hex='11cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='12cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='13cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='14cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='15cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='16cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='17cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='18cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='19cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='1acd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='1bcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='1ccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='1dcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='1ecd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='1fcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='21cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='22cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='23cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='24cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='25cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='26cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='27cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='28cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='29cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='2acd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='2bcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='2ccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='2dcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='2ecd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='2fcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='31cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='32cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='33cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='34cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='35cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='36cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='37cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='38cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='39cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='3acd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='3bcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='3ccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='3dcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='3ecd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='3fcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='41cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='42cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='43cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='44cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='45cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='46cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='47cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='48cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='49cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='4acd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='4bcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='4ccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='4dcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='4ecd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='4fcd5827b6ef4067b5ac3ceac07dde9f')
    )
    TEST_UUIDS_STR = [str(uuid_) for uuid_ in TEST_UUIDS]

    @staticmethod
    def print_contents():
        """Print database content."""

        rows = ()
        collection = Collection()
        connection = SqliteDbHelper._connect()
        with closing(connection.cursor()) as cursor:
            cursor.execute('SELECT * FROM contents')
            rows = cursor.fetchall()
        connection.close()
        collection.convert(rows)
        print(collection)

    @classmethod
    def get_collection(cls):
        """Return database rows as collection."""

        rows = ()
        collection = Collection()
        try:
            connection = SqliteDbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute('SELECT * FROM contents')
                rows = cursor.fetchall()
            connection.close()
            collection.convert(rows)
        except sqlite3.Error:
            pass

        return collection

    @staticmethod
    def get_snippets():
        """Return snippets from database as collection."""

        return SqliteDbHelper._select(Const.SNIPPET)

    @staticmethod
    def get_solutions():
        """Return solutions from database as collection."""

        return SqliteDbHelper._select(Const.SOLUTION)

    @staticmethod
    def get_references():
        """Return references from database as collection."""

        return SqliteDbHelper._select(Const.REFERENCE)

    @staticmethod
    def get_schema():
        """Return the file where the database schema is located."""

        schema = os.path.join(pkg_resources.resource_filename('snippy', 'data/storage'), 'database.sql')

        return  schema

    @staticmethod
    def get_storage():
        """Return the file where the database is located."""

        # Sqlite in Python2 does not support shared memory databases.
        # Because of this, the database is stored on disk.
        if not Const.PYTHON2:
            storage = 'file::memory:?cache=shared'
        else:
            storage = os.path.join(pkg_resources.resource_filename('snippy', 'data/storage'), 'snippy-test.db')

        return storage

    @staticmethod
    def store(content):
        """Store content into database.

        Args:
            content (dict): Content in a dictionary.
        """

        query = ('INSERT OR ROLLBACK INTO contents (data, brief, description, groups, tags, links, category, name, ' +
                 'filename, versions, source, uuid, created, updated, digest, metadata) ' +
                 'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        qargs = (
            Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, content.get('data', ()))),
            content.get('brief', ''),
            content.get('description', ''),
            Const.DELIMITER_GROUPS.join(map(Const.TEXT_TYPE, sorted(content.get('groups', ('default',))))),
            Const.DELIMITER_TAGS.join(map(Const.TEXT_TYPE, sorted(content.get('tags', ())))),
            Const.DELIMITER_LINKS.join(map(Const.TEXT_TYPE, content.get('links', ()))),
            content.get('category', ''),
            content.get('name', ''),
            content.get('filename', ''),
            content.get('versions', ''),
            content.get('source', ''),
            content.get('uuid', ''),
            content.get('created', ''),
            content.get('updated', ''),
            content.get('digest', ''),
            content.get('metadata', '')
        )
        try:
            connection = SqliteDbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                connection.commit()
        except sqlite3.OperationalError:
            pass

    @staticmethod
    def delete_all_contents():
        """Delete all content from database."""

        # In successful case the database table does not exist anymore
        try:
            connection = SqliteDbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute('DELETE FROM contents')
                connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            pass

    @staticmethod
    def delete_storage():
        """Delete the database file created for the test."""

        # The file based database is used in testing only in case of Python2.
        if Const.PYTHON2:
            filename = SqliteDbHelper.get_storage()
            if os.path.isfile(filename):
                try:
                    os.remove(filename)
                except OSError:
                    pass

    @staticmethod
    def _connect():
        """Connect to database."""

        if not Const.PYTHON2:
            connection = sqlite3.connect(SqliteDbHelper.get_storage(), check_same_thread=False, uri=True)
        else:
            connection = sqlite3.connect(SqliteDbHelper.get_storage(), check_same_thread=False)

        return connection

    @staticmethod
    def _select(category):
        """Return content based on category."""

        rows = ()
        collection = Collection()
        try:
            query = ('SELECT * FROM contents WHERE category=?')
            qargs = [category]
            connection = SqliteDbHelper._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                rows = cursor.fetchall()
            connection.close()
        except sqlite3.Error as exception:
            print(exception)

        collection.convert(rows)

        return collection
