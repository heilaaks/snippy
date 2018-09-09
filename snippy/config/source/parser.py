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

"""parser: Parse content attributes from text string."""

from snippy.cause import Cause
from snippy.config.source.parsers.base import ContentParserBase
from snippy.config.source.parsers.text import ContentParserText as Text
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger


class Parser(ContentParserBase):
    """Parse content attributes from text source."""

    def __init__(self, filetype, timestamp, text):
        """
        Args:
            filetype (str): Filetype that defines used parser.
            timestamp (str): IS8601 timestamp used with created resources.
            text (str): Source text that is parsed.
        """

        self._logger = Logger.get_logger(__name__)
        self._filetype = filetype
        self._text = text
        self._timestamp = timestamp
        self._parser = self._select_parser(filetype)

    def read(self):
        """Read content attributes from text source.

        Text source specific parser is run against the provided text string.
        The text source can be either the tool specific text or Markdown
        template.

        Returns:
            Collection(): Parsed content in a Collection object.
        """

        collection = Collection()
        if not self._parser:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not select parser for filetype: {}'.format(self._filetype))

            return collection

        data = []
        category = self._parser.content_category(self._text)
        if category == Const.SNIPPET:
            data = self._parser.get_contents(self._text, '# Add mandatory snippet below', 2)
        elif category == Const.SOLUTION:
            data = self._parser.get_contents(self._text, Text.BRIEF[Const.SOLUTION], 1)
        elif category == Const.REFERENCE:
            data = self._parser.get_contents(self._text, '# Add mandatory links below one link per line', 2)
        else:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not identify text source content category: {}'.format(category))

        for item in data:
            resource = collection.get_resource(category, self._timestamp)
            resource.data = self._parser.content_data(category, item)
            resource.brief = self._parser.content_brief(category, item)
            resource.groups = self._parser.content_groups(category, item)
            resource.tags = self._parser.content_tags(category, item)
            resource.links = self._parser.content_links(category, item)
            resource.category = category
            resource.filename = self._parser.content_filename(category, item)
            resource.digest = resource.compute_digest()
            collection.migrate(resource)

        return collection

    @staticmethod
    def _select_parser(filetype):
        """Select parser based on filetype."""

        if filetype == Const.CONTENT_FORMAT_TEXT:
            return Text()

        return None
