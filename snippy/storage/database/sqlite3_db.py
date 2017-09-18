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

    def insert_snippet(self, snippet, digest, metadata=None):
        """Insert snippet into database."""

        cause = Const.DB_FAILURE
        if self.conn:
            query = ('INSERT OR ROLLBACK INTO snippets(content, brief, groups, tags, links, digest, metadata) ' +
                     'VALUES(?,?,?,?,?,?,?)')
            self.logger.debug('insert snippet "%s" with digest %.16s', snippet[Const.SNIPPET_BRIEF], digest)
            try:
                # The join/map is sorted because it seems that this somehow randomly changes
                # the order of tags in the string. This seems to happen only in Python 2.7.
                self.cursor.execute(query, (Const.get_content_string(snippet),
                                            snippet[Const.SNIPPET_BRIEF],
                                            snippet[Const.SNIPPET_GROUP],
                                            Const.DELIMITER_TAGS.join(map(str, sorted(snippet[Const.SNIPPET_TAGS]))),
                                            Const.DELIMITER_LINKS.join(map(str, sorted(snippet[Const.SNIPPET_LINKS]))),
                                            digest,
                                            metadata))
                self.conn.commit()
                cause = Const.DB_INSERT_OK
            except sqlite3.IntegrityError as exception:
                cause = Const.DB_DUPLICATE
                self.logger.info('unique constraint violation with content "%s"', snippet[Const.SNIPPET_CONTENT])
            except sqlite3.Error as exception:
                self.logger.exception('inserting into sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

        return cause

    def bulk_insert_snippets(self, snippets):
        """Insert multiple snippets into database."""

        for snippet in snippets:
            digest = snippet[Const.SNIPPET_DIGEST]
            snippet = snippet[Const.SNIPPET_CONTENT:Const.SNIPPET_DIGEST]
            self.insert_snippet(snippet, digest)

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
            #     1) SELECT content, brief, groups, tags, links, digest, utc, metadata, id FROM snippets WHERE
            #        (content REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?)
            #        ORDER BY id ASC
            #     2) SELECT content, brief, groups, tags, links,digest, utc, metadata FROM snippets WHERE (content REGEXP ?
            #        or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) OR (content REGEXP ?
            #        or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) OR (content REGEXP ?
            #        or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) ORDER BY id ASC
            if keywords and Config.is_search_all():
                columns = ['content', 'brief', 'groups', 'tags', 'links']
                query, qargs = Sqlite3Db._make_regexp_query(keywords, columns)
            elif keywords and Config.is_search_grp():
                columns = ['groups']
                query, qargs = Sqlite3Db._make_regexp_query(keywords, columns)
            elif keywords and Config.is_search_tag():
                columns = ['tags']
                query, qargs = Sqlite3Db._make_regexp_query(keywords, columns)
            elif digest:
                query = ('SELECT content, brief, groups, tags, links, digest, utc, metadata, id FROM snippets ' +
                         'WHERE digest LIKE ?')
                qargs = [digest+'%']
            elif content:
                query = ('SELECT content, brief, groups, tags, links, digest, utc, metadata, id FROM snippets ' +
                         'WHERE content=?')
                qargs = [Const.DELIMITER_CONTENT.join(map(str, content))]
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

    def update_snippet(self, snippet, digest_updated, digest_new, metadata=None):
        """Update existing snippet."""

        if self.conn:
            query = ('UPDATE snippets SET content=?, brief=?, groups=?, tags=?, links=?, digest=?, metadata=? ' +
                     'WHERE digest LIKE ?')
            self.logger.debug('updating snippet %.16s with new digest %.16s and brief "%s"', digest_updated, digest_new,
                              snippet[Const.SNIPPET_BRIEF])
            try:
                self.cursor.execute(query, (Const.get_content_string(snippet),
                                            snippet[Const.SNIPPET_BRIEF],
                                            snippet[Const.SNIPPET_GROUP],
                                            Const.DELIMITER_TAGS.join(map(str, snippet[Const.SNIPPET_TAGS])),
                                            Const.DELIMITER_LINKS.join(map(str, snippet[Const.SNIPPET_LINKS])),
                                            digest_new,
                                            metadata,
                                            digest_updated))
                self.conn.commit()
            except sqlite3.Error as exception:
                self.logger.exception('updating sqlite3 database failed with exception "%s"', exception)
        else:
            self.logger.error('sqlite3 database connection did not exist while new entry was being insert')

    def delete_snippet(self, digest):
        """Delete one snippet based on given digest."""

        cause = Const.DB_FAILURE
        if self.conn:
            query = ('DELETE FROM snippets WHERE digest LIKE ?')
            self.logger.debug('delete snippet with digest %s', digest)
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
            self.logger.error('sqlite3 database connection did not exist while snippet was being deleted')

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
    def _make_regexp_query(keywords, columns):
        """Generate SQL query parameters for specific fields and keywords."""

        query_args = []
        query = 'SELECT content, brief, groups, tags, links, digest, utc, metadata, id FROM snippets WHERE '

        # Generate regexp search like:
        #   1. '(content REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) '
        #   2. '(tags REGEXP ?) '
        search = '('
        for column in columns:
            search = search + column + ' REGEXP ? OR '
        search = search[:-4] # Remove last ' OR ' added by the loop.
        search = search + ') '

        # Generate token for each searched column like
        for token in keywords:
            query = query + search + 'OR '
            query_args = query_args + [token] * len(columns) # Token for each search colum in the row.
        query = query[:-3] # Remove last 'OR ' added by the loop.
        query = query + ' ORDER BY id ASC'

        return (query, query_args)
