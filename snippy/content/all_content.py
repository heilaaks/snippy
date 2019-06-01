#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""all_content: All content management."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.base import ContentBase
from snippy.content.migrate import Migrate


class AllContent(ContentBase):
    """Content field management."""

    def __init__(self, storage, run_cli=True):
        super(AllContent, self).__init__(storage, Const.ALL_CATEGORIES, run_cli)

    def import_all(self):
        """Import content."""

        if Config.defaults:
            self._logger.debug('importing all default content')
            collection = Migrate.load(Config.default_content_file(Const.SNIPPET))
            collection.migrate(Migrate.load(Config.default_content_file(Const.SOLUTION)))
            collection.migrate(Migrate.load(Config.default_content_file(Const.REFERENCE)))
            self._storage.import_content(collection)
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'import operation for content category \'all\' is supported only with default content')
