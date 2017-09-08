#!/usr/bin/env python3

"""logger.py: Common logger for the tool."""

import sys
import logging


class Logger(object):
    """Logging wrapper."""

    def __init__(self, module):
        self.logger = logging.getLogger('snippy.' + module)
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-13s : %(message)s'
        logging.basicConfig(format=log_format)
        self.logger = logging

    def get(self):
        """Return logger object."""

        return self.logger

    @staticmethod
    def set_level():
        """Set log level for all the loggers inherited under the root logger.
        This relies on that the module level logger does not set the level
        which causes module level logger to rely only higher level logger
        in the logging hierarchy."""
        #logging.getLogger().setLevel(logging.ERROR)
        logging.getLogger().disabled = True
        if '--debug' in sys.argv or '-vv' in sys.argv:
            logging.getLogger().disabled = False
            logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def exit(logger, cause):
        """Print exit cause for the tool."""
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            logger.info('exiting with cause %s', cause.lower())
        else:
            print(cause)
