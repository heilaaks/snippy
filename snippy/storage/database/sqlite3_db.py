#!/usr/bin/env python3

"""sqlite3_db.py: Database management."""

import os
import re
import sys
import sqlite3
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config


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

    def insert_snippet(self, snippet, metadata=None):
        """Insert snippet into database."""

        result = Const.DB_FAILURE
        if self.conn:
            tags_string = Const.DELIMITER_TAGS.join(map(str, snippet['tags']))
            links_string = Const.DELIMITER_LINKS.join(map(str, snippet['links']))
            query = ('INSERT OR ROLLBACK INTO snippets(snippet, brief, groups, tags, links, \
                      metadata, digest) VALUES(?,?,?,?,?,?,?)')
            self.logger.debug('insert snippet "%s" with digest %.16s', snippet['content'], snippet['digest'])
            try:
                self.cursor.execute(query, (snippet['content'], snippet['brief'], snippet['group'], tags_string,
                                            links_string, metadata, snippet['digest']))
                self.conn.commit()
                result = Const.DB_INSERT_OK
            except sqlite3.IntegrityError as exception:
                result = Const.DB_DUPLICATE
                self.logger.info('unique constraint violation with content "%s"', snippet['content'])
            except sqlite3.Error as exception:
                self.logger.exception('inserting into sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

        return result

    def bulk_insert_snippets(self, snippets):
        """Insert multiple snippets into database."""

        for snippet in snippets:
            self.insert_snippet(snippet)

    def select_snippets(self, keywords=None, digest=None, content=None):
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
            #     1) SELECT id, snippet, brief, groups, tags, links, metadata, digest FROM snippets WHERE
            #        (snippet REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?)
            #        ORDER BY id ASC
            #     2) SELECT id, snippet, brief, groups, tags, links, metadata, digest FROM snippets WHERE (snippet REGEXP ?
            #        or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) OR (snippet REGEXP ?
            #        or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) OR (snippet REGEXP ?
            #        or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) ORDER BY id ASC
            if keywords and Config.is_search_all():
                query, qargs = Sqlite3Db._get_regexp_query(keywords)
            elif digest:
                query = ('SELECT id, snippet, brief, groups, tags, links, metadata, digest FROM snippets \
                          WHERE digest LIKE ?')
                qargs = [digest+'%']
            elif content:
                query = ('SELECT id, snippet, brief, groups, tags, links, metadata, digest FROM snippets \
                          WHERE snippet=?')
                qargs = [content]
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

    def select_all_snippets(self):
        """Select all snippets."""

        if self.conn:
            query = ('SELECT * FROM snippets')
            self.logger.debug('select all snippets')
            try:
                self.cursor.execute(query)

                return self.cursor.fetchall()
            except sqlite3.Error as exception:
                self.logger.exception('deleting from sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while all entries were being queried')

        return []

    def update_snippet(self, digest, snippet, metadata=None):
        """Update existing snippet."""

        if self.conn:
            tags_string = Const.DELIMITER_TAGS.join(map(str, snippet['tags']))
            links_string = Const.DELIMITER_LINKS.join(map(str, snippet['links']))
            query = ('UPDATE snippets SET snippet=?, brief=?, groups=?, tags=?, links=?, metadata=?, digest=? \
                      WHERE digest LIKE ?')
            qargs = [snippet['content'], snippet['brief'], snippet['group'], tags_string,
                     links_string, metadata, snippet['digest'], digest+'%']
            self.logger.debug('updating snippet %.16s with new digest %.16s and brief "%s"', digest, snippet['digest'],
                              snippet['brief'])
            try:
                self.cursor.execute(query, qargs)
                self.conn.commit()
            except sqlite3.Error as exception:
                self.logger.exception('updating sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

    def delete_snippet(self, digest):
        """Delete one snippet based on given digest."""

        if self.conn:
            query = ('DELETE FROM snippets WHERE digest LIKE ?')
            self.logger.debug('delete snippet with index %s', digest)
            try:
                self.cursor.execute(query, (digest+'%',))
                if self.cursor.rowcount == 1:
                    self.conn.commit()
                elif self.cursor.rowcount == 0:
                    self.logger.info('the requested row was not found with digest %s', digest)
                else:
                    self.logger.info('unexpected row count %d while deleting with digest %s', self.cursor.rowcount, digest)
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
    def _get_regexp_query(keywords):
        """Generate query parameters for the SQL query."""

        query_args = []
        query = 'SELECT id, snippet, brief, groups, tags, links, metadata, digest FROM snippets WHERE '
        search = '(snippet REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) '
        for token in keywords:
            query = query + search + 'OR '
            query_args = query_args + [token, token, token, token, token] # Token for each search colum in the row.
        query = query[:-3] # Remove last 'OR ' added by the loop.
        query = query + ' ORDER BY id ASC'

        return (query, query_args)
