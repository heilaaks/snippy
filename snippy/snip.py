#!/usr/bin/env python3

"""Snippy - Command and solution management from console."""

from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.source.cli import Cli
from snippy.config.config import Config
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
        self.config = Config()
        self.storage = Storage()
        self.snippet = Snippet(self.storage)
        self.solution = Solution(self.storage)
        self.server = None
        self.storage.init()

    def run(self):
        """Run Snippy."""

        if Config.is_server():
            self.run_server()
        else:
            self.run_cli()

    def run_cli(self):
        """Run command line session."""

        self.logger.info('running command line interface')
        self.config.read_source(Cli())
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

    def run_server(self):
        """Run API server."""

        # Requires Snippy installed with server dependencies.
        from snippy.server.server import Server

        self.server = Server(self.config, self.storage)
        self.server.run()

    def release(self):
        """Release session."""

        self.storage.disconnect()
        self.cause.reset()
        Logger.reset()


def main():
    """Main"""

    Profiler.enable()
    snippy = Snippy()
    snippy.run()
    snippy.release()
    Profiler.disable()


if __name__ == "__main__":
    main()
