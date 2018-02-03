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

import sys

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

    def __init__(self, args=None):
        Config(args)
        self.logger = Logger(__name__).get()
        self.storage = Storage()
        self.server = None

    def run(self):
        """Run Snippy."""

        if Config.server:
            self.run_server()
        elif Config.cli:
            self.run_cli()
        else:
            self.release()

    def run_cli(self, args=None):
        """Run command line session."""

        self.logger.debug('running command line interface')
        args = Config.init_args if args is None else args
        Config.read_source(Cli(args))
        if Config.is_category_snippet:
            Snippet(self.storage).run()
        elif Config.is_category_solution:
            Solution(self.storage).run()
        elif Config.is_category_all and Config.is_operation_search:
            Snippet(self.storage).run()
            Solution(self.storage).run()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content category \'all\' is supported only with search operation')

        Logger.print_cause(Cause.get_message())

        return Cause.reset()

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
        Cause.reset()
        Logger.reset()


def main():
    """Main"""

    Profiler.enable()
    snippy = Snippy(sys.argv)
    snippy.run()
    snippy.release()
    Profiler.disable()


if __name__ == "__main__":
    main()
