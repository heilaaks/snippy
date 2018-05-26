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

from snippy.config.constants import Constants as Const
from snippy.logger import Logger
from snippy.storage.database.sqlite3db import Sqlite3Db as Database


class Storage(object):
    """Storage management for content."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._database = Database()
        self._database.init()

    def create(self, collection):
        """Create new content."""

        collection = self._database.insert(collection)

        return collection

    def search(self, category, sall=None, stag=None, sgrp=None, digest=None, data=None):
        """Search content."""

        collection = self._database.select(category, sall, stag, sgrp, digest, data)

        return collection

    def update(self, digest, resource):
        """Update resource specified by digest."""
        
        from snippy.config.config import Config
        
        resource.updated = Config.utcnow()
        collection = self._database.update(digest, resource)

        return collection

    def delete(self, digest):
        """Delete content."""

        self._database.delete(digest)

    def export_content(self, category):
        """Export content."""

        collection = self._database.select_all_content(category)

        return collection

    def import_content(self, collection):
        """Import content."""

        return self._database.insert(collection)

    def disconnect(self):
        """Disconnect storage."""

        if self._database:
            self._database.disconnect()
            self._database = None
