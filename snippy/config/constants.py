#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""

import sys


class Constants(object): # pylint: disable=too-few-public-methods
    """Globals constants for the tool."""

    SPACE = ' '
    EMPTY = ''
    COMMA = ','
    NEWLINE = '\n'
    EMPTY_LIST = []
    EMPTY_TUPLE = ()

    # Python2
    PYTHON2 = sys.version_info.major == 2

    # Digest
    DIGEST_MIN_LENGTH = 16

    # Content categories.
    SNIPPET = 'snippet'
    SOLUTION = 'solution'
    ALL = 'all'

    # Content delimiters
    DELIMITER_NEWLINE = NEWLINE
    DELIMITER_SPACE = SPACE
    DELIMITER_DATA = NEWLINE
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = NEWLINE

    # Content index numbers in data structures.
    DATA = 0
    BRIEF = 1
    GROUP = 2
    TAGS = 3
    LINKS = 4
    CATEGORY = 5
    FILENAME = 6
    UTC = 7
    DIGEST = 8
    METADATA = 9
    KEY = 10
    TESTING = 11

    # Content formats
    NATIVE_CONTENT = 0 # Native format from content.
    STRING_CONTENT = 1 # Single String from content.

    # Default values for content fields.
    DEFAULT_GROUP = 'default'

    # Export formats
    FILE_TYPE_NONE = 'none'
    FILE_TYPE_YAML = 'yaml'
    FILE_TYPE_JSON = 'json'
    FILE_TYPE_TEXT = 'text'

    # Search types
    NO_SEARCH = 'none'
    SEARCH_ALL = 'all'
    SEARCH_TAG = 'tag'
    SEARCH_GRP = 'grp'
