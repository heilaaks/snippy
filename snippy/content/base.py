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

"""base: Base class for content types."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger
from snippy.migrate.migrate import Migrate


class ContentTypeBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for content types."""

    def __init__(self, storage, content_type=Const.CONTENT_TYPE_TEXT):
        self._logger = Logger.get_logger(__name__)
        self._content_type = content_type
        self.category = Const.SNIPPET
        self.storage = storage
        self.collection = Collection()

    @property
    def collection(self):
        """Get collection."""

        return self._collection

    @collection.setter
    def collection(self, value):
        """Content collection."""

        self._collection = value

    @staticmethod
    def _meta_content(contents=None, total=None):
        """Wrap content with metadata."""

        if contents is None:
            contents = []

        meta_content = {
            'data': contents,
            'meta': {
                'total': len(contents) if total is None else total,
            }
        }

        return meta_content
