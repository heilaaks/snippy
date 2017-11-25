#!/usr/bin/env python3

"""api_snippets.py - JSON REST API for Snippets."""

from snippy.version import __version__


class ApiSnippets(object):  # pylint: disable=too-few-public-methods
    """Snippets API."""

    @staticmethod
    def on_get(_, response):
        """Handle GET reguest."""

        hello = __version__

        response.media = hello
