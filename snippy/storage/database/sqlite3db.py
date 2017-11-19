#!/usr/bin/env python3

"""sqlite3db.py: Database management."""

import re
import os.path
import sqlite3
from contextlib import closing
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config


class Sqlite3Db(object):
    """Sqlite3 database management."""

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.connection = None

    def init(self):
        """Initialize database."""

        self.connection = self._create_db()

        return self

    def disconnect(self):
        """Close database connection."""

        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.logger.debug('closed sqlite3 database')
            except sqlite3.Error as exception:
                self.logger.exception('closing sqlite3 database failed with exception "%s"', exception)

    def insert_content(self, content, digest, utc, metadata=None):
        """Insert content into database."""

        if self.connection:
            query = ('INSERT OR ROLLBACK INTO contents (data, brief, groups, tags, links, category, filename, ' +
                     'runalias, versions, utc, digest, metadata) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)')
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
                                           utc,
                                           digest,
                                           metadata))
                    self.connection.commit()
            except sqlite3.IntegrityError as exception:
                Cause.set_text('content data already exist with digest {:.16}'.format(self._get_db_digest(content)))
            except sqlite3.Error as exception:
                Cause.set_text('inserting into database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented inserting into database')

    def bulk_insert_content(self, contents):
        """Insert multiple contents into database."""

        # Common failure cases:
        # 1. User imports default content again. In this case there is a list of contents.
        # 2. User imports content from template. In this case there is a single failing content.

        cause = Const.EMPTY
        inserted = 0
        for content in contents:
            if not content.has_data():
                cause = 'no content was inserted due to missing mandatory content data'
                self.logger.info(cause)

                continue
            if content.is_data_template():
                cause = 'no content was stored because the content data is matching to empty template'
                self.logger.info(cause)

                continue

            utc = content.get_utc()
            digest = content.get_digest()
            if not self._select_content_data(content.get_data()):
                if digest != content.compute_digest():
                    self.logger.debug('invalid digest found and updated while importing content "%s"', content.get_data())
                    digest = content.compute_digest()

                inserted = inserted + 1
                self.insert_content(content, digest, utc)
            else:
                cause = 'no content was inserted because content data already existed'
                self.logger.info(cause)

        self.logger.debug('inserted %d out of %d content', inserted, len(contents))

        if not contents:
            cause = 'no content found to be stored'

        if not inserted and cause:
            Cause.set_text(cause)

    def select_content(self, category, keywords=None, digest=None, data=None):
        """Select content."""

        rows = ()
        if self.connection:
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
            elif Config.is_content_digest():
                query = ('SELECT * FROM contents WHERE digest LIKE ?')
                qargs = [digest+'%']
            elif Config.is_content_data():
                query = ('SELECT * FROM contents WHERE data LIKE ?')
                qargs = ['%'+Const.DELIMITER_DATA.join(map(str, data))+'%']
            else:
                Cause.set_text('please define keyword, digest or content data as search criteria')

                return rows

            self.logger.debug('running select query "%s"', query)
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute(query, qargs)
                    rows = cursor.fetchall()
            except sqlite3.Error as exception:
                Cause.set_text('selecting from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented searching from database')

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
                Cause.set_text('selecting data from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented searching from database')

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
                Cause.set_text('selecting all from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented selecting all content from database')

        return rows

    def update_content(self, content, digest, utc, metadata=None):
        """Update existing content."""

        if self.connection:
            query = ('UPDATE contents SET data=?, brief=?, groups=?, tags=?, links=?, category=?, filename=?, '
                     'runalias=?, versions=?, utc=?, digest=?, metadata=? WHERE digest LIKE ?')
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
                                           utc,
                                           digest,
                                           metadata,
                                           content.get_digest(Const.STRING_CONTENT)))
                    self.connection.commit()
            except sqlite3.Error as exception:
                Cause.set_text('updating database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented updaring content in database')

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
                    elif cursor.rowcount == 0:
                        Cause.set_text('cannot find content to be deleted with digest {:.16}'.format(digest))
                    else:
                        self.logger.info('unexpected row count %d while deleting with digest %s', cursor.rowcount, digest)
            except sqlite3.Error as exception:
                Cause.set_text('deleting from database failed with exception {}'.format(exception))
        else:
            Cause.set_text('internal error prevented deleting content from database')

    def debug(self):
        """Dump the whole database."""

        if self.connection:
            try:
                with closing(self.connection.cursor()) as cursor:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    self.logger.debug('sqlite3 dump %s', cursor.fetchall())
            except sqlite3.Error as exception:
                Cause.set_text('dumping database failed with exception {}'.format(exception))

    def _create_db(self):
        """Create the database."""

        schema = Const.EMPTY
        location = Sqlite3Db._get_db_location()
        storage_schema = Config.get_storage_schema()
        if os.path.isfile(storage_schema):
            with open(storage_schema, 'rt') as schema_file:
                try:
                    schema = schema_file.read()
                except IOError as exception:
                    Cause.set_text('reading database schema failed with exception {}'.format(exception))
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
            Cause.set_text('creating database failed with exception {}'.format(exception))

        return connection

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
        contents = self._select_content_data(content.get_data())
        if len(contents) == 1:
            digest = contents[0][Const.DIGEST]
        else:
            self.logger.debug('unexpected number %d of %s received while searching', len(contents), category)

        return digest
