#!/usr/bin/env python3

"""constants.py: Globals for the tool."""


class Constants(object): # pylint: disable=too-few-public-methods
    """Globals for the tool."""

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

    # Snippet console print formatting.
    SNIPPET_HEADER_STR = '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0;2m [%s]\x1b[0m\n'
    SNIPPET_SNIPPET_STR = '%s   \x1b[91m$\x1b[0m \x1b[2m%s\x1b[0m\n'
    SNIPPET_BRIEF_STR = '%s   \x1b[91m+\x1b[0m %s\n'
    SNIPPET_TAGS_STR = '%s   \x1b[91m#\x1b[0m %s\n'
    SNIPPET_LINKS_STR = '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n'

    # Export formats
    EXPORT_YAML = 'yaml'
    EXPORT_JSON = 'json'
