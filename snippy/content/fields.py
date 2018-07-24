#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""snippet: Content fields management."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.base import ContentTypeBase
from snippy.content.collection import Collection
from snippy.logger import Logger


class Fields(ContentTypeBase):
    """Content field management."""

    def __init__(self, storage, run_cli=False):
        super(Fields, self).__init__(storage, run_cli, Const.ALL_CATEGORIES)

#    GROUP = 'groups'
#
#    def __init__(self, storage):
#        self._logger = Logger.get_logger(__name__)
#        self._storage = storage
#        self._collection = Collection()
#
#    @property
#    def collection(self):
#        """Get collection."""
#
#        return self._collection
#
#    @collection.setter
#    def collection(self, value):
#        """Store collection of resources."""
#
#        self._collection = value
#
#    def search_group(self):
#        """Search content from any category based on field."""
#
#        self._logger.debug('searching fields')
#        self.collection = self._storage.search(
#            Const.ALL_CATEGORIES,
#            sall=Config.search_all_kws,
#            stag=Config.search_tag_kws,
#            sgrp=Config.search_grp_kws,
#            digest=Config.operation_digest,
#            data=Config.content_data
#        )
#
#    @Logger.timeit
#    def run(self, field):
#        """Run search operation for defined field."""
#
#        self._logger.debug('run search: %s :field', field)
#        if field == Fields.GROUP:
#            self.search_group()
#        else:
#            Cause.push(Cause.HTTP_BAD_REQUEST, 'unknown field: {}'.format(field))
#
#        self._logger.debug('end search: %s :field', field)
#
#        return self.collection
#