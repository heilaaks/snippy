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

"""sqlite3db: Database management."""

import re
import os.path
import sqlite3
from contextlib import closing

from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.cause import Cause
from snippy.config.config import Config
from snippy.content.collection import Collection


class Sqlite3Db(object):
    """Sqlite3 database management."""

    QUERY_TYPE_REGEX = 'regex'
    QUERY_TYPE_TOTAL = 'total'

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._connection = None

    def init(self):
        """Initialize database."""

        if not self._connection:
            self._connection = self._create_db()

    def disconnect(self):
        """Close database connection."""

        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                self._logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self._logger.exception('closing sqlite3 database failed with exception "%s"', exception)

    def insert(self, collection):
        """Insert Collection() into database."""

        inserted = 0
        cause = (Cause.HTTP_OK, Const.EMPTY)
        for resource in collection.resources():
            if resource.digest != resource.compute_digest():
                self._logger.debug('invalid digest found and updated while storing content data: "%s"', resource.data)
                resource.update_digest()
            cause = self._insert(resource)
            if cause[0] == Cause.HTTP_OK:
                inserted = inserted + 1

        self._logger.debug('inserted %d out of %d content', inserted, collection.size())
        if collection.empty():
            cause = (Cause.HTTP_NOT_FOUND, 'no content found to be stored')
        elif inserted == collection.size():
            Cause.push(Cause.HTTP_CREATED, 'content created')

        if not inserted and cause[1]:
            Cause.push(cause[0], cause[1])

        stored = Collection()
        for resource in collection.resources():
            stored.migrate(self.select(resource.category, digest=resource.digest))

        return stored

    def _insert(self, resource):
        """Insert Resource into database."""

        cause = self._test_content(resource)
        if cause[0] != Cause.HTTP_OK:

            return cause

        query = ('INSERT OR ROLLBACK INTO contents (data, brief, groups, tags, links, category, filename, ' +
                 'runalias, versions, created, updated, digest, metadata) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)')
        qargs = resource.dump_qargs()
        #print("qargs (%s)" % (qargs,))

        try:
            self._put_db(query, qargs)
        except sqlite3.IntegrityError:
            Cause.push(Cause.HTTP_CONFLICT,
                       'content already exist with digest {:.16}'.format(self._get_db_digest(resource)))

        return cause

    def select(self, category, sall=(), stag=(), sgrp=(), digest=None, data=None):
        """Select content based on defined filters."""

        collection = Collection()
        query, qargs = self._get_query(category, sall, stag, sgrp, digest, data, Sqlite3Db.QUERY_TYPE_REGEX)
        if query:
            rows = self._get_db(query, qargs)
            total = self._count_content(category, sall, stag, sgrp, digest, data)
            collection.convert(rows)
            collection.total = total
            self._logger.debug('selected %d rows %s', len(rows), rows)

        return collection

    def _select_data(self, data):
        """Select content based on data."""

        collection = Collection()
        if self._connection:
            query = ('SELECT * FROM contents WHERE data=?')
            qargs = [Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, data))]
            self._logger.debug('running select query "%s"', query)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting data from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')

        self._logger.debug('selected rows %s', rows)

        return collection

    def select_all_content(self, category):
        """Select all content."""

        collection = Collection()
        if self._connection:
            self._logger.debug('select all contents from category %s', category)
            query = ('SELECT * FROM contents WHERE category=?')
            qargs = [category]
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting all from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented selecting all content from database')

        return collection

    def _count_content(self, category, sall=(), stag=(), sgrp=(), digest=None, data=None):
        """Count content based on defined filters."""

        count = 0
        query, qargs = self._get_query(category, sall, stag, sgrp, digest, data, Sqlite3Db.QUERY_TYPE_TOTAL)
        if query:
            rows = self._get_db(query, qargs)
            try:
                count = rows[0][0]
            except IndexError:
                pass

        return count

    def update(self, digest, resource):
        """Update existing content."""

        query = ('UPDATE contents SET data=?, brief=?, groups=?, tags=?, links=?, category=?, filename=?, '
                 'runalias=?, versions=?, created=?, updated=?, digest=?, metadata=? WHERE digest LIKE ?')
        qargs = resource.dump_qargs() + (digest,)
        self._put_db(query, qargs)

        stored = Collection()
        stored.migrate(self.select(resource.category, digest=resource.digest))

        return stored

    def delete(self, digest):
        """Delete single content based on given digest."""

        if self._connection:
            query = ('DELETE FROM contents WHERE digest LIKE ?')
            self._logger.debug('delete content with digest %s', digest)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, (digest+'%',))
                    if cursor.rowcount == 1:
                        self._connection.commit()
                        Cause.push(Cause.HTTP_NO_CONTENT, 'content deleted successfully')
                    elif cursor.rowcount == 0:
                        Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content to be deleted with digest {:.16}'.format(digest))
                    else:
                        self._logger.debug('unexpected row count %d while deleting with digest %s', cursor.rowcount, digest)
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'deleting from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented deleting content in database')

    def _create_db(self):
        """Create the database."""

        schema = Const.EMPTY
        location = Config.storage_file
        storage_schema = Config.storage_schema
        if os.path.isfile(storage_schema):
            with open(storage_schema, 'rt') as schema_file:
                try:
                    schema = schema_file.read()
                except IOError as exception:
                    Cause.push(Cause.HTTP_500, 'reading database schema failed with exception {}'.format(exception))
        try:
            if not Const.PYTHON2:
                connection = sqlite3.connect(location, check_same_thread=False, uri=True)
            else:
                connection = sqlite3.connect(location, check_same_thread=False)
            connection.create_function('REGEXP', 2, Sqlite3Db._regexp)
            with closing(connection.cursor()) as cursor:
                cursor.execute(schema)
            self._logger.debug('sqlite3 database persisted in %s', location)
        except sqlite3.Error as exception:
            Cause.push(Cause.HTTP_500, 'creating database failed with exception {}'.format(exception))

        return connection

    @staticmethod
    def _regexp(expr, item):
        """Regular expression for the sqlite3."""

        return re.search(expr, item, re.IGNORECASE) is not None

    def _test_content(self, resource):
        """Test content validity."""

        cause = (Cause.HTTP_OK, Const.EMPTY)
        if resource.is_template():
            cause = (Cause.HTTP_BAD_REQUEST, 'content was not stored because it was matching to an empty template')
            self._logger.debug(cause[1])

            return cause

        if not resource.has_data():
            cause = (Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content data was missing')
            self._logger.debug(cause[1])

            return cause

        if self._select_data(resource.data).size():
            cause = (Cause.HTTP_CONFLICT, 'content data already exist with digest {:.16}'.format(self._get_db_digest(resource)))
            self._logger.debug(cause[1])

            return cause

        return cause

    def _get_db_digest(self, resource):
        """Return digest of given content from database."""

        digest = Const.EMPTY
        category = resource.category
        collection = self._select_data(resource.data)
        if collection.size() == 1:
            digest = next(collection.resources()).digest
        else:
            self._logger.debug('unexpected number %d of %s received while searching', collection.size(), category)

        return digest

    def _get_db(self, query, qargs):
        """Run generic query to get data."""

        rows = ()
        if self._connection:
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'reading from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented reading from database')

        return rows

    def _put_db(self, query, qargs):
        """Run generic query for insert or update."""

        if self._connection:
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    self._connection.commit()
            except sqlite3.IntegrityError:
                raise sqlite3.IntegrityError
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'writing into database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented writing into database')

    def _get_query(self, category, sall, stag, sgrp, digest, data, query_type):
        """Get query based on defined type."""

        query = ()
        qargs = []
        if query_type == Sqlite3Db.QUERY_TYPE_TOTAL:
            query_pointer = self._query_count
        else:
            query_pointer = self._query_regex
        if sall and Config.search_all_kws:
            columns = ['data', 'brief', 'groups', 'tags', 'links', 'digest']
            query, qargs = query_pointer(sall, columns, sgrp, category)
        elif stag and Config.search_tag_kws:
            columns = ['tags']
            query, qargs = query_pointer(stag, columns, sgrp, category)
        elif sgrp and Config.search_grp_kws:
            columns = ['groups']
            query, qargs = query_pointer(sgrp, columns, (), category)
        elif Config.is_content_digest() or digest:  # The later condition is for tool internal search based on digest.
            if query_type == Sqlite3Db.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE digest LIKE ?')
            else:
                query = ('SELECT * FROM contents WHERE digest LIKE ?')
            qargs = [digest+'%']
        elif Config.content_data:
            if query_type == Sqlite3Db.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE data LIKE ?')
            else:
                query = ('SELECT * FROM contents WHERE data LIKE ?')
            qargs = ['%'+Const.DELIMITER_DATA.join(map(str, data))+'%']
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'please define keyword, digest or content data as search criteria')

        return query, qargs

    def _query_regex(self, keywords, columns, groups, category):
        """Filtered regex query that can limit the results."""

        query = ('SELECT * FROM contents WHERE ')
        query, qargs = self._add_regex_filters(query, keywords, columns, groups, category)

        # Sort result set.
        if Config.sort_fields:
            query = query + 'ORDER BY '
            for field in Config.sort_fields:
                query = query + field + ' ' + Config.sort_fields[field].upper() + ', '
            query = query[:-2]  # Remove last ', ' added by the loop.
        else:
            query = query + 'ORDER BY created ASC'

        # Define limit and offset.
        query = query + ' LIMIT ' + str(Config.search_limit) + ' OFFSET ' + str(Config.search_offset)

        return query, qargs

    def _query_count(self, keywords, columns, groups, category):
        """Count total hits of filtered regex query."""

        query = ('SELECT count(*) FROM contents WHERE ')
        query, qargs = self._add_regex_filters(query, keywords, columns, groups, category)

        return query, qargs

    @staticmethod
    def _add_regex_filters(query, keywords, columns, groups, category):
        """Return regex query."""

        qargs = []

        # Generate regexp search like:
        #   1. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND (category=?) '
        #   2. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND
        #       (groups=? OR groups=?) AND (category=?) '
        #   3. '(tags REGEXP ?) AND (category=?) '
        regex = '('
        for column in columns:
            regex = regex + column + ' REGEXP ? OR '
        regex = regex[:-4]  # Remove last ' OR ' added by the loop.
        regex = regex + ') '

        # Add optional group search filter.
        if groups:
            regex = regex + 'AND ('
            for _ in groups:
                regex = regex + 'groups=? OR '
            regex = regex[:-4]  # Remove last ' OR ' added by the loop.
            regex = regex + ') '

        # Add mandatory categery.
        regex = regex + 'AND (category=?) '

        # Generate token for each searched column.
        for token in keywords:
            query = query + regex + 'OR '
            qargs = qargs + [token] * len(columns) + list(groups) + [category]  # Tokens for each search keyword.
        query = query[:-3]  # Remove last 'OR ' added by the loop.

        return query, qargs
