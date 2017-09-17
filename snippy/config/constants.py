#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""

import sys


class Constants(object):
    """Globals constants for the tool."""

    NEWLINE = '\n'
    SPACE = ' '
    EMPTY = ''
    EMPTY_LIST = []
    EMPTY_TUPLE = ()

    # Python2
    PYTHON2 = sys.version_info.major == 2

    # Delimiters
    DELIMITER_CONTENT = NEWLINE
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = '>' # Disallowed characters in URI: <|>|#|%|"
    DELIMITER_SPACE = SPACE
    DELIMITER_NEWLINE = NEWLINE

    # Column and tuple numbers for snippets.
    SNIPPET_CONTENT = 0
    SNIPPET_BRIEF = 1
    SNIPPET_GROUP = 2
    SNIPPET_TAGS = 3
    SNIPPET_LINKS = 4
    SNIPPET_DIGEST = 5
    SNIPPET_UTC = 6
    SNIPPET_METADATA = 7
    SNIPPET_ID = 8
    SNIPPET_TESTING = 9

    # Default values for snippets
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

    EDITED_CONTENT = {'head': EDITOR_CONTENT_HEAD, 'tail': EDITOR_CONTENT_TAIL, 'delimiter': DELIMITER_NEWLINE}
    EDITED_BRIEF = {'head': EDITOR_BRIEF_HEAD, 'tail': EDITOR_BRIEF_TAIL, 'delimiter': DELIMITER_SPACE}
    EDITED_GROUP = {'head': EDITOR_GROUP_HEAD, 'tail': EDITOR_GROUP_TAIL, 'delimiter': DELIMITER_SPACE}
    EDITED_TAGS = {'head': EDITOR_TAGS_HEAD, 'tail': EDITOR_TAGS_TAIL, 'delimiter': DELIMITER_TAGS}
    EDITED_LINKS = {'head': EDITOR_LINKS_HEAD, 'tail': EDITOR_LINKS_TAIL, 'delimiter': DELIMITER_NEWLINE}

    @staticmethod
    def format_header(colors=False):
        """Format snippet text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0;2m \x1b[0m@%s \x1b[0;2m[%.16s]\x1b[0m\n' if colors \
               else '%d. %s @%s [%.16s]\n'

    @staticmethod
    def format_snippet(colors=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m \x1b[0m%s\x1b[0m\n' if colors else '%s   $ %s\n'

    @staticmethod
    def format_links(colors=False):
        """Format snippet links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   > %s\n'

    @staticmethod
    def format_tags(colors=False):
        """Format snippet tags."""

        return '%s   \x1b[91m#\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   # %s\n'

    @staticmethod
    def get_content_string(snippet):
        """Format snippet content to string."""

        return Constants.DELIMITER_CONTENT.join(map(str, snippet[Constants.SNIPPET_CONTENT]))
