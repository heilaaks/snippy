#!/usr/bin/env python3

"""constants.py: Globals constants for the tool."""


class Constants(object):
    """Globals constants for the tool."""

    NEWLINE = '\n'

    # Delimiters
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = '>' # Disallowed characters in URI: <|>|#|%|"

    # Column numbers in snippets table.
    SNIPPET_ID = 0
    SNIPPET_SNIPPET = 1
    SNIPPET_BRIEF = 2
    SNIPPET_TAGS = 3
    SNIPPET_LINKS = 4
    SNIPPET_METADATA = 5

    # Export formats
    EXPORT_YAML = 'yaml'
    EXPORT_JSON = 'json'
    EXPORT_TEXT = 'text'

    # Editor input tags
    EDITOR_SNIPPET_HEAD = '# Add mandatory snippet below.\n'
    EDITOR_SNIPPET_TAIL = '# Add optional brief description below.\n'
    EDITOR_BRIEF_HEAD = '# Add optional brief description below.\n'
    EDITOR_BRIEF_TAIL = '# Add optional comma separated list of tags below.\n'
    EDITOR_TAGS_HEAD = '# Add optional comma separated list of tags below.\n'
    EDITOR_TAGS_TAIL = '# Add optional links below one link per line.\n'
    EDITOR_LINKS_HEAD = '# Add optional links below one link per line.\n'
    EDITOR_LINKS_TAIL = '.'

    @staticmethod
    def format_header(colors=False):
        """Format snippet text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0;2m [%s]\x1b[0m\n' if colors else '%d. %s [%s]\n'

    @staticmethod
    def format_snippet(colors=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   $ %s\n'

    @staticmethod
    def format_brief(colors=False):
        """Format snippet brief description."""

        return '%s   \x1b[91m+\x1b[0m %s\n' if colors else '%s   + %s\n'

    @staticmethod
    def format_tags(colors=False):
        """Format snippet tags."""

        return '%s   \x1b[91m#\x1b[0m %s\n' if colors else '%s   # %s\n'

    @staticmethod
    def format_links(colors=False):
        """Format snippet links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   > %s\n'
