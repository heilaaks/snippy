#!/usr/bin/env python3

"""sqlite3_db.py: Database management."""

import os
import re
import sys
import sqlite3
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config
from snippy.format import Format


class Sqlite3Db(object):
    """Sqlite3 database management."""

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.conn = None
        self.cursor = None

    def init(self):
        """Initialize database."""

        self.conn, self.cursor = self._create_db()

        return self

    def disconnect(self):
        """Close database connection."""

        if self.conn:
            try:
                self.cursor.close()
                self.cursor = None
                self.conn.close()
                self.conn = None
                self.logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self.logger.exception('closing sqlite3 database failed with exception "%s"', exception)

    def insert_content(self, content, digest, utc, metadata=None):
        """Insert content into database."""

        cause = Const.DB_FAILURE
        if self.conn:
            query = ('INSERT OR ROLLBACK INTO contents (data, brief, groups, tags, links, category, filename, utc, ' +
                     'digest, metadata) VALUES(?,?,?,?,?,?,?,?,?,?)')
            self.logger.debug('insert "%s" with digest %.16s', content[Const.BRIEF], digest)
            try:
                self.cursor.execute(query, (Format.get_db_data(content),
                                            Format.get_db_brief(content),
                                            Format.get_db_group(content),
                                            Format.get_db_tags(content),
                                            Format.get_db_links(content),
                                            Format.get_db_category(content),
                                            Format.get_db_filename(content),
                                            utc,
                                            digest,
                                            metadata))
                self.conn.commit()
                cause = Const.DB_INSERT_OK
            except sqlite3.IntegrityError as exception:
                cause = Const.DB_DUPLICATE
                self.logger.info('unique constraint violation with content "%s"', content[Const.DATA])
            except sqlite3.Error as exception:
                self.logger.exception('inserting into sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

        return cause

    def bulk_insert_content(self, contents):
        """Insert multiple contents into database."""

        for content in contents:
            utc = content[Const.UTC]
            digest = content[Const.DIGEST]
            content = content[Const.DATA:Const.DIGEST]
            self.insert_content(content, digest, utc)

    def select_content(self, category, keywords=None, digest=None, content=None):
        """Select content."""

        rows = ()
        if self.conn:
            # The regex based queries contain the same amount of regex queries than there are
            # keywords. The reason is that each keyword (one keyword) must be searched from all
            # the colums where the search is made. The query argumes are generated so that each
            # query is made with the same keyword for all the colums thus also the query arguments
            # can be counted by multiplying the query keywords (e.g 3)and the searched colums.
            #
            # Example queries:
            # 1) SELECT * FROM contents WHERE (data REGEXP ? or brief REGEXP ? or groups REGEXP ?
            #    or tags REGEXP ? or links REGEXP ? and category = ?) ORDER BY id ASC
            # 2) SELECT * FROM contents WHERE
            #    (data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ?) AND (category = ?) OR
            #    (data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ?) AND (category = ?) OR
            #    (data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ?) AND (category = ?)
            #    ORDER BY id ASC
            if keywords and Config.is_search_all():
                columns = ['data', 'brief', 'groups', 'tags', 'links']
                query, qargs = Sqlite3Db._make_regexp_query(keywords, columns, category)
            elif keywords and Config.is_search_grp():
                columns = ['groups']
                query, qargs = Sqlite3Db._make_regexp_query(keywords, columns, category)
            elif keywords and Config.is_search_tag():
                columns = ['tags']
                query, qargs = Sqlite3Db._make_regexp_query(keywords, columns, category)
            elif digest:
                query = ('SELECT * FROM contents WHERE digest LIKE ?')
                qargs = [digest+'%']
            elif content:
                query = ('SELECT * FROM contents WHERE data=?')
                qargs = [Const.DELIMITER_DATA.join(map(str, content))]
            else:
                self.logger.error('exiting because of internal error where search query was not defined')
                sys.exit(1)

            self.logger.debug('running select query "%s"', query)
            try:
                self.cursor.execute(query, qargs)
                rows = self.cursor.fetchall()
            except sqlite3.Error as exception:
                self.logger.exception('selecting from sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while selecting records was execured')

        self.logger.debug('selected rows %s', rows)

        return rows

    def select_all_content(self, category):
        """Select all content."""

        rows = ()
        if self.conn:
            self.logger.debug('select all contents from category %s', category)
            query = ('SELECT * FROM contents WHERE category=?')
            qargs = [category]
            try:
                self.cursor.execute(query, qargs)

                rows = self.cursor.fetchall()
            except sqlite3.Error as exception:
                self.logger.exception('deleting from sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while all entries were being queried')

        return rows

    def update_content(self, content, digest_updated, digest_new, utc, metadata=None):
        """Update existing content."""

        if self.conn:
            query = ('UPDATE contents SET data=?, brief=?, groups=?, tags=?, links=?, category=?, filename=?, utc=?, '
                     'digest=?, metadata=? WHERE digest LIKE ?')
            self.logger.debug('updating content %.16s with new digest %.16s and brief "%s"', digest_updated, digest_new,
                              content[Const.BRIEF])
            try:
                self.cursor.execute(query, (Format.get_db_data(content),
                                            Format.get_db_brief(content),
                                            Format.get_db_group(content),
                                            Format.get_db_tags(content),
                                            Format.get_db_links(content),
                                            Format.get_db_category(content),
                                            Format.get_db_filename(content),
                                            utc,
                                            digest_new,
                                            metadata,
                                            digest_updated))
                self.conn.commit()
            except sqlite3.Error as exception:
                self.logger.exception('updating sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

    def delete_content(self, digest):
        """Delete single content based on given digest."""

        cause = Const.DB_FAILURE
        if self.conn:
            query = ('DELETE FROM contents WHERE digest LIKE ?')
            self.logger.debug('delete content with digest %s', digest)
            try:
                self.cursor.execute(query, (digest+'%',))
                if self.cursor.rowcount == 1:
                    self.conn.commit()
                    cause = Const.DB_DELETE_OK
                elif self.cursor.rowcount == 0:
                    Config.set_cause('cannot find content to be deleted with digest %s' % digest)
                    cause = Const.DB_ENTRY_NOT_FOUND
                else:
                    self.logger.info('unexpected row count %d while deleting with digest %s', self.cursor.rowcount, digest)
            except sqlite3.Error as exception:
                self.logger.exception('deleting from sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while content was being deleted')

        return cause

    def debug(self):
        """Dump the whole database."""

        if self.conn:
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.logger.debug('sqlite3 dump %s', self.cursor.fetchall())
            except sqlite3.Error as exception:
                self.logger.exception('dumping sqlite3 database failed with exception "%s"', exception)

    def _create_db(self):
        """Create the database."""

        location = self._get_db_location()
        try:
            if not Const.PYTHON2:
                conn = sqlite3.connect(location, check_same_thread=False, uri=True)
            else:
                conn = sqlite3.connect(location, check_same_thread=False)
            conn.create_function('REGEXP', 2, Sqlite3Db._regexp)
            cursor = conn.cursor()
            with open(Config.get_storage_schema(), 'rt') as schema_file:
                schema = schema_file.read()
                conn.executescript(schema)
            self.logger.debug('sqlite3 database persisted in {:s}'.format(location))
        except sqlite3.Error as exception:
            self.logger.exception('creating sqlite3 database failed with exception "%s"', exception)

        return (conn, cursor)

    def _get_db_location(self):
        """Get the location where there the database is going to be stored."""

        location = ''
        if Config.is_storage_in_memory():
            location = "file::memory:?cache=shared"
        else:
            if os.path.exists(Config.get_storage_path()) and os.access(Config.get_storage_path(), os.W_OK):
                location = Config.get_storage_file()
            else:
                self.logger.error('storage path does not exist or is not accessible: {:s}'.format(Config.get_storage_path()))

                sys.exit('storage path does not exist or is not accessible: {:s}'.format(Config.get_storage_path()))

        return location

    @staticmethod
    def _regexp(expr, item):
        """Regular expression for the sqlite3."""

        return re.search(expr, item, re.IGNORECASE) is not None

    @staticmethod
    def _make_regexp_query(keywords, columns, category):
        """Generate SQL query parameters for specific fields and keywords."""

        query_args = []
        query = ('SELECT * FROM contents WHERE ')

        # Generate regexp search like:
        #   1. '(data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ? AND category=?) '
        #   2. '(tags REGEXP ? AND category=?) '
        search = '('
        for column in columns:
            search = search + column + ' REGEXP ? OR '
        search = search[:-4] # Remove last ' OR ' added by the loop.
        search = search + ') AND (category=?) '

        # Generate token for each searched column like
        for token in keywords:
            query = query + search + 'OR '
            query_args = query_args + [token] * len(columns) + [category] # Token for each search colum in the row.
        query = query[:-3] # Remove last 'OR ' added by the loop.
        query = query + 'ORDER BY id ASC'

        return (query, query_args)
