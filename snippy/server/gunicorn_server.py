#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""gunicorn_server: Gunicorn WSGI HTTP server."""

import gunicorn.app.base
from gunicorn.six import iteritems

from snippy.config.config import Config
from snippy.logger import Logger


class GunicornServer(gunicorn.app.base.BaseApplication):  # pylint: disable=abstract-method
    """Gunicorn WSGI HTTP server."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornServer, self).__init__()

    def load_config(self):
        """Load configuration."""

        config = {key: value for key, value in iteritems(self.options)
                  if key in self.cfg.settings and value is not None}
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        """Load configuration."""

        return self.application

    @staticmethod
    def post_worker_init(_):
        """Called by Gunicorn server after worker has been initialized.

        This is used to tell user that the server is running.
        """

        Logger.print_status("snippy server running at {0}:{1}".format(Config.server_ip, Config.server_port))

    @staticmethod
    def pre_request(_, __):
        """Called by Gunicorn before executing request.

        This method is used to prevent log from Gunicorn and to rely only
        for Snippy logger in this case. Without this, there is one log printed
        with incorrect operation ID (OID) into logs. The OID refreshed in
        Snippy so the Gunicorn log from new request would be otherwise printed
        with previous request OID which would be incorrect.
        """

        pass

    @staticmethod
    def on_exit(_):
        """Called by Gunicorn server on exit.

        This is used to tell user that the server has been stopped.
        """

        Logger.print_status("snippy server stopped at {0}:{1}".format(Config.server_ip, Config.server_port))
