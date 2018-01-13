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

"""logger.py: Common logging."""

from __future__ import print_function
import logging
from random import getrandbits
from signal import signal, getsignal, SIGPIPE, SIG_DFL
import sys
try:
    from gunicorn.glogging import Logger as GunicornLogger
except ImportError as exception:
    pass


class Logger(object):
    """Common logging."""

    # Unique operation ID that identifies logs for each operation.
    SERVER_OID = format(getrandbits(32), "08x")

    def __init__(self, module):
        log_format = '%(asctime)s %(appName)s[%(process)04d] [%(oid)s] [%(levelname)-5s]: %(message)s'
        self.logger = logging.getLogger(module)
        if not self.logger.handlers:
            formatter = CustomFormatter(log_format)
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(formatter)
            handler.addFilter(CustomFilter())
            self.logger.addHandler(handler)
        self.logger = logging.LoggerAdapter(self.logger, {'appName': 'snippy', 'oid': Logger.SERVER_OID})

    def get(self):
        """Return logger."""

        return self.logger

    @staticmethod
    def set_level():
        """Set log level."""

        # Set the log level for all the loggers created under the 'snippy' logger.
        # namespace. This relies on that the module level logger does not set the
        # level and it remains as NOTSET. This causes module level logger to
        # propagete the log to parent where the log record propagates tp the
        # 'snippy' level that is just below root level. The disabled flag will
        # prevent even the critical level logs.
        #
        # Note! The below settings manage also the Gunicorn server logs. There
        #       is a custom logger set for the Gunicorn that causes the Gunicorn
        #       logs to be formatted by this logger class.
        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.CRITICAL)
        if '--debug' in sys.argv or '-vv' in sys.argv:
            logging.getLogger('snippy').disabled = False
            logging.getLogger('snippy').setLevel(logging.DEBUG)

    @classmethod
    def set_new_oid(cls):
        """Set new operation ID."""

        Logger.SERVER_OID = format(getrandbits(32), "08x")

    @staticmethod
    def print_cause(cause):
        """Print exit cause."""

        if logging.getLogger('snippy').getEffectiveLevel() == logging.DEBUG:
            Logger(__name__).get().info('exiting with cause %s', cause.lower())
        elif '-q' not in sys.argv:
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(cause)
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)

    @staticmethod
    def reset():
        """Reset log level to default."""

        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.WARNING)

    @staticmethod
    def debug():
        """Debug logging hierarchy."""

        from logging_tree import printout
        printout()


class CustomFormatter(logging.Formatter):
    """Custom log formatter."""

    def format(self, record):
        """Format log string."""

        max_log_string_length = 150

        # Note! Debug option prints the logs "as is" in full length. Very
        #       verbose option is intended for quick glance of logs when
        #       there is always one log per line.
        #
        # Note! The whole log string including log level name is forced to
        #       lower case in case of very verbose option.
        #
        record_string = super(CustomFormatter, self).format(record)
        if '-vv' in sys.argv:
            record_string = super(CustomFormatter, self).format(record).lower()
            record_string = record_string.replace('\n', ' ').replace('\r', '')
            record_string = record_string[:max_log_string_length] + (record_string[max_log_string_length:] and '...')

        return record_string


class CustomFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Customer log filter."""

    def filter(self, record):
        """Filter with dynamic operation ID setting."""

        record.oid = Logger.SERVER_OID

        return True


class CustomGunicornLogger(GunicornLogger):
    """Custom logger for Gunicorn WSGI HTTP server."""

    def setup(self, cfg):
        super(CustomGunicornLogger, self).setup(cfg)

        # Disable all handlers under 'gunicorn' namespace and prevent log
        # propagation to root logger. The loggers under 'snippy' namespace
        # will take care of the log writing for Gunicorn.
        self._remove_handlers(self.error_log)
        self._remove_handlers(self.access_log)
        logging.getLogger('gunicorn').propagate = False

        self.error_log = Logger('snippy.server.gunicorn.error').get()
        self.access_log = Logger('snippy.server.gunicorn.access').get()

    @staticmethod
    def _remove_handlers(logger):
        """Remove handlers and disable logger."""

        handlers = logger.handlers
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
