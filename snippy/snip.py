#!/usr/bin/env python3

"""Snippy - Command and solution management from console."""

from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.arguments import Arguments
from snippy.storage.storage import Storage
from snippy.content.snippet import Snippet
from snippy.content.solution import Solution
from snippy.devel.profiler import Profiler


class Snippy(object):
    """Command and solution management."""

    def __init__(self):
        Logger.set_level()
        self.logger = Logger(__name__).get()
        self.cause = Cause()
        self.config = None
        self.storage = Storage()
        self.snippet = Snippet(self.storage)
        self.solution = Solution(self.storage)

    def run_cli(self):
        """Run command line session."""

        self.logger.info('running command line interface')
        self.config = Config(Arguments())
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

        Logger.print_cause(Cause.get_text())

        return self.cause.reset()

    def release(self):
        """Release session."""

        self.storage.disconnect()
        self.cause.reset()


def main():
    """Main"""

    Profiler.enable()
    snippy = Snippy()
    snippy.run_cli()
    snippy.release()
    Profiler.disable()


if __name__ == "__main__":
    main()
