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

"""parser.py: Parse configuration source parameters."""

import copy
import datetime
import re
from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger


class Parser(object):
    """Parse configuration source parameters."""

    _logger = Logger(__name__).get()

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

    @staticmethod
    def read_content(content, source, timestamp):
        """Read content from text source."""

        data = []
        contents = []
        category = Parser.content_category(source)
        if category == Const.SNIPPET:
            data = Parser._split_source(source, '# Add mandatory snippet below', 2)
        elif category == Const.SOLUTION:
            data = Parser._split_source(source, '## BRIEF :', 1)
        else:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'could not identify text template content category')

        # Initialize time from 1) Content() or from 2) time given by caller.
        # These are always needed because it can be that user did not set
        # the date correctly to ISO8601 format in the text input.
        if content.get_utc():
            timestamp = content.get_utc()
        for item in data:
            content_copy = copy.copy(content)
            content_copy.set((Parser.content_data(category, item),
                              Parser.content_brief(category, item),
                              Parser.content_group(category, item),
                              Parser.content_tags(category, item),
                              Parser.content_links(category, item),
                              category,
                              Parser.content_filename(category, item),
                              content_copy.get_runalias(),
                              content_copy.get_versions(),
                              Parser.content_date(category, item, timestamp),
                              content_copy.get_digest(),
                              content_copy.get_metadata(),
                              content_copy.get_key()))
            content_copy.update_digest()
            if content_copy.is_template(edited=item):
                Cause.push(Cause.HTTP_BAD_REQUEST, 'no content was stored because it matched to empty template')

            contents.append(content_copy)

        return contents

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
                lines = tuple([s.strip() for s in match.group(1).rstrip().split(Const.DELIMITER_SPACE)])
                brief = Const.DELIMITER_SPACE.join(lines)
        else:
            match = re.search(r'## BRIEF :\s*?(.*|$)', source, re.MULTILINE)
            if match:
                brief = match.group(1).strip()
        cls._logger.debug('parsed content brief from "%s"', brief)

        return brief

    @classmethod
    def content_date(cls, category, source, timestamp):
        """Read content date from text source."""

        date = timestamp
        if category == Const.SOLUTION:
            match = re.search(r'## DATE  :\s*?(.*|$)', source, re.MULTILINE)
            if match:
                try:
                    datetime.datetime.strptime(match.group(1).strip(), '%Y-%m-%d %H:%M:%S')
                    date = match.group(1).strip()
                except ValueError:
                    cls._logger.info('incorrect date and time format "%s"', match.group(1))

        cls._logger.debug('parsed content date from "%s"', date)

        return date

    @classmethod
    def content_group(cls, category, source):
        """Read content group from text source."""

        group = Const.EMPTY
        if category == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (cls.GROUP_HEAD, cls.GROUP_TAIL), source, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple([s.strip() for s in match.group(1).rstrip().split(Const.DELIMITER_SPACE)])
                group = Const.DELIMITER_SPACE.join(lines)
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
        """Parse user provided keyword list. The keywords are tags or search
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

    @staticmethod
    def links(links):
        """Parse user provided link list. Because URL and keyword have different
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
    def search_keywords(cls, value):
        """Convert value to list of search keywrods."""

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

    @classmethod
    def to_string(cls, value):
        """Return value as string by joining list items with newlines."""

        string_ = Const.EMPTY
        value = Parser._six_string(value)
        if isinstance(value, str):
            string_ = value
        elif isinstance(value, (list, tuple)):
            string_ = Const.NEWLINE.join([x.rstrip() for x in value])  # Enforce only one newline at the end.
        else:
            cls._logger.debug('source value conversion to string skipped in normal condition %s : %s', type(value), value)

        cls._logger.debug('testing')

        return string_

    @classmethod
    def _to_list(cls, value):
        """Return option as list of items."""

        list_ = []
        value = Parser._six_string(value)
        if isinstance(value, str):
            list_.append(value)
        elif isinstance(value, (list, tuple)):
            list_ = list(value)
        else:
            cls._logger.debug('source value conversion to list skipped in normal condition: %s : %s', type(value), value)

        return list_

    @staticmethod
    def _six_string(parameter):
        """Take care of converting Python 2 unicode string to str."""

        # In Python 2 a string can be str or unicode but in Python 3 strings
        # are always unicode strings. This makes sure that a string is always
        # str for Python 2 and python 3.
        if Const.PYTHON2 and isinstance(parameter, unicode):  # noqa: F821 # pylint: disable=undefined-variable
            parameter = parameter.encode('utf-8')

        return parameter
