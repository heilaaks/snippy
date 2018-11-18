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

"""base: Parse content from dictionary."""

from snippy.constants import Constants as Const
from snippy.content.parsers.base import ContentParserBase
from snippy.logger import Logger


class ContentParserDict(ContentParserBase):
    """Parse content from dictionary."""

    def __init__(self, timestamp, dictionary, collection):
        """
        Args:
            timestamp (str): IS8601 timestamp used with created resources.
            dictionary (dict): Dictionary where the content is read.
            collection (Collection()): Collection where the content is stored.
        """

        self._logger = Logger.get_logger(__name__)
        self._timestamp = timestamp
        self._dictionary = dictionary
        self._collection = collection

    def read_collection(self):
        """Read collection from the given dictionary source."""

        if 'data' in self._dictionary:
            for content in self._dictionary['data']:
                if 'category' in content and content['category'] in Const.CATEGORIES:
                    category = content.get('category')
                    resource = self._collection.get_resource(category, self._timestamp)
                    resource.data = self.format_data(category, content.get('data', resource.data))
                    resource.brief = self.format_string(content.get('brief', resource.brief))
                    resource.description = self.format_string(content.get('description', resource.description))
                    resource.groups = self.format_list(content.get('groups', resource.groups))
                    resource.tags = self.format_list(content.get('tags', resource.tags))
                    resource.links = self.format_links(content.get('links', resource.links))
                    resource.category = content.get('category')
                    resource.filename = self.format_string(content.get('filename', resource.filename))
                    resource.name = self.format_string(content.get('name', resource.name))
                    resource.versions = self.format_string(content.get('versions', resource.versions))
                    resource.source = self.format_string(content.get('source', resource.source))
                    resource.uuid = content.get('uuid', resource.uuid)
                    resource.created = content.get('created', resource.created)
                    resource.updated = content.get('updated', resource.updated)
                    resource.digest = content.get('digest', resource.digest)
                    self._collection.migrate(resource)
                else:
                    self._logger.debug('content category not indentified: %s', content)
        else:
            self._logger.debug('structured content format not indentified: %s', self._dictionary)
