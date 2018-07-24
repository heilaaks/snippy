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

"""base: Base class for content types."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.content.collection import Collection
from snippy.logger import Logger
from snippy.content.migrate import Migrate


class ContentTypeBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for content types."""

    def __init__(self, storage, run_cli, category):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._run_cli = run_cli
        self._storage = storage
        self._collection = Collection()

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

        self._logger.debug('creating new: %s', self._category)
        collection = Config.get_collection()
        collection = self._storage.create(collection)
        self.collection.migrate(collection)

    def search(self):
        """Search content."""

        self._logger.debug('searching: %s', self._category)
        self.collection = self._storage.search(
            self._category,
            sall=Config.search_all_kws,
            scat=Config.search_cat_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if self._run_cli:
            self.collection.dump_term(Config.use_ansi, Config.debug_logs, Config.search_filter)

    def update(self):
        """Update content."""

        collection = self._storage.search(
            self._category,
            sall=Config.search_all_kws,
            scat=Config.search_cat_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if collection.size() == 1:
            stored = next(collection.resources())
            digest = stored.digest
            self._logger.debug('updating stored: %s :with digest: %.16s', self._category, digest)
            updates = Config.get_resource(updates=stored)
            if Config.merge:
                stored.merge(updates)
            else:
                stored.migrate(updates)
            self.collection = self._storage.update(digest, stored)
        else:
            Config.validate_search_context(collection, 'update')

    def delete(self):
        """Delete content."""

        collection = self._storage.search(
            self._category,
            sall=Config.search_all_kws,
            scat=Config.search_cat_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if collection.size() == 1:
            resource = next(collection.resources())
            self._logger.debug('deleting: %s :with digest: %.16s', resource.category, resource.digest)
            self._storage.delete(resource.digest)
        else:
            Config.validate_search_context(collection, 'delete')

    def export_all(self):
        """Export content."""

        filename = Config.get_operation_file()
        if Config.template:
            self._logger.debug('exporting: %s :template: %s', self._category, Config.get_operation_file())
            Migrate.dump_template(self._category)
        elif Config.is_search_criteria():
            self._logger.debug('exporting: %s :based on search criteria', self._category)
            collection = self._storage.search(
                self._category,
                sall=Config.search_all_kws,
                scat=Config.search_cat_kws,
                stag=Config.search_tag_kws,
                sgrp=Config.search_grp_kws,
                digest=Config.operation_digest,
                data=Config.content_data
            )
            if collection.size() == 1:
                resource = next(collection.resources())
                filename = Config.get_operation_file(resource=resource)
            elif collection.empty():
                Config.validate_search_context(collection, 'export')
            Migrate.dump(collection, filename)
        else:
            self._logger.debug('exporting all: %s :content: %s', self._category, filename)
            collection = self._storage.export_content(self._category)
            Migrate.dump(collection, filename)

    def import_all(self):
        """Import content."""

        content_digest = Config.operation_digest
        if content_digest:
            collection = self._storage.search(self._category, digest=content_digest)
            if collection.size() == 1:
                resource = next(collection.resources())
                digest = resource.digest
                self._logger.debug('importing: %s :with digest: %.16s', resource.category, resource.digest)
                collection = Migrate.load(Config.get_operation_file())
                updates = next(collection.resources())
                resource.migrate(updates)
                self._storage.update(digest, resource)
            elif collection.empty():
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find: {} :identified with digest: {:.16}'.format(self._category, content_digest))
            else:
                Cause.push(Cause.HTTP_CONFLICT, 'cannot import: {} :because digest: {:.16} :matched: {} :times'.format(self._category,
                                                                                                                       content_digest,
                                                                                                                       collection.size()))
        else:
            self._logger.debug('importing content: %s', Config.get_operation_file())
            collection = Migrate.load(Config.get_operation_file())
            self._storage.import_content(collection)

    @Logger.timeit
    def run(self):
        """Run operation."""

        self._logger.debug('run: %s :content', self._category)
        Config.content_category = self._category
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
            Cause.push(Cause.HTTP_BAD_REQUEST, 'unknown operation for: {}'.format(self._category))

        self._logger.debug('end: %s :content', self._category)

        return self.collection
