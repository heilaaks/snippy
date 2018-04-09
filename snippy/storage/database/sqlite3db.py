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

from snippy.config.constants import Constants as Const
from snippy.logger import Logger
from snippy.cause import Cause
from snippy.config.config import Config


class Sqlite3Db(object):
    """Sqlite3 database management."""

    def __init__(self):
        self.logger = Logger(__name__).logger
        self.connection = None

    def init(self):
        """Initialize database."""

        if not self.connection:
            self.connection = self._create_db()

    def disconnect(self):
        """Close database connection."""

        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self.logger.exception('closing sqlite3 database failed with exception "%s"', exception)

    def insert_content(self, content, digest, metadata=None, bulk_insert=False):
        """Insert content into database."""

        cause = self._test_content(content)
        if cause[0] != Cause.HTTP_OK:
            if not bulk_insert:
                Cause.push(cause[0], cause[1])

            return cause

        if self.connection:
            query = ('INSERT OR ROLLBACK INTO contents (data, brief, groups, tags, links, category, filename, ' +
                     'runalias, versions, created, updated, digest, metadata) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)')
            self.logger.debug('insert "%s" with digest %.16s', content.get_brief(), digest)
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, (content.get_data(Const.STRING_CONTENT),
                                           content.get_brief(Const.STRING_CONTENT),
                                           content.get_group(Const.STRING_CONTENT),
                                           content.get_tags(Const.STRING_CONTENT),
                                           content.get_links(Const.STRING_CONTENT),
                                           content.get_category(Const.STRING_CONTENT),
                                           content.get_filename(Const.STRING_CONTENT),
                                           content.get_runalias(Const.STRING_CONTENT),
                                           content.get_versions(Const.STRING_CONTENT),
                                           content.get_created(Const.STRING_CONTENT),
                                           content.get_updated(Const.STRING_CONTENT),
                                           digest,
                                           metadata))
                    self.connection.commit()
                    if not bulk_insert:
                        Cause.push(Cause.HTTP_CREATED, 'content created')

            except sqlite3.IntegrityError as exception:
                Cause.push(Cause.HTTP_CONFLICT,
                           'content data already exist with digest {:.16}'.format(self._get_db_digest(content)))
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'inserting into database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented inserting into database')

        return cause

    def bulk_insert_content(self, contents):
        """Insert multiple contents into database."""

        inserted = 0
        cause = (Cause.HTTP_OK, Const.EMPTY)
        for content in contents:
            digest = content.get_digest()
            if digest != content.compute_digest():
                self.logger.debug('invalid digest found and updated while storing content data: "%s"', content.get_data())
                digest = content.compute_digest()

            cause = self.insert_content(content, digest, bulk_insert=True)
            if cause[0] == Cause.HTTP_OK:
                inserted = inserted + 1

        self.logger.debug('inserted %d out of %d content', inserted, len(contents))

        if not contents:
            cause = (Cause.HTTP_NOT_FOUND, 'no content found to be stored')
        elif inserted == len(contents):
            Cause.push(Cause.HTTP_CREATED, 'content created')

        if not inserted and cause[1]:
            Cause.push(cause[0], cause[1])

    def select_content(self, category, sall=(), stag=(), sgrp=(), digest=None, data=None):
        """Select content."""

        rows = ()
        if self.connection:
            # The regex based queries contain the same amount of regex queries than there are
            # keywords. The reason is that each keyword (one keyword) must be searched from all
            # colums where the search is made. The query arguments are generated so that each
            # query is made with the same keyword for all the colums thus also the query arguments
            # can be countend by multiplying the query keywords (e.g 3) and the searched colums.
            #
            # Example queries:
            # 1) SELECT * FROM contents WHERE (data REGEXP ? or brief REGEXP ? or groups REGEXP ?
            #    or tags REGEXP ? or links REGEXP ? and category = ?) ORDER BY id ASC
            # 2) SELECT * FROM contents WHERE
            #    (data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ?) AND (category = ?) OR
            #    (data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ?) AND (category = ?) OR
            #    (data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ?) AND (category = ?)
            #    ORDER BY id ASC
            query = ()
            qargs = []
            if sall and Config.search_all_kws:
                columns = ['data', 'brief', 'groups', 'tags', 'links', 'digest']
                query, qargs = Sqlite3Db._make_regexp_query(sall, columns, sgrp, category)
            elif stag and Config.search_tag_kws:
                columns = ['tags']
                query, qargs = Sqlite3Db._make_regexp_query(stag, columns, sgrp, category)
            elif sgrp and Config.search_grp_kws:
                columns = ['groups']
                query, qargs = Sqlite3Db._make_regexp_query(sgrp, columns, (), category)
            elif Config.is_content_digest() or digest:  # The later condition is for tool internal search based on digest.
                query = ('SELECT * FROM contents WHERE digest LIKE ?')
                qargs = [digest+'%']
            elif Config.content_data:
                query = ('SELECT * FROM contents WHERE data LIKE ?')
                qargs = ['%'+Const.DELIMITER_DATA.join(map(str, data))+'%']
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'please define keyword, digest or content data as search criteria')

                return rows

            self.logger.debug('running select query "%s"', query)
            self.logger.debug('running select query with arguments "%s"', qargs)
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')

        self.logger.debug('selected %d rows %s', len(rows), rows)

        return rows

    def _select_content_data(self, data):
        """Select content based on data."""

        rows = ()
        if self.connection:
            query = ('SELECT * FROM contents WHERE data=?')
            qargs = [Const.DELIMITER_DATA.join(map(str, data))]
            self.logger.debug('running select query "%s"', query)
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting data from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented searching from database')

        self.logger.debug('selected rows %s', rows)

        return rows

    def select_all_content(self, category):
        """Select all content."""

        rows = ()
        if self.connection:
            self.logger.debug('select all contents from category %s', category)
            query = ('SELECT * FROM contents WHERE category=?')
            qargs = [category]
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'selecting all from database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented selecting all content from database')

        return rows

    def update_content(self, content, digest, metadata=None):
        """Update existing content."""

        if self.connection:
            query = ('UPDATE contents SET data=?, brief=?, groups=?, tags=?, links=?, category=?, filename=?, '
                     'runalias=?, versions=?, created=?, updated=?, digest=?, metadata=? WHERE digest LIKE ?')
            self.logger.debug('updating content %.16s with new digest %.16s and brief "%s"', content.get_digest(), digest,
                              content.get_brief())
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, (content.get_data(Const.STRING_CONTENT),
                                           content.get_brief(Const.STRING_CONTENT),
                                           content.get_group(Const.STRING_CONTENT),
                                           content.get_tags(Const.STRING_CONTENT),
                                           content.get_links(Const.STRING_CONTENT),
                                           content.get_category(Const.STRING_CONTENT),
                                           content.get_filename(Const.STRING_CONTENT),
                                           content.get_runalias(Const.STRING_CONTENT),
                                           content.get_versions(Const.STRING_CONTENT),
                                           content.get_created(Const.STRING_CONTENT),
                                           content.get_updated(Const.STRING_CONTENT),
                                           content.get_digest(Const.STRING_CONTENT),
                                           metadata,
                                           digest))
                    self.connection.commit()
            except sqlite3.Error as exception:
                Cause.push(Cause.HTTP_500, 'updating database failed with exception {}'.format(exception))
        else:
            Cause.push(Cause.HTTP_500, 'internal error prevented updating content in database')

    def delete_content(self, digest):
        """Delete single content based on given digest."""

        if self.connection:
            query = ('DELETE FROM contents WHERE digest LIKE ?')
            self.logger.debug('delete content with digest %s', digest)
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, (digest+'%',))
                    if cursor.rowcount == 1:
                        self.connection.commit()
                        Cause.push(Cause.HTTP_NO_CONTENT, 'content deleted successfully')
                    elif cursor.rowcount == 0:
                        Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content to be deleted with digest {:.16}'.format(digest))
                    else:
                        self.logger.debug('unexpected row count %d while deleting with digest %s', cursor.rowcount, digest)
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
            self.logger.debug('sqlite3 database persisted in %s', location)
        except sqlite3.Error as exception:
            Cause.push(Cause.HTTP_500, 'creating database failed with exception {}'.format(exception))

        return connection

    def _test_content(self, content):
        """Test content validity."""

        # Common failure cases:
        #   1. Content is imported from template that is not changed.
        #   2. Default content is imported multiple times.
        #   3. Content already exists.
        cause = (Cause.HTTP_OK, Const.EMPTY)
        if content.is_template():
            cause = (Cause.HTTP_BAD_REQUEST, 'content was not stored because it was matching to an empty template')
            self.logger.debug(cause[1])

            return cause

        if not content.has_data():
            cause = (Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content data was missing')
            self.logger.debug(cause[1])

            return cause

        if self._select_content_data(content.get_data()):
            cause = (Cause.HTTP_CONFLICT, 'content data already exist with digest {:.16}'.format(self._get_db_digest(content)))
            self.logger.debug(cause[1])

            return cause

        return cause

    @staticmethod
    def _regexp(expr, item):
        """Regular expression for the sqlite3."""

        return re.search(expr, item, re.IGNORECASE) is not None

    @staticmethod
    def _make_regexp_query(keywords, columns, groups, category):
        """Generate SQL query parameters for specific fields and keywords."""

        query_args = []
        query = ('SELECT * FROM contents WHERE ')

        # Generate regexp search like:
        #   1. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND (category=?) '
        #   2. '(data REGEXP ? OR brief REGEXP ? OR groups REGEXP ? OR tags REGEXP ? OR links REGEXP ?) AND
        #       (groups=? OR groups=?) AND (category=?) '
        #   3. '(tags REGEXP ?) AND (category=?) '
        search = '('
        for column in columns:
            search = search + column + ' REGEXP ? OR '
        search = search[:-4]  # Remove last ' OR ' added by the loop.
        search = search + ') '

        # Add optional group search filter.
        if groups:
            search = search + 'AND ('
            for _ in groups:
                search = search + 'groups=? OR '
            search = search[:-4]  # Remove last ' OR ' added by the loop.
            search = search + ') '

        # Add mandatory categery.
        search = search + 'AND (category=?) '

        # Generate token for each searched column like
        for token in keywords:
            query = query + search + 'OR '
            query_args = query_args + [token] * len(columns) + list(groups) + [category]  # Tokens for each search keyword.
        query = query[:-3]  # Remove last 'OR ' added by the loop.
        query = query + 'ORDER BY id ASC'

        return (query, query_args)

    def _get_db_digest(self, content):
        """Return digest of given content from database."""

        digest = Const.EMPTY
        category = content.get_category(Const.STRING_CONTENT)
        contents = self._select_content_data(content.get_data())
        if len(contents) == 1:
            digest = contents[0][Const.DIGEST]
        else:
            self.logger.debug('unexpected number %d of %s received while searching', len(contents), category)

        return digest
