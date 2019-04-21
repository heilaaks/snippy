#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""database: Helper methods for testing with any database."""

from __future__ import print_function

import os.path
import sqlite3
import traceback
import uuid
from contextlib import closing

import pytest
import pkg_resources
try:
    import psycopg2
except ImportError:
    class psycopg2(object):  # noqa pylint: disable=C,R
        """Dummy psycopg2 class to use exceptions."""

    setattr(psycopg2, 'IntegrityError', sqlite3.IntegrityError)
    setattr(psycopg2, 'Error', sqlite3.Error)

from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from tests.lib.helper import Helper


class Database(object):
    """Helper methods for testing with generic database."""

    # Database options.
    DB_SQLITE = Helper.DB_SQLITE
    DB_POSTGRESQL = Helper.DB_POSTGRESQL
    DB_COCKROACHDB = Helper.DB_COCKROACHDB
    _DATABASE = DB_SQLITE
    _DATABASES = (DB_SQLITE, DB_POSTGRESQL, DB_COCKROACHDB)
    _PLACEHOLDER = '?'

    # Mocked UUIDs must not collide with predefined resource UUIDs.
    TEST_UUIDS = (
        uuid.UUID(hex='a1cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a2cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a3cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a4cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a5cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a6cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a7cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a8cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='a9cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='aacd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='abcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='accd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='adcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='aecd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='afcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b1cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b2cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b3cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b4cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b5cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b6cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b7cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b8cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='b9cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='bacd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='bbcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='bccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='bdcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='becd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='bfcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c1cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c2cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c3cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c4cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c5cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c6cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c7cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c8cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='c9cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='cacd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='cbcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='cccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='cdcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='cecd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='cfcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d1cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d2cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d3cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d4cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d5cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d6cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d7cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d8cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='d9cd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='dacd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='dbcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='dccd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='ddcd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='decd5827b6ef4067b5ac3ceac07dde9f'),
        uuid.UUID(hex='dfcd5827b6ef4067b5ac3ceac07dde9f')
    )
    TEST_UUIDS_STR = [str(uuid_) for uuid_ in TEST_UUIDS]

    @classmethod
    def set_database(cls, database):
        """Set used database."""

        if database not in cls._DATABASES:
            database = cls.DB_SQLITE
        cls._DATABASE = database

        if cls._DATABASE == cls.DB_SQLITE:
            cls._PLACEHOLDER = '?'
        else:
            cls._PLACEHOLDER = '%s'

        cls._assert_database_connection()

    @staticmethod
    def get_count():
        """Get the total number of contents.

        Returns:
            int: Number of all rows in database.
        """

        total = 0
        try:
            connection = Database._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute('SELECT count(*) FROM contents')
                total = cursor.fetchone()
            connection.close()
        except (sqlite3.Error, psycopg2.Error) as error:
            print('database helper select exception: {}'.format(error))

        return total[0]

    @staticmethod
    def get_collection():
        """Return database rows as collection.

        This method may be called before the database is created. Because of
        this, the exception is silently discarded here.
        """

        rows = ()
        collection = Collection()
        try:
            connection = Database._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute('SELECT * FROM contents ORDER BY created ASC, brief ASC')
                rows = cursor.fetchall()
            connection.close()
            collection.convert(rows)
        except (sqlite3.Error, psycopg2.Error) as error:
            print('database helper select exception: {}'.format(error))

        return collection

    @classmethod
    def print_contents(cls):
        """Print database content."""

        print(cls.get_collection())

    @staticmethod
    def get_snippets():
        """Return snippets from database as collection."""

        return Database._select(Const.SNIPPET)

    @staticmethod
    def get_solutions():
        """Return solutions from database as collection."""

        return Database._select(Const.SOLUTION)

    @staticmethod
    def get_references():
        """Return references from database as collection."""

        return Database._select(Const.REFERENCE)

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

    @classmethod
    def get_cli_params(cls):
        """Return CLI parameters for database."""

        params = []
        if cls._DATABASE == cls.DB_POSTGRESQL:
            params.append('--storage-type')
            params.append('postgresql')
            params.append('--storage-host')
            params.append('localhost:5432')
            params.append('--storage-database')
            params.append('postgres')
            params.append('--storage-user')
            params.append('postgres')
            params.append('--storage-password')
            params.append('postgres')

        return params

    @classmethod
    def store(cls, content):
        """Store content into database.

        Args:
            content (dict): Content in a dictionary.
        """

        query = '''
            INSERT INTO contents
                      (
                                id
                              , category
                              , data
                              , brief
                              , description
                              , name
                              , groups
                              , tags
                              , links
                              , source
                              , versions
                              , filename
                              , created
                              , updated
                              , uuid
                              , digest
                      )
                      VALUES
                      (
                              {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}
                      )
        '''.format(cls._PLACEHOLDER)
        qargs = (
            content.get('id', Database.TEST_UUIDS_STR[0]),
            content.get('category', ''),
            Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, content.get('data', ()))),
            content.get('brief', ''),
            content.get('description', ''),
            content.get('name', ''),
            Const.DELIMITER_GROUPS.join(map(Const.TEXT_TYPE, sorted(content.get('groups', ('default',))))),
            Const.DELIMITER_TAGS.join(map(Const.TEXT_TYPE, sorted(content.get('tags', ())))),
            Const.DELIMITER_LINKS.join(map(Const.TEXT_TYPE, content.get('links', ()))),
            content.get('source', ''),
            Const.DELIMITER_VERSIONS.join(map(Const.TEXT_TYPE, content.get('versions', ()))),
            content.get('filename', ''),
            content.get('created', Helper.IMPORT_TIME),
            content.get('updated', Helper.IMPORT_TIME),
            content.get('uuid', Database.TEST_UUIDS_STR[0]),
            content.get('digest', '')
        )
        try:
            connection = Database._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                connection.commit()
        except (sqlite3.Error, psycopg2.Error):
            print(traceback.format_exc())

    @staticmethod
    def delete_all_contents():
        """Delete all content from database."""

        # In successful case the database table does not exist anymore
        # and exception is allowed.
        try:
            connection = Database._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute('DELETE FROM contents')
                connection.commit()
            connection.close()
        except (sqlite3.Error, psycopg2.Error):
            pass

    @staticmethod
    def delete_storage():
        """Delete the database file created for the test."""

        # The file based database is used in testing only in case of Python2.
        if Const.PYTHON2:
            filename = Database.get_storage()
            if os.path.isfile(filename):
                try:
                    os.remove(filename)
                except OSError:
                    pass

    @classmethod
    def _connect(cls):
        """Connect to database."""

        if cls._DATABASE == cls.DB_SQLITE:
            if not Const.PYTHON2:
                connection = sqlite3.connect(Database.get_storage(), check_same_thread=False, uri=True)
            else:
                connection = sqlite3.connect(Database.get_storage(), check_same_thread=False)
        elif cls._DATABASE == cls.DB_POSTGRESQL:
            connection = psycopg2.connect(host="localhost", user="postgres", password="postgres")

        return connection

    @classmethod
    def _assert_database_connection(cls):
        """Test that database can be connencted."""

        try:
            cls._connect()
        except (sqlite3.Error, psycopg2.Error):
            pytest.exit('cannot connect to used database: {}'.format(cls._DATABASE))

    @classmethod
    def _select(cls, category):
        """Return content based on category."""

        rows = ()
        collection = Collection()
        try:
            query = ('SELECT * FROM contents WHERE category={0} ORDER BY created ASC, brief ASC'.format(cls._PLACEHOLDER))
            qargs = [category]
            connection = Database._connect()
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                rows = cursor.fetchall()
            connection.close()
        except (sqlite3.Error, psycopg2.Error):
            print(traceback.format_exc())

        collection.convert(rows)

        return collection
