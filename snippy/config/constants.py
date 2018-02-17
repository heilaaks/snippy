#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""

import sys


class Constants(object):  # pylint: disable=too-few-public-methods
    """Globals constants for the tool."""

    SPACE = ' '
    EMPTY = ''
    COMMA = ','
    NEWLINE = '\n'
    EMPTY_LIST = []
    EMPTY_TUPLE = ()

    # Python2
    PYTHON2 = sys.version_info.major == 2

    # Content categories.
    SNIPPET = 'snippet'
    SOLUTION = 'solution'
    ALL = 'all'
    UNKNOWN_CONTENT = 'unknown'

    # Content delimiters
    DELIMITER_NEWLINE = NEWLINE
    DELIMITER_SPACE = SPACE
    DELIMITER_DATA = NEWLINE
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = NEWLINE

    # Content index in the data structure.
    NUMBER_OF_COLUMS = 13  # The number of colums in contents table.
    DATA = 0
    BRIEF = 1
    GROUP = 2
    TAGS = 3
    LINKS = 4
    CATEGORY = 5
    FILENAME = 6
    RUNALIAS = 7
    VERSIONS = 8
    CREATED = 9
    DIGEST = 10
    METADATA = 11
    KEY = 12

    # Content formats
    NATIVE_CONTENT = 0  # Native format from content.
    STRING_CONTENT = 1  # Single String from content.

    # Default values for content fields.
    DEFAULT_GROUP = 'default'

    # Content formats
    CONTENT_TYPE_NONE = 'none'
    CONTENT_TYPE_YAML = 'yaml'
    CONTENT_TYPE_JSON = 'json'
    CONTENT_TYPE_TEXT = 'text'

    # JSON API media type
    MEDIA_JSON_API = 'application/vnd.api+json; charset=UTF-8'
