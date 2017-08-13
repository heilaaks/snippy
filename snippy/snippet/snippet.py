#!/usr/bin/env python3

"""snippet.py: Snippet management."""

import sys
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config


class Snippet(object):
    """Snippet management."""

    def __init__(self):
        self.logger = Logger().get()
        self.storage = None

    def add(self):
        """Add new snippet."""

        self.logger.debug('adding new snippet')
        self.storage.store(Config.get_snippet(), Config.get_brief(), Config.get_tags(), Config.get_link())

    def find_keywords(self):
        """Find snippets based on keywords."""

        self.logger.info('finding snippet based on keywords')

        return self.storage.search(Config.get_find_keywords())

    def delete(self):
        """Delete new snippet."""

        self.logger.debug('deleting snippet')

        return self.storage.delete(Config.get_delete())

    def export(self):
        """export snippets."""

        self.logger.debug('exporting snippet')
        hits = self.storage.export()
        hits = self.format_yaml(hits)
        self.print_file(hits)

    def format_console(self, hits):
        """Format hits for console."""

        self.logger.debug('format search hits for console')

        console = ''
        for idx, row in enumerate(hits):
            console = console + Const.SNIPPET_HEADER_STR % (idx+1, row[Const.SNIPPET_BRIEF], row[Const.SNIPPET_ID])
            console = Const.SNIPPET_SNIPPET_STR % (console, row[Const.SNIPPET_SNIPPET]) + Const.NEWLINE
            console = Const.SNIPPET_LINK_STR % (console, row[Const.SNIPPET_LINK])
            console = Const.SNIPPET_TAGS_STR % (console, row[Const.SNIPPET_TAGS])
            console = console + Const.NEWLINE

        return console

    def format_yaml(self, hits):
        """Format hits for yaml file."""

        import yaml

        self.logger.debug('format search hits to yaml string')
        yaml_string = ''
        yaml_string = yaml_string + '%YAML 1.2\n'
        yaml_string = yaml_string + '---\n'
        yaml_string = yaml_string + 'snippets:\n  -'
        for row in hits:
            yaml_string = yaml_string + Const.NEWLINE
            yaml_string = yaml_string + '{0:s}brief: "{1:s}"\n'.format(Const.YAML_INDENT, row[Const.SNIPPET_BRIEF])
            yaml_string = yaml_string + '{0:s}snippet: >-\n{0:s}{0:s}$ {1:s}\n'.format(Const.YAML_INDENT, row[Const.SNIPPET_SNIPPET])
            yaml_string = yaml_string + '{0:s}links:\n{0:s}{0:s}- "{1:s}"\n'.format(Const.YAML_INDENT, row[Const.SNIPPET_LINK])
            yaml_string = yaml_string + '{0:s}tags: [{1:s}]\n'.format(Const.YAML_INDENT, row[Const.SNIPPET_TAGS])
            yaml_string = yaml_string + '  -'
        yaml_string = yaml_string[:-3] # Remove last 'OR ' added by the loop.
        try:
            yaml.load(yaml_string)
            self.logger.info('generated valid yaml file')
        except yaml.YAMLError as exception:
            self.logger.exception('fatal failure to generate yaml formatted export file "%s"', exception)
            sys.exit()

        return yaml_string

    def print_console(self, hits):
        """Print hits into console."""

        self.logger.debug('printing search results')
        print(hits)

    def print_file(self, yaml_string):
        """Print hits into file."""

        export = Config.get_export()
        self.logger.debug('exporting storage into file %s', export)
        with open(export, 'w') as outfile:
            outfile.write(yaml_string)

    def run(self, storage):
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        self.storage = storage
        if Config.get_snippet():
            self.add()
        elif Config.get_find_keywords():
            hits = self.find_keywords()
            hits = self.format_console(hits)
            self.print_console(hits)
        elif Config.get_delete():
            self.delete()
        elif Config.get_export():
            self.export()
        else:
            self.logger.error('unknown action for snippet')
