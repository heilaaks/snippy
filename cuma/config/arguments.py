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
        parser.add_argument('-s', '--snippet', type=str, help='add command or code snippet')
        parser.add_argument('-t', '--tags', type=str, help='add tags with the give snippet')
        parser.add_argument('-c', '--comment', type=str, help='add comment with the snippet')
        parser.add_argument('-f', '--find', type=str, help='find with any give keyword')
        parser.add_argument('--ftag', type=str, help='find from tags only')
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
