#!/usr/bin/env python3

"""search_snippets_api.py - JSON REST API for searching snippets."""

from snippy.version import __version__


class SearchSnippetsApi(object):  # pylint: disable=too-few-public-methods
    """Search snippets API."""

    @staticmethod
    def on_get(_, response):
        """Handle GET reguest."""

        hello = __version__

        response.media = hello
