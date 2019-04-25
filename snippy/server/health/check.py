#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""check: Healthcheck service for the Snippy server."""

import traceback

try:
    import http.client as httplib
except ImportError:
    import httplib

from snippy.config.config import Config
from snippy.logger import Logger


class Check(object):  # pylint: disable=too-few-public-methods
    """Healthcheck service for the Snippy server."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def run(cls):
        """Run server healthcheck.

        Print logs only from failures. Printing logs from all successful tests
        may be considered valid information to trace that the health check was
        actually run and it was succesful. But creating too many log message
        loses the relevant logs in a mass of logs. As of now, too many extra
        logs are avoided.

        The httplib is a builtin module in Python. The requests module is much
        better from usage point of view. This implementation is chose to avoid
        unnecessary dependencies for a very simple task.

        Returns:
            int: Exit code 0 for success and 1 of failure.
        """

        if Config.server_ssl_cert:
            scheme = 'https://'
            conn = httplib.HTTPSConnection(Config.server_host, timeout=2)
        else:
            scheme = 'http://'
            conn = httplib.HTTPConnection(Config.server_host, timeout=2)

        url = scheme + Config.server_host + Config.server_base_path_rest
        exit_code = 1
        try:
            conn.request(method='GET', url=url)
            resp = conn.getresponse()
            if resp.status == 200:
                exit_code = 0
        except (ConnectionRefusedError, httplib.HTTPException):
            cls._log_exception('server healthcheck failed with exception')
        except Exception:  # pylint: disable=broad-except
            cls._log_exception('server healthcheck failed with unknown exception')

        try:
            conn.close()
        except Exception:  # pylint: disable=broad-except
            cls._log_exception('server healthcheck connection close failed')

        return exit_code

    @classmethod
    def _log_exception(cls, message):
        """Log exception

        Args:
            message (str): Message for the exception log.
        """

        minimized = ' '.join(str(traceback.format_exc()).split())
        cls._logger.debug('{}: {}'.format(message, minimized))
