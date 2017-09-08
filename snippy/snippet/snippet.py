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

    def create(self):
        """Create new snippet."""

        self.logger.debug('creating new snippet')
        snippet = Config.get_snippet()
        result = self.storage.create(snippet)
        if result == Const.DB_DUPLICATE:
            rows = self.storage.search(None, None, snippet['content'])
            if len(rows) == 1:
                Config.set_exit_cause('content already exist with digest %.16s' % rows[0][Const.SNIPPET_DIGEST])
                self.logger.info('use update operation for duplicated content %.16s', rows[0][Const.SNIPPET_DIGEST])
            else:
                self.logger.error('unexpected number of rows received while searching content')

    def search(self):
        """Search snippets based on keywords."""

        self.logger.info('searching snippets')
        snippets = self.storage.search(Config.get_search_keywords())
        snippets = self.format_text(snippets, colors=True)
        self.print_terminal(snippets)

    def update(self):
        """Update snippet based on message digest or content."""

        digest = Config.get_operation_digest()
        content = Config.get_content_data()
        if digest:
            self.logger.debug('updating snippet with digest %.16s', digest)
            rows = self.storage.search(None, digest)
        elif content:
            self.logger.debug('updating snippet with content "%s"', content)
            rows = self.storage.search(None, None, content)

        if len(rows) == 1:
            if digest:
                snippet = Config.get_snippet(self.convert_db_row(rows[0]))
            else:
                digest = rows[0][Const.SNIPPET_DIGEST]
                snippet = Config.get_snippet(None, use_editor=True)
            self.storage.update(digest, snippet)
        elif not rows:
            self.logger.info('cannot find requested snippet with digest %.16s or content "%s"', digest, content)
        else:
            self.logger.error('cannot update multiple snippets with same digest  %.16s or content "%s"', digest, content)

    def delete(self):
        """Delete snippet."""

        self.logger.debug('deleting snippet')
        self.storage.delete(Config.get_operation_digest())

    def export_all(self):
        """Export snippets."""

        self.logger.debug('exporting snippets')
        snippets = self.storage.export_snippets()
        self.print_file(snippets)

    def import_all(self):
        """Import snippets."""

        self.logger.debug('importing snippets %s', Config.get_operation_file())
        snippets = self.load_dictionary(Config.get_operation_file())
        self.storage.import_snippets(snippets)

    def format_text(self, snippets, colors=False):
        """Format snippets for terminal with color codes or for a raw text output."""

        text = ''
        snippet_string = ''
        link_string = ''
        self.logger.debug('format snippets for text based output')
        for idx, row in enumerate(snippets, start=1):
            text = text + Const.format_header(colors) % (idx, row[Const.SNIPPET_BRIEF], row[Const.SNIPPET_GROUP], \
                                                              row[Const.SNIPPET_DIGEST])
            text = text + ''.join([Const.format_snippet(colors) % (snippet_string, snippet_line) \
                      for snippet_line in row[Const.SNIPPET_DATA].split(Const.NEWLINE)])
            text = text + Const.NEWLINE
            text = text + ''.join([Const.format_links(colors) % (link_string, link) \
                      for link in row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS)])
            text = Const.format_tags(colors) % (text, row[Const.SNIPPET_TAGS])
            text = text + Const.NEWLINE

        return text

    @staticmethod
    def convert_db_row(row):
        """Convert row from database to snippet dictionary."""
        snippet = {'content': row[Const.SNIPPET_DATA],
                   'brief': row[Const.SNIPPET_BRIEF],
                   'group': row[Const.SNIPPET_GROUP],
                   'tags': row[Const.SNIPPET_TAGS].split(Const.DELIMITER_TAGS),
                   'links': row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS),
                   'digest': row[Const.SNIPPET_DIGEST]}

        return snippet

    def create_dictionary(self, snippets):
        """Create dictionary from snippets in the database for data serialization."""

        snippet_dict = {}
        snippet_list = []
        self.logger.debug('creating dictionary from snippets')
        for row in snippets:
            snippet_list.append(self.convert_db_row(row))
        snippet_dict = {'snippets': snippet_list}

        return snippet_dict

    def load_dictionary(self, snippets):
        """Create dictionary from snippets in a file for data serialization."""

        snippet_dict = {}
        self.logger.debug('loading snippet dictionary from file')
        with open(snippets, 'r') as infile:
            try:
                if Config.is_file_type_yaml():
                    import yaml

                    snippet_dict = yaml.load(infile)
                elif Config.is_file_type_json():
                    import json

                    snippet_dict = json.load(infile)
                else:
                    self.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                self.logger.exception('fatal exception while loading the import file %s "%s"', snippets, exception)
                sys.exit()

        return snippet_dict

    def print_terminal(self, snippets):
        """Print snippets into terminal."""

        self.logger.debug('printing search results')
        print(snippets)

    def print_file(self, snippets):
        """Print snippets into file."""

        export_file = Config.get_operation_file()
        self.logger.debug('export storage into file %s', export_file)
        with open(export_file, 'w') as outfile:
            try:
                if Config.is_file_type_yaml():
                    import yaml

                    yaml.dump(self.create_dictionary(snippets), outfile)
                elif Config.is_file_type_json():
                    import json

                    json.dump(self.create_dictionary(snippets), outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_file_type_text():
                    self.format_text(snippets)
                    outfile.write(self.format_text(snippets))
                else:
                    self.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                self.logger.exception('fatal failure to generate formatted export file "%s"', exception)
                sys.exit()

    def run(self):
        """Run the snippet management operation."""

        self.logger.info('managing snippet')
        if Config.is_operation_create():
            self.create()
        elif Config.is_operation_search():
            self.search()
        elif Config.is_operation_update():
            self.update()
        elif Config.is_operation_delete():
            self.delete()
        elif Config.is_operation_export():
            self.export_all()
        elif Config.is_operation_import():
            self.import_all()
        else:
            self.logger.error('unknown operation for snippet')
