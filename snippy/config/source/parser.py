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
from snippy.config.source.parsers.mkdn import ContentParserMkdn as Mkdn
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
        self._parser = self._parser_factory()

    def read(self):
        """Read content attributes from text source.

        Text source specific parser is run against the provided text string.
        The text source can be either the tool specific text or Markdown
        template.

        Returns:
            Collection(): Parsed content in a Collection object.
        """

        if not self._parser:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not select parser for filetype: {}'.format(self._filetype))

            return Collection()

        collection = self._parser.read_collection()

        return collection

    def _parser_factory(self):
        """Parse collection based on filetype."""

        parser = None
        if self._filetype == Const.CONTENT_FORMAT_TEXT:
            parser = Text(self._timestamp, self._text)
        elif self._filetype == Const.CONTENT_FORMAT_MKDN:
            parser = Mkdn(self._timestamp, self._text)

        return parser
