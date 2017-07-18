#!/usr/bin/env python3

"""Command Utility Manager for code and command sniplets."""

from cuma.database import Database
from cuma.config import Config
from cuma.logger import Logger

__author__    = "Heikki J. Laaksonen"
__copyright__ = "Copyright 2017, Heikki J. Laaksonen"
__license__   = "MIT"


class Cuma(object):

    def __init__(self):
        self.logger = Logger().get()
        self.config = Config()

    def run(self):
        self.logger.info('initiating service')
        Database().init(self.config.get_storage_location())

def main():
    Cuma().run()

if __name__ == "__main__":
    main()
