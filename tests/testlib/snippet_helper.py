#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

from snippy.logger import Logger


class SnippetHelper(object): # pylint: skip-file
    """Helper methods for Sqlite3 database testing."""

    SNIPPET_1 = {'content': 'docker rm $(docker ps -a -q)',
                 'brief': 'Remove all docker containers',
                 'group': 'docker',
                 'tags': ['container', 'cleanup', 'docker'],
                 'links': ['https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'],
                 'digest': 'da217a911ec37e9a2ad4a89ebb28d4f10e3216a7ce7d317b07ba41c95ec4152c'}

    def __init__(self):
        self.logger = Logger(__name__).get()

    def get_snippet(self, snippet_id):
        """Get list of default snippets"""

        snippets = []

        return SnippetHelper.SNIPPET_1
