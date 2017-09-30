#!/usr/bin/env python3

"""snippet.py: Snippet management."""

from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config
from snippy.migrate import Migrate


class Snippet(object):
    """Snippet management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def create(self):
        """Create new snippet."""

        self.logger.debug('creating new snippet')
        snippet = Config.get_content()
        if snippet.has_data():
            cause = self.storage.create(snippet)
            if cause == Const.DB_DUPLICATE:
                snippets = self.storage.search(Const.SNIPPET, data=snippet.get_data())
                if len(snippets) == 1:
                    Config.set_cause('content already exist with digest %.16s' % snippets[0].get_digest())
                else:
                    self.logger.error('unexpected number of snippets %d received while searching', len(snippets))
        else:
            Config.set_cause('mandatory content data not defined')

    def search(self):
        """Search snippets."""

        self.logger.info('searching snippets')
        snippets = ()
        keywords = Config.get_search_keywords()
        content_data = Config.get_content_data()
        if keywords:
            snippets = self.storage.search(Const.SNIPPET, keywords=keywords)
        elif content_data:
            snippets = self.storage.search(Const.SNIPPET, data=content_data)
        Migrate().print_terminal(snippets)

    def update(self):
        """Update existing snippet."""

        snippets = ()
        content_digest = Config.get_content_digest()
        content_data = Config.get_content_data()
        log_string = 'invalid digest %.16s' % content_digest
        if content_digest:
            self.logger.debug('updating snippet with digest %.16s', content_digest)
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            log_string = 'digest %.16s' % content_digest
        elif content_data:
            self.logger.debug('updating snippet with content "%s"', content_data)
            snippets = self.storage.search(Const.SNIPPET, data=content_data)
            log_string = 'content %.20s' % content_data

        if len(snippets) == 1:
            if content_digest:
                snippet = Config.get_content(content=snippets[0])
            elif content_data:
                snippet = Config.get_content(content=snippets[0], use_editor=True)
            self.storage.update(snippet)
        elif not snippets:
            Config.set_cause('cannot find snippet to be updated with %s' % log_string)
        else:
            self.logger.error('cannot update multiple snippets with same %s', log_string)

    def delete(self):
        """Delete snippet."""

        self.logger.debug('deleting snippet')
        snippets = ()
        content_digest = Config.get_content_digest()
        content_data = Config.get_content_data()
        log_string = 'invalid digest %.16s' % content_digest
        if content_digest and len(content_digest) >= Const.DIGEST_MIN_LENGTH:
            self.logger.debug('deleting snippet with digest %.16s', content_digest)
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            log_string = 'digest %.16s' % content_digest
        elif content_data:
            self.logger.debug('deleting snippet with content "%s"', content_data)
            snippets = self.storage.search(Const.SNIPPET, data=content_data)
            log_string = 'content %.20s' % content_data

        if len(snippets) == 1:
            content_digest = snippets[0].get_digest()
            self.storage.delete(content_digest)
        elif not snippets:
            Config.set_cause('cannot find snippet to be deleted with %s' % log_string)
        else:
            self.logger.error('cannot delete multiple snippets with same %s', log_string)

    def export_all(self):
        """Export snippets."""

        self.logger.debug('exporting snippets %s', Config.get_operation_file())
        snippets = self.storage.export_content(Const.SNIPPET)
        Migrate().dump(snippets)

    def import_all(self):
        """Import snippets."""

        self.logger.debug('importing snippets %s', Config.get_operation_file())
        snippets = Migrate().load(Config.get_operation_file())
        self.storage.import_content(snippets)

    def run(self):
        """Run the snippet management operation."""

        self.logger.info('managing snippet')
        Config.set_category(Const.SNIPPET)
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
