#!/usr/bin/env python3

"""logger.py: Common logger for the tool."""

from __future__ import print_function
import sys
import logging


class Logger(object):
    """Logging wrapper."""

    def __init__(self, module):
        attributes = {'appName':'snippy'}
        self.logger = logging.getLogger('snippy.' + module)
        handler = logging.StreamHandler()
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-13s : %(message)s'
        formatter = CustomFormatter(log_format)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger = logging.LoggerAdapter(self.logger, attributes)

    def get(self):
        """Return logger object."""

        return self.logger

    @staticmethod
    def set_level():
        """Set log level for all the loggers inherited under the root logger.
        This relies on that the module level logger does not set the level
        which causes module level logger to rely only higher level logger
        in the logging hierarchy."""

        logging.getLogger().disabled = True
        if '--debug' in sys.argv or '-vv' in sys.argv:
            logging.getLogger().disabled = False
            logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def exit(cause):
        """Print exit cause for the tool."""

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            Logger(__name__).get().info('exiting with cause %s', cause.lower())
        elif '-q' not in sys.argv:
            print(cause)

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
