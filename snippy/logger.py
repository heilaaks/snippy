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

"""logger: Logging services."""

from __future__ import print_function

from functools import wraps
from random import getrandbits
from signal import signal, getsignal, SIGPIPE, SIG_DFL
import logging
import sys
import time

import json

try:
    from gunicorn.glogging import Logger as GunicornLogger
except ImportError:
    GunicornLogger = object

try:
    from collections import OrderedDict
except ImportError:
    pass


class Logger(object):
    """Logging services."""

    # Logger configuration.
    CONFIG = {}

    # Unique operation ID that identifies logs for each operation.
    SERVER_OID = format(getrandbits(32), "08x")

    def __init__(self, module):
        """

        Parameters
        ----------
        Args:
           module (str): Name of the module that requests a Logger.
        """

        # Use severity level names from RFC 5424 /1/. The level name is
        # printed with one letter when debug logs are in text mode. In
        # JSON format logs contain full length severity level name.
        #
        # /1/ https://en.wikipedia.org/wiki/Syslog#Severity_level
        logging.addLevelName(logging.CRITICAL, 'crit')
        logging.addLevelName(logging.ERROR, 'err')
        logging.addLevelName(logging.WARNING, 'warning')
        logging.addLevelName(logging.INFO, 'info')
        logging.addLevelName(logging.DEBUG, 'debug')
        log_format = '%(asctime)s %(appname)s[%(process)04d] [%(levelname).1s] [%(oid)s]: %(message)s'
        self.logger = logging.getLogger(module)
        if not self.logger.handlers:
            formatter = CustomFormatter(log_format)
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(formatter)
            handler.addFilter(CustomFilter())
            self.logger.addHandler(handler)
        self.logger = logging.LoggerAdapter(self.logger, {'appname': 'snippy', 'oid': Logger.SERVER_OID})

    @classmethod
    def configure(cls, config):
        """Set logger configuration.

        Parameters
        ----------
        Args:
            config (dict): Logger configuration dictionary.

        Examples
        --------
        >>> Logger.configure({'debug': True,
        >>>                   'very_verbose': False,
        >>>                   'quiet': False,
        >>>                   'json_logs': True})
        """

        cls.CONFIG = config

        # Set the effective log level for all the loggers created under
        # 'snippy' logger namespace. This relies on that the module level
        # logger does not set the level and it remains as NOTSET. This
        # causes module level logger to propagate the log record to parent
        # logger where it eventually reaches the 'snippy' level that is
        # just below the 'root' level logger.
        #
        # The 'disabled' flag prevents also the critical level logs.
        #
        # Note! The below settings manage also the Gunicorn server logs.
        #       There is a custom logger set that causes the Gunicorn logs
        #       to be formatted by Snippy logging framework.
        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.CRITICAL)
        if cls.CONFIG['debug'] or config['very_verbose']:
            logging.getLogger('snippy').disabled = False
            logging.getLogger('snippy').setLevel(logging.DEBUG)

    @classmethod
    def refresh_oid(cls):
        """Refresh operation ID (OID).

        The OID is used to separate logs within one operation. The helps
        post-processing of the logs by allowing for example querying all
        the logs in failing operatoion.
        """

        cls.SERVER_OID = format(getrandbits(32), "08x")

    @classmethod
    def print_cause(cls, cause):
        """Print exit cause.

        Parameters
        ----------
        Args:
            cause (str): Exit cause to be printed on stdout.
        """

        # The signal handler manipulation and the flush below prevent the
        # 'broken pipe' errors with grep. For example incorrect parameter
        # usage in grep may cause this. /1,2/
        #
        # /1/ https://stackoverflow.com/a/16865106
        # /2/ https://stackoverflow.com/a/26738736
        if logging.getLogger('snippy').getEffectiveLevel() == logging.DEBUG:
            Logger(__name__).logger.info('exiting with cause %s', cause.lower())
        elif not cls.CONFIG['quiet']:
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
    def timeit(method):
        """Time method by measuring it latency.

        The operation ID (OID) is refreshed automatically at the end.
        """

        @wraps(method)
        def timed(*args, **kw):
            """Wrapper to measure latency."""

            start = time.time()
            result = method(*args, **kw)
            Logger(__name__).logger.debug('operation duration: %.6fs', (time.time() - start))
            Logger.refresh_oid()

            return result

        return timed

    @staticmethod
    def debug():
        """Debug Logger by printing logging hierarchy."""

        from logging_tree import printout
        printout()


class CustomFormatter(logging.Formatter):
    """Custom log formatting."""

    MAX_MSG = 150
    gmttime = True if '--json-logs' in sys.argv else False
    converter = time.gmtime if gmttime else time.localtime
    dateformat = '%Y-%m-%dT%H:%M:%S' if gmttime else '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        """Format log string."""

        # Debug option prints logs "as is" in full-length. Very verbose
        # option truncates logs and guarantees only one log per line
        # with all lower case characters.
        if '--json-logs' in sys.argv:
            log_string = super(CustomFormatter, self).format(record)
            log_string = self._jsonify(record)
        elif '-vv' in sys.argv:
            log_string = super(CustomFormatter, self).format(record).lower()
            log_string = log_string.replace('\n', ' ').replace('\r', '')
            log_string = log_string[:CustomFormatter.MAX_MSG] + (log_string[CustomFormatter.MAX_MSG:] and '...')
        else:
            log_string = super(CustomFormatter, self).format(record)

        return log_string

    def formatTime(self, record, datefmt=None):
        """Format log timestamp."""

        # JSON logs are printed in ISO8601 format with UTC timestamps. All
        # other logs are printed in local time with space between date and
        # time instead of 'T' that is required by ISO8601.
        created = self.converter(record.created)
        timstamp = time.strftime(self.dateformat, created)
        if self.gmttime:
            time_string = '%s.%03dZ' % (timstamp, record.msecs)
        else:
            time_string = '%s.%03d' % (timstamp, record.msecs)

        return time_string

    @staticmethod
    def _jsonify(record):
        """Create JSON string from log record."""

        try:
            log = OrderedDict()
        except NameError:
            log = {}

        fields = ['asctime', 'appname', 'process', 'oid', 'levelno', 'levelname', 'name', 'lineno', 'thread', 'message']
        for field in fields:
            log[field] = record.__dict__.get(field)

        if '-vv' in sys.argv:
            log['message'] = log['message'][:CustomFormatter.MAX_MSG] + (log['message'][CustomFormatter.MAX_MSG:] and '...')

        return json.dumps(log)


class CustomFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Customer log filter."""

    def filter(self, record):
        """Filtering with dynamic operation ID setting."""

        record.oid = Logger.SERVER_OID

        return True


class CustomGunicornLogger(GunicornLogger):
    """Custom logger for Gunicorn HTTP server."""

    def setup(self, cfg):
        super(CustomGunicornLogger, self).setup(cfg)

        # Disable all handlers under 'gunicorn' namespace and prevent log
        # propagation to root logger. The loggers under 'snippy' namespace
        # will take care of the log writing for Gunicorn.
        self._remove_handlers(self.error_log)
        self._remove_handlers(self.access_log)
        logging.getLogger('gunicorn').propagate = False

        self.error_log = Logger('snippy.server.gunicorn.error').logger
        self.access_log = Logger('snippy.server.gunicorn.access').logger

    @staticmethod
    def _remove_handlers(logger):
        """Remove handlers."""

        handlers = logger.handlers
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
