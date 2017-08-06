#!/usr/bin/env python3

"""constants.py: Globals for the tool."""


class Constants(object): # pylint: disable=too-few-public-methods
    """Globals for the tool."""

    NEWLINE = '\n'

    # Colum numbers in snippets table.
    SNIPPET_ID = 0
    SNIPPET = 1
    SNIPPET_TAGS = 2
    SNIPPET_DESCRIPTION = 3
    SNIPPET_LINK = 4
    SNIPPET_METADATA = 5

    # Snippet console print formatting.
    SNIPPET_HEADER_STR = '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0;2m [%s]\x1b[0m\n'
    SNIPPET_STR = '%s   \x1b[91m$\x1b[0m \x1b[2m%s\x1b[0m\n'
    SNIPPET_DESCRIPTION_STR = '%s   \x1b[91m+\x1b[0m %s\n'
    SNIPPET_TAGS_STR = '%s   \x1b[91m#\x1b[0m %s\n'
    SNIPPET_LINK_STR = '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n'
