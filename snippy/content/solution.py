#!/usr/bin/env python3

"""solution.py: Solution management."""

from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.migrate.migrate import Migrate
from snippy.content.content import Content


class Solution(object):
    """Solution management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def create(self):
        """Create new solution."""

        self.logger.debug('creating new solution')
        solution = Config.get_content(Content(), use_editor=True)
        if not solution.has_data():
            Cause.set_text('mandatory solution data not defined')
        elif solution.is_data_template():
            Cause.set_text('no content was stored because the solution data is matching to empty template')
        else:
            self.storage.create(solution)

    def search(self):
        """Search solutions."""

        self.logger.info('searching solutions')
        solutions = self.storage.search(Const.SOLUTION,
                                        keywords=Config.get_search_keywords(),
                                        digest=Config.get_content_digest(),
                                        data=Config.get_content_data())
        Migrate.print_terminal(solutions)

    def update(self):
        """Update existing solution."""

        solutions = self.storage.search(Const.SOLUTION,
                                        keywords=Config.get_search_keywords(),
                                        digest=Config.get_content_digest(),
                                        data=Config.get_content_data())
        if len(solutions) == 1:
            self.logger.debug('updating solution with digest %.16s', solutions[0].get_digest())
            solution = Config.get_content(content=solutions[0], use_editor=True)
            self.storage.update(solution)
        else:
            text = Config.validate_search_context(solutions, 'update')
            Cause.set_text(text)

    def delete(self):
        """Delete solutions."""

        solutions = self.storage.search(Const.SOLUTION,
                                        keywords=Config.get_search_keywords(),
                                        digest=Config.get_content_digest(),
                                        data=Config.get_content_data())
        if len(solutions) == 1:
            self.logger.debug('deleting solution with digest %.16s', solutions[0].get_digest())
            self.storage.delete(solutions[0].get_digest())
        else:
            text = Config.validate_search_context(solutions, 'delete')
            Cause.set_text(text)

    def export_all(self):
        """Export solutions."""

        filename = Config.get_operation_file()
        if Config.is_migrate_template():
            self.logger.debug('exporting solution template %s', Config.get_operation_file())
            Migrate.dump_template(Content())
        elif Config.is_search_criteria():
            self.logger.debug('exporting solutions based on search criteria')
            solutions = self.storage.search(Const.SOLUTION,
                                            keywords=Config.get_search_keywords(),
                                            digest=Config.get_content_digest(),
                                            data=Config.get_content_data())
            if len(solutions) == 1:
                filename = Config.get_operation_file(content_filename=solutions[0].get_filename())
            elif not solutions:
                text = Config.validate_search_context(solutions, 'export')
                Cause.set_text(text)
            Migrate.dump(solutions, filename)
        else:
            self.logger.debug('exporting all solutions %s', filename)
            solutions = self.storage.export_content(Const.SOLUTION)
            Migrate.dump(solutions, filename)

    def import_all(self):
        """Import solutions."""

        content_digest = Config.get_content_valid_digest()
        if content_digest:
            solutions = self.storage.search(Const.SOLUTION, digest=content_digest)
            if len(solutions) == 1:
                dictionary = Migrate.load(Config.get_operation_file(), Content())
                contents = Content.load(dictionary)
                solutions[0].migrate_edited(contents)
                self.storage.update(solutions[0])
            elif not solutions:
                Cause.set_text('cannot find solution to be imported with digest {:.16}'.format(content_digest))
            else:
                Cause.set_text('cannot import multiple solutions with same digest {:.16}'.format(content_digest))
        else:
            self.logger.debug('importing solutions %s', Config.get_operation_file())
            dictionary = Migrate.load(Config.get_operation_file(), Content())
            solutions = Content.load(dictionary)
            self.storage.import_content(solutions)

    def run(self):
        """Run the solution management operation."""

        self.logger.info('managing solution')
        Config.set_category(Const.SOLUTION)
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
            Cause.set_text('unknown operation for solution')
