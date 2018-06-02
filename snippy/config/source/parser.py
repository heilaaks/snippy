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

"""parser: Parse configuration source parameters."""

import re

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger


class Parser(object):
    """Parse configuration source parameters."""

    SOLUTION_BRIEF = '## BRIEF :'
    SOLUTION_DATE = '## DATE  :'
    DATA_HEAD = '# Add mandatory snippet below.\n'
    DATA_TAIL = '# Add optional brief description below.\n'
    BRIEF_HEAD = '# Add optional brief description below.\n'
    BRIEF_TAIL = '# Add optional single group below.\n'
    GROUP_HEAD = '# Add optional single group below.\n'
    GROUP_TAIL = '# Add optional comma separated list of tags below.\n'
    TAGS_HEAD = '# Add optional comma separated list of tags below.\n'
    TAGS_TAIL = '# Add optional links below one link per line.\n'
    LINKS_HEAD = '# Add optional links below one link per line.\n'
    LINKS_TAIL = '.'

    _logger = Logger.get_logger(__name__)

    @staticmethod
    def read_content(timestamp, source):
        """Read contents from text source."""

        data = []
        category = Parser.content_category(source)
        if category == Const.SNIPPET:
            data = Parser._split_source(source, '# Add mandatory snippet below', 2)
        elif category == Const.SOLUTION:
            data = Parser._split_source(source, '## BRIEF :', 1)
        else:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not identify text template content category')

        collection = Collection()
        for item in data:
            resource = collection.get_resource(category, timestamp)
            resource.data = Parser.content_data(category, item)
            resource.brief = Parser.content_brief(category, item)
            resource.group = Parser.content_group(category, item)
            resource.tags = Parser.content_tags(category, item)
            resource.links = Parser.content_links(category, item)
            resource.category = category
            resource.filename = Parser.content_filename(category, item)
            resource.digest = resource.compute_digest()
            collection.migrate(resource)

        return collection

    @staticmethod
    def _split_source(source, split, offset):
        """Split solution content from a text file."""

        # Find line numbers that are identified by split tag and offset. The matching
        # line numbers are substracted with offset to get the first line of the solution.
        # The first item from the list is popped and used as a head and following items
        # are treated as as line numbers where the next solution starts.
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
        """Read content category from text source."""

        category = Const.UNKNOWN_CONTENT

        if cls.DATA_HEAD in source and cls.BRIEF_HEAD:
            category = Const.SNIPPET
        elif cls.SOLUTION_BRIEF in source and cls.SOLUTION_DATE:
            category = Const.SOLUTION

        return category

    @classmethod
    def content_data(cls, category, source):
        """Read content data from text source."""

        data = ()
        if category == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (cls.DATA_HEAD, cls.DATA_TAIL), source, re.DOTALL)
            if match and not match.group(1).isspace():
                data = tuple([s.strip() for s in match.group(1).rstrip().split(Const.NEWLINE)])
        else:
            # Remove unnecessary newlines at the end and make sure there is one at the end.
            data = tuple(source.rstrip().split(Const.NEWLINE) + [Const.EMPTY])
        cls._logger.debug('parsed content data from "%s"', data)

        return data

    @classmethod
    def content_brief(cls, category, source):
        """Read content brief from text source."""

        brief = Const.EMPTY
        if category == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (cls.BRIEF_HEAD, cls.BRIEF_TAIL), source, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple([s.strip() for s in match.group(1).rstrip().split(Const.SPACE)])
                brief = Const.SPACE.join(lines)
        else:
            match = re.search(r'## BRIEF :\s*?(.*|$)', source, re.MULTILINE)
            if match:
                brief = match.group(1).strip()
        cls._logger.debug('parsed content brief from "%s"', brief)

        return brief

    @classmethod
    def content_group(cls, category, source):
        """Read content group from text source."""

        group = Const.EMPTY
        if category == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (cls.GROUP_HEAD, cls.GROUP_TAIL), source, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple([s.strip() for s in match.group(1).rstrip().split(Const.SPACE)])
                group = Const.SPACE.join(lines)
        else:
            match = re.search(r'## GROUP :\s*?(\S+|$)', source, re.MULTILINE)
            if match:
                group = match.group(1).strip()
        cls._logger.debug('parsed content group from "%s"', group)

        return group

    @classmethod
    def content_tags(cls, category, source):
        """Read content tags from text source."""

        tags = ()
        if category == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (cls.TAGS_HEAD, cls.TAGS_TAIL), source, re.DOTALL)
            if match and not match.group(1).isspace():
                tags = Parser.keywords([match.group(1)])
        else:
            match = re.search(r'## TAGS  :\s*?(.*|$)', source, re.MULTILINE)
            if match:
                tags = tuple([s.strip() for s in match.group(1).rstrip().split(Const.DELIMITER_TAGS)])
        cls._logger.debug('parsed content tags from "%s"', tags)

        return tags

    @classmethod
    def content_links(cls, category, source):
        """Read content links from text source."""

        # In case of solution, the links are read from the whole content data.
        links = ()
        if category == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (cls.LINKS_HEAD, cls.LINKS_TAIL), source, re.DOTALL)
            if match and not match.group(1).isspace():
                links = tuple([s.strip() for s in match.group(1).rstrip().split(Const.NEWLINE)])
        else:
            links = tuple(re.findall('> (http.*)', source))
        cls._logger.debug('parsed content links from "%s"', links)

        return links

    @classmethod
    def content_filename(cls, category, source):
        """Read content filename from text source."""

        # Only solution content uses optional filename field.
        filename = Const.EMPTY
        if category == Const.SOLUTION:
            match = re.search(r'## FILE  :\s*?(\S+|$)', source, re.MULTILINE)
            if match and match.group(1):
                filename = match.group(1)
        cls._logger.debug('parsed content filename from "%s"', filename)

        return filename

    @staticmethod
    def keywords(keywords, sort_=True):
        """Convert keywords to utf-8 encoded list of keywords.

        Parse user provided keyword list. The keywords are tags or search
        keywords. User may use various formats so each item in a list may be
        for example a string of comma separated tags.

        The dot is a special case. It is allowed for the regexp to match and
        print all records."""

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t dockertesting', container-managemenet', cleanup_testing
        #           6. --sall '.'
        list_ = []
        keywords = Parser._to_list(keywords)
        for tag in keywords:
            list_ = list_ + re.findall(r"[\w\-\.]+", tag)

        if sort_:
            list_ = sorted(list_)

        return tuple(list_)


    @classmethod
    def search_keywords(cls, value):
        """Convert keywords to utf-8 encoded search keywords."""

        # The keyword list may be empty or it can contain empty string.
        # Both cases must be evaluated to 'match any'.
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
    def links(links):
        """Convert links to utf-8 encoded list of links.


        Parse user provided link list. Because URL and keyword have different
        forbidden characters, the methods to parse keywords are simular but still
        they are separated. URLs can be separated only with space and bar. These
        are defined 'unsafe characters' in URL character set /1/.

        /1/ https://perishablepress.com/stop-using-unsafe-characters-in-urls/"""

        # Examples: Support processing of:
        #           1. -l link1    link2
        #           2. -l link1| link2| link3
        #           3. -l link1|link2|link3
        #           4. -l 'link1 link2 link3'
        #           5. -l 'link1| link2| link3'
        #           6. -l 'link1|link2|link3'
        #           7. -l '.'
        list_ = []
        links = Parser._to_list(links)
        for link in links:
            list_ = list_ + re.split(r'\s+|\|', link)
        sorted_list = sorted(list_)

        return tuple(sorted_list)

    @classmethod
    def to_unicode(cls, value):
        """Convert value to utf-8 coded unicode string.

        Conversion quarantees only one newline at the end of the string.
        """

        string_ = Const.EMPTY
        if isinstance(value, Const.TEXT_TYPE):
            string_ = value
        elif isinstance(value, Const.BINARY_TYPE):
            string_ = value.decode('utf-8')
        elif isinstance(value, (list, tuple)):
            string_ = Const.NEWLINE.join([Parser.to_unicode(x.rstrip()) for x in value])  # Enforce only one newline at the end.
        else:
            cls._logger.debug('conversion to unicode string failed with unknown type %s : %s', type(value), value)

        return string_

    @classmethod
    def _to_list(cls, value):
        """Return list of UTF-8 encoded unicode strings."""

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
