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
        Config.update()
        snippet = {'content': Config.get_job_content(), 'brief': Config.get_job_brief(),
                   'category': Config.get_job_category(), 'tags': Config.get_job_tags(),
                   'links': Config.get_job_links()}
        self.storage.create(snippet)

    def search(self):
        """Search snippets based on keywords."""

        self.logger.info('searching snippets based on keywords')
        snippets = self.storage.search(Config.get_search_keywords())
        snippets = self.format_text(snippets, colors=True)
        self.print_terminal(snippets)

    def update(self):
        """Update snippet."""

        self.logger.debug('updating snippet')
        keywords = []
        digest = Config.get_target_id()
        snippets = self.storage.search(keywords, digest)
        if len(snippets) == 1:
            Config.update(self.create_dictionary(snippets)['snippets'][0])
            snippet = {'content': Config.get_job_content(), 'brief': Config.get_job_brief(),
                       'category': Config.get_job_category(), 'tags': Config.get_job_tags(),
                       'links': Config.get_job_links()}
            self.storage.update(digest, snippet)
        elif not snippets:
            self.logger.info('cannot find requested snippet %s', digest)
        else:
            self.logger.error('cannot update two snippets with the same leading digest')

    def delete(self):
        """Delete snippet."""

        self.logger.debug('deleting snippet')
        self.storage.delete(Config.get_target_id())

    def export(self):
        """Export snippets."""

        self.logger.debug('exporting snippets')
        snippets = self.storage.export_snippets()
        self.print_file(snippets)

    def digest(self):
        """Import snippets."""

        self.logger.debug('importing snippets %s', Config.get_file())
        snippets = self.load_dictionary(Config.get_file())
        self.storage.import_snippets(snippets)

    def format_text(self, snippets, colors=False):
        """Format snippets for terminal with color codes or for a raw text output."""

        text = ''
        snippet_string = ''
        link_string = ''
        self.logger.debug('format snippets for text based output')
        for idx, row in enumerate(snippets, start=1):
            text = text + Const.format_header(colors) % (idx, row[Const.SNIPPET_BRIEF], row[Const.SNIPPET_CATEGORY], \
                                                              row[Const.SNIPPET_DIGEST])
            text = text + ''.join([Const.format_snippet(colors) % (snippet_string, snippet_line) \
                      for snippet_line in row[Const.SNIPPET_SNIPPET].split(Const.NEWLINE)])
            text = text + Const.NEWLINE
            text = text + ''.join([Const.format_links(colors) % (link_string, link) \
                      for link in row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS)])
            text = Const.format_tags(colors) % (text, row[Const.SNIPPET_TAGS])
            text = text + Const.NEWLINE

        return text

    def create_dictionary(self, snippets):
        """Create dictionary from snippets in the database for data serialization."""

        snippet_dict = {}
        snippet_list = []
        self.logger.debug('creating dictionary from snippets')
        for row in snippets:
            snippet = {'content': row[Const.SNIPPET_SNIPPET],
                       'brief': row[Const.SNIPPET_BRIEF],
                       'category': row[Const.SNIPPET_CATEGORY],
                       'tags': row[Const.SNIPPET_TAGS].split(Const.DELIMITER_TAGS),
                       'links': row[Const.SNIPPET_LINKS].split(Const.DELIMITER_LINKS),
                       'digest': row[Const.SNIPPET_DIGEST]}
            snippet_list.append(snippet.copy())
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

        export_file = Config.get_file()
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
        """Run the snippet management task."""

        self.logger.info('managing snippet')
        if Config.is_job_create():
            self.create()
        elif Config.is_job_search():
            self.search()
        elif Config.is_job_update():
            self.update()
        elif Config.is_job_delete():
            self.delete()
        elif Config.is_job_export():
            self.export()
        elif Config.is_job_import():
            self.digest()
        else:
            self.logger.error('unknown job for snippet')
