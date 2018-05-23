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
from snippy.content.content import Content
from snippy.content.collection import Collection
from snippy.logger import Logger
from snippy.migrate.migrate import Migrate


class ContentTypeBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for content types."""

    def __init__(self, storage, category):
        self._logger = Logger.get_logger(__name__)
        self.category = category
        self.collection = Collection()
        self._storage = storage
        self.__tobe_removed = Content(category=category, timestamp='2017-10-14T19:56:31.000001+0000') # Remove when done

    @property
    def collection(self):
        """Get collection."""

        return self._collection

    @collection.setter
    def collection(self, value):
        """Store collection of resources."""

        self._collection = value

    def create(self):
        """Create new content."""

        self._logger.debug('creating new %s', self.category)
        collection = Config.get_contents(Content(category=self.category, timestamp=Config.utcnow())) # TODO remove Content when  done
        collection = self._storage.create(collection)
        self.collection.migrate(collection)

    def search(self):
        """Search content."""

        self._logger.debug('searching %s', self.category)
        self.collection = self._storage.search(
            Const.SNIPPET,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )

    def update(self):
        """Update content."""

        collection = self._storage.search(
            self.category,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if collection.size() == 1:
            stored = next(collection.resources())
            digest = stored.digest
            self._logger.debug('updating stored %s with digest %.16s', self.category, digest)
            updates = Config.get_resource(self.__tobe_removed)
            if Config.merge:
                stored.merge(updates)
                updates = stored
            self.collection = self._storage.update(digest, updates)
        else:
            Config.validate_search_context(collection, 'update')

    def delete(self):
        """Delete content."""

        collection = self._storage.search(
            self.category,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if collection.size() == 1:
            resource = next(collection.resources())
            self._logger.debug('deleting %s with digest %.16s', resource.category, resource.digest)
            self._storage.delete(resource.digest)
        else:
            Config.validate_search_context(collection, 'delete')

    @Logger.timeit
    def run(self):
        """Run operation."""

        self._logger.debug('run %s content', self.category)
        Config.content_category = self.category
        if Config.is_operation_create:
            self.create()
        elif Config.is_operation_search:
            self.search()
        elif Config.is_operation_update:
            self.update()
        elif Config.is_operation_delete:
            self.delete()
        elif Config.is_operation_export:
            self.export_all()
        elif Config.is_operation_import:
            self.import_all()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'unknown operation for %s', self.category)

        self._logger.debug('end %s content', self.category)

        return self.collection

