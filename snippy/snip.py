#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""Snippy is a software development and maintenance notes manager."""

import sys

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.config.source.cli import Cli
from snippy.content.all_content import AllContent
from snippy.content.content import Content
from snippy.logger import Logger
from snippy.storage.storage import Storage


class Snippy(object):
    """Software development and maintenance notes manager."""

    def __init__(self, args):
        Config.init(args)
        self._exit_code = 0
        self._logger = Logger.get_logger(__name__)
        self.storage = Storage()
        self.server = None

    def run(self, args=None):
        """Run service.

        Args:
            list: Command line arguments.
        """

        if args:
            Config.load(Cli(args))

        if Config.failure:
            Cause.print_failure()

            return Cause.reset()

        if Config.run_server:
            self._run_server()
        elif Config.run_healthcheck:
            self._run_healthcheck()
        else:
            self._run_cli()

        return Cause.reset()

    def release(self):
        """Release service resource."""

        self.storage.disconnect()
        Cause.reset()
        Config.reset()
        Logger.reset()

    def _run_cli(self):
        """Run CLI command."""

        if Config.is_category_snippet:
            Content(self.storage, Const.SNIPPET).run()
        elif Config.is_category_solution:
            Content(self.storage, Const.SOLUTION).run()
        elif Config.is_category_reference:
            Content(self.storage, Const.REFERENCE).run()
        elif Config.is_multi_category and (Config.is_operation_search or Config.is_operation_export or Config.is_operation_import):
            AllContent(self.storage).run()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content category \'all\' is supported only with search, import or export operations')

        Cause.print_message()

    def _run_server(self):
        """Run server."""

        try:
            from snippy.server.server import Server  # pylint: disable=bad-option-value, import-outside-toplevel

            if Config.defaults:
                AllContent(self.storage).import_all()
            self.server = Server(self.storage)
            self.server.run()
        except ImportError:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'install snippy as a server in order to run api server')
            Cause.print_message()

    def _run_healthcheck(self):
        """Run server healthcheck."""

        from snippy.server.health.check import Check  # pylint: disable=bad-option-value, import-outside-toplevel

        self._exit_code = Check().run()

    def exit(self):
        """Exit service wrapper."""

        sys.exit(self._exit_code)


def main(args=None):
    """Run Snippy."""

    if not args:
        args = sys.argv

    snippy = Snippy(args)
    snippy.run()
    snippy.release()
    snippy.exit()


if __name__ == "__main__":
    main()
