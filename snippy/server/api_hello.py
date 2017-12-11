#!/usr/bin/env python3

"""api_hello.py - JSON REST API for hello health check."""

import json
import falcon
from snippy.metadata import __version__


class ApiHello(object):  # pylint: disable=too-few-public-methods
    """Hello API."""

    @staticmethod
    def on_get(_, response):
        """Handle GET reguest."""

        hello = {'snippy': __version__}
        response.content_type = falcon.MEDIA_JSON
        response.media = json.dumps(hello, ensure_ascii=False)
        response.status = falcon.HTTP_200
