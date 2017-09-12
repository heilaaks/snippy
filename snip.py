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
        """Return storage session."""

        return self.storage

    def disconnect(self):
        """Disconnect storage session."""

        self.storage.debug()
        self.storage.disconnect()

    def run(self):
        """Run the tool."""

        self.logger.info('running services')
        if Config.is_content_snippet():
            Snippet(self.storage).run()
        elif Config.is_content_solution():
            Solution(self.storage).run()
        else:
            self.logger.error('exiting because of unknown content')

        Logger.exit(self.config.get_exit_cause())


def main(args=None):
    Logger.set_level()
    Profiler.enable()
    Snippy().run()
    Snippy().disconnect()
    Profiler.disable()

if __name__ == "__main__":
    main()
