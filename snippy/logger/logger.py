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

"""logger.py: Common logger for the tool."""

from __future__ import print_function
import sys
import logging
from signal import signal, getsignal, SIGPIPE, SIG_DFL
try:
    from gunicorn.glogging import Logger as GunicornLogger
except ImportError as exception:
    pass


class Logger(object):
    """Logging wrapper."""

    def __init__(self, module):
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-13s : %(message)s'
        self.logger = logging.getLogger(module)
        if not self.logger.handlers:
            formatter = CustomFormatter(log_format)
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            # Logger adapter has extended API over logger. The adapter
            # overriding the logger is intended behaviour here.
            self.logger = logging.LoggerAdapter(self.logger, {'appName': 'snippy'})

    def get(self):
        """Return logger."""

        return self.logger

    @staticmethod
    def set_level():
        """Set log level."""

        # Set the log level for all the loggers created under the snippy logger.
        # This relies on that the module level logger does not set the level and
        # it remains NOTSET. This causes module level logger to propagete the log
        # to higher levels where it ends up the 'snippy' level that is just below
        # root level. The disabled flag will prevent even the critical level logs.
        #
        # Note! The below manages also the Gunicorn server logs. There is a custom
        #       logger set for the Gunicorn that sets the access and error logs
        #       under snippy namespace.
        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.CRITICAL)
        if '--debug' in sys.argv or '-vv' in sys.argv:
            logging.getLogger('snippy').disabled = False
            logging.getLogger('snippy').setLevel(logging.DEBUG)

    @staticmethod
    def reset():
        """Reset log level to default."""

        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.WARNING)

    @staticmethod
    def print_cause(cause):
        """Print exit cause for the tool."""

        if logging.getLogger('snippy').getEffectiveLevel() == logging.DEBUG:
            Logger(__name__).get().info('exiting with cause %s', cause.lower())
        elif '-q' not in sys.argv:
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(cause)
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)

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

        # Option -vv gets all the logs but they are truncated. The --debug
        # option prints the full length logs.
        record_string = super(CustomFormatter, self).format(record)
        if '--debug' not in sys.argv:
            record_string = record_string[:max_log_string_length] + (record_string[max_log_string_length:] and '...')

        return record_string


class CustomGunicornLogger(GunicornLogger):
    """Custom logger for Gunicorn WSGI HTTP server."""

    def setup(self, cfg):
        super(CustomGunicornLogger, self).setup(cfg)
        self.error_log = Logger('snippy.server.gunicorn.error').get()
        self.access_log = Logger('snippy.server.gunicorn.access').get()
