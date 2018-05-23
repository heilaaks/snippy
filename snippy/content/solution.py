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
from snippy.content.base import ContentTypeBase
from snippy.content.content import Content
from snippy.logger import Logger
from snippy.migrate.migrate import Migrate


class Solution(ContentTypeBase):
    """Solution management."""

    def __init__(self, storage):
        super(Solution, self).__init__(storage, Const.SOLUTION)

    def export_all(self):
        """Export solutions."""

        filename = Config.get_operation_file()
        if Config.template:
            self._logger.debug('exporting solution template %s', Config.get_operation_file())
            Migrate.dump_template(Content(category=Const.SOLUTION, timestamp=Config.utcnow()))
        elif Config.is_search_criteria():
            self._logger.debug('exporting solutions based on search criteria')
            collection = self.storage.search(
                Const.SOLUTION,
                sall=Config.search_all_kws,
                stag=Config.search_tag_kws,
                sgrp=Config.search_grp_kws,
                digest=Config.operation_digest,
                data=Config.content_data
            )
            if collection.size() == 1:
                resource = next(collection.resources())
                filename = Config.get_operation_file(content_filename=resource.filename)
            elif not collection.size():
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
            solutions, _ = self.storage.search(Const.SOLUTION, digest=content_digest)
            if len(solutions) == 1:
                digest = solutions[0].get_digest()
                self._logger.debug('importing solution with digest %.16s', digest)
                content = Content(category=Const.SOLUTION, timestamp=Config.utcnow())
                dictionary = Migrate.load(Config.get_operation_file(), content)
                contents = Content.load(dictionary)
                solutions[0].migrate(contents[0])
                self.storage.update(solutions[0], digest)
            elif not solutions:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find solution identified with digest {:.16}'.format(content_digest))
            else:
                Cause.push(Cause.HTTP_CONFLICT, 'cannot import multiple solutions with same digest {:.16}'.format(content_digest))
        else:
            self._logger.debug('importing solutions %s', Config.get_operation_file())
            content = Content(category=Const.SOLUTION, timestamp=Config.utcnow())
            dictionary = Migrate.load(Config.get_operation_file(), content)
            solutions = Content.load(dictionary)
            self.storage.import_content(solutions)

