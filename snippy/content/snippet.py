#!/usr/bin/env python3

"""snippet.py: Snippet management."""

from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.migrate.migrate import Migrate
from snippy.content.content import Content


class Snippet(object):
    """Snippet management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def create(self):
        """Create new snippet."""

        self.logger.debug('creating new snippet')
        snippet = Config.get_content(Content())
        if snippet.has_data():
            self.storage.create(snippet)
        else:
            Cause.set_text('mandatory snippet data not defined')

    def search(self):
        """Search snippets."""

        self.logger.info('searching snippets')
        snippets = self.storage.search(Const.SNIPPET,
                                       keywords=Config.get_search_keywords(),
                                       digest=Config.get_content_digest(),
                                       data=Config.get_content_data())
        Migrate().print_terminal(snippets)

    def update(self):
        """Update existing snippet."""

        snippets = ()
        content_digest = Config.get_content_valid_digest()
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
            snippet = Config.get_content(content=snippets[0], use_editor=True)
            self.storage.update(snippet)
        elif not snippets:
            Cause.set_text('cannot find snippet to be updated with %s' % log_string)
        else:
            Cause.set_text('cannot update multiple snippets with same {}'.format(log_string))

    def delete(self):
        """Delete snippet."""

        self.logger.debug('deleting snippet')
        snippets = ()
        content_digest = Config.get_content_valid_digest()
        content_data = Config.get_content_data()
        log_string = 'invalid digest %.16s' % content_digest
        if content_digest:
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
            Cause.set_text('cannot find snippet to be deleted with {}'.format(log_string))
        else:
            Cause.set_text('cannot delete multiple snippets with same {}'.format(log_string))

    def export_all(self):
        """Export snippets."""

        filename = Config.get_operation_file()
        content_digest = Config.get_content_valid_digest()
        if Config.is_migrate_template():
            self.logger.debug('exporting snippet template %s', Config.get_operation_file())
            Migrate().dump_template(Content())
        elif content_digest:
            self.logger.debug('exporting snippet with digest %.16s', content_digest)
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            if len(snippets) == 1:
                filename = Config.get_operation_file(content_filename=snippets[0].get_filename())
            elif not snippets:
                Cause.set_text('cannot find snippet to be exported with digest {:.16}'.format(content_digest))
            Migrate().dump(snippets, filename)
        else:
            self.logger.debug('exporting snippets %s', Config.get_operation_file())
            snippets = self.storage.export_content(Const.SNIPPET)
            Migrate().dump(snippets, filename)

    def import_all(self):
        """Import snippets."""

        content_digest = Config.get_content_valid_digest()
        if content_digest:
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            if len(snippets) == 1:
                dictionary = Migrate().load(Config.get_operation_file(), Content())
                contents = Content().load(dictionary)
                snippets[0].migrate_edited(contents)
                self.storage.update(snippets[0])
            elif not snippets:
                Cause.set_text('cannot find snippet to be imported with digest {:.16}'.format(content_digest))
            else:
                Cause.set_text('cannot import multiple snippets with same digest {:.16}'.format(content_digest))
        else:
            self.logger.debug('importing snippets %s', Config.get_operation_file())
            dictionary = Migrate().load(Config.get_operation_file(), Content())
            snippets = Content().load(dictionary)
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
