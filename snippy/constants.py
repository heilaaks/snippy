#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""

import sys


class Constants(object):  # pylint: disable=too-few-public-methods
    """Globals constants."""

    SPACE = ' '
    EMPTY = ''
    COMMA = ','
    NEWLINE = '\n'

    PYTHON2 = sys.version_info.major == 2

    # Content categories.
    SNIPPET = 'snippet'
    SOLUTION = 'solution'
    ALL = 'all'
    UNKNOWN_CONTENT = 'unknown'

    # Content delimiters
    DELIMITER_DATA = NEWLINE
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = NEWLINE

    # Default values for content fields.
    DEFAULT_GROUP = 'default'
