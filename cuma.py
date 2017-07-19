#!/usr/bin/env python3

"""Command Utility Manager for code and command sniplets."""

from cuma.logger import Logger
from cuma.logger import LoggerWrapper
from cuma.config import Config
from cuma.database import Database

__author__    = "Heikki J. Laaksonen"
__copyright__ = "Copyright 2017, Heikki J. Laaksonen"
__license__   = "MIT"


class Cuma(object):

    def __init__(self):
        self.logger = Logger().get()
        self.config = Config()

    def run(self):
        self.logger.info('initiating service')
        #LoggerWrapper.debug('initiating serviceeeeee') # does not work.
        Database().init()

def main(args=None):
    Cuma().run()

if __name__ == "__main__":
    main()
