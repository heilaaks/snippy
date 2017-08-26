#!/usr/bin/env python3

"""snippet.py: Snippet management."""

import sys
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config


class Snippet(object):
    """Snippet management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def add(self):
        """Add new snippet."""

        self.logger.debug('adding new snippet')
        self.storage.store(Config.get_snippet(), Config.get_brief(), Config.get_tags(), Config.get_links())

    def find(self):
        """Find snippets based on keywords."""

        self.logger.info('finding snippet based on keywords')
        snippets = self.storage.search(Config.get_find_keywords())
        snippets = self.format_text(snippets, colors=True)
        self.print_terminal(snippets)

    def delete(self):
        """Delete snippet."""

        self.logger.debug('deleting snippet')
        self.storage.delete(Config.get_delete())

    def export(self):
        """export snippets."""

        self.logger.debug('exporting snippets')
        snippets = self.storage.export()
        self.print_file(snippets)

    def format_text(self, snippets, colors=False):
        """Format snippets for terminal with color codes or for a raw text output."""

        text = ''
        snippet_string = ''
        link_string = ''
        self.logger.debug('format snippets for text based output')
        for idx, row in enumerate(snippets, start=1):
            text = text + Const.format_header(colors) % (idx, row[Const.SNIPPET_BRIEF], row[Const.SNIPPET_ID])
            text = text + ''.join([Const.format_snippet(colors) % (snippet_string, snippet_line) \
                      for snippet_line in row[Const.SNIPPET_SNIPPET].split(Const.NEWLINE)])
            text = text + Const.NEWLINE
            text = text + ''.join([Const.format_links(colors) % (link_string, link) \
                      for link in row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS)])
            text = Const.format_tags(colors) % (text, row[Const.SNIPPET_TAGS])
            text = text + Const.NEWLINE

        return text

    def create_dictionary(self, snippets):
        """Create dictionary from snippets for data serialization."""

        snippet_dict = {}
        snippet_list = []
        self.logger.debug('create dictionary from snippets')
        for row in snippets:
            snippet = {'brief': row[Const.SNIPPET_BRIEF],
                       'snippet': row[Const.SNIPPET_SNIPPET],
                       'links': row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS),
                       'tags': row[Const.SNIPPET_TAGS].split(Const.DELIMITER_TAGS)}
            snippet_list.append(snippet.copy())
        snippet_dict = {'snippets': snippet_list}

        return snippet_dict

    def print_terminal(self, snippets):
        """Print snippets into terminal."""

        self.logger.debug('printing search results')
        print(snippets)

    def print_file(self, snippets):
        """Print snippets into file."""

        export = Config.get_export()
        self.logger.debug('export storage into file %s', export)
        with open(export, 'w') as outfile:
            try:
                if Config.is_export_format_yaml():
                    import yaml

                    yaml.dump(self.create_dictionary(snippets), outfile)
                elif Config.is_export_format_json():
                    import json

                    json.dump(self.create_dictionary(snippets), outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_export_format_text():
                    self.format_text(snippets)
                    outfile.write(self.format_text(snippets))
                else:
                    self.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                self.logger.exception('fatal failure to generate formatted export file "%s"', exception)
                sys.exit()

    def run(self):
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        if Config.get_snippet():
            self.add()
        elif Config.get_find_keywords():
            self.find()
        elif Config.get_delete():
            self.delete()
        elif Config.get_export():
            self.export()
        else:
            self.logger.error('unknown action for snippet')
