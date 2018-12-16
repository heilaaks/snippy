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

"""storage: Storage management for content."""

from snippy.config.config import Config
from snippy.logger import Logger
from snippy.storage.database import Database


class Storage(object):
    """Storage management for content."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._database = Database()
        self._database.init()

    def create(self, collection):
        """Create new content.

        Args:
            collection (Collection): Content container to be stored into database.
        """

        self._logger.debug('store content')
        collection = self._database.insert(collection)

        return collection

    def search(self, scat=(), sall=(), stag=(), sgrp=(), search_filter=None, uuid=None, digest=None, data=None):
        """Search content.

        Args:
            scat (tuple): Search category keyword list.
            sall (tuple): Search all keyword list.
            stag (tuple): Search tag keyword list.
            sgrp (tuple): Search group keyword list.
            search_filter (str): Regexp filter to limit search results.
            uuid (str): Search specific uuid or part of it.
            digest (str): Search specific digest or part of it.
            data (str): Search specific content data or part of it.

        Returns:
            Collection: Search result in Collection of content.
        """

        self._logger.debug('search content')
        collection = self._database.select(scat, sall, stag, sgrp, search_filter, uuid, digest, data)

        return collection

    def unique_values(self, field):
        """Get unique values for given field.

        Args:
            field (str): Content field which unique values are read.

        Returns:
            tuple: List of unique values for give field.
        """

        self._logger.debug('search unique values for field: ', field)
        values = self._database.select_distinct(field)

        return values

    def update(self, digest, resource):
        """Update resource specified by digest.

        Args:
            digest (str): Content digest that is udpated.
            resource (Resource): A single Resource() container that contains updates.
        """

        self._logger.debug('update content')
        resource.updated = Config.utcnow()
        collection = self._database.update(digest, resource)

        return collection

    def delete(self, digest):
        """Delete content.

        Args:
            digest (str): Content digest that is deleted.
        """

        self._logger.debug('delete content')
        self._database.delete(digest)

    def export_content(self, scat=()):
        """Export content.

        Args:
            scat (tuple): Search category keyword list.
        """

        self._logger.debug('export content')
        collection = self._database.select_all(scat)

        return collection

    def import_content(self, collection):
        """Import content.

        Args:
            collection (Collection): Content container to be imported into database.
        """

        self._logger.debug('import content')
        collection = self._database.insert(collection)

        return collection

    def disconnect(self):
        """Disconnect storage."""

        if self._database:
            self._database.disconnect()
            self._database = None

    def debug(self):
        """Debug storage."""

        if self._database:
            self._database.debug()
