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

"""snippet: Snippet management."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.content.base import ContentTypeBase
from snippy.content.content import Content
from snippy.content.collection import Collection
from snippy.logger import Logger
from snippy.migrate.migrate import Migrate


class Snippet(ContentTypeBase):
    """Snippet management."""

    def __init__(self, storage):
        super(Snippet, self).__init__(storage, Const.SNIPPET)

    def export_all(self):
        """Export snippets."""

        filename = Config.get_operation_file()
        if Config.template:
            self._logger.debug('exporting snippet template %s', Config.get_operation_file())
            Migrate.dump_template(Content(category=Const.SNIPPET, timestamp=Config.utcnow()))
        elif Config.is_search_criteria():
            self._logger.debug('exporting snippets based on search criteria')
            collection = self._storage.search(
                Const.SNIPPET,
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
                Config.validate_search_context(snippets, 'export')
            Migrate.dump(collection, filename)
        else:
            self._logger.debug('exporting all snippets %s', filename)
            snippets = self._storage.export_content(Const.SNIPPET)
            Migrate.dump(snippets, filename)

    def import_all(self):
        """Import snippets."""

        collection = Collection()
        content_digest = Config.operation_digest
        if content_digest:
            collection = self._storage.search(Const.SNIPPET, digest=content_digest)
            if collection.size() == 1:
                digest = collection[0].get_digest()
                self._logger.debug('importing solution with digest %.16s', digest)
                content = Content(category=Const.SNIPPET, timestamp=Config.utcnow())
                dictionary = Migrate.load(Config.get_operation_file(), content)
                contents = Content.load(dictionary)
                snippets[0].migrate(contents[0])
                self._storage.update(snippets[0], digest)
            elif not snippets:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find snippet identified with digest {:.16}'.format(content_digest))
            else:
                Cause.push(Cause.HTTP_CONFLICT, 'cannot import multiple snippets with same digest {:.16}'.format(content_digest))
        else:
            self._logger.debug('importing snippets %s', Config.get_operation_file())
            content = Content(category=Const.SNIPPET, timestamp=Config.utcnow())
            collection = Migrate.load(collection, Config.get_operation_file(), content)
            self._storage.import_content(collection)

