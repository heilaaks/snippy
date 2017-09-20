#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""

import sys
import re


class Constants(object):
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

    # Content types
    SNIPPET = 'snippet'
    SOLUTION = 'solution'

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
    DIGEST = 5
    UTC = 6
    METADATA = 7
    KEY = 8
    TESTING = 9

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
    def get_content_string(content):
        """Format content data to string."""

        data = Constants.DELIMITER_CONTENT.join(map(str, content[Constants.CONTENT]))

        return data

    @staticmethod
    def get_brief_string(content):
        """Format content brief to string."""

        brief = content[Constants.BRIEF]

        return brief

    @staticmethod
    def get_group_string(content):
        """Format content group to string."""

        # If the group is in default value, don't show it to end user
        # since it may be confusing. If there is no input for the group
        # the default is set back.
        group = Constants.EMPTY
        if not content[Constants.GROUP] == Constants.DEFAULT_GROUP:
            group = content[Constants.GROUP]

        return group

    @staticmethod
    def get_tags_string(content):
        """Format content tags to string."""

        tags = Constants.DELIMITER_TAGS.join(map(str, content[Constants.TAGS]))

        return tags

    @staticmethod
    def get_links_string(content):
        """Format content links to string."""

        links = Constants.DELIMITER_NEWLINE.join(map(str, content[Constants.LINKS]))

        return links

    @staticmethod
    def get_file_string(content):
        """Format content file to string."""

        file = Constants.EMPTY
        match = re.search('## FILE  :(.*)', Constants.get_content_string(content))
        if match:
            file = match.group(1)

        if '<SNIPPY_FILE>' in file:
            file = Constants.EMPTY

        return file
