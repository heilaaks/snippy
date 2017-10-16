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
        if solution.has_data():
            self.storage.create(solution)
        else:
            Cause.set_text('mandatory solution data not defined')

    def search(self):
        """Search solutions."""

        self.logger.info('searching solutions')
        solutions = self.storage.search(Const.SOLUTION,
                                        keywords=Config.get_search_keywords(),
                                        digest=Config.get_content_digest(),
                                        data=Config.get_content_data())
        Migrate().print_terminal(solutions)

    def update(self):
        """Update existing solution."""

        solution = ()
        content_digest = Config.get_content_digest()
        if content_digest and len(content_digest) >= Const.DIGEST_MIN_LENGTH:
            self.logger.debug('updating soulution with digest %.16s', content_digest)
            solutions = self.storage.search(Const.SOLUTION, digest=content_digest)

        if len(solutions) == 1:
            solution = Config.get_content(content=solutions[0], use_editor=True)
            self.storage.update(solution)
        elif not solutions:
            Cause.set_text('cannot find solution to be updated with digest {:.16}'.format(content_digest))
        else:
            Cause.set_text('cannot update multiple soutions with same digest {:.16}'.format(content_digest))

    def delete(self):
        """Delete solutions."""

        self.logger.debug('deleting solution')
        solutions = ()
        content_digest = Config.get_content_digest()
        if content_digest and len(content_digest) >= Const.DIGEST_MIN_LENGTH:
            self.logger.debug('deleting soulution with digest %.16s', content_digest)
            solutions = self.storage.search(Const.SOLUTION, digest=content_digest)

        if len(solutions) == 1:
            content_digest = solutions[0].get_digest()
            self.storage.delete(content_digest)
        elif not solutions:
            Cause.set_text('cannot find solution to be deleted with digest {:.16}'.format(content_digest))
        else:
            Cause.set_text('cannot delete multiple soutions with same digest {:.16}'.format(content_digest))

    def export_all(self):
        """Export solutions."""

        if Config.is_export_template():
            self.export_template()
        else:
            self.logger.debug('exporting solutions %s', Config.get_operation_file())
            solutions = self.storage.export_content(Const.SOLUTION)
            Migrate().dump(solutions)

    def import_all(self):
        """Import solutions."""

        self.logger.debug('importing solutions %s', Config.get_operation_file())
        dictionary = Migrate().load(Config.get_operation_file())
        solutions = Content().load(dictionary)
        self.storage.import_content(solutions)

    def export_template(self):
        """Export solution template."""

        template = Config.get_template(Content())
        filename = Config.get_template_filename()
        self.logger.debug('exporting solution template to file %s', filename)
        try:
            with open(filename, 'w') as outfile:
                outfile.write(template)
        except IOError as exception:
            self.logger.exception('fatal failure in creating solution template file "%s"', exception)
            Cause.set_text('cannot export solution template {}'.format(filename))

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
