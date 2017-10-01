#!/usr/bin/env python3

"""Snippy - Command and solution management from console."""

from snippy.logger import Logger
from snippy.cause import Cause
from snippy.config import Config
from snippy.storage import Storage
from snippy.snippet import Snippet
from snippy.solution import Solution
from snippy.profiler import Profiler


class Snippy(object):
    """Command and solution management."""

    def __init__(self):
        Logger.set_level()
        self.logger = Logger(__name__).get()
        self.config = Config()
        self.storage = Storage()
        self.snippet = Snippet(self.storage)
        self.solution = Solution(self.storage)

    def run_cli(self):
        """Run command line session."""

        self.logger.info('running command line interface')
        self.storage.init()
        if Config.is_category_snippet():
            self.snippet.run()
        elif Config.is_category_solution():
            self.solution.run()
        elif Config.is_category_all() and Config.is_operation_search():
            self.snippet.run()
            self.solution.run()
        else:
            Cause.set_text('content category \'all\' is supported only with search operation')

    def release(self):
        """Release session."""

        Logger.exit(Cause.get_text())
        self.storage.disconnect()
        self.storage = None
        self.snippet = None
        self.solution = None
        self.config = None
        self.logger = None


def main():
    """Main"""

    Profiler.enable()
    snippy = Snippy()
    snippy.run_cli()
    snippy.release()
    Profiler.disable()

if __name__ == "__main__":
    main()
