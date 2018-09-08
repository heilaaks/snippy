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

"""parser: Parse content attributes from text source."""

import re

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger


class Parser(object):
    """Parse content attributes from text source."""

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
    def read_content(timestamp, source):
        """Read contents from text source.

        Args:
            timestamp (str): UTC time stamp in ISO8601 format.
            source (str): Contents text source.

        Returns:
            Collection(): Parsed content in Collection.
        """

        data = []
        category = Parser.content_category(source)
        if category == Const.SNIPPET:
            data = Parser._split_source(source, '# Add mandatory snippet below', 2)
        elif category == Const.SOLUTION:
            data = Parser._split_source(source, Parser.BRIEF[Const.SOLUTION], 1)
        elif category == Const.REFERENCE:
            data = Parser._split_source(source, '# Add mandatory links below one link per line', 2)
        else:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not identify text template content category')

        collection = Collection()
        for item in data:
            resource = collection.get_resource(category, timestamp)
            resource.data = Parser.content_data(category, item)
            resource.brief = Parser.content_brief(category, item)
            resource.groups = Parser.content_groups(category, item)
            resource.tags = Parser.content_tags(category, item)
            resource.links = Parser.content_links(category, item)
            resource.category = category
            resource.filename = Parser.content_filename(category, item)
            resource.digest = resource.compute_digest()
            collection.migrate(resource)

        return collection

    @staticmethod
    def _split_source(source, split, offset):
        """Split text to multiple contents.

        This method parses text files to extract multiple contents from it.

        Find line numbers that are identified by split tag and offset. The
        matching line numbers are substracted with offset to get the first
        line of the content. The first item from the list is popped and
        used as a head and following items are treated as as line numbers
        where the next solution starts.

        Args:
            source (str): Contents text source.
            split (str): Tag in text content that identifies each content
            offset (int): Offset from head of the text content for split tag.

        Returns:
            list: List of text contents.
        """

        source_list = source.split(Const.NEWLINE)
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
    def content_category(cls, source):
        """Read content category from text source.

        Args:
            source (str): Content text source.

        Returns:
            str: Content category.
        """

        category = Const.UNKNOWN_CATEGORY

        if cls.DATA[Const.SNIPPET] in source and cls.BRIEF[Const.SNIPPET]:
            category = Const.SNIPPET
        elif cls.BRIEF[Const.SOLUTION] in source and cls.FILENAME[Const.SOLUTION] in source:
            category = Const.SOLUTION
        elif cls.LINKS[Const.REFERENCE] in source:
            category = Const.REFERENCE

        return category

    @classmethod
    def content_data(cls, category, source):
        """Read content data from text source.

        Each content data line is stored in element in a tuple. Solution
        content data is stored only by trimming the trailing newlines at the
        end of the data. In case of snippet content, each line is trimmed.

        Args:
            category (str): Content category.
            source (str): Content text source.

        Returns:
            tuple: Tuple of utf-8 encoded content data.
        """

        data = ()
        if category not in Const.CATEGORIES:
            return data

        match = Parser.REGEXP['data'][category].search(source)
        if match:
            data = Parser.data(category, match.group(1))
            if category == Const.REFERENCE:
                data = ()  # There is no data with reference content.
            cls._logger.debug('parsed content data: %s', data)
        else:
            cls._logger.debug('parser did not find content for data')

        return data

    @classmethod
    def content_brief(cls, category, source):
        """Read content brief from text source.

        Args:
            category (str): Content category.
            source (str): Content text source.

        Returns:
            str: Utf-8 encoded unicode brief string.
        """

        brief = ''
        if category not in Const.CATEGORIES:
            return brief

        match = Parser.REGEXP['brief'][category].search(source)
        if match:
            brief = Parser.value(match.group('brief'))
            cls._logger.debug('parsed content brief: %s', brief)
        else:
            cls._logger.debug('parser did not find content for brief')

        return brief

    @classmethod
    def content_groups(cls, category, source):
        """Read content groups from text source.

        Args:
            category (str): Content category.
            source (str): Content text source.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        groups = ()
        if category not in Const.CATEGORIES:
            return groups

        match = Parser.REGEXP['groups'][category].search(source)
        if match:
            groups = Parser.keywords([match.group('groups')])
            cls._logger.debug('parsed content groups: %s', groups)
        else:
            cls._logger.debug('parser did not find content for groups')

        return groups

    @classmethod
    def content_tags(cls, category, source):
        """Read content tags from text source.

        Args:
            category (str): Content category.
            source (str): Content text source.

        Returns:
            tuple: Tuple of utf-8 encoded tags.
        """

        tags = ()
        if category not in Const.CATEGORIES:
            return tags

        match = Parser.REGEXP['tags'][category].search(source)
        if match:
            tags = Parser.keywords([match.group('tags')])
            cls._logger.debug('parsed content tags: %s', tags)
        else:
            cls._logger.debug('parser did not find content for tags')

        return tags

    @classmethod
    def content_links(cls, category, source):
        """Read content links from text source.

        Args:
            category (str): Content category.
            source (str): Content text source.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        links = ()
        if category not in Const.CATEGORIES:
            return links

        match = Parser.REGEXP['links'][category].findall(source)
        if match:
            links = Parser.links(match)
            cls._logger.debug('parsed content links: %s', links)
        else:
            cls._logger.debug('parser did not find content for links')

        return links

    @classmethod
    def content_filename(cls, category, source):
        """Read content filename from text source.

        Args:
            category (str): Content category.
            source (str): Content text source.

        Returns:
            str: Utf-8 encoded unicode filename string.
        """

        filename = ''
        if category not in Const.CATEGORIES:
            return filename

        match = Parser.REGEXP['filename'][category].search(source)
        if match:
            filename = Parser.value(match.group('filename'))
            cls._logger.debug('parsed content filename: %s', filename)
        else:
            cls._logger.debug('parser did not find content for filename')

        return filename

    @staticmethod
    def data(category, value):
        """Convert content data to utf-8 encoded tuple of lines.

        Content data is stored as a tuple with one line per element.

        Solutions are trimmed only from end of the whole solution string but
        snippets and references from both sides of each line. Solutions are
        quaranteed to have one newline at the end of solution.

        Any value including empty string is considered valid data.

        Args:
            value (str,list): Content data in string or list.

        Returns:
            tuple: Tuple of utf-8 encoded unicode strings.
        """

        data = Parser.to_unicode(value)
        if category in [Const.SNIPPET, Const.REFERENCE]:
            data = [s.strip() for s in data.rstrip().split(Const.DELIMITER_DATA)]
        elif category == Const.SOLUTION:
            data = data.rstrip().split(Const.NEWLINE) + [Const.EMPTY]

        return tuple(data)

    @staticmethod
    def value(value):
        """Convert content string value to utf-8 encoded string.

        Args:
            value (str,list,tuple): Content field value in string, list or tuple.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        value = Parser.to_unicode(value).strip()

        return value

    @classmethod
    def search_keywords(cls, value):
        """Convert search keywords to utf-8 encoded tuple.

        If the value is None it indicates that the search keywords were not
        given at all.

        The keyword list may be empty or it can contain empty string. Both
        cases must be evaluated to 'match any'.

        Args:
            value (str,list,tuple): Search keywords in string, list or tuple.

        Returns:
            tuple: Tuple of utf-8 encoded keywords.
        """

        keywords = ()
        if value is not None:
            keywords = Parser.keywords(value)
            if not any(keywords):
                cls._logger.debug('all content listed because keywords were not provided')
                keywords = ('.')
        else:
            keywords = ()

        return keywords

    @staticmethod
    def keywords(keywords, sort_=True):
        """Convert list of keywords to utf-8 encoded list of strings.

        Parse user provided keyword list. The keywords are for example groups,
        tags or search all keywords. User may use string or list context for
        the keywords. In case of list context for the keywords, each element
        in the list is split separately.

        The keywords are split in word boundary.

        The dot is a special case. It is allowed for the regexp to match and
        print all records.

        Args:
            keywords (str,list,tuple): Keywords in string, list or tuple.

        Returns:
            tuple: Tuple of utf-8 encoded keywords.
        """

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t docker–testing', container-managemenet', cleanup_testing
        #           6. --sall '.'
        list_ = []
        keywords = Parser._to_list(keywords)
        for tag in keywords:
            list_ = list_ + re.findall(u'[\\w–\\-\\.]+', tag, flags=re.UNICODE)  # Python 2 and 3 compatible unicode regexp.

        if sort_:
            list_ = sorted(list_)

        return tuple(list_)

    @staticmethod
    def links(links):
        """Convert links to utf-8 encoded list of links.

        Parse user provided link list. Because URL and keyword have different
        forbidden characters, the methods to parse keywords are similar but
        still they are separated. URLs can be separated only with space, bar
        or newline. Space and bar characters are defined 'unsafe characters'
        in URL character set [1]. The newline is always URL encoded so it does
        not appear as newline.

        The newline is supported here because that is used to separate links
        in text input.

        Links are not sorted. The reason is that the sort is done based on
        content category. The content category is not know for sure when
        command options are parsed in this class. For this reason, the sort
        is always made later in the Resource when content category is known
        for sure.

        [1] https://perishablepress.com/stop-using-unsafe-characters-in-urls/

        Args:
            links (str,list,tuple): Links in string, list or tuple.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        # Examples: Support processing of:
        #           1. -l link1    link2
        #           2. -l link1| link2| link3
        #           3. -l link1|link2|link3
        #           4. -l 'link1 link2 link3'
        #           5. -l 'link1| link2| link3'
        #           6. -l 'link1|link2|link3'
        #           7. -l '.'
        #           7. -l 'link1\nlink2'
        list_ = []
        links = Parser._to_list(links)
        for link in links:
            list_ = list_ + re.split(r'\s+|\|', link)
        list_ = list(filter(None, list_))

        return tuple(list_)

    @classmethod
    def to_unicode(cls, value):
        """Convert value to utf-8 coded unicode string.

        If the value is already unicode character, the tool always assumes
        utf-8 encoded unicode characters.

        Conversion quarantees only one newline at the end of the string.

        Args:
            value (str,list,tuple): Value in string, list or tuple.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        string_ = Const.EMPTY
        if isinstance(value, Const.TEXT_TYPE):
            string_ = value  # Already in unicode format.
        elif isinstance(value, Const.BINARY_TYPE):
            string_ = value.decode('utf-8')
        elif isinstance(value, (list, tuple)):
            string_ = Const.NEWLINE.join([Parser.to_unicode(x.rstrip()) for x in value])  # Enforce only one newline at the end.
        else:
            cls._logger.debug('conversion to unicode string failed with unknown type %s : %s', type(value), value)

        return string_

    @classmethod
    def _to_list(cls, value):
        """Return list of UTF-8 encoded unicode strings.

        Args:
            value (str,list,tuple): Value in string, list or tuple.

        Returns:
            list: List of Utf-8 encoded unicode strings.
        """

        list_ = []
        if isinstance(value, Const.TEXT_TYPE):
            list_.append(value)
        elif isinstance(value, Const.BINARY_TYPE):
            list_.append(value.decode('utf-8'))
        elif isinstance(value, (list, tuple)):
            list_ = list([Parser.to_unicode(i) for i in value])
        else:
            cls._logger.debug('conversion to list of unicode unicode strings failed with unknown type %s : %s', type(value), value)

        return list_
