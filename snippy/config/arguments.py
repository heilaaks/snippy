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
        parser.add_argument('-b', '--brief', type=str, default='', help='set brief description for the input')
        parser.add_argument('-t', '--tags', nargs='*', type=str, default='', help='set tags for the input')
        parser.add_argument('-l', '--link', type=str, default='', help='set reference link for more information')
        parser.add_argument('-f', '--find', nargs='*', type=str, default='', help='find with all given keyword')
        parser.add_argument('--ftag', type=str, help='find from tags only')
        parser.add_argument('--profiler', action='store_true', default=False, help=argparse.SUPPRESS)
        Arguments.args = parser.parse_args()

    @classmethod
    def get_snippet(cls):
        """Return the snippet that user gave exactly as it was."""

        cls.logger.info('parsed argument --snippet with value "%s"', cls.args.snippet)

        return cls.args.snippet

    @classmethod
    def get_resolve(cls):
        """Return the resolution that user gave exactly as it was."""

        cls.logger.info('parsed argument --resolve with value "%s"', cls.args.resolve)

        return cls.args.resolve

    @classmethod
    def get_brief(cls):
        """Return the brief description that user gave exactly as it was."""

        cls.logger.info('parsed argument --brief with value "%s"', cls.args.brief)

        return cls.args.brief

    @classmethod
    def get_tags(cls):
        """Return the tags that user gave exactly as it was."""

        cls.logger.info('parsed argument --tags with value "%s"', cls.args.tags)

        return cls.args.tags

    @classmethod
    def get_link(cls):
        """Return the link that user gave exactly as it was."""

        cls.logger.info('parsed argument --link with value "%s"', cls.args.link)

        return cls.args.link

    @classmethod
    def get_find(cls):
        """Return the find keywords that user gave exactly as it was."""

        cls.logger.info('parsed argument --find with value "%s"', cls.args.find)

        return cls.args.find

    @classmethod
    def get_profiler(cls):
        """Return the profiler switch based on user input or from default."""

        cls.logger.info('parsed argument --profile with value "%s"', cls.args.profiler)

        return cls.args.profiler
