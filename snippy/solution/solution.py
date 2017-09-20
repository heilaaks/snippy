#!/usr/bin/env python3

"""solution.py: Solution management."""

from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config


class Solution(object):
    """Solution management."""

    def __init__(self, storage):
        self.logger = Logger(__name__).get()
        self.storage = storage

    def create(self):
        """Create new solution."""

        # pylint: disable=duplicate-code
        self.logger.debug('creating new solution')
        solution = Config.get_content(form=Const.SOLUTION)
        cause = self.storage.create(solution)
        Config.set_cause('snippet created with cause' % cause)

    def run(self):
        """Run the solution management operation."""

        self.logger.info('managing solution')
        if Config.is_operation_create():
            self.create()
        #elif Config.is_operation_search():
        #    self.search()
        #elif Config.is_operation_update():
        #    self.update()
        #elif Config.is_operation_delete():
        #    self.delete()
        #elif Config.is_operation_export():
        #    self.export_all()
        #elif Config.is_operation_import():
        #    self.import_all()
        else:
            self.logger.error('unknown operation for solution')
