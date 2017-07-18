#!/usr/bin/env python3

"""Code Unit MAnager for managing code and command sniplets."""

from cuma.database import Database
from cuma.config import Config

__author__    = "Heikki J. Laaksonen"
__copyright__ = "Copyright 2017, Heikki J. Laaksonen"
__license__   = "MIT"


class Cuma(object):

    def __init__(self):
        print("main init")

    def run(self):
        """Start the manager."""
        print("running")
        config = Config()
        Database().init(config.get_storage_location())

def main():
    Cuma().run()

if __name__ == "__main__":
    main()
