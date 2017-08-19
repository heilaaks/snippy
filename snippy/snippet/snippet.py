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
        self.storage.store(Config.get_snippet(), Config.get_brief(), Config.get_tags(), Config.get_links())

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

        self.logger.debug('exporting snippets')
        snippets = self.storage.export()
        snippets = self.format_dict(snippets)
        self.print_file(snippets)

    def format_console(self, snippets):
        """Format snippets for console."""

        self.logger.debug('format search snippets for console')
        console = ''
        links = ''
        for idx, row in enumerate(snippets):
            console = console + Const.SNIPPET_HEADER_STR % (idx+1, row[Const.SNIPPET_BRIEF], row[Const.SNIPPET_ID])
            console = Const.SNIPPET_SNIPPET_STR % (console, row[Const.SNIPPET_SNIPPET]) + Const.NEWLINE
            console = console + ''.join([Const.SNIPPET_LINKS_STR % (links, link) \
                      for link in row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS)])
            console = Const.SNIPPET_TAGS_STR % (console, row[Const.SNIPPET_TAGS])
            console = console + Const.NEWLINE

        return console

    def format_dict(self, snippets):
        """Format snippets for yaml file."""

        self.logger.debug('format search snippets to yaml')
        snippet_dict = {}
        snippet_list = []
        for row in snippets:
            snippet = {'brief': row[Const.SNIPPET_BRIEF],
                       'snippet': row[Const.SNIPPET_SNIPPET],
                       'links': row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS),
                       'tags': row[Const.SNIPPET_TAGS]}
            snippet_list.append(snippet.copy())
        snippet_dict = {'snippets': snippet_list}

        return snippet_dict

    def print_console(self, snippets):
        """Print snippets into console."""

        self.logger.debug('printing search results')
        print(snippets)

    def print_file(self, snippet_dict):
        """Print snippets into file."""

        import yaml
        import json

        export = Config.get_export()
        self.logger.debug('exporting storage into file %s', export)
        with open(export, 'w') as outfile:
            try:
                if Config.is_export_format_yaml():
                    yaml.dump(snippet_dict, outfile)
                elif Config.is_export_format_json():
                    json.dump(snippet_dict, outfile)
                else:
                    self.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                self.logger.exception('fatal failure to generate yaml formatted export file "%s"', exception)
                self.logger.exception('fatal failure with dictionary %s', snippet_dict)
                sys.exit()

    def run(self, storage):
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        self.storage = storage
        if Config.get_snippet():
            self.add()
        elif Config.get_find_keywords():
            snippets = self.find_keywords()
            snippets = self.format_console(snippets)
            self.print_console(snippets)
        elif Config.get_delete():
            self.delete()
        elif Config.get_export():
            self.export()
        else:
            self.logger.error('unknown action for snippet')
