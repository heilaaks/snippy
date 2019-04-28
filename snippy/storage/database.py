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

"""database: Database management."""

import os.path
import re
import sqlite3
import sys
import traceback
import warnings
from contextlib import closing

try:
    if not sys.warnoptions:
        warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')
    import psycopg2
except ImportError:
    try:
        from psycopg2cffi import compat
        compat.register()
        import psycopg2  # noqa pylint: disable=ungrouped-imports
    except ImportError:
        class psycopg2(object):  # noqa pylint: disable=C,R
            """Dummy psycopg2 class to use exceptions."""

        setattr(psycopg2, 'Error', sqlite3.Error)
        setattr(psycopg2, 'DataError', sqlite3.DataError)
        setattr(psycopg2, 'IntegrityError', sqlite3.IntegrityError)

from snippy.constants import Constants as Const
from snippy.logger import Logger
from snippy.cause import Cause
from snippy.config.config import Config
from snippy.content.collection import Collection


class Database(object):
    """Generic SQL database manager."""

    QUERY_TYPE_REGEX = 'regex'
    QUERY_TYPE_TOTAL = 'total'

    RE_CATCH_UNIQUE_SQLITE_COLUMN = re.compile(r'''
        contents[.]{1}  # Match leading table name.
        (?P<column>.*)  # Catch column name.
        ''', re.VERBOSE)

    # Example:
    #
    #   duplicate key value violates unique constraint "contents_data_key"
    #   DETAIL:  Key (data)=(docker rm --volumes $(docker ps --all --quiet)) already exists.
    RE_CATCH_UNIQUE_POSTGRE_COLUMN = re.compile(r'''
        DETAIL[:]\s+Key\s+[(]   # Match leading string before column name.
        (?P<column>[\s\S]*?)    # Catch column name.
        [)][=]                  # Match closing parenthesis and equal sign followed by value of key.
        ''', re.DOTALL | re.VERBOSE)

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._db = Const.DB_SQLITE
        self._connection = None
        self._columns = ()
        self._regexp = 'REGEXP'
        self._placeholder = '?'
        self._catch_violating_column = self.RE_CATCH_UNIQUE_SQLITE_COLUMN

    def init(self):
        """Initialize database."""

        if Config.storage_type == Const.DB_SQLITE:
            self._db = Config.storage_type
            self._regexp = 'REGEXP'
            self._placeholder = '?'
            self._catch_violating_column = self.RE_CATCH_UNIQUE_SQLITE_COLUMN
        elif Config.storage_type in (Const.DB_POSTGRESQL, Const.DB_COCKROACHDB):
            self._db = Config.storage_type
            self._regexp = '~*'
            self._placeholder = '%s'
            self._catch_violating_column = self.RE_CATCH_UNIQUE_POSTGRE_COLUMN
        else:
            self._logger.debug('unknown database type - using default sqlite', Config.storage_type)

        if not self._connection:
            self._connection = self._connect()

    def disconnect(self):
        """Close database connection."""

        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                self._logger.debug('closed database connection')
            except (sqlite3.Error, psycopg2.Error) as error:
                self._logger.info('closing database connection failed with exception: {}'.format(error))

    def insert(self, collection):
        """Insert collection into database.

        If any of the resources in the given collection is successfully
        inseted, the operation results Created status. The failing resources
        each produce own failure cause.

        Args:
            collection (Collection): Content container to be stored.

        Returns:
            Collection: Collection of inserted content.
        """

        stored = Collection()
        if not collection:
            Cause.push(Cause.HTTP_NOT_FOUND, 'no content to be stored')

            return stored

        if self._insert(collection):
            Cause.push(Cause.HTTP_CREATED, 'content created')
            for resource in collection:
                stored.migrate(self.select(resource.category, digest=resource.digest))
        self._logger.debug('inserted: %d :out of: %d :content', len(stored), len(collection))

        return stored

    def _insert(self, collection):
        """Insert collection into database.

        Insert all resources in collection in one batch. If any of queries
        in the batch fail, each resource is tried to be insert on by one.

        Args:
            collection (Collection): Content container to be stored.

        Returns:
            bool: True if any of resources in collection is inserted.
        """

        def execute(query, qargs):
            "Execute database query."""

            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.executemany(query, qargs)
                    self._connection.commit()
            except (sqlite3.IntegrityError, psycopg2.IntegrityError):
                self._connection.rollback()
                raise
            except (sqlite3.Error, psycopg2.Error):
                self._connection.rollback()
                self._logger.info('database error in insert with query: {}'.format(query))
                self._logger.info('database error in insert with query arguments: {}'.format(qargs))
                raise

        stored = False
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
            '''.format(self._placeholder)
        qargs = []
        for resource in collection:
            qargs.append(resource.dump_qargs())
        try:
            execute(query, qargs)
            stored = True
        except (sqlite3.IntegrityError, psycopg2.IntegrityError):
            self._logger.info('database integrity error with query: {}'.format(query))
            self._logger.info('database integrity error with query arguments: {}'.format(qargs))
            for resource in collection:
                try:
                    execute(query, [resource.dump_qargs()])
                    stored = True
                except (sqlite3.IntegrityError, psycopg2.IntegrityError) as error:
                    self._set_integrity_error(error, resource)
        except (sqlite3.Error, psycopg2.Error) as error:
            self._set_error(error)

        return stored

    def select(self, scat=(), sall=(), stag=(), sgrp=(), search_filter=None, uuid=None, digest=None, identity=None, data=None):  # noqa pylint: disable=too-many-arguments,too-many-locals
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
            identity (str): Search specific digest or UUID or part of them.
            data (str): Search specific content data or part of it.

        Returns:
            Collection: Collection of selected content.
        """

        collection = Collection()
        query, qargs = self._get_query(scat, sall, stag, sgrp, uuid, digest, identity, data, Database.QUERY_TYPE_REGEX)
        if query:
            rows = self._select(query, qargs)
            self._logger.debug('selected: %d :rows: %s', len(rows), rows)
            if search_filter:
                rows = [row for row in rows if any(search_filter.search(str(column)) for column in row)]
                self._logger.debug('regexp filter applied: %s :resulting: %d :rows: %s', search_filter, len(rows), rows)
            total = self._count_content(scat, sall, stag, sgrp, uuid, digest, identity, data)
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
                query = query + 'category={0} OR '.format(self._placeholder)
            query = query[:-4]  # Remove last ' OR ' added by the loop.
            query = query + ') ORDER BY created ASC, brief ASC'
            qargs = list(scat)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except (sqlite3.Error, psycopg2.Error) as error:
                Cause.push(Cause.HTTP_500, 'selecting all from database failed with exception: {}'.format(error))
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
            except (sqlite3.Error, psycopg2.Error) as error:
                Cause.push(Cause.HTTP_500, 'selecting all from database failed with exception {}'.format(error))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented selecting all content from database')

        return tuple(uniques)

    def _count_content(self, scat=(), sall=(), stag=(), sgrp=(), uuid=None, digest=None, identity=None, data=None):
        """Count content based on search criteria.

        Args:
            scat (tuple): Search category keyword list.
            sall (tuple): Search all keyword list.
            stag (tuple): Search tag keyword list.
            sgrp (tuple): Search group keyword list.
            uuid (str): Search specific uuid or part of it.
            digest (str): Search specific digest or part of it.
            identity (str): Search specific digest or UUID or part of them.
            data (str): Search specific content data or part of it.

        Returns:
            Int: Number of content in database based on given filters.
        """

        count = 0
        query, qargs = self._get_query(scat, sall, stag, sgrp, uuid, digest, identity, data, Database.QUERY_TYPE_TOTAL)
        if query:
            rows = self._select(query, qargs)
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
        if not resource:
            Cause.push(Cause.HTTP_NOT_FOUND, 'no content to be updated')

            return stored

        query = '''
            UPDATE
                          contents
            SET           id          = {0}
                        , category    = {0}
                        , data        = {0}
                        , brief       = {0}
                        , description = {0}
                        , name        = {0}
                        , groups      = {0}
                        , tags        = {0}
                        , links       = {0}
                        , source      = {0}
                        , versions    = {0}
                        , filename    = {0}
                        , created     = {0}
                        , updated     = {0}
                        , uuid        = {0}
                        , digest      = {0}
            WHERE
                        digest LIKE     {0}
            '''.format(self._placeholder)
        qargs = resource.dump_qargs() + (digest,)
        try:
            with closing(self._connection.cursor()) as cursor:
                cursor.execute(query, qargs)
                self._connection.commit()
        except (sqlite3.IntegrityError, psycopg2.IntegrityError) as error:
            self._logger.info('database integrity error with query: {}'.format(query))
            self._logger.info('database integrity error with query arguments: {}'.format(qargs))
            self._set_integrity_error(error, resource)
        except (sqlite3.Error, psycopg2.Error) as error:
            self._set_error(error)
        stored.migrate(self.select(resource.category, digest=resource.digest))

        return stored

    def delete(self, digest):
        """Delete content based on given digest.

        Args:
            digest (str): Content digest that is deleted.
        """

        if self._connection:
            query = ('DELETE FROM contents WHERE digest LIKE {0}'.format(self._placeholder))
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
            except (sqlite3.Error, psycopg2.Error) as error:
                Cause.push(Cause.HTTP_500, 'deleting from database failed with exception {}'.format(error))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented deleting content in database')

    def debug(self):
        """Debug databse."""

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
            query = ('SELECT * FROM contents WHERE data={0}'.format(self._placeholder))
            qargs = [Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, data))]
            self._logger.debug('running select data query: %s :with qargs: %s', query, qargs)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except (sqlite3.Error, psycopg2.Error) as error:
                Cause.push(Cause.HTTP_500, 'selecting content from database with data failed with exception: {}'.format(error))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')

        self._logger.debug('selected rows %s', rows)

        return collection

    def _select_uuid(self, suuid):
        """Select content based on uuid.

        Args:
            uuid (str): Content uuid or part of it.

        Returns:
            Collection: Collection of selected content.
        """

        collection = Collection()
        if self._connection:
            query = ('SELECT * FROM contents WHERE uuid = {0}'.format(self._placeholder))
            qargs = [suuid]
            self._logger.debug('running select uuid query: %s :with qargs: %s', query, qargs)
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
                    collection.convert(rows)
            except (sqlite3.DataError, psycopg2.DataError) as error:
                # This method is used only validated content which should
                # always have valid external UUID field. Because of this,
                # the error here is internal server error.
                self._connection.rollback()
                self._set_data_error(error)
                Cause.push(Cause.HTTP_500, 'invalid user data for search: {}'.format(qargs))
            except (sqlite3.Error, psycopg2.Error) as error:
                self._set_error(error)
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')
        self._logger.debug('selected rows: %s', rows)

        return collection

    def _connect(self):
        """Create the database."""

        connection = None
        location = Config.storage_file
        if not location:
            self._logger.debug('database not connected')
            return connection

        schema = Const.EMPTY
        storage_schema = Config.storage_schema
        if os.path.isfile(storage_schema):
            with open(storage_schema, 'rt') as schema_file:
                try:
                    schema = schema_file.read()
                except IOError as error:
                    Cause.push(Cause.HTTP_500, 'reading database schema failed with exception {}'.format(error))
        try:
            if self._db == Const.DB_SQLITE:
                if not Const.PYTHON2:
                    connection = sqlite3.connect(location, check_same_thread=False, uri=True)
                else:
                    connection = sqlite3.connect(location, check_same_thread=False)
                connection.create_function('REGEXP', 2, lambda regex, value: bool(re.search(regex, value, re.IGNORECASE)))
                with closing(connection.cursor()) as cursor:
                    cursor.execute("pragma table_info('contents')")
                    self._columns = [column[1] for column in cursor.fetchall()]
                self._logger.debug('sqlite3 database persisted in: %s', location)
            elif self._db == Const.DB_POSTGRESQL:
                # This allows adding connection parameters like connect_timeout
                # after the database name. For example database parameter string
                # with values like 'database?connect_timeout=10', the parameters
                # are directly passed to connection string on purpose.
                #
                # The host can contain also multiple hosts separated with syntax
                # required for each database [1].
                #
                # [1] https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
                connection = psycopg2.connect(
                    'postgresql://' +
                    Config.storage_user +
                    ':' +
                    Config.storage_password +
                    '@' +
                    Config.storage_host +
                    '/' +
                    Config.storage_database
                )
                connection.set_client_encoding('UTF8')
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
            elif self._db == Const.DB_COCKROACHDB:
                Cause.push(Cause.HTTP_500, 'unsupported database: {}'.format(self._db))
            else:
                Cause.push(Cause.HTTP_500, 'connecting to unknown database failed: {}'.format(self._db))

            with closing(connection.cursor()) as cursor:
                cursor.execute(schema)
        except (sqlite3.Error, psycopg2.Error) as error:
            self._set_error(error)

        if not connection:
            Config.failure = True

        return connection

    def _get_digest(self, resource):
        """Return digest of given content from database."""

        digest = 'not found'
        category = resource.category
        collection = self._select_data(resource.data)
        if not collection:
            collection = self._select_uuid(resource.uuid)

        if len(collection) == 1:
            digest = next(collection.resources()).digest
        else:
            Cause.push(Cause.HTTP_500, 'internal error when searching content possibly violating database unique constraints')
            self._logger.debug('internal server error searching resource from database: {}'.format(Logger.remove_ansi(str(resource))))
            self._logger.debug('internal server error searching unique digest hits: %d :from category: %s', len(collection), category)

        return digest

    def _select(self, query, qargs):
        """Run generic query to get data."""

        rows = ()
        if self._connection:
            try:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
            except (sqlite3.DataError, psycopg2.DataError) as error:
                # This is executed with PostgreSQL when queried with invalid
                # content external UUID field. There is also UUID field that
                # is used only for internal purposes as a database primary
                # key but that is always assumed to work hence no 'Internal
                # Server Error' here.
                #
                # If rollback is not executed, there will be PostgreSQL error:
                # 'current transaction is aborted, commands ignored until end
                # of transaction block'.
                #
                # The only reason why Cause is not set here is that this works
                # differently between Sqlite and PostgreSQL. The intention is
                # to have same end user behavior also from error cause point
                # of view.
                self._connection.rollback()
                self._set_data_error(error)
            except (sqlite3.Error, psycopg2.Error) as error:
                self._set_error(error)
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented reading from database')

        return rows

    def _get_query(self, scat, sall, stag, sgrp, suuid, sdigest, sidentity, sdata, query_type):  # noqa pylint: disable=too-many-arguments,too-many-locals,too-many-branches
        """Build SQL query."""

        query = ()
        qargs = []
        self._logger.debug('query scat: %s :sall: %s :stag: %s :sgrp: %s :suuid: %s :sdigest: %s :and sdata: %.20s',
                           scat, sall, stag, sgrp, suuid, sdigest, sdata)

        if query_type == Database.QUERY_TYPE_TOTAL:
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
            if query_type == Database.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE digest LIKE {0}'.format(self._placeholder))
            else:
                query = ('SELECT * FROM contents WHERE digest LIKE {0}'.format(self._placeholder))
            qargs = [sdigest+'%']
        elif suuid is not None:
            if query_type == Database.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE uuid = {0}'.format(self._placeholder))
            else:
                query = ('SELECT * FROM contents WHERE uuid = {0}'.format(self._placeholder))
            qargs = [suuid]
        elif sidentity is not None:
            if query_type == Database.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE (digest LIKE {0} OR CAST(uuid AS text) = {0})'.format(self._placeholder))
            else:
                query = ('SELECT * FROM contents WHERE (digest LIKE {0} OR CAST(uuid AS text) = {0})'.format(self._placeholder))
            qargs = [sidentity+'%', sidentity]
        elif sdata:
            if query_type == Database.QUERY_TYPE_TOTAL:
                query = ('SELECT count(*) FROM contents WHERE data LIKE {0}'.format(self._placeholder))
            else:
                query = ('SELECT * FROM contents WHERE data LIKE {0}'.format(self._placeholder))
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
            query = query + 'ORDER BY created ASC, brief ASC'

        # Define limit and offset.
        query = query + ' LIMIT ' + str(Config.search_limit) + ' OFFSET ' + str(Config.search_offset)

        return query, qargs

    def _query_count(self, keywords, columns, groups, categories):
        """Count total hits of filtered regex query."""

        query = ('SELECT count(*) FROM contents WHERE ')
        query, qargs = self._add_regex_filters(query, keywords, columns, groups, categories)

        return query, qargs

    def _add_regex_filters(self, query, keywords, columns, groups, categories):
        """Return regex query."""

        qargs = []

        # Generate regexp search like:
        #   1. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND (category=?) '
        #   2. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND
        #       (groups=? OR groups=?) AND (category=?) '
        #   3. '(tags REGEXP ?) AND (category=? or category=?) '
        regex = '('
        for column in columns:
            regex = regex + column + ' {0} {1} OR '.format(self._regexp, self._placeholder)
        regex = regex[:-4]  # Remove last ' OR ' added by the loop.
        regex = regex + ') '

        if groups:
            regex = regex + 'AND ('
            for _ in groups:
                regex = regex + 'groups={0} OR '.format(self._placeholder)
            regex = regex[:-4]  # Remove last ' OR ' added by the loop.
            regex = regex + ') '

        if categories:
            regex = regex + 'AND ('
            for _ in categories:
                regex = regex + 'category={0} OR '.format(self._placeholder)
            regex = regex[:-4]  # Remove last ' OR ' added by the loop.
            regex = regex + ') '

        # Generate token for each searched column.
        for token in keywords:
            query = query + regex + 'OR '
            qargs = qargs + [token] * len(columns) + list(groups) + list(categories)  # Tokens for each search keyword.
        query = query[:-3]  # Remove last 'OR ' added by the loop.

        return query, qargs

    def _set_error(self, error):
        """Set generic error.

        Args:
            error (Exception): Exception string from integrity error.
        """

        self._logger.info('database error: {}'.format(traceback.format_exc()))
        self._logger.info('database error stack trace: {}'.format(traceback.format_stack(limit=20)))
        Cause.push(Cause.HTTP_500, 'database operation failed with exception: {}'.format(error).lower())

    def _set_integrity_error(self, error, resource):
        """Set integrity error.

        Args:
            error (Exception): Exception string from integrity error.
            resource (Resource): Resource which SQL operation caused exception.
        """

        digest = self._get_digest(resource)
        match = self._catch_violating_column.search(str(error))
        if match:
            if match.group('column') == 'uuid':
                cause = Cause.HTTP_500
            else:
                cause = Cause.HTTP_CONFLICT
            Cause.push(cause, 'content: {} :already exist with digest: {:.16}'.format(match.group('column'), digest))
        else:
            self._logger.info('database integrity error parse failure: {}'.format(error))
            Cause.push(Cause.HTTP_CONFLICT, 'content already exist with digest: {:.16}'.format(digest))
        self._logger.info('database integrity error from database: {}'.format(traceback.format_exc()))
        self._logger.info('database integrity error from resource: {}'.format(Logger.remove_ansi(str(resource))))
        self._logger.info('database integrity error stack trace: {}'.format(traceback.format_stack(limit=20)))

    def _set_data_error(self, error):
        """Set data error.

        Args:
            error (Exception): Exception string from integrity error.
        """

        self._logger.info('invalid data with database operation error: {}'.format(traceback.format_exc()))
        self._logger.info('invalid data with database operation exception: {}'.format(error))
        self._logger.info('invalid data with database operation stack trace: {}'.format(traceback.format_stack(limit=20)))
