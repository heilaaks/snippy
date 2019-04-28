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

"""logger: Logging services."""

from __future__ import print_function

import logging
import sys
import time
from collections import OrderedDict
from functools import wraps
from random import getrandbits
from signal import signal, getsignal, SIGPIPE, SIG_DFL

import json

from snippy.constants import Constants as Const

try:
    from gunicorn.glogging import Logger as GunicornLogger
except ImportError:
    GunicornLogger = object


class Logger(object):
    """Global logging services."""

    # Default maximum length of log message.
    DEFAULT_LOG_MSG_MAX = 80

    # Maximum length of log message for safety and security reasons.
    SECURITY_LOG_MSG_MAX = 10000

    # Custom security log level.
    SECURITY = logging.CRITICAL + 10

    # Unique operation ID that identifies logs for each operation.
    SERVER_OID = format(getrandbits(32), "08x")

    # Custom log format
    LOG_FORMAT = '%(asctime)s %(appname)s[%(process)04d] [%(levelname).1s] [%(oid)s]: %(message)s'

    # Global logger configuration.
    CONFIG = {
        'debug': False,
        'log_json': False,
        'log_msg_max': DEFAULT_LOG_MSG_MAX,
        'quiet': False,
        'very_verbose': False
    }

    # Use severity level names from RFC 5424 /1/. The level name is printed
    # with one letter when debug logs are in text mode. The JSON formatted
    # logs will contain full length log severity level name.
    #
    # The security level is a custom log level only for security events.
    #
    # /1/ https://en.wikipedia.org/wiki/Syslog#Severity_level
    logging.SECURITY = SECURITY
    logging.addLevelName(logging.SECURITY, 'security')
    logging.addLevelName(logging.CRITICAL, 'crit')
    logging.addLevelName(logging.ERROR, 'err')
    logging.addLevelName(logging.WARNING, 'warning')
    logging.addLevelName(logging.INFO, 'info')
    logging.addLevelName(logging.DEBUG, 'debug')

    # Ignore exceptions from logger to prevent them to be shown to end user.
    # For example 'broken pipe' errors with grep can cause these when logs
    # are enabled.
    #
    # There was an effort to implement custom StreamHandler to write log
    # messages to stderr instead of stdout if there is a broken pipe error.
    # The problem was the 'broken pipe' exception does not exist in Python 2
    # and thus making generic code is difficult.
    logging.raiseExceptions = False

    @classmethod
    def get_logger(cls, name=__name__):
        """Get logger.

        A custom logger adapater is returned to support custom level with
        additional logging parameters.

        Args:
            name (str): Name of the module that requests a Logger.

        Returns:
            obj: CustomLoggerAdapter logger to be used by caller.
        """

        logger = logging.getLogger(name)
        if not logger.handlers:
            formatter = CustomFormatter(Logger.LOG_FORMAT)
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(formatter)
            handler.addFilter(CustomFilter())
            logger.addHandler(handler)
        logger = CustomLoggerAdapter(logger, {'appname': 'snippy', 'oid': Logger.SERVER_OID})

        return logger

    @classmethod
    def configure(cls, config):
        """Set and update logger configuration.

        The debug and very_verbose options have precedence over the
        quiet option. That is, if any of the debug options are enabled,
        quiet option does not have effect.

        Args:
            config (dict): Logger configuration dictionary.

        Examples
        --------
        >>> Logger.configure({'debug': True,
        >>>                   'log_json': True,
        >>>                   'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
        >>>                   'quiet': False,
        >>>                   'very_verbose': False})
        """

        cls.CONFIG['debug'] = config['debug']
        cls.CONFIG['log_json'] = config['log_json']
        cls.CONFIG['log_msg_max'] = config['log_msg_max']
        cls.CONFIG['quiet'] = config['quiet']
        cls.CONFIG['very_verbose'] = config['very_verbose']
        if cls.CONFIG['log_msg_max'] > Logger.SECURITY_LOG_MSG_MAX:
            cls.CONFIG['log_msg_max'] = Logger.DEFAULT_LOG_MSG_MAX

        # Set the effective log level for all the loggers created under the
        # 'snippy' namespace. This relies on that the module level logger
        # does not set the level and it remains as NOTSET. This causes
        # module level logger to propagate the log record to parent logger
        # where it eventually reaches the 'snippy' level that is just below
        # the 'root' level logger.
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

        if config['log_msg_max'] > Logger.SECURITY_LOG_MSG_MAX:
            Logger.get_logger().debug('log message length: %s :cannot exceed security limit: %s',
                                      config['log_msg_max'], Logger.SECURITY_LOG_MSG_MAX)

        Logger._update()

    @staticmethod
    def reset():
        """Reset log level to default."""

        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.WARNING)

    @staticmethod
    def remove():
        """Delete all logger handlers."""

        # Remove all handlers. This is needed for testing. This is related
        # to defining the stdout for StreamHandler and to the way how Pytest
        # uses stdout when capsys is used /1/. More information from Python
        # issue /2/.
        #
        # /1/ https://github.com/pytest-dev/pytest/issues/14
        # /2/ https://bugs.python.org/issue6333
        items = list(logging.root.manager.loggerDict.items())
        for name, logger in items:
            if 'snippy' in name:
                logger.handlers = []

    @classmethod
    def refresh_oid(cls):
        """Refresh operation ID (OID).

        The OID is used to separate logs within one operation. The helps
        post-processing of the logs by allowing for example querying all
        the logs in failing operation.
        """

        cls.SERVER_OID = format(getrandbits(32), "08x")

    @classmethod
    def print_stdout(cls, message):
        """Print output to stdout.

        Take care of nasty details like broken pipe when printing to
        stdout.

        Args:
            message (str): Text string to be printed to stdout.
        """

        # The signal handler manipulation and flush setting below prevents
        # 'broken pipe' errors with grep. For example incorrect parameter
        # usage in grep may cause this. See below listed references [1] and
        # [2] with examples that can be used in manual testing testing.
        #
        # NOTE! Catching broken pipe signal can be dangerous [3]. This is
        #       not changed because the alternative is problematic with
        #       Python 2 [3].
        #
        # [1] https://stackoverflow.com/a/16865106
        # [2] https://stackoverflow.com/a/26738736
        # [3] https://stackoverflow.com/a/35761190
        #
        # $ snippy search --sall '--all' --filter crap | grep --all
        # $ snippy search --sall 'test' --filter test -vv | grep --all
        # $ snippy --server-host 127.0.0.1:8080 -vv | grep get
        # $ snippy --help | head -n 20
        # $ snippy --help | tail -n 20
        # $ snippy search --sall . | head -n 20
        # $ snippy search --sall . | tail -n 20
        # $ snippy search --sall . -vv | head -n 20
        # $ snippy search --sall . -vv | tail -n 20
        if message:
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(message)
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)

    @classmethod
    def print_status(cls, status):
        """Print status information like exit cause or server running.

        Print user formatted log messages unless the JSON log formating
        is enabled. The debug and very_verbose options have precedence
        over the quiet option.

        If JSON logs are used, the format of the log must always be JSON.
        This is important for server installation where post processing of
        logs might be done elsewhere and incorrectly formatted logs may be
        discarded or cause errors.

        In order to post process a JSON log, the dictionary structure must
        always follow the same format. Because of this, the log is pushed
        always as a debug level log regardless of the log level to get the
        formatting done.

        Args:
            status (str): Status to be printed on stdout.
        """

        if Logger.CONFIG['log_json'] and not cls.CONFIG['quiet']:
            level = logging.getLogger('snippy').getEffectiveLevel()
            logging.getLogger('snippy').setLevel(logging.DEBUG)
            Logger.get_logger().debug('%s', status)
            logging.getLogger('snippy').setLevel(level)
        elif logging.getLogger('snippy').getEffectiveLevel() == logging.DEBUG:
            Logger.get_logger().debug(status)
        elif not cls.CONFIG['quiet']:
            cls.print_stdout(status)

    @staticmethod
    def timeit(method=None, refresh_oid=False):
        """Time method by measuring it latency.

        The operation ID (OID) is refreshed at the end.

        Args:
            method (str): Name of the method calling the timeit.
            refresh_oid (bool): Define if operation ID is refreshed or not.

        Returns:
            obj: Timeit wrapper function for decorators.
        """

        def _timeit(method):

            @wraps(method)
            def timed(*args, **kwargs):
                """Wrapper to measure latency."""

                start = time.time()
                if refresh_oid:
                    Logger.refresh_oid()
                Logger.get_logger().debug('run method: %s', method.__name__)
                result = method(*args, **kwargs)
                Logger.get_logger().debug('end method: %s :duration: %.6fs', method.__name__, (time.time() - start))

                return result

            return timed

        if method:
            return _timeit(method)

        return _timeit

    @staticmethod
    def remove_ansi(message):
        """Remove all ANSI escape codes from log message.

        Args:
            message (str): Log message which ANSI escape codes are removed.

        Returns:
            str: Same log message but without ANSI escape codes.
        """

        return Const.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', message)

    @staticmethod
    def debug():
        """Debug Logger by printing logging hierarchy."""

        from logging_tree import printout
        printout()

    @classmethod
    def _update(cls):
        """Update logger configuration."""

        items = list(logging.root.manager.loggerDict.items())
        for _, logger in items:
            for handler in getattr(logger, 'handlers', ()):
                logger.removeHandler(handler)
                formatter = CustomFormatter(Logger.LOG_FORMAT)
                handler = logging.StreamHandler(stream=sys.stdout)
                handler.setFormatter(formatter)
                handler.addFilter(CustomFilter())
                logger.addHandler(handler)


class CustomLoggerAdapter(logging.LoggerAdapter):  # pylint: disable=too-few-public-methods
    """Custom logger adapter.

    The logging.LoggerAdapter does not support custom log levels
    and therefore they need to be implemented here.
    """

    def __init__(self, logger, extra):
        logging.LoggerAdapter.__init__(self, logger, extra)

    def security(self, msg, *args, **kwargs):
        """Customer log level for security events.

        Args:
            msg (str): Log message as a string.
        """

        self.log(logging.SECURITY, msg, *args, **kwargs)


class CustomFormatter(logging.Formatter):
    """Custom log formatting."""

    def __init__(self, *args, **kwargs):
        self._snippy_msg_end = '...'
        self._snippy_msg_max = Logger.CONFIG['log_msg_max'] - len(self._snippy_msg_end)
        self._snippy_msg_max_security = Logger.SECURITY_LOG_MSG_MAX - len(self._snippy_msg_end)
        super(CustomFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        """Format log record.

        Gunicorn logs have special conversion for info level logs. In order
        to follow the Snippy logging standard, which defines the usage of
        debug level, Gunicorn informative logs are converted to debug level
        logs. Warning and error levels do not get converted because in these
        cases the level is considered relevant for user.

        Args:
            record (obj): Logging module LogRecord.

        Returns:
            str: Log string.
        """

        # Debug option tries to print logs "as is" in full length. There is a
        # maximum limitation for log message for safety and security reasons.
        # Very verbose option truncates log message in order to try to keep
        # one log per line for easier log reading. In case of the very verbose
        # option, log message is printed with all lower case letters.
        if record.args:
            record.msg = record.msg % record.args
            if len(record.msg) > Logger.SECURITY_LOG_MSG_MAX:
                Logger.get_logger().security('long log message detected and truncated: {0}, {1:.{2}}'.format(
                    len(record.msg), record.msg, Logger.DEFAULT_LOG_MSG_MAX))
                record.msg = record.msg[:self._snippy_msg_max_security] + (record.msg[self._snippy_msg_max_security:] and
                                                                           self._snippy_msg_end)
            record.args = None
        if Logger.CONFIG['very_verbose']:
            record.msg = record.msg.replace('\n', ' ').replace('\r', '')
            record.msg = record.msg[:self._snippy_msg_max] + (record.msg[self._snippy_msg_max:] and self._snippy_msg_end)
            record.msg = record.msg.lower()

        if record.name == 'snippy.server.gunicorn' and record.levelno == logging.INFO:
            record.levelname = 'debug'
            record.levelno = logging.DEBUG

        if Logger.CONFIG['log_json']:
            log_string = super(CustomFormatter, self).format(record)
            log_string = self._jsonify(record)
        else:
            log_string = super(CustomFormatter, self).format(record)

        return log_string

    def formatTime(self, record, datefmt=None):
        """Format log timestamp.

        JSON logs are printed in ISO8601 format with UTC timestamps. All
        other logs are printed in local time with space between date and
        time instead of 'T' because of better readability.

        The ISO8601 formatted JSON timestamp is set in microseconds. It
        seems that the msecs field of the logging record contains mseconds
        as floating point number. It is assumed that the microseconds can
        be read by reading three significat digits after point.

        Args:
            record (obj): Logging module LogRecord.
            datefmt (str): Datetime format as accepted by time.strftime().

        Returns:
            str: Log timestamp in string format.
        """

        if Logger.CONFIG['log_json']:
            timstamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(record.created))
            time_string = '%s.%d+00:00' % (timstamp, int(Const.TEXT_TYPE(record.msecs).replace('.', '')[:6]))
        else:
            timstamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
            time_string = '%s.%03d' % (timstamp, record.msecs)

        return time_string

    @staticmethod
    def _jsonify(record):
        """Create JSON string from log record.

        Args:
            record (obj): Logging module LogRecord.
        """

        log = OrderedDict()

        fields = ['asctime', 'appname', 'process', 'oid', 'levelno', 'levelname', 'name', 'lineno', 'thread', 'message']
        for field in fields:
            log[field] = record.__dict__.get(field)

        return json.dumps(log)


class CustomFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Customer log filter."""

    def filter(self, record):
        """Filtering with dynamic operation ID setting.

        Args:
            record (obj): Logging module LogRecord.
        """

        record.oid = Logger.SERVER_OID

        return True


class CustomGunicornLogger(GunicornLogger):  # pylint: disable=too-few-public-methods
    """Custom logger for Gunicorn HTTP server."""

    def setup(self, cfg):
        """Custom setup.

        Disable all handlers under the 'gunicorn' namespace and prevent log
        propagation to root logger. The loggers under the 'snippy' namespace
        will take care of the log writing for Gunicorn server.

        Both Gunicor error and access log categories are printed from the same
        namespace. In case of 'snippy.server.gunicorn.error', informative logs
        in JSON format would have this in the class ``name`` attribute which
        is considered to be misleading for other than error logs.

        Args:
            cfg (obj): The Gunicorn server class Config() object.
        """

        super(CustomGunicornLogger, self).setup(cfg)
        self._remove_handlers(self.error_log)
        self._remove_handlers(self.access_log)
        logging.getLogger('gunicorn').propagate = False
        self.error_log = Logger.get_logger('snippy.server.gunicorn')
        self.access_log = Logger.get_logger('snippy.server.gunicorn')

    @staticmethod
    def _remove_handlers(logger):
        """Remove handlers."""

        handlers = logger.handlers
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
