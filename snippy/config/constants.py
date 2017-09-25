#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""

import sys


class Constants(object): # pylint: disable=too-few-public-methods
    """Globals constants for the tool."""

    NEWLINE = '\n'
    SPACE = ' '
    EMPTY = ''
    EMPTY_LIST = []
    EMPTY_TUPLE = ()

    # Python2
    PYTHON2 = sys.version_info.major == 2

    # Digest
    DIGEST_MIN_LENGTH = 16

    # Content categories that must match SQL table names.
    SNIPPET = 'snippets'
    SOLUTION = 'solutions'
    ALL = 'all'

    # Content delimiters
    DELIMITER_CONTENT = NEWLINE
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = '>' # Disallowed characters in URI: <|>|#|%|"
    DELIMITER_SPACE = SPACE
    DELIMITER_NEWLINE = NEWLINE

    # Content index numbers in data structures.
    CONTENT = 0
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

    # Default values for content fields.
    DEFAULT_GROUP = 'default'

    # Export formats
    FILE_TYPE_NONE = 'none'
    FILE_TYPE_YAML = 'yaml'
    FILE_TYPE_JSON = 'json'
    FILE_TYPE_TEXT = 'text'

    # Search types
    SEARCH_ALL = 'all'
    SEARCH_TAG = 'tag'
    SEARCH_GRP = 'grp'

    # Database
    DB_INSERT_OK = 'insert-ok'
    DB_UPDATE_OK = 'update-ok'
    DB_DELETE_OK = 'delete-ok'
    DB_DUPLICATE = 'unique-constraint-violation'
    DB_FAILURE = 'internal-failure'
    DB_ENTRY_NOT_FOUND = 'not-found'

    # Editor inputs
    EDITOR_CONTENT_HEAD = '# Add mandatory snippet below.\n'
    EDITOR_CONTENT_TAIL = '# Add optional brief description below.\n'
    EDITOR_BRIEF_HEAD = '# Add optional brief description below.\n'
    EDITOR_BRIEF_TAIL = '# Add optional single group below.\n'
    EDITOR_GROUP_HEAD = '# Add optional single group below.\n'
    EDITOR_GROUP_TAIL = '# Add optional comma separated list of tags below.\n'
    EDITOR_TAGS_HEAD = '# Add optional comma separated list of tags below.\n'
    EDITOR_TAGS_TAIL = '# Add optional links below one link per line.\n'
    EDITOR_LINKS_HEAD = '# Add optional links below one link per line.\n'
    EDITOR_LINKS_TAIL = '.'
