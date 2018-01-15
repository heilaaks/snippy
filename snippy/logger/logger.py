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
from random import getrandbits
from signal import signal, getsignal, SIGPIPE, SIG_DFL
import logging
import sys
import time
import json
try:
    from gunicorn.glogging import Logger as GunicornLogger
except ImportError:
    pass

try:
    from collections import OrderedDict
except ImportError:
    pass


class Logger(object):
    """Logging methods and rules for Snippy.

    Description
    ===========

    By default, there are no logs printed to the users. This applies also
    to error logs. 
    
    There are two levels of logging verbosity. All logs are printed in full
    length without filters with the --debug option. The -vv (very verbose)
    option prints limited length log messages in lower case letters.

    There are two formats for logs: text (default) and JSON. JSON logs can
    be enabled with --json-logs option. JSON log have more information
    fields than text formatted logs. When -vv option is used with JSON logs,
    it truncates log message in the same way as with text logs.

    Timestamps are in local time with text formatted logs. In case of JSON
    logs, the timestamp is in GMT time zone and it follows strictly the
    ISO8601 format. Both timestamps are in millisecond granularity.

    All logs include operation ID that uniquely identifies all logs within
    specific operation. The operation ID must be refreshed by logger user
    after each operation is completed.

    All logs including Gunicorn server logs are formatted to match format
    defined in this logger.

    All logs are printed to stdout.

    Logging Rules
    =============

    1. Only OK or NOK with cause text must be printed with defaults.
    2. There must be no logs printed to user.
    3. There must be no exceptions printed to user.
    4. Exceptions logs are printed is INFO and all other logs is DEBUG.
    5. Variables printed in logs must be separated with colon.
    6. All other than error logs must be printed in lower case string.
    7. The --debug option must print logs without filters in full-length.
    8. The -vv option must print logs in lower case and one log per line.
    9. All external libraries must follow same log format.
    10. All logs must be printed to stdout.
    """

    # Unique operation ID that identifies logs for each operation.
    SERVER_OID = format(getrandbits(32), "08x")

    def __init__(self, module):
        log_format = '%(asctime)s %(appname)s[%(process)04d] [%(oid)s] [%(levelname)-5s]: %(message)s'
        self.logger = logging.getLogger(module)
        if not self.logger.handlers:
            formatter = CustomFormatter(log_format)
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(formatter)
            handler.addFilter(CustomFilter())
            self.logger.addHandler(handler)
        self.logger = logging.LoggerAdapter(self.logger, {'appname': 'snippy', 'oid': Logger.SERVER_OID})

    def get(self):
        """Return logger."""

        return self.logger

    @staticmethod
    def set_level():
        """Set log level."""

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
        if '--debug' in sys.argv or '-vv' in sys.argv:
            logging.getLogger('snippy').disabled = False
            logging.getLogger('snippy').setLevel(logging.DEBUG)

    @classmethod
    def set_new_oid(cls):
        """Set new operation ID."""

        cls.SERVER_OID = format(getrandbits(32), "08x")

    @staticmethod
    def print_cause(cause):
        """Print exit cause."""

        # The signal handler manipulation and the flush below prevent the
        # 'broken pipe' errors with grep. For example incorrect parameter
        # usage in grep may cause this. /1,2/
        #
        # /1/ https://stackoverflow.com/a/16865106
        # /2/ https://stackoverflow.com/a/26738736
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

        self.error_log = Logger('snippy.server.gunicorn.error').get()
        self.access_log = Logger('snippy.server.gunicorn.access').get()

    @staticmethod
    def _remove_handlers(logger):
        """Remove handlers."""

        handlers = logger.handlers
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
