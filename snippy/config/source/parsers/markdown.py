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

"""base: Parse content from text templates."""

import re

from snippy.config.source.parsers.base import ContentParserBase
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger


class ContentParserMarkdown(ContentParserBase):
    """Parse content from Markdown templates."""

    def __init__(self, timestamp, text):
        """
        Args:
            timestamp (str): IS8601 timestamp used with created resources.
            text (str): Source text that is parsed.
        """

        self._logger = Logger.get_logger(__name__)
        self._timestamp = timestamp
        self._text = text

    def read_collection(self):
        """Read collection from the given text source."""

        collection = Collection()
        contents = self._split_contents()
        for content in contents:
            category = self._read_category(content)
            resource = collection.get_resource(category, self._timestamp)
            resource.data = self._read_data(category, content)
            resource.brief = self._read_brief(category, content)
            resource.groups = self._read_groups(category, content)
            resource.tags = self._read_tags(category, content)
            resource.links = self._read_links(category, content)
            resource.category = category
            resource.filename = self._read_filename(category, content)
            resource.digest = resource.compute_digest()
            collection.migrate(resource)

        return collection
