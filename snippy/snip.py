#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Snippy - command, solution and code snippet management."""

from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.migrate.migrate import Migrate
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
        self.migrate = Migrate()
        self.server = None
        Config.init()
        self.storage.init()

    def run(self):
        """Run Snippy."""

        if Config.server:
            self.run_server()
        else:
            self.run_cli()

    def run_cli(self):
        """Run command line session."""

        self.logger.debug('running command line interface')
        cli = Cli()  # Exits e.g. in case only a support option like --help is used.
        Config.read_source(cli)
        if Config.is_category_snippet():
            Snippet(self.storage).run()
        elif Config.is_category_solution():
            Solution(self.storage).run()
        elif Config.is_category_all() and Config.is_operation_search():
            Snippet(self.storage).run()
            Solution(self.storage).run()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content category \'all\' is supported only with search operation')

        Logger.print_cause(Cause.get_message())

        return self.cause.reset()

    def run_server(self):
        """Run API server."""

        try:
            from snippy.server.server import Server

            self.server = Server(self.storage)
            self.server.run()
        except ImportError:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'install snippy as server in order to run api server')
            Logger.print_cause(Cause.get_message())

    def release(self):
        """Release session."""

        self.storage.disconnect()
        self.cause.reset()
        self.config.reset()
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
