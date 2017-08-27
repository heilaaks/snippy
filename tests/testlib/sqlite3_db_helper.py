#!/usr/bin/env python3

"""sqlite3_db_helper.py: Helper methods for Sqlite3 database testing."""

import sqlite3
from snippy.logger import Logger


class Sqlite3DbHelper(object): # pylint: disable=too-few-public-methods
    """Helper methods for Sqlite3 database testing."""

    SNIPPET1 = {'content': 'docker rm $(docker ps -a -q)',
                'brief': 'Remove all docker containers',
                'category': 'docker',
                'tags': ['container', 'cleanup', 'docker'],
                'links': ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'],
                'digest': 'da217a911ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}
    SNIPPET2 = {'content': 'docker rmi $(docker images -f dangling=true -q)',
                'brief': 'Remove all dangling image layers',
                'category': 'docker',
                'tags': ['container', 'cleanup', 'docker'],
                'links': ['https://www.faked.com/tutorials/how-to-remove-docker-images-containers-and-volumes'],
                'digest': 'aa106d811ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.conn, self.cursor = self._connect_db()

    def select_snippet(self, snippet_id):
        """Select requested snippet with unique ID."""

        self.logger.debug('select snippet with id {:d}'.format(snippet_id))
        self.cursor.execute('select * from snippets')
        rows = self.cursor.fetchall()
        for row in rows:
            self.logger.debug("fetched row %s", row)

    def select_all_snippets(self):
        """Select all snippets."""

        self.cursor.execute('select * from snippets')
        rows = self.cursor.fetchall()
        for row in rows:
            self.logger.debug("fetched row %s", row)

        return rows

    def _connect_db(self):
        """Connect to shared memory database."""

        self.logger.debug("connect to sqlite3 database")
        conn = sqlite3.connect('file::memory:?cache=shared', check_same_thread=False, uri=True)
        cursor = conn.cursor()

        return (conn, cursor)
