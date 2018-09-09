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
from snippy.logger import Logger


class ContentParserText(ContentParserBase):
    """Parse content from text templates."""

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
    REGEXP['data'][Const.SNIPPET] = re.compile(
        r'(?:%s|%s)(?P<data>.*?)(?:\n{2}|#|$)' % (
            DATA[Const.SNIPPET],
            DATA[Const.REFERENCE]
        ),
        re.DOTALL
    )
    REGEXP['data'][Const.REFERENCE] = REGEXP['data'][Const.SNIPPET]
    REGEXP['data'][Const.SOLUTION] = re.compile(r'(?P<data>.*)', re.DOTALL)
    REGEXP['brief'] = {}
    REGEXP['brief'][Const.SNIPPET] = re.compile(
        r'(?:%s|%s)(?P<brief>.*?)(?:\n{2}|#|$)' % (
            BRIEF[Const.SNIPPET],
            BRIEF[Const.REFERENCE]
        ),
        re.DOTALL
    )
    REGEXP['brief'][Const.REFERENCE] = REGEXP['brief'][Const.SNIPPET]
    REGEXP['brief'][Const.SOLUTION] = re.compile(r'%s\s*?(?P<brief>.*|$)' % BRIEF[Const.SOLUTION], re.MULTILINE)
    REGEXP['groups'] = {}
    REGEXP['groups'][Const.SNIPPET] = re.compile(
        r'(?:%s|%s)(?P<groups>.*?)(?:\n{2}|#|$)' % (
            GROUPS[Const.SNIPPET],
            GROUPS[Const.REFERENCE]
        ),
        re.DOTALL
    )
    REGEXP['groups'][Const.REFERENCE] = REGEXP['groups'][Const.SNIPPET]
    REGEXP['groups'][Const.SOLUTION] = re.compile(r'%s\s*?(?P<groups>.*|$)' % GROUPS[Const.SOLUTION], re.MULTILINE)
    REGEXP['tags'] = {}
    REGEXP['tags'][Const.SNIPPET] = re.compile(
        r'(?:%s|%s)(?P<tags>.*?)(?:\n{2}|#|$)' % (
            TAGS[Const.SNIPPET],
            TAGS[Const.REFERENCE]
        ),
        re.DOTALL
    )
    REGEXP['tags'][Const.REFERENCE] = REGEXP['tags'][Const.SNIPPET]
    REGEXP['tags'][Const.SOLUTION] = re.compile(r'%s\s*?(?P<tags>.*|$)' % TAGS[Const.SOLUTION], re.MULTILINE)
    REGEXP['links'] = {}
    REGEXP['links'][Const.SNIPPET] = re.compile(
        r'(?:%s|%s)(?P<links>.*?)(?:\n{2}|#|$)' % (
            LINKS[Const.SNIPPET],
            LINKS[Const.REFERENCE]
        ),
        re.DOTALL
    )
    REGEXP['links'][Const.REFERENCE] = REGEXP['links'][Const.SNIPPET]
    REGEXP['links'][Const.SOLUTION] = re.compile(r'> (?P<links>http.*)', re.MULTILINE)
    REGEXP['filename'] = {}
    REGEXP['filename'][Const.SNIPPET] = re.compile(r'\A(?!x)x')  # Never match anything because there is no filename in content.
    REGEXP['filename'][Const.REFERENCE] = REGEXP['filename'][Const.SNIPPET]
    REGEXP['filename'][Const.SOLUTION] = re.compile(r'%s\s*?(?P<filename>.*|$)' % FILENAME[Const.SOLUTION], re.MULTILINE)

    _logger = Logger.get_logger(__name__)

    @staticmethod
    def get_contents(text, split, offset):
        """Split text to multiple contents.

        This method parses text files to extract multiple contents from it.

        Find line numbers that are identified by split tag and offset. The
        matching line numbers are substracted with offset to get the first
        line of the content. The first item from the list is popped and
        used as a head and following items are treated as as line numbers
        where the next solution starts.

        Args:
            text (str): Contents as a text string.
            split (str): Tag in text content that identifies each content
            offset (int): Offset from head of the text content for split tag.

        Returns:
            list: List of text contents.
        """

        source_list = text.split(Const.NEWLINE)
        solutions = []
        line_numbers = [i for i, line in enumerate(source_list) if line.startswith(split)]
        line_numbers[:] = [x-offset for x in line_numbers]
        if line_numbers:
            head = line_numbers.pop(0)
            for line in line_numbers:
                solutions.append(Const.NEWLINE.join(source_list[head:line]))
                head = line
            solutions.append(Const.NEWLINE.join(source_list[head:]))

        return solutions

    @classmethod
    def content_category(cls, text):
        """Read content category from text string.

        Args:
            text (str): Content text string.

        Returns:
            str: Content category.
        """

        category = Const.UNKNOWN_CATEGORY

        if cls.DATA[Const.SNIPPET] in text and cls.BRIEF[Const.SNIPPET]:
            category = Const.SNIPPET
        elif cls.BRIEF[Const.SOLUTION] in text and cls.FILENAME[Const.SOLUTION] in text:
            category = Const.SOLUTION
        elif cls.LINKS[Const.REFERENCE] in text:
            category = Const.REFERENCE

        return category

    @classmethod
    def content_data(cls, category, text):
        """Read content data from text string.

        Each content data line is stored in element in a tuple. Solution
        content data is stored only by trimming the trailing newlines at the
        end of the data. In case of snippet content, each line is trimmed.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded content data.
        """

        data = ()
        if category not in Const.CATEGORIES:
            return data

        match = cls.REGEXP['data'][category].search(text)
        if match:
            data = cls.data(category, match.group(1))
            if category == Const.REFERENCE:
                data = ()  # There is no data with reference content.
            cls._logger.debug('parsed content data: %s', data)
        else:
            cls._logger.debug('parser did not find content for data')

        return data

    @classmethod
    def content_brief(cls, category, text):
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

        match = cls.REGEXP['brief'][category].search(text)
        if match:
            brief = cls.value(match.group('brief'))
            cls._logger.debug('parsed content brief: %s', brief)
        else:
            cls._logger.debug('parser did not find content for brief')

        return brief

    @classmethod
    def content_groups(cls, category, text):
        """Read content groups from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        groups = ()
        if category not in Const.CATEGORIES:
            return groups

        match = cls.REGEXP['groups'][category].search(text)
        if match:
            groups = cls.keywords([match.group('groups')])
            cls._logger.debug('parsed content groups: %s', groups)
        else:
            cls._logger.debug('parser did not find content for groups')

        return groups

    @classmethod
    def content_tags(cls, category, text):
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

        match = cls.REGEXP['tags'][category].search(text)
        if match:
            tags = cls.keywords([match.group('tags')])
            cls._logger.debug('parsed content tags: %s', tags)
        else:
            cls._logger.debug('parser did not find content for tags')

        return tags

    @classmethod
    def content_links(cls, category, text):
        """Read content links from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        links = ()
        if category not in Const.CATEGORIES:
            return links

        match = cls.REGEXP['links'][category].findall(text)
        if match:
            links = cls.links(match)
            cls._logger.debug('parsed content links: %s', links)
        else:
            cls._logger.debug('parser did not find content for links')

        return links

    @classmethod
    def content_filename(cls, category, text):
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

        match = cls.REGEXP['filename'][category].search(text)
        if match:
            filename = cls.value(match.group('filename'))
            cls._logger.debug('parsed content filename: %s', filename)
        else:
            cls._logger.debug('parser did not find content for filename')

        return filename
