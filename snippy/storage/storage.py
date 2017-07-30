#!/usr/bin/env python3

"""storage.py: Storage management."""

from snippy.logger import Logger
from snippy.storage.database import Database


class Storage(object):
    """Storage management for snippets."""

    def __init__(self):
        self.logger = Logger().get()
        self.database = Database()

    def init(self):
        """Initialize storage."""

        self.database.init()

    def disconnect(self):
        """Disconnect storage."""

        self.database.disconnect()

    def debug(self):
        """Dump the whole storage."""

        self.database.debug()
