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
        self.storage = Storage()

    def storage(self):
        """Return active storage session."""

        return self.storage

    def config(self):
        """Return active configuration."""

        return self.config

    def release(self):
        """Release the command line session."""

        self.storage.debug()
        self.storage.disconnect()

        Logger.exit(self.config.get_exit_cause())

    def run(self):
        """Run the command line session."""

        self.logger.info('running command line interface')
        if Config.is_content_snippet():
            Snippet(self.storage).run()
        elif Config.is_content_solution():
            Solution(self.storage).run()
        else:
            self.logger.error('unknown content type')


def main(args=None):
    Logger.set_level()
    Profiler.enable()
    snippy = Snippy()
    snippy.run()
    snippy.release()
    Profiler.disable()

if __name__ == "__main__":
    main()
