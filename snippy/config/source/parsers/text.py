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

from snippy.cause import Cause
from snippy.config.source.parsers.base import ContentParserBase
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger


class ContentParserText(ContentParserBase):
    """Parse content from text template."""

    DATA = {}
    DATA[Const.SNIPPET] = '# Add mandatory snippet below.\n'
    DATA[Const.REFERENCE] = DATA[Const.SNIPPET]
    DATA[Const.SOLUTION] = '## BRIEF  :'

    BRIEF = {}
    BRIEF[Const.SNIPPET] = '# Add optional brief description below.\n'
    BRIEF[Const.REFERENCE] = BRIEF[Const.SNIPPET]
    BRIEF[Const.SOLUTION] = '## BRIEF  :'

    GROUPS = {}
    GROUPS[Const.SNIPPET] = '# Add optional comma separated list of groups below.\n'
    GROUPS[Const.REFERENCE] = GROUPS[Const.SNIPPET]
    GROUPS[Const.SOLUTION] = '## GROUPS :'

    TAGS = {}
    TAGS[Const.SNIPPET] = '# Add optional comma separated list of tags below.\n'
    TAGS[Const.REFERENCE] = TAGS[Const.SNIPPET]
    TAGS[Const.SOLUTION] = '## TAGS   :'

    LINKS = {}
    LINKS[Const.SNIPPET] = '# Add optional links below one link per line.\n'
    LINKS[Const.REFERENCE] = '# Add mandatory links below one link per line.\n'

    FILENAME = {}
    FILENAME[Const.SOLUTION] = '## FILE   :'

    REGEXP = {}
    REGEXP['data'] = {}
    REGEXP['data'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)           # Match snippet or reference data header.
        (?P<data>.*?)       # Catch data.
        (?:\n{2}|[#]|$)     # Match newlines or next header indicated by hash or end of the line.
        ''' % (re.escape(DATA[Const.SNIPPET]), re.escape(DATA[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['data'][Const.REFERENCE] = REGEXP['data'][Const.SNIPPET]
    REGEXP['data'][Const.SOLUTION] = re.compile(r'''
        (?P<data>.*)        # Catch all the content to data.
        ''', re.DOTALL | re.VERBOSE)

    REGEXP['brief'] = {}
    REGEXP['brief'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)           # Match snippet or reference brief header.
        (?P<brief>.*?)      # Catch brief.
        (?:\n{2}|[#]|$)     # Match newlines or next header indicated by hash or end of the line.
        ''' % (re.escape(BRIEF[Const.SNIPPET]), re.escape(BRIEF[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['brief'][Const.REFERENCE] = REGEXP['brief'][Const.SNIPPET]
    REGEXP['brief'][Const.SOLUTION] = re.compile(r'''
        %s\s*?              # Match solution brief header.
        (?P<brief>.*|$)     # Catch brief.
        ''' % re.escape(BRIEF[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    REGEXP['groups'] = {}
    REGEXP['groups'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)           # Match snippet or reference groups header.
        (?P<groups>.*?)     # Catch groups.
        (?:\n{2}|[#]|$)     # Match newlines or next header indicated by hash or end of the line.
        ''' % (re.escape(GROUPS[Const.SNIPPET]), re.escape(GROUPS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['groups'][Const.REFERENCE] = REGEXP['groups'][Const.SNIPPET]
    REGEXP['groups'][Const.SOLUTION] = re.compile(r'''
        %s\s*?              # Match groups tag from solution.
        (?P<groups>.*|$)    # Catch groups.
        ''' % re.escape(GROUPS[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    REGEXP['tags'] = {}
    REGEXP['tags'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)           # Match snippet or reference tags header.
        (?P<tags>.*?)       # Catch tags.
        (?:\n{2}|[#]|$)     # Match newlines or next header indicated by hash or end of the line.
        ''' % (re.escape(TAGS[Const.SNIPPET]), re.escape(TAGS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['tags'][Const.REFERENCE] = REGEXP['tags'][Const.SNIPPET]
    REGEXP['tags'][Const.SOLUTION] = re.compile(r'''
        %s\s*?              # Match tags tag from solution.
        (?P<tags>.*|$)      # Catch tags.
        ''' % re.escape(TAGS[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    REGEXP['links'] = {}
    REGEXP['links'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)           # Match snippet or reference links header.
        (?P<links>.*?)      # Catch links.
        (?:[\n]{2}|[#]|$)     # Match newlines or next header indicated by hash or end of the line.
        ''' % (re.escape(LINKS[Const.SNIPPET]), re.escape(LINKS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['links'][Const.REFERENCE] = REGEXP['links'][Const.SNIPPET]
    REGEXP['links'][Const.SOLUTION] = re.compile(r'''
        [> ]{2}             # Match fixed tag preceding all links in solution.
        (?P<links>http.*)   # Catch link.
        ''', re.MULTILINE | re.VERBOSE)

    REGEXP['filename'] = {}
    REGEXP['filename'][Const.SNIPPET] = re.compile(r'''
        \A(?!x)x            # Never match anything because there is no filename in the content.
        ''', re.VERBOSE)
    REGEXP['filename'][Const.REFERENCE] = REGEXP['filename'][Const.SNIPPET]
    REGEXP['filename'][Const.SOLUTION] = re.compile(r'''
        %s\s*?              # Match filename tag from solution.
        (?P<filename>.*|$)  # Catch filename.
        ''' % re.escape(FILENAME[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

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

    def _split_contents(self):
        """Split text to multiple contents.

        This method parses text string and extracts a list of text contents
        from it.

        All line numbers with content specific tag is searched. The tag is
        the first content field in the text template. The content is then
        split based on line numbers based on specific tag and the offset.
        The offset is substracted from the line number that had the content
        specific tag.

        Returns:
            list: List of text contents.
        """

        contents = []
        category = self._read_category(self._text)
        if category == Const.SNIPPET:
            offset = 2
            tag = '# Add mandatory snippet below'
        elif category == Const.SOLUTION:
            offset = 1
            tag = self.BRIEF[Const.SOLUTION]
        elif category == Const.REFERENCE:
            offset = 1
            tag = '# Add mandatory links below one link per line'
        else:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not identify text source content category: {}'.format(category))

            return contents

        lines = self._text.split(Const.NEWLINE)
        line_numbers = [i for i, line in enumerate(lines) if line.startswith(tag)]
        line_numbers[:] = [max(x-offset, 0) for x in line_numbers]
        if line_numbers:
            head = line_numbers.pop(0)
            for line in line_numbers:
                contents.append(Const.NEWLINE.join(lines[head:line]))
                head = line
            contents.append(Const.NEWLINE.join(lines[head:]))

        return contents

    def _read_category(self, text):
        """Read content category from text string.

        Returns:
            str: Content category.
        """

        category = Const.UNKNOWN_CATEGORY

        if self.DATA[Const.SNIPPET] in text and self.BRIEF[Const.SNIPPET]:
            category = Const.SNIPPET
        elif self.BRIEF[Const.SOLUTION] in text and self.FILENAME[Const.SOLUTION] in text:
            category = Const.SOLUTION
        elif self.LINKS[Const.REFERENCE] in text:
            category = Const.REFERENCE

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

        match = self.REGEXP['data'][category].search(text)
        if match:
            data = self.format_data(category, match.group(1))
            self._logger.debug('parsed content data: %s', data)
        else:
            self._logger.debug('parser did not find content for data')

        return data

    def _read_brief(self, category, text):
        """Read content brief from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode brief string.
        """

        brief = ''
        if category not in Const.CATEGORIES:
            return brief

        match = self.REGEXP['brief'][category].search(text)
        if match:
            brief = self.format_string(match.group('brief'))
            self._logger.debug('parsed content brief: %s', brief)
        else:
            self._logger.debug('parser did not find content for brief')

        return brief

    def _read_groups(self, category, text):
        """Read content groups from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        return ContentParserBase.parse_groups(category, self.REGEXP['groups'].get(category, None), text)

    def _read_tags(self, category, text):
        """Read content tags from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded tags.
        """

        tags = ()
        if category not in Const.CATEGORIES:
            return tags

        match = self.REGEXP['tags'][category].search(text)
        if match:
            tags = self.format_list([match.group('tags')])
            self._logger.debug('parsed content tags: %s', tags)
        else:
            self._logger.debug('parser did not find content for tags')

        return tags

    def _read_links(self, category, text):
        """Read content links from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        return ContentParserBase.parse_links(category, self.REGEXP['links'].get(category, None), text)

    def _read_filename(self, category, text):
        """Read content filename from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode filename string.
        """

        filename = ''
        if category not in Const.CATEGORIES:
            return filename

        match = self.REGEXP['filename'][category].search(text)
        if match:
            filename = self.format_string(match.group('filename'))
            self._logger.debug('parsed content filename: %s', filename)
        else:
            self._logger.debug('parser did not find content for filename')

        return filename
