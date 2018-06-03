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

"""storage: Storage management for content."""

from snippy.config.config import Config
from snippy.logger import Logger
from snippy.storage.database.sqlitedb import SqliteDb as Database


class Storage(object):
    """Storage management for content."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._database = Database()
        self._database.init()

    def create(self, collection):
        """Create new content.

        Parameters
        ----------
        Args:
           collection (Collection): Content container to be stored into database.
        """

        self._logger.debug('store content')
        collection = self._database.insert(collection)

        return collection

    def search(self, category, sall=None, stag=None, sgrp=None, digest=None, data=None):
        """Search content.

        Parameters
        ----------
        Args:
           category (str): Content category.
           sall (tuple): Search all keyword list.
           stag (tuple): Search tag keyword list.
           sgrp (tuple): Search group keyword list.
           digest (str): Search specific digest or part of it.
           data (str): Search specific content data or part of it.
        """

        self._logger.debug('search content')
        collection = self._database.select(category, sall, stag, sgrp, digest, data)

        return collection

    def update(self, digest, resource):
        """Update resource specified by digest.

        Parameters
        ----------
        Args:
           digest (str): Content digest that is udpated.
           resource (Resource): A single Resource container that contains updates.
        """

        self._logger.debug('update content')
        resource.updated = Config.utcnow()
        collection = self._database.update(digest, resource)

        return collection

    def delete(self, digest):
        """Delete content.

        Parameters
        ----------
        Args:
           digest (str): Content digest that is deleted.
        """

        self._logger.debug('delete content')
        self._database.delete(digest)

    def export_content(self, category):
        """Export content.

        Parameters
        ----------
        Args:
           category (str): Content category.
        """

        self._logger.debug('export content')
        collection = self._database.select_all(category)

        return collection

    def import_content(self, collection):
        """Import content.

        Parameters
        ----------
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
