#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""solution: Solution management."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.content.content import Content
from snippy.logger import Logger
from snippy.migrate.migrate import Migrate


class Solution(object):
    """Solution management."""

    def __init__(self, storage, content_type=Const.CONTENT_TYPE_TEXT):
        self._logger = Logger(__name__).logger
        self.storage = storage
        self.content_type = content_type

    def create(self):
        """Create new solution."""

        self._logger.debug('creating new solution')
        solutions = Config.get_contents(Content(category=Const.SOLUTION))
        self.storage.create(solutions)
        solutions = self.storage.search(Const.SOLUTION, digest=solutions[0].get_digest())
        solutions = Migrate.content(solutions, self.content_type)

        return solutions

    def search(self):
        """Search solutions."""

        self._logger.debug('searching solutions')
        solutions = self.storage.search(
            Const.SOLUTION,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        solutions = Migrate.content(solutions, self.content_type)

        return solutions

    def update(self):
        """Update existing solution."""

        solutions = self.storage.search(
            Const.SOLUTION,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if len(solutions) == 1:
            digest = solutions[0].get_digest()
            self._logger.debug('updating solution with digest %.16s', digest)
            contents = Config.get_contents(content=solutions[0])
            self.storage.update(contents[0], digest)
            solutions = self.storage.search(Const.SNIPPET, digest=contents[0].get_digest())
        else:
            Config.validate_search_context(solutions, 'update')

        solutions = Migrate.content(solutions, self.content_type)

        return solutions

    def delete(self):
        """Delete solutions."""

        solutions = self.storage.search(
            Const.SOLUTION,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if len(solutions) == 1:
            self._logger.debug('deleting solution with digest %.16s', solutions[0].get_digest())
            self.storage.delete(solutions[0].get_digest())
        else:
            Config.validate_search_context(solutions, 'delete')

    def export_all(self):
        """Export solutions."""

        filename = Config.get_operation_file()
        if Config.template:
            self._logger.debug('exporting solution template %s', Config.get_operation_file())
            Migrate.dump_template(Content(category=Const.SOLUTION))
        elif Config.is_search_criteria():
            self._logger.debug('exporting solutions based on search criteria')
            solutions = self.storage.search(
                Const.SOLUTION,
                sall=Config.search_all_kws,
                stag=Config.search_tag_kws,
                sgrp=Config.search_grp_kws,
                digest=Config.operation_digest,
                data=Config.content_data
            )
            if len(solutions) == 1:
                filename = Config.get_operation_file(content_filename=solutions[0].get_filename())
            elif not solutions:
                Config.validate_search_context(solutions, 'export')
            Migrate.dump(solutions, filename)
        else:
            self._logger.debug('exporting all solutions %s', filename)
            solutions = self.storage.export_content(Const.SOLUTION)
            Migrate.dump(solutions, filename)

    def import_all(self):
        """Import solutions."""

        content_digest = Config.operation_digest
        if content_digest:
            solutions = self.storage.search(Const.SOLUTION, digest=content_digest)
            if len(solutions) == 1:
                digest = solutions[0].get_digest()
                self._logger.debug('importing solution with digest %.16s', digest)
                dictionary = Migrate.load(Config.get_operation_file(), Content(category=Const.SOLUTION))
                contents = Content.load(dictionary)
                solutions[0].migrate_edited(contents)
                self.storage.update(solutions[0], digest)
            elif not solutions:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find solution identified with digest {:.16}'.format(content_digest))
            else:
                Cause.push(Cause.HTTP_CONFLICT, 'cannot import multiple solutions with same digest {:.16}'.format(content_digest))
        else:
            self._logger.debug('importing solutions %s', Config.get_operation_file())
            dictionary = Migrate.load(Config.get_operation_file(), Content(category=Const.SOLUTION))
            solutions = Content.load(dictionary)
            self.storage.import_content(solutions)

    def run(self):
        """Run the solution management operation."""

        solutions = ()

        self._logger.debug('managing solution')
        Config.content_category = Const.SOLUTION
        if Config.is_operation_create:
            solutions = self.create()
        elif Config.is_operation_search:
            solutions = self.search()
        elif Config.is_operation_update:
            solutions = self.update()
        elif Config.is_operation_delete:
            self.delete()
        elif Config.is_operation_export:
            self.export_all()
        elif Config.is_operation_import:
            self.import_all()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'unknown operation for solution')

        return solutions
