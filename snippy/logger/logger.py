#!/usr/bin/env python3

"""logger.py: Common logger for the tool."""

from __future__ import print_function
import sys
import logging
from signal import signal, getsignal, SIGPIPE, SIG_DFL


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
        logging.getLogger('snippy').disabled = True
        logging.getLogger('snippy').setLevel(logging.CRITICAL)
        #logging.getLogger('snippy').propagate = False
        if '--debug' in sys.argv or '-vv' in sys.argv:
            logging.getLogger('snippy').disabled = False
            logging.getLogger('snippy').setLevel(logging.DEBUG)

        # Prevent gunicorn logs
        #logging.getLogger('gunicorn.error').disabled = True
        #logging.getLogger('gunicorn.error').setLevel(logging.CRITICAL)
        #if '--debug' in sys.argv or '-vv' in sys.argv:
        #    logging.getLogger('gunicorn.error').disabled = False
        #    logging.getLogger('gunicorn.error').setLevel(logging.DEBUG)

            # Format Gunicorn logs.
            #glogs = logging.getLogger('gunicorn.error')
            #print(glogs)
            #if glogs.hasHandlers():
            #    print("DAA")
            #    glogs.handlers.pop()
            #print("passed")
            #glogs.propagate = True
            #log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-13s : %(message)s'
            #formatter = CustomFormatter(log_format)
            #handler = logging.StreamHandler(stream=sys.stdout)
            #handler.setFormatter(formatter)
            #glogs.addHandler(handler)

            #Logger.debug()
            #testing = logging.getLogger('gunicorn')
            #testing.propagate = False
            #testing = logging.getLogger('gunicorn.access')
            #testing.propagate = False
            
    @staticmethod
    def set_gunicorn_logging():
        """Set gunicorn serever logging."""

        # Format Gunicorn logs.
        glogs = logging.getLogger('gunicorn.error')
        print(glogs)
        if glogs.hasHandlers():
            print("DAA")
            print("size %d" % len(glogs.handlers))
            glogs.handlers.pop()
            print("size %d" % len(glogs.handlers))
        print("PASSED")
        glogs.propagate = False
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-13s : %(message)s'
        formatter = CustomFormatter(log_format)
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        glogs.addHandler(handler)
        Logger.debug()

        glogs1 = logging.getLogger('gunicorn')
        if glogs1.hasHandlers():
            print("DAA2")
        print("PASSED2")
        glogs1.propagate = False
        #glogs = logging.getLogger('gunicorn.access')
        #print(glogs)
        #if glogs.hasHandlers():
        #    print("DAA")
        #    print("size %d" % len(glogs.handlers))
        #    glogs.handlers.pop()
        #    print("size %d" % len(glogs.handlers))
        #print("PASSED2")

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
