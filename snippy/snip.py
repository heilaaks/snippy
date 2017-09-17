#!/usr/bin/env python3

"""Snippy - Command and solution example management from console."""

from snippy.logger import Logger
from snippy.config import Config
from snippy.storage import Storage
from snippy.snippet import Snippet
from snippy.solution import Solution
from snippy.profiler import Profiler


class Snippy(object):
    """Command and solution management."""

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.config = Config()
        self.storage = Storage()

    def release(self):
        """Release the command line session."""

        self.storage.debug()
        self.storage.disconnect()

        Logger.exit(self.config.get_exit_cause())

    def run(self):
        """Run the command line session."""

        self.logger.info('running command line interface')
        self.storage.init()
        if Config.is_content_snippet():
            Snippet(self.storage).run()
        elif Config.is_content_solution():
            Solution(self.storage).run()
        else:
            self.logger.error('unknown content type')


def main():
    """Main"""

    Logger.set_level()
    Profiler.enable()
    snippy = Snippy()
    snippy.run()
    snippy.release()
    Profiler.disable()

if __name__ == "__main__":
    main()
