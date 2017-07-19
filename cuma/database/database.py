#!/usr/bin/env python3

"""database.py: Database management."""

import os
#import sqlite3
from cuma.logger import Logger
from cuma.config import Config


class Database(object):
    """Database management."""

    def __init__(self):
        self.logger = Logger().get()

    def init(self):
        if os.path.exists(Config.get_storage_path()):
            cuma_db = Config.get_storage_file()
            self.logger.debug('creating database into file {:s}'.format(cuma_db))
        else:
            self.logger.error('storage path does not exist {:s}'.format(Config.get_storage_path()))
