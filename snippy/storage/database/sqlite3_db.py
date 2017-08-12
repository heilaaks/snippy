#!/usr/bin/env python3

"""sqlite3_db.py: Database management."""

import os
import re
import sys
import sqlite3
from snippy.logger import Logger
from snippy.config import Config


class Sqlite3Db(object):
    """Sqlite3 database management."""

    def __init__(self):
        self.logger = Logger().get()
        self.conn = None
        self.cursor = None

    def init(self):
        """Initialize database."""

        self.conn, self.cursor = self._create_db()

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

    def insert_snippet(self, snippet, brief=None, tags=None, link=None, metadata=None):
        """Insert snippet into database."""

        if self.conn:
            tags_string = ','.join(map(str, tags))
            query = ('INSERT INTO snippets(snippet, brief, tags, link, metadata) VALUES(?,?,?,?,?)')
            self.logger.debug('insert snippet %s with brief %s and tags %s', snippet, brief, tags_string)
            try:
                self.cursor.execute(query, (snippet, brief, tags_string, link, metadata))
                self.conn.commit()
            except sqlite3.Error as exception:
                self.logger.exception('inserting into sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

    def select_snippet(self, keywords, regex=True):
        """Select snippets."""

        rows = []
        if self.conn:
            # The regex based queries contain the same amount of regex queries than there are
            # keywords. The reason is that each keyword (one keyword) must be searched from all
            # the colums where the search is made. The query argumes are generated so that each
            # query is made with the same keyword for all the colums thus also the query arguments
            # can be counted by multiplying the query keywords (e.g 3)and the searched colums.
            #
            # Example queries:
            #     1) SELECT id, snippet, brief, tags, link, metadata FROM snippets WHERE
            #        (snippet REGEXP ? or tags REGEXP ? or brief REGEXP? or link REGEXP ?) ORDER BY id ASC
            #     2) SELECT id, snippet, brief, tags, link, metadata FROM snippets WHERE (snippet REGEXP ?
            #        or tags REGEXP ? or brief REGEXP? or link REGEXP ?) OR (snippet REGEXP ? or tags REGEXP ?
            #        or brief REGEXP? or link REGEXP ?) OR (snippet REGEXP ? or tags REGEXP ? or brief REGEXP ?
            #        or link REGEXP ?) ORDER BY id ASC
            if regex:
                query, qargs = Sqlite3Db._get_regexp_query(keywords)
            else:
                query, qargs = Sqlite3Db._get_regexp_query(keywords)

            self.logger.debug('running query "%s"', query)
            try:
                self.cursor.execute(query, qargs)
                rows = self.cursor.fetchall()
            except sqlite3.Error as exception:
                self.logger.exception('selecting from sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while all entries were being queried')

        self.logger.debug('selected rows %s', rows)

        return rows

    def delete_snippet(self, db_index):
        """Delete snippets."""

        if self.conn:
            query = ('DELETE FROM snippets where id = ?')
            self.logger.debug('delete snippet with index %d', db_index)
            try:
                self.cursor.execute(query, (db_index,))
                if self.cursor.rowcount == 1:
                    self.conn.commit()
                else:
                    self.logger.info('database index was not found %d', db_index)
            except sqlite3.Error as exception:
                self.logger.exception('deleting from sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while index was being deleted')

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
            conn = sqlite3.connect(location, check_same_thread=False, uri=True)
            conn.create_function('REGEXP', 2, Sqlite3Db._regexp)
            cursor = conn.cursor()
            with open(Config.get_storage_schema(), 'rt') as schema_file:
                schema = schema_file.read()
                conn.executescript(schema)
            self.logger.debug('initialized sqlite3 database into {:s}'.format(location))
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
    def _get_regexp_query(keywords):
        """Generate query parameters for the SQL query."""

        query_args = []
        query = 'SELECT id, snippet, brief, tags, link, metadata FROM snippets WHERE '
        search = '(snippet REGEXP ? or brief REGEXP ? or tags REGEXP ? or link REGEXP ?) '
        for token in keywords:
            query = query + search + 'OR '
            query_args = query_args + [token, token, token, token] # Token for each search colum in the row.
        query = query[:-3] # Remove last 'OR ' added by the loop.
        query = query + ' ORDER BY id ASC'

        return (query, query_args)
