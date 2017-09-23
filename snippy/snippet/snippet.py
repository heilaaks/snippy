#!/usr/bin/env python3

"""snippet.py: Snippet management."""

import sys
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config
from snippy.format import Format


class Snippet(object):
    """Snippet management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def create(self):
        """Create new snippet."""

        self.logger.debug('creating new snippet')
        snippet = Config.get_content(form=Const.SNIPPET)
        if snippet[Const.CONTENT]:
            cause = self.storage.create(Const.SNIPPET, snippet)
            if cause == Const.DB_DUPLICATE:
                snippets = self.storage.search(Const.SNIPPET, content=snippet[Const.CONTENT])
                if len(snippets) == 1:
                    Config.set_cause('content already exist with digest %.16s' % snippets[0][Const.DIGEST])
                else:
                    self.logger.error('unexpected number of snippets %d received while searching', len(snippets))
        else:
            Config.set_cause('mandatory content not defined')

    def search(self):
        """Search snippets."""

        self.logger.info('searching snippets')
        snippets = ()
        keywords = Config.get_search_keywords()
        content = Config.get_content_data()
        if keywords:
            snippets = self.storage.search(Const.SNIPPET, keywords=keywords)
        elif content:
            snippets = self.storage.search(Const.SNIPPET, content=content)
        snippets = Format.get_snippet_text(snippets, colors=True)
        self.print_terminal(snippets)

    def update(self):
        """Update existing snippet."""

        snippets = ()
        content_digest = Config.get_content_digest()
        snippet_data = Config.get_content_data()
        log_string = 'invalid digest %.16s' % content_digest
        if content_digest:
            self.logger.debug('updating snippet with digest %.16s', content_digest)
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            log_string = 'digest %.16s' % content_digest
        elif snippet_data:
            self.logger.debug('updating snippet with content "%s"', snippet_data)
            snippets = self.storage.search(Const.SNIPPET, content=snippet_data)
            log_string = 'content %.20s' % snippet_data

        if len(snippets) == 1:
            if content_digest:
                snippet = Config.get_content(content=snippets[0], form=Const.SNIPPET)
                content_digest = snippets[0][Const.DIGEST]
            elif snippet_data:
                snippet = Config.get_content(use_editor=True, form=Const.SNIPPET)
                content_digest = snippets[0][Const.DIGEST]
            self.storage.update(Const.SNIPPET, snippet, content_digest)
        elif not snippets:
            Config.set_cause('cannot find snippet to be updated with %s' % log_string)
        else:
            self.logger.error('cannot update multiple snippets with same %s', log_string)

    def delete(self):
        """Delete snippet."""

        self.logger.debug('deleting snippet')
        snippets = ()
        content_digest = Config.get_content_digest()
        snippet_data = Config.get_content_data()
        log_string = 'invalid digest %.16s' % content_digest
        if content_digest and len(content_digest) >= Const.DIGEST_MIN_LENGTH:
            self.logger.debug('deleting snippet with digest %.16s', content_digest)
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            log_string = 'digest %.16s' % content_digest
        elif snippet_data:
            self.logger.debug('deleting snippet with content "%s"', snippet_data)
            snippets = self.storage.search(Const.SNIPPET, content=snippet_data)
            log_string = 'content %.20s' % snippet_data

        if len(snippets) == 1:
            content_digest = snippets[0][Const.DIGEST]
            self.storage.delete(Const.SNIPPET, content_digest)
        elif not snippets:
            Config.set_cause('cannot find snippet to be deleted with %s' % log_string)
        else:
            self.logger.error('cannot delete multiple snippets with same %s', log_string)

    def export_all(self):
        """Export snippets."""

        self.logger.debug('exporting snippets')
        snippets = self.storage.export_content()
        self.print_file(snippets)

    def import_all(self):
        """Import snippets."""

        self.logger.debug('importing snippets %s', Config.get_operation_file())
        snippets = self.load_dictionary(Config.get_operation_file())
        snippets = self.storage.convert_from_dictionary(snippets['snippets'])
        self.storage.import_content(snippets)

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
                    outfile.write(Format.get_snippet_text(snippets, colors=False))
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
