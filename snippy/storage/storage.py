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

"""storage.py: Storage management."""

from snippy.config.constants import Constants as Const
from snippy.logger import Logger
from snippy.config.config import Config
from snippy.content.content import Content
from snippy.storage.database.sqlite3db import Sqlite3Db as Database


class Storage(object):
    """Storage management for all types of content."""

    def __init__(self):
        self._logger = Logger(__name__).logger
        self._database = Database()
        self._database.init()

    def create(self, content):
        """Create content."""

        utc = Config.get_utc_time()
        digest = content.compute_digest()
        self._database.insert_content(content, digest, utc)

        return digest

    def search(self, category, sall=None, stag=None, sgrp=None, digest=None, data=None):
        """Search content."""

        rows = self._database.select_content(category, sall, stag, sgrp, digest, data)
        contents = Storage._get_contents(rows)

        return contents

    def update(self, content):
        """Update content."""

        utc = Config.get_utc_time()
        digest = content.compute_digest()
        self._database.update_content(content, digest, utc)

        return digest

    def delete(self, digest):
        """Delete content."""

        self._database.delete_content(digest)

    def export_content(self, category):
        """Export content."""

        rows = self._database.select_all_content(category)
        contents = Storage._get_contents(rows)

        return contents

    def import_content(self, contents):
        """Import contents."""

        return self._database.bulk_insert_content(contents)

    def disconnect(self):
        """Disconnect storage."""

        if self._database:
            self._database.disconnect()
            self._database = None

    @staticmethod
    def _get_contents(rows):
        """Convert database rows to tuple of contents."""

        contents = []
        for row in rows:
            contents.append(Storage._convert(row))

        return tuple(contents)

    @staticmethod
    def _convert(row):
        """Convert single row from database into content."""

        content = Content((tuple(row[Const.DATA].split(Const.DELIMITER_DATA)),
                           row[Const.BRIEF],
                           row[Const.GROUP],
                           tuple(row[Const.TAGS].split(Const.DELIMITER_TAGS) if row[Const.TAGS] else []),
                           tuple(row[Const.LINKS].split(Const.DELIMITER_LINKS) if row[Const.LINKS] else []),
                           row[Const.CATEGORY],
                           row[Const.FILENAME],
                           row[Const.RUNALIAS],
                           row[Const.VERSIONS],
                           row[Const.UTC],
                           row[Const.DIGEST],
                           row[Const.METADATA],
                           row[Const.KEY]))

        return content
