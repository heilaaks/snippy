#!/usr/bin/env python3

"""solution.py: Solution management."""

from snippy.logger import Logger


class Solution(object):
    """Solution management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def add(self):
        """Add new solution."""

        self.logger.info('add new solution')

    def run(self):
        """Run the solution management task."""

        self.logger.info('managing solution')
