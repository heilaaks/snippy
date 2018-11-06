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

"""sqlitedb: Database management."""

import re
import os.path
import sqlite3
import traceback
from contextlib import closing

from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.cause import Cause
from snippy.config.config import Config
from snippy.content.collection import Collection


class SqliteDb(object):
    """Sqlite database management."""

    QUERY_TYPE_REGEX = 'regex'
    QUERY_TYPE_TOTAL = 'total'

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._connection = None
        self._columns = ()

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
        """Insert collection into database.

        Args:
            collection (Collection): Content container to be stored into database.

        Returns:
            Collection: Collection of inserted content.
        """

        inserted = 0
        error = (Cause.HTTP_OK, Const.EMPTY)
        for resource in collection.resources():
            if resource.digest != resource.compute_digest():
                self._logger.debug('invalid digest found and updated while storing content data: "%s"', resource.data)
                resource.update_digest()
            error = self._insert(resource)
            if error[0] == Cause.HTTP_OK:
                inserted = inserted + 1

        self._logger.debug('inserted: %d :out of: %d :content', inserted, collection.size())
        if collection.empty():
            error = (Cause.HTTP_NOT_FOUND, 'no content found to be stored')
        elif inserted == collection.size():
            Cause.push(Cause.HTTP_CREATED, 'content created')

        if not inserted and error[0] != Cause.HTTP_OK:
            Cause.push(*error)

        stored = Collection()
        for resource in collection.resources():
            stored.migrate(self.select(resource.category, digest=resource.digest))

        return stored

    def _insert(self, resource):
        """Insert one resource into database.

        Args:
            resource (Resource): Stored content in ``Resource()`` container.

        Returns:
            List: Local error that contains cause and message.
        """

        error = self._test_content(resource)
        if error[0] != Cause.HTTP_OK:

            return error

        query = ('INSERT OR ROLLBACK INTO contents (data, brief, description, groups, tags, links, category, name, ' +
                 'filename, versions, source, uuid, created, updated, digest, metadata) ' +
                 'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        qargs = resource.dump_qargs()
        try:
            self._put_db(query, qargs)
        except sqlite3.IntegrityError:
            error = (Cause.HTTP_CONFLICT, 'content already exist with digest: {:.16}'.format(self._get_digest(resource)))
            Cause.push(*error)
            self._logger.info('database integrity error from database: {}'.format(traceback.format_exc()))
            self._logger.info('database integrity error from resource: {}'.format(Logger.remove_ansi(str(resource))))
            self._logger.info('database integrity error from query: {}'.format(query))
            self._logger.info('database integrity error from query arguments: {}'.format(qargs))
            self._logger.info('database integrity error stack trace: {}'.format(traceback.format_stack(limit=20)))

        return error

    def select(self, scat=(), sall=(), stag=(), sgrp=(), search_filter=None, uuid=None, digest=None, data=None):
        """Select content based on search criteria.

        The search filter is applied after the result is received from
        database. The search filter removes all resources from returned
        collection that do not match to the filter.

        Args:
            scat (tuple): Search category keyword list.
            sall (tuple): Search all keyword list.
            stag (tuple): Search tag keyword list.
            sgrp (tuple): Search group keyword list.
            search_filter (str): Regexp filter to limit search results.
            uuid (str): Search specific uuid or part of it.
            digest (str): Search specific digest or part of it.
            data (str): Search specific content data or part of it.

        Returns:
            Collection: Collection of selected content.
        """

        collection = Collection()
        query, qargs = self._get_query(scat, sall, stag, sgrp, uuid, digest, data, SqliteDb.QUERY_TYPE_REGEX)
        if query:
            rows = self._get_db(query, qargs)
            self._logger.debug('selected: %d :rows: %s', len(rows), rows)
            if search_filter:
                rows = [row for row in rows if any(search_filter.search(str(column)) for column in row)]
                self._logger.debug('regexp filter applied: %s :resulting: %d :rows: %s', search_filter, len(rows), rows)
            total = self._count_content(scat, sall, stag, sgrp, uuid, digest, data)
            collection.convert(rows)
            collection.total = total

        return collection

    def select_all(self, scat):
        """Select all content from specific categories.

        Args:
            scat (tuple): Search category keyword list.

        Returns:
            Collection: Collection of all content in database.
        """

        collection = Collection()
        if self._connection:
            self._logger.debug('select all contents from categories: %s', scat)

            query = ('SELECT * FROM contents WHERE (')
            for _ in scat:
                query = query + 'category=? OR '
            query = query[:-4]  # Remove last ' OR ' added by the loop.
            query = query + ')'
            qargs = list(scat)
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

    def select_distinct(self, column):
        """Select unique values from given column.

        Args:
            column (str): column name.

        Returns:
            tuple: List of unique values in given column.
        """

        uniques = ()
        if column not in self._columns:
            self._logger.security('unidentified column name cannot be accepted: %s', column)

            return uniques

        if self._connection:
            self._logger.debug('select distinct values from columns: %s', column)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute('SELECT DISTINCT {} FROM contents'.format(column))
                    uniques = [tup[0] for tup in cursor.fetchall()]
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting all from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented selecting all content from database')

        return tuple(uniques)

    def _count_content(self, scat=(), sall=(), stag=(), sgrp=(), uuid=None, digest=None, data=None):
        """Count content based on search criteria.

        Args:
            scat (tuple): Search category keyword list.
            sall (tuple): Search all keyword list.
            stag (tuple): Search tag keyword list.
            sgrp (tuple): Search group keyword list.
            uuid (str): Search specific uuid or part of it.
            digest (str): Search specific digest or part of it.
            data (str): Search specific content data or part of it.

        Returns:
            Int: Number of content in database based on given filters.
        """

        count = 0
        query, qargs = self._get_query(scat, sall, stag, sgrp, uuid, digest, data, SqliteDb.QUERY_TYPE_TOTAL)
        if query:
            rows = self._get_db(query, qargs)
            try:
                count = rows[0][0]
            except IndexError:
                pass

        self._logger.debug('content count: %d', count)

        return count

    def update(self, digest, resource):
        """Update existing content.

        Args:
            digest (str): Content digest that is udpated.
            resource (Resource): Stored content in ``Resource()`` container.

        Returns:
            Collection: Collection of updated content.
        """

        stored = Collection()
        error = self._test_content(resource, update=True)
        if error[0] != Cause.HTTP_OK:
            Cause.push(*error)

            return stored

        query = ('UPDATE contents SET data=?, brief=?, description=?, groups=?, tags=?, links=?, category=?, name=?, '
                 'filename=?, versions=?, source=?, uuid=?, created=?, updated=?, digest=?, metadata=? '
                 'WHERE digest LIKE ?')
        qargs = resource.dump_qargs() + (digest,)
        self._put_db(query, qargs)

        stored.migrate(self.select(resource.category, digest=resource.digest))

        return stored

    def delete(self, digest):
        """Delete content based on given digest.

        Args:
            digest (str): Content digest that is deleted.
        """

        if self._connection:
            query = ('DELETE FROM contents WHERE digest LIKE ?')
            self._logger.debug('delete content with digest: %s', digest)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, (digest+'%',))
                    if cursor.rowcount == 1:
                        self._connection.commit()
                        Cause.push(Cause.HTTP_NO_CONTENT, 'content deleted successfully')
                    elif cursor.rowcount == 0:
                        Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content to be deleted with digest {:.16}'.format(digest))
                    else:
                        self._logger.debug('unexpected row count: %d :while deleting with digest: %s', cursor.rowcount, digest)
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'deleting from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented deleting content in database')

    def debug(self):
        """Debug Sqlitedb."""

        with closing(self._connection.cursor()) as cursor:
            cursor.execute('SELECT * FROM contents')
            rows = cursor.fetchall()

        import pprintpp
        pprintpp.pprint(rows)

    def _select_data(self, data):
        """Select content based on data.

        Args:
            data (str): Content data or part of it.

        Returns:
            Collection: Collection of selected content.
        """

        collection = Collection()
        if self._connection:
            query = ('SELECT * FROM contents WHERE data=?')
            qargs = [Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, data))]
            self._logger.debug('running select data query: %s :with qargs: %s', query, qargs)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting content from database with data failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')

        self._logger.debug('selected rows %s', rows)

        return collection

    def _select_uuid(self, uuid):
        """Select content based on uuid.

        Args:
            uuid (str): Content uuid or part of it.

        Returns:
            Collection: Collection of selected content.
        """

        collection = Collection()
        if self._connection:
            query = ('SELECT * FROM contents WHERE uuid=?')
            qargs = [uuid]
            self._logger.debug('running select uuid query: %s :with qargs: %s', query, qargs)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting content from database with uuid failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')

        self._logger.debug('selected rows: %s', rows)

        return collection

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
            connection.create_function('REGEXP', 2, SqliteDb._regexp)
            with closing(connection.cursor()) as cursor:
                cursor.execute(schema)
            with closing(connection.cursor()) as cursor:
                cursor.execute("pragma table_info('contents')")
                self._columns = [column[1] for column in cursor.fetchall()]
            self._logger.debug('sqlite3 database persisted in: %s', location)
        except sqlite3.Error as exception:
            Cause.push(Cause.HTTP_500, 'creating database failed with exception {}'.format(exception))

        return connection

    @staticmethod
    def _regexp(expr, item):
        """Regular expression for the sqlite database."""

        return re.search(expr, item, re.IGNORECASE) is not None

    def _test_content(self, resource, update=False):
        """Test content validity.

        In case of update, the same content data and uuid are existing. These
        two checks are relevant only in case of insert.
        """

        error = (Cause.HTTP_OK, Const.EMPTY)
        if resource.is_template():
            error = (Cause.HTTP_BAD_REQUEST, 'content was not stored because it was matching to an empty template')
            self._logger.debug(error[1])

            return error

        if not resource.has_data():
            error = (Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field data was missing')
            self._logger.debug(error[1])

            return error

        if not update:
            if self._select_data(resource.data).size():
                error = (Cause.HTTP_CONFLICT, 'content data already exist with digest: {:.16}'.format(self._get_digest(resource)))
                self._logger.debug(error[1])

                return error

            if self._select_uuid(resource.uuid).size():
                error = (Cause.HTTP_CONFLICT, 'content uuid already exist with digest: {:.16}'.format(self._get_digest(resource)))
                self._logger.debug(error[1])

                return error

        return error

    def _get_digest(self, resource):
        """Return digest of given content from database."""

        digest = 'not found'
        category = resource.category
        collection = self._select_data(resource.data)
        if collection.empty():
            collection = self._select_uuid(resource.uuid)

        if collection.size() == 1:
            digest = next(collection.resources()).digest
        else:
            Cause.push(Cause.HTTP_500, 'internal error when searching content possibly violating database unique constraints')
            self._logger.debug('internal server error searching resource from database: {}'.format(Logger.remove_ansi(str(resource))))
            self._logger.debug('internal server error searching unique digest hits: %d :from category: %s', collection.size(), category)

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

    def _get_query(self, scat, sall, stag, sgrp, suuid, sdigest, sdata, query_type):  # noqa pylint: disable=too-many-arguments,too-many-locals,too-many-branches
        """Get query based on defined type."""

        query = ()
        qargs = []
        self._logger.debug('query scat: %s :sall: %s :stag: %s :sgrp: %s :suuid: %s :sdigest: %s :and sdata: %.20s',
                           scat, sall, stag, sgrp, suuid, sdigest, sdata)

        if query_type == SqliteDb.QUERY_TYPE_TOTAL:
            query_pointer = self._query_count
        else:
            query_pointer = self._query_regex

        if sall:
            columns = ['data', 'brief', 'description', 'groups', 'tags', 'links', 'digest']
            query, qargs = query_pointer(sall, columns, sgrp, scat)
        elif stag:
            columns = ['tags']
            query, qargs = query_pointer(stag, columns, sgrp, scat)
        elif sgrp:
            columns = ['groups']
            query, qargs = query_pointer(sgrp, columns, (), scat)
        elif sdigest is not None:
            if query_type == SqliteDb.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE digest LIKE ?')
            else:
                query = ('SELECT * FROM contents WHERE digest LIKE ?')
            qargs = [sdigest+'%']
        elif suuid is not None:
            if query_type == SqliteDb.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE uuid LIKE ?')
            else:
                query = ('SELECT * FROM contents WHERE uuid LIKE ?')
            qargs = [suuid+'%']
        elif sdata:
            if query_type == SqliteDb.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE data LIKE ?')
            else:
                query = ('SELECT * FROM contents WHERE data LIKE ?')
            qargs = ['%'+Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, sdata))+'%']
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'please define keyword, uuid, digest or content data as search criteria')

        return query, qargs

    def _query_regex(self, keywords, columns, groups, categories):
        """Filtered regex query that can limit the results."""

        query = ('SELECT * FROM contents WHERE ')
        query, qargs = self._add_regex_filters(query, keywords, columns, groups, categories)

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

    def _query_count(self, keywords, columns, groups, categories):
        """Count total hits of filtered regex query."""

        query = ('SELECT count(*) FROM contents WHERE ')
        query, qargs = self._add_regex_filters(query, keywords, columns, groups, categories)

        return query, qargs

    @staticmethod
    def _add_regex_filters(query, keywords, columns, groups, categories):
        """Return regex query."""

        qargs = []

        # Generate regexp search like:
        #   1. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND (category=?) '
        #   2. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND
        #       (groups=? OR groups=?) AND (category=?) '
        #   3. '(tags REGEXP ?) AND (category=? or category=?) '
        regex = '('
        for column in columns:
            regex = regex + column + ' REGEXP ? OR '
        regex = regex[:-4]  # Remove last ' OR ' added by the loop.
        regex = regex + ') '

        if groups:
            regex = regex + 'AND ('
            for _ in groups:
                regex = regex + 'groups=? OR '
            regex = regex[:-4]  # Remove last ' OR ' added by the loop.
            regex = regex + ') '

        if categories:
            regex = regex + 'AND ('
            for _ in categories:
                regex = regex + 'category=? OR '
            regex = regex[:-4]  # Remove last ' OR ' added by the loop.
            regex = regex + ') '

        # Generate token for each searched column.
        for token in keywords:
            query = query + regex + 'OR '
            qargs = qargs + [token] * len(columns) + list(groups) + list(categories)  # Tokens for each search keyword.
        query = query[:-3]  # Remove last 'OR ' added by the loop.

        return query, qargs
