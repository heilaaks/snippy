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
        cause = self.storage.create(snippet)
        if cause == Const.DB_DUPLICATE:
            snippets = self.storage.search(content=snippet[Const.SNIPPET_CONTENT])
            if len(snippets) == 1:
                Config.set_cause('content already exist with digest %.16s' % snippets[0][Const.SNIPPET_DIGEST])
            else:
                self.logger.error('unexpected number of snippets received while searching content')

    def search(self):
        """Search snippets."""

        self.logger.info('searching snippets')
        keywords = Config.get_search_keywords()
        content = Config.get_content_data()
        if keywords:
            snippets = self.storage.search(keywords=keywords)
        elif content:
            snippets = self.storage.search(content=content)
        snippets = self.format_to_text(snippets, colors=True)
        self.print_terminal(snippets)

    def update(self):
        """Update existing snippet."""

        operation_digest = Config.get_operation_digest()
        snippet_data = Config.get_content_data()
        if operation_digest:
            self.logger.debug('updating snippet with digest %.16s', operation_digest)
            snippets = self.storage.search(digest=operation_digest)
            log_string = 'digest %.16s' % operation_digest
        elif snippet_data:
            self.logger.debug('updating snippet with content "%s"', snippet_data)
            snippets = self.storage.search(content=snippet_data)
            log_string = 'content %.20s' % snippet_data

        if len(snippets) == 1:
            if operation_digest:
                snippet = Config.get_snippet(snippets[0])
                operation_digest = snippets[0][Const.SNIPPET_DIGEST]
            elif snippet_data:
                snippet = Config.get_snippet(use_editor=True)
                operation_digest = snippets[0][Const.SNIPPET_DIGEST]
            self.storage.update(snippet, operation_digest)
        elif not snippets:
            Config.set_cause('cannot find content to be updated with %s' % log_string)
        else:
            self.logger.error('cannot update multiple snippets with same %s', log_string)

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
        snippets = self.storage.convert_from_dictionary(snippets['snippets'])
        self.storage.import_snippets(snippets)

    def format_to_text(self, snippets, colors=False):
        """Format snippets for terminal with color codes or for a raw text output."""

        text = ''
        content = ''
        links = ''
        self.logger.debug('format snippets into text format')
        for idx, snippet in enumerate(snippets, start=1):
            text = text + Const.format_header(colors) % (idx, snippet[Const.SNIPPET_BRIEF],
                                                         snippet[Const.SNIPPET_GROUP], \
                                                         snippet[Const.SNIPPET_DIGEST])
            text = text + Const.EMPTY.join([Const.format_snippet(colors) % (content, line) \
                                            for line in snippet[Const.SNIPPET_CONTENT]])
            text = text + Const.NEWLINE
            text = Const.format_tags(colors) % (text, Const.DELIMITER_TAGS.join(snippet[Const.SNIPPET_TAGS]))
            text = text + Const.EMPTY.join([Const.format_links(colors) % (links, link) \
                                            for link in snippet[Const.SNIPPET_LINKS]])
            text = text + Const.NEWLINE

        return text

    def load_dictionary(self, snippets):
        """Create dictionary from snippets in a file."""

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

                    snippet_dict = {'snippets': self.storage.convert_to_dictionary(snippets)}
                    yaml.dump(snippet_dict, outfile, default_flow_style=False)
                elif Config.is_file_type_json():
                    import json

                    snippet_dict = {'snippets': self.storage.convert_to_dictionary(snippets)}
                    json.dump(snippet_dict, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_file_type_text():
                    outfile.write(self.format_to_text(snippets))
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
