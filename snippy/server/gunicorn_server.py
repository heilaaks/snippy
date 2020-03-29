# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""gunicorn_server: Gunicorn WSGI HTTP server."""

import gunicorn.app.base

from snippy.logger import Logger


class GunicornServer(gunicorn.app.base.BaseApplication):  # pylint: disable=abstract-method
    """Gunicorn WSGI HTTP server."""

    def __init__(self, app, options):
        self.options = options
        self.application = app
        super(GunicornServer, self).__init__()

    def load_config(self):
        """Load configuration."""

        for key in self.options.keys():
            self.cfg.set(key, self.options[key])

    def load(self):
        """Load configuration."""

        return self.application

    @staticmethod
    def post_worker_init(worker):
        """Gunicorn worker initialized hook.

        This is called by the Gunicorn framework after a worker has been
        initialized. This is used to tell user that the server is running.
        Gunicorn server listen IP address is printed from workber because
        of a use where a random free ephemeral port is selected by OS.

        Args:
            worker (obj): Gunicorn Worker() class object.
        """

        listeners = ','.join([str(l) for l in worker.sockets])
        Logger.print_status('snippy server running at: {}'.format(listeners))

    @staticmethod
    def pre_fork(server, worker):
        """Gunicorn worker pre-fork hook.

        This hook is used to transfer the worker real port to the server to
        be used when the server close. In case ephemeral ports allocated by
        the operating system is used, the port is not known by the Snippy
        configuration.

        Because the server and worker are difference processes, it is not
        possible to transfer the data from worker after it has been forked.

        Args:
            server (obj): Gunicorn Arbiter() class object.
            worker (obj): Gunicorn Worker() class object.
        """

        listeners = ','.join([str(l) for l in worker.sockets])
        server.app.options['snippy_host'] = listeners

    @staticmethod
    def pre_request(_, __):
        """Gunicorn pre-request hook.

        This hook is used to prevent a log from the Gunicorn with incorrect
        operation ID (OID).  Without this, the first log message for each
        HTTP request would contain OID from the previous HTTP request.
        """

    @staticmethod
    def on_exit(server):
        """Gunicorn server exit hook.

        This is used to tell user that the server has been stopped.

        Args:
            server (obj): Gunicorn Arbiter() class object.
        """

        Logger.print_status('snippy server stopped at: {}'.format(server.app.options['snippy_host']))
