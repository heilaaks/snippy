#!/usr/bin/env python3

"""api_hello.py - JSON REST API for hello route."""

import gunicorn.app.base
from gunicorn.six import iteritems


class GunicornServer(gunicorn.app.base.BaseApplication):  # pylint: disable=abstract-method
    """Gunicor WSGI server."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornServer, self).__init__()

    def load_config(self):
        """Load configuration."""

        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        """Load configuration."""

        return self.application
