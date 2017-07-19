#!/usr/bin/env python3

"""database.py: Database management."""

import sqlite3
from cuma.logger import Logger


class Database(object):
    """Database management."""

    def __init__(self):
        self.logger = Logger().get()

    def init(self, location):
        self.logger.debug('creating database into file {:s}'.format(location))
