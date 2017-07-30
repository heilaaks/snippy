#!/usr/bin/env python3

"""arguments.py: Command line argument management."""

import argparse
from snippy.logger import Logger


class Arguments(object):
    """Command line argument management."""

    args = {}
    logger = {}

    def __init__(self):
        Arguments.logger = Logger().get()
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--snippet', type=str, default='', help='add command or code snippet')
        parser.add_argument('-r', '--resolve', type=str, default='', help='add troubleshooting resolution')
        parser.add_argument('-t', '--tags', nargs='*', type=str, default='', help='add tags with the give snippet')
        parser.add_argument('-c', '--comment', type=str, default='', help='add comment with the snippet')
        parser.add_argument('-f', '--find', type=str, help='find with any give keyword')
        parser.add_argument('--ftag', type=str, help='find from tags only')
        parser.add_argument('--profiler', action='store_true', default=False, help=argparse.SUPPRESS)
        Arguments.args = parser.parse_args()

    @classmethod
    def get_snippet(cls):
        """Return the snippet that user gave from CLI exactly as it was."""

        cls.logger.info('parsed argument --snippet with value "%s"', cls.args.snippet)

        return cls.args.snippet

    @classmethod
    def get_resolve(cls):
        """Return the resolve log that user gave from CLI exactly as it was."""

        cls.logger.info('parsed argument --resolve with value "%s"', cls.args.resolve)

        return cls.args.resolve

    @classmethod
    def get_tags(cls):
        """Return the tags that user gave from CLI exactly as it was."""

        cls.logger.info('parsed argument --tags with value "%s"', cls.args.tags)

        return cls.args.tags

    @classmethod
    def get_comment(cls):
        """Return the comment that user gave from CLI exactly as it was."""

        cls.logger.info('parsed argument --comment with value "%s"', cls.args.comment)

        return cls.args.comment

    @classmethod
    def get_profiler(cls):
        """Return the profiler switch based on user input or from default."""

        cls.logger.info('parsed argument --profile with value "%s"', cls.args.profiler)

        return cls.args.profiler
