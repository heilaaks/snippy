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

"""snippy: command, solution and code snippet management."""

import sys

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.source.cli import Cli
from snippy.content.snippet import Snippet
from snippy.content.solution import Solution
from snippy.logger import Logger
from snippy.storage.storage import Storage


class Snippy(object):
    """Command and solution management."""

    def __init__(self, args=None):
        Config.init(args)
        self._logger = Logger(__name__).get_logger()
        self.storage = Storage()
        self.server = None

    def run(self, args=None):
        """Run Snippy."""

        if args:
            Config.load(Cli(args))

        if Config.failure:
            Cause.print_failure()

            return Cause.reset()

        if Config.server:
            self._run_server()
        else:
            self._run_cli()

        return Cause.reset()

    def release(self):
        """Release instance."""

        self.storage.disconnect()
        Cause.reset()
        Config.reset()
        Logger.reset()

    def _run_cli(self):
        """Run command line session."""

        if Config.is_category_snippet:
            Snippet(self.storage).run()
        elif Config.is_category_solution:
            Solution(self.storage).run()
        elif Config.is_category_all and Config.is_operation_search:
            Snippet(self.storage).run()
            Solution(self.storage).run()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content category \'all\' is supported only with search operation')

        Cause.print_message()

    def _run_server(self):
        """Run API server."""

        try:
            from snippy.server.server import Server

            self.server = Server(self.storage)
            self.server.run()
        except ImportError:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'install snippy as a server in order to run api server')
            Cause.print_message()


def main(args):
    """Run Snippy."""

    snippy = Snippy(args)
    snippy.run()
    snippy.release()


if __name__ == "__main__":
    main(sys.argv)
