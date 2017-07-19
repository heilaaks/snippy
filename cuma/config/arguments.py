#!/usr/bin/env python3

"""arguments.py: Command line arguments"""

import argparse
from cuma.logger import Logger


class Arguments(object):
    """Command line argument management."""

    args = {}
    logger = {}

    def __init__(self):
        Arguments.logger = Logger().get()
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--add', type=str, help='add command or code example')
        parser.add_argument('-s', '--search', type=str, help='search command or code example')
        Arguments.args = parser.parse_args()

    @classmethod
    def get_argument(cls, argument):
        if argument in vars(cls.args):
            cls.logger.info('parsed argument "{:s}" with value "{}"'.format(argument, vars(cls.args)[argument]))

            return vars(cls.args)[argument]

        return None

    @classmethod
    def get(cls):
        cls.logger.info('reading command line arguments')
