#!/usr/bin/env python3

"""Snippy - A small command line tool to manage command and troubleshooting examples."""

from snippy.logger import Logger
from snippy.config import Config
from snippy.storage import Storage
from snippy.snippet import Snippet
from snippy.resolve import Resolve
from snippy.profiler import Profiler

__author__    = 'Heikki J. Laaksonen'
__copyright__ = 'Copyright 2017, Heikki J. Laaksonen'
__license__   = 'MIT'
__version__   = '0.1'


class Snippy(object):

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.config = Config()

    def run(self):
        self.logger.info('running services')
        storage = Storage().init()
        if Config.is_role_snippet():
            Snippet(storage).run()
        elif Config.is_role_resolve():
            Resolve(storage).run()
        else:
            self.logger.error('exiting because of unknown role')

        storage.debug()
        storage.disconnect()

def main(args=None):
    Logger.set_level()
    Profiler.enable()
    Snippy().run()
    Profiler.disable()

if __name__ == "__main__":
    main()
