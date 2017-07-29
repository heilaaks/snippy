#!/usr/bin/env python3

"""Snippy - A small command line tool to manage command and troubleshooting examples."""

from snippy.logger import Logger
from snippy.config import Config
from snippy.database import Database
from snippy.profiler import Profiler

__author__    = "Heikki J. Laaksonen"
__copyright__ = "Copyright 2017, Heikki J. Laaksonen"
__license__   = "MIT"


class Snippy(object):

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
    Snippy().run()
    Profiler.disable()

if __name__ == "__main__":
    main()