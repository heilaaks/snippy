#!/usr/bin/env python3

"""solution.py: Solution management."""

from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config
from snippy.format import Format
from snippy.migrate import Migrate


class Solution(object):
    """Solution management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def create(self):
        """Create new solution."""

        self.logger.debug('creating new solution')
        solution = Config.get_content()
        if solution:
            cause = self.storage.create(solution)
            if cause == Const.DB_DUPLICATE:
                solutions = self.storage.search(Const.SOLUTION, content=solution[Const.CONTENT])
                if len(solutions) == 1:
                    Config.set_cause('content already exist with digest %.16s' % solutions[0][Const.DIGEST])
                else:
                    self.logger.error('unexpected number of solutions %d received while searching', len(solutions))
        else:
            Config.set_cause('mandatory content not defined')

    def search(self):
        """Search solutions."""

        self.logger.info('searching solutions')
        solutions = ()
        keywords = Config.get_search_keywords()
        if keywords:
            solutions = self.storage.search(Const.SOLUTION, keywords=keywords)
            solutions = Format.get_solution_text(solutions, colors=True)
            Migrate().print_terminal(solutions)

    def update(self):
        """Update existing solution."""

        solution = ()
        content_digest = Config.get_content_digest()
        if content_digest and len(content_digest) >= Const.DIGEST_MIN_LENGTH:
            self.logger.debug('updating soulution with digest %.16s', content_digest)
            solutions = self.storage.search(Const.SOLUTION, digest=content_digest)

        if len(solutions) == 1:
            content_digest = solutions[0][Const.DIGEST]
            solution = Config.get_content(content=solutions[0], use_editor=True)
            self.storage.update(solution, content_digest)
        elif not solutions:
            Config.set_cause('cannot find solution to be updated with digest %.16s' % content_digest)
        else:
            self.logger.error('cannot update multiple soutions with same digest %.16s', content_digest)

    def delete(self):
        """Delete solutions."""

        self.logger.debug('deleting solution')
        solutions = ()
        content_digest = Config.get_content_digest()
        if content_digest and len(content_digest) >= Const.DIGEST_MIN_LENGTH:
            self.logger.debug('deleting soulution with digest %.16s', content_digest)
            solutions = self.storage.search(Const.SOLUTION, digest=content_digest)

        if len(solutions) == 1:
            content_digest = solutions[0][Const.DIGEST]
            self.storage.delete(Const.SOLUTION, content_digest)
        elif not solutions:
            Config.set_cause('cannot find solution to be deleted with digest %.16s' % content_digest)
        else:
            self.logger.error('cannot delete multiple soutions with same digest %.16s', content_digest)

    def export_all(self):
        """Export solutions."""

        self.logger.debug('exporting solutions %s', Config.get_operation_file())
        solution = self.storage.export_content(Const.SOLUTION)
        Migrate().print_file(solution)

    def import_all(self):
        """Import solutions."""

        self.logger.debug('importing solutions %s', Config.get_operation_file())
        solutions = Migrate().load_dictionary(Config.get_operation_file())
        solutions = Format.get_storage(solutions['content'])
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
            self.logger.error('unknown operation for solution')
