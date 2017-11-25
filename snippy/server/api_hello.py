#!/usr/bin/env python3

"""api_hello.py - JSON REST API for hello health check."""

from snippy.version import __version__


class HelloApi(object):  # pylint: disable=too-few-public-methods
    """Hello API."""

    @staticmethod
    def on_get(_, response):
        """Handle GET reguest."""

        hello = __version__

        response.media = hello
