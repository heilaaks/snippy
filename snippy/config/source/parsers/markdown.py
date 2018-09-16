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

"""base: Parse content from Markdown templates."""

import re

from snippy.config.source.parsers.base import ContentParserBase
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger


class ContentParserMarkdown(ContentParserBase):
    """Parse content from Markdown templates."""

    # Example 1: Capture optional comment and mandatory command.
    #
    #            - Remove all exited containers
    #
    #              `$ docker rm $(docker ps --all -q -f status=exited)`
    REGEXP = {}
    REGEXP['data'] = {}
    REGEXP['data'][Const.SNIPPET] = re.compile(
        r"""(
        (?:-\s+.*$\n\s*\n)?     # Catch one line optional comment followed by one empty line.
        \s.*`\$.*`              # Catch one line mandatory command indicated by dollar sign between grave accents (`).
        )
        {1}                     # Catch only one optional command and mandatory command.
        """, re.MULTILINE | re.VERBOSE)
    REGEXP['data'][Const.SOLUTION] = re.compile(
        r"""
        (?P<data>.*)            # All the content is data.
        """, re.DOTALL | re.VERBOSE)
    REGEXP['data'][Const.REFERENCE] = re.compile(r'\A(?!x)x')  # Never match anything because there is no data in the content.

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
        contents = self._text.split('---')
        for content in contents:
            category = self._read_category(content)
            resource = collection.get_resource(category, self._timestamp)
            resource.data = self._read_data(category, content)
            #resource.brief = self._read_brief(category, content)
            #resource.groups = self._read_groups(category, content)
            #resource.tags = self._read_tags(category, content)
            #resource.links = self._read_links(category, content)
            #resource.category = category
            #resource.filename = self._read_filename(category, content)
            #resource.digest = resource.compute_digest()
            collection.migrate(resource)

        return collection

    def _read_category(self, text):
        """Read content category from text string.

        Returns:
            str: Content category.
        """

        category = Const.UNKNOWN_CATEGORY
        match = re.compile(r'> category : (?P<category>.*|$)').search(text)
        if match:
            category = self.value(match.group('category'))
            self._logger.debug('parsed content category: %s', category)
        else:
            self._logger.debug('parser did not find content category')

        if category not in Const.CATEGORIES:
            self._logger.debug('parser read invalid category: %s', category)
            category = Const.UNKNOWN_CATEGORY

        return category

    def _read_data(self, category, text):
        """Read content data from text string.

        Each content data line is stored in element in a tuple. Solution
        content data is stored only by trimming the trailing newlines at the
        end of the data. In case of snippet content, each line is trimmed.

        References do not have data field. In case of references, the links
        are considered as a data.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded content data.
        """

        data = ()
        if category not in Const.CATEGORIES or category == Const.REFERENCE:
            return data

        # (>\s{1}.*?)\n\s*\n(>\s{1}.*?)\n\s*\n(.*)#\sMeta
        match = self.REGEXP['data'][category].findall(text)
        if match:
            if category == Const.SNIPPET:
                data = self._snippet_data(match)
            elif category == Const.SOLUTION:
                data = self.data(category, match[0])
            self._logger.debug('parsed content data: %s', data)
        else:
            self._logger.debug('parser did not find content for data: %s', text)

        return data

    def _snippet_data(self, text):
        """Parse snippet data from Markdown formatted string."""

        data = Const.EMPTY
        for command in text:
            match = re.compile(r"""(?:
                -\s+                            # Match hyphen and spaces before comment
                (?P<comment>.*$)\n\s*\n)?       # Catch optional one line comment and skip one empty line before command.
                \s+                             # Match spaces in the beginning of the line which has the command.
                `\$\s(?P<command>.*)`           # Catch one line command indicated by dollar sign between grave accents (`).
                """, re.MULTILINE | re.VERBOSE).search(command)
            if match:
                if match.group('comment'):
                    data = data + match.group('command') + ' # ' + match.group('comment') + Const.NEWLINE
                else:
                    data = data + match.group('command') + Const.NEWLINE
                self._logger.debug('parsed snippet data: %s', data)
            else:
                self._logger.debug('parser did not find snippet data data: %s', command)
        data = self.data(Const.SNIPPET, data)

        return data
