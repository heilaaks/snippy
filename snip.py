#!/usr/bin/env python3

"""Snippy - Command line tool to manage command examples and troubleshooting solutions."""

from snippy.logger import Logger
from snippy.config import Config
from snippy.storage import Storage
from snippy.snippet import Snippet
from snippy.solution import Solution
from snippy.profiler import Profiler


class Snippy(object):

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.config = Config()

    def run(self):
        self.logger.info('running services')
        storage = Storage().init()
        if Config.is_content_snippet():
            Snippet(storage).run()
        elif Config.is_content_solution():
            Resolve(storage).run()
        else:
            self.logger.error('exiting because of unknown content')

        storage.debug()
        storage.disconnect()
        Logger.exit(self.logger, Config.get_exit_cause(),)

def main(args=None):
    Logger.set_level()
    Profiler.enable()
    Snippy().run()
    Profiler.disable()

if __name__ == "__main__":
    main()
