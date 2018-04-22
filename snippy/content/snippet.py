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
from snippy.content.content import Content
from snippy.logger import Logger
from snippy.migrate.migrate import Migrate


class Snippet(object):
    """Snippet management."""

    def __init__(self, storage, content_type=Const.CONTENT_TYPE_TEXT):
        self._logger = Logger(__name__).logger
        self.storage = storage
        self.content_type = content_type

    def create(self):
        """Create new snippet."""

        self._logger.debug('creating new snippet')
        snippets = Config.get_contents(Content(category=Const.SNIPPET))
        self.storage.create(snippets)
        snippets = self.storage.search(Const.SNIPPET, digest=snippets[0].get_digest())
        snippets = Migrate.content(snippets, self.content_type)

        return snippets

    def search(self):
        """Search snippets."""

        self._logger.debug('searching snippets')
        snippets = self.storage.search(
            Const.SNIPPET,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        snippets = Migrate.content(snippets, self.content_type)

        return snippets

    def update(self):
        """Update snippet."""

        snippets = self.storage.search(
            Const.SNIPPET,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if len(snippets) == 1:
            digest = snippets[0].get_digest()
            self._logger.debug('updating snippet with digest %.16s', digest)
            contents = Config.get_contents(content=snippets[0])
            self.storage.update(contents[0], digest)
            snippets = self.storage.search(Const.SNIPPET, digest=contents[0].get_digest())
        else:
            Config.validate_search_context(snippets, 'update')

        snippets = Migrate.content(snippets, self.content_type)

        return snippets

    def delete(self):
        """Delete snippet."""

        snippets = self.storage.search(
            Const.SNIPPET,
            sall=Config.search_all_kws,
            stag=Config.search_tag_kws,
            sgrp=Config.search_grp_kws,
            digest=Config.operation_digest,
            data=Config.content_data
        )
        if len(snippets) == 1:
            self._logger.debug('deleting snippet with digest %.16s', snippets[0].get_digest())
            self.storage.delete(snippets[0].get_digest())
        else:
            Config.validate_search_context(snippets, 'delete')

    def export_all(self):
        """Export snippets."""

        filename = Config.get_operation_file()
        if Config.template:
            self._logger.debug('exporting snippet template %s', Config.get_operation_file())
            Migrate.dump_template(Content(category=Const.SNIPPET))
        elif Config.is_search_criteria():
            self._logger.debug('exporting snippets based on search criteria')
            snippets = self.storage.search(
                Const.SNIPPET,
                sall=Config.search_all_kws,
                stag=Config.search_tag_kws,
                sgrp=Config.search_grp_kws,
                digest=Config.operation_digest,
                data=Config.content_data
            )
            if len(snippets) == 1:
                filename = Config.get_operation_file(content_filename=snippets[0].get_filename())
            elif not snippets:
                Config.validate_search_context(snippets, 'export')
            Migrate.dump(snippets, filename)
        else:
            self._logger.debug('exporting all snippets %s', filename)
            snippets = self.storage.export_content(Const.SNIPPET)
            Migrate.dump(snippets, filename)

    def import_all(self):
        """Import snippets."""

        content_digest = Config.operation_digest
        if content_digest:
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            if len(snippets) == 1:
                digest = snippets[0].get_digest()
                self._logger.debug('importing solution with digest %.16s', digest)
                dictionary = Migrate.load(Config.get_operation_file(), Content(category=Const.SNIPPET))
                contents = Content.load(dictionary)
                snippets[0].migrate(contents)
                self.storage.update(snippets[0], digest)
            elif not snippets:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find snippet identified with digest {:.16}'.format(content_digest))
            else:
                Cause.push(Cause.HTTP_CONFLICT, 'cannot import multiple snippets with same digest {:.16}'.format(content_digest))
        else:
            self._logger.debug('importing snippets %s', Config.get_operation_file())
            dictionary = Migrate.load(Config.get_operation_file(), Content(category=Const.SNIPPET))
            snippets = Content.load(dictionary)
            self.storage.import_content(snippets)

    def run(self):
        """Run the snippet management operation."""

        snippets = ()
        self._logger.debug('managing snippet')
        Config.content_category = Const.SNIPPET
        if Config.is_operation_create:
            snippets = self.create()
        elif Config.is_operation_search:
            snippets = self.search()
        elif Config.is_operation_update:
            snippets = self.update()
        elif Config.is_operation_delete:
            self.delete()
        elif Config.is_operation_export:
            self.export_all()
        elif Config.is_operation_import:
            self.import_all()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'unknown operation for snippet')

        return snippets
