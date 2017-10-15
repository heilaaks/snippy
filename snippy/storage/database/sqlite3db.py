#!/usr/bin/env python3

"""sqlite3db.py: Database management."""

import os
import re
import sqlite3
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config


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

        if self.conn:
            query = ('INSERT OR ROLLBACK INTO contents (data, brief, groups, tags, links, category, filename, utc, ' +
                     'digest, metadata) VALUES(?,?,?,?,?,?,?,?,?,?)')
            self.logger.debug('insert "%s" with digest %.16s', content.get_brief(), digest)
            try:
                self.cursor.execute(query, (content.get_data(Const.STRING_CONTENT),
                                            content.get_brief(Const.STRING_CONTENT),
                                            content.get_group(Const.STRING_CONTENT),
                                            content.get_tags(Const.STRING_CONTENT),
                                            content.get_links(Const.STRING_CONTENT),
                                            content.get_category(Const.STRING_CONTENT),
                                            content.get_filename(Const.STRING_CONTENT),
                                            utc,
                                            digest,
                                            metadata))
                self.conn.commit()
            except sqlite3.IntegrityError as exception:
                Cause.set_text('content data already exist with digest {:.16}'.format(self._get_db_digest(content)))
            except sqlite3.Error as exception:
                Cause.set_text('inserting into database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented inserting into database')

    def bulk_insert_content(self, contents):
        """Insert multiple contents into database."""

        inserted = 0
        for content in contents:
            utc = content.get_utc()
            digest = content.get_digest()
            if not self.select_content(content.get_category(), data=content.get_data()):
                if digest != content.compute_digest():
                    self.logger.debug('invalid digest found and updated while importing content "%s"', content.get_data())
                    digest = content.compute_digest()

                inserted = inserted + 1
                self.insert_content(content, digest, utc)
            else:
                self.logger.debug('content data already exists "%s"', content.get_data())
        self.logger.debug('inserted %d out of %d content', inserted, len(contents))

    def select_content(self, category, keywords=None, digest=None, data=None):
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
            query = ()
            qargs = []
            if keywords and Config.is_search_all():
                columns = ['data', 'brief', 'groups', 'tags', 'links', 'digest']
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
            elif data:
                query = ('SELECT * FROM contents WHERE data=?')
                qargs = [Const.DELIMITER_DATA.join(map(str, data))]
            else:
                Cause.set_text('internal error where search query was not defined')

            self.logger.debug('running select query "%s"', query)
            try:
                self.cursor.execute(query, qargs)
                rows = self.cursor.fetchall()
            except sqlite3.Error as exception:
                Cause.set_text('selecting from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented searching from database')

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
                Cause.set_text('selecting all from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented selecting all content from database')

        return rows

    def update_content(self, content, digest, utc, metadata=None):
        """Update existing content."""

        if self.conn:
            query = ('UPDATE contents SET data=?, brief=?, groups=?, tags=?, links=?, category=?, filename=?, utc=?, '
                     'digest=?, metadata=? WHERE digest LIKE ?')
            self.logger.debug('updating content %.16s with new digest %.16s and brief "%s"', content.get_digest(), digest,
                              content.get_brief())
            try:
                self.cursor.execute(query, (content.get_data(Const.STRING_CONTENT),
                                            content.get_brief(Const.STRING_CONTENT),
                                            content.get_group(Const.STRING_CONTENT),
                                            content.get_tags(Const.STRING_CONTENT),
                                            content.get_links(Const.STRING_CONTENT),
                                            content.get_category(Const.STRING_CONTENT),
                                            content.get_filename(Const.STRING_CONTENT),
                                            utc,
                                            digest,
                                            metadata,
                                            content.get_digest(Const.STRING_CONTENT)))
                self.conn.commit()
            except sqlite3.Error as exception:
                Cause.set_text('updating database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented updaring content in database')

    def delete_content(self, digest):
        """Delete single content based on given digest."""

        if self.conn:
            query = ('DELETE FROM contents WHERE digest LIKE ?')
            self.logger.debug('delete content with digest %s', digest)
            try:
                self.cursor.execute(query, (digest+'%',))
                if self.cursor.rowcount == 1:
                    self.conn.commit()
                elif self.cursor.rowcount == 0:
                    Cause.set_text('cannot find content to be deleted with digest {:.16}'.format(digest))
                else:
                    self.logger.info('unexpected row count %d while deleting with digest %s', self.cursor.rowcount, digest)
            except sqlite3.Error as exception:
                Cause.set_text('deleting from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented deleting content from database')

    def debug(self):
        """Dump the whole database."""

        if self.conn:
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.logger.debug('sqlite3 dump %s', self.cursor.fetchall())
            except sqlite3.Error as exception:
                Cause.set_text('dumping database failed with exception {}'.format(exception))

    def _create_db(self):
        """Create the database."""

        location = Sqlite3Db._get_db_location()
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
            self.logger.debug('sqlite3 database persisted in %s', location)
        except sqlite3.Error as exception:
            Cause.set_text('creating database failed with exception {}'.format(exception))

        return (conn, cursor)

    @staticmethod
    def _get_db_location():
        """Get the location where there the database is going to be stored."""

        location = Const.EMPTY

        if Config.is_storage_in_memory():
            location = "file::memory:?cache=shared"
        else:
            if os.path.exists(Config.get_storage_path()) and os.access(Config.get_storage_path(), os.W_OK):
                location = Config.get_storage_file()
            else:
                Cause.set_text('storage path does not exist or is not accessible: {}'.format(Config.get_storage_path()))

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
        #   1. '(data REGEXP ? or brief REGEXP ? or groups REGEXP ? or tags REGEXP ? or links REGEXP ?) AND (category=?) '
        #   2. '(tags REGEXP ?) AND (category=?) '
        search = '('
        for column in columns:
            search = search + column + ' REGEXP ? OR '
        search = search[:-4]  # Remove last ' OR ' added by the loop.
        search = search + ') AND (category=?) '

        # Generate token for each searched column like
        for token in keywords:
            query = query + search + 'OR '
            query_args = query_args + [token] * len(columns) + [category]  # Token for each search colum in the row.
        query = query[:-3]  # Remove last 'OR ' added by the loop.
        query = query + 'ORDER BY id ASC'

        return (query, query_args)

    def _get_db_digest(self, content):
        """Return digest of given content from database."""

        digest = Const.EMPTY
        category = content.get_category(Const.STRING_CONTENT)
        contents = self.select_content(category, data=content.get_data())
        if len(contents) == 1:
            digest = contents[0][Const.DIGEST]
        else:
            self.logger.error('unexpected number %d of %s received while searching', len(contents), category)

        return digest
