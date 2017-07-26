#!/usr/bin/env python3

"""Command Utility Manager for code and command snippets."""

from cuma.logger import Logger
from cuma.config import Config
from cuma.database import Database
from cuma.profiler import Profiler

__author__    = "Heikki J. Laaksonen"
__copyright__ = "Copyright 2017, Heikki J. Laaksonen"
__license__   = "MIT"


class Cuma(object):

    def __init__(self):
        self.logger = Logger().get()
        self.config = Config()

    def run(self):
        self.logger.info('initiating services')
        storage = Database()
        storage.init()
        storage.debug()
        storage.disconnect()

def main(args=None):
    Profiler.enable()
    Cuma().run()
    Profiler.disable()

if __name__ == "__main__":
    main()
