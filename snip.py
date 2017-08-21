#!/usr/bin/env python3

"""Snippy - A small command line tool to manage command and troubleshooting examples."""

from snippy.logger import Logger
from snippy.config import Config
from snippy.storage import Storage
from snippy.snippet import Snippet
from snippy.resolve import Resolve
from snippy.profiler import Profiler

__author__    = "Heikki J. Laaksonen"
__copyright__ = "Copyright 2017, Heikki J. Laaksonen"
__license__   = "MIT"


class Snippy(object):

    def __init__(self):
        self.logger = Logger().get()
        self.config = Config()

    def run(self):
        self.logger.info('running services')
        storage = Storage()
        storage.init()
        if Config.is_snippet_task():
            Snippet(storage).run()
        elif Config.is_resolve_task():
            Resolve(storage).run()
        else:
            self.logger.error('unknown task defined exiting')

        storage.debug()
        storage.disconnect()

def main(args=None):
    Profiler.enable()
    Snippy().run()
    Profiler.disable()

if __name__ == "__main__":
    main()
