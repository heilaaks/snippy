#!/usr/bin/env python3

"""logger.py: Common logger for the tool."""

import logging


class Logger(object): # pylint: disable=too-few-public-methods
    """Logging wrapper."""

    def __init__(self):
        self.logger = logging.getLogger('root')
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-13s : %(message)s'
        logging.basicConfig(level='DEBUG', format=log_format)
        self.logger = logging

    def get(self):
        """Get logger object."""

        return self.logger
