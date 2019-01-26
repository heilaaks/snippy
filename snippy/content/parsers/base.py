#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""base: Base class for text content parsers."""

import re

from snippy.constants import Constants as Const
from snippy.logger import Logger


class ContentParserBase(object):
    """Base class for text content parser."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def format_data(cls, category, value):
        """Convert content data to utf-8 encoded tuple of lines.

        Content data is stored as a tuple with one line per element.

        All but solution data is trimmed from right for every line. In case
        of solution data, it is considered that user wants to leave it as is.
        Solutions are trimmed only so that there will be only one newline at
        the end of the solution data.

        Any value including empty string is considered as a valid data.

        Args:
            category (str): Content category.
            value (str,list): Content data in string or list.

        Returns:
            tuple: Tuple of utf-8 encoded unicode strings.
        """

        data = ()
        if category in [Const.SNIPPET, Const.REFERENCE]:
            data = cls.to_unicode(value).rstrip().split(Const.DELIMITER_DATA)
        elif category == Const.SOLUTION:
            data = cls.to_unicode(value, strip_lines=False)
            data = data.rstrip('\r\n').split(Const.NEWLINE) + [Const.EMPTY]

        return tuple(data)

    @classmethod
    def format_string(cls, value):
        """Convert content string value to utf-8 encoded string.

        Args:
            value (str,list,tuple): Content field value in string, list or tuple.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        value = cls.to_unicode(value).strip()

        return value

    @classmethod
    def format_search_keywords(cls, value):
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
            keywords = cls.format_list(value)
            if not any(keywords):
                cls._logger.debug('all content listed because keywords were not provided')
                keywords = ('.')
        else:
            keywords = ()

        return keywords

    @classmethod
    def format_list(cls, keywords, sort_=True):
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
            sort_ (bool): Define if keywords are sorted or not.

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
        #           6. kafka=1.0.0 '.'
        list_ = []
        keywords = cls._to_list(keywords)
        for tag in keywords:
            list_ = list_ + re.findall(u'''
                [\\w–\\-\\.\\=]+   # Python 2 and 3 compatible unicode regexp.
                ''', tag, re.UNICODE | re.VERBOSE)

        if sort_:
            list_ = sorted(list_)

        return tuple(list_)

    @classmethod
    def format_links(cls, links):
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
        links = cls._to_list(links)
        for link in links:
            list_ = list_ + re.split(r'\s+|\|', link)
        list_ = list(filter(None, list_))

        return tuple(list_)

    @classmethod
    def parse_links(cls, category, regexp, text):
        """Parse content links from text string.

        Args:
            category (str): Content category.
            regexp (re): Compiled regexp to search links.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        links = ()
        if category not in Const.CATEGORIES:
            return links

        match = regexp.findall(text)
        if match:
            links = cls.format_links(match)
            cls._logger.debug('parsed content links: %s', links)
        else:
            cls._logger.debug('parser did not find content for links')

        return links

    @classmethod
    def parse_groups(cls, category, regexp, text):
        """Parse content groups from text string.

        Args:
            category (str): Content category.
            regexp (re): Compiled regexp to search groups.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        groups = ()
        if category not in Const.CATEGORIES:
            return groups

        match = regexp.search(text)
        if match:
            groups = cls.format_list([match.group('groups')])
            cls._logger.debug('parsed content groups: %s', groups)
        else:
            cls._logger.debug('parser did not find content for groups')

        return groups

    @classmethod
    def to_unicode(cls, value, strip_lines=True):
        """Convert value to utf-8 coded unicode string.

        If the value is already an unicode character, it is assumed that it is
        a valid utf-8 encoded unicode character.

        The conversion quarantees one newline at the end of string.

        Args:
            value (str,list,tuple): Value in a string, list or tuple.
            strip_lines (bool): Defines if all lines are stripped.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        string_ = Const.EMPTY
        if isinstance(value, Const.TEXT_TYPE):
            string_ = value  # Already in unicode format.
        elif isinstance(value, Const.BINARY_TYPE):
            string_ = value.decode('utf-8')
        elif isinstance(value, (list, tuple)):
            if strip_lines:
                string_ = Const.NEWLINE.join([cls.to_unicode(line.strip()) for line in value])
            else:
                string_ = Const.NEWLINE.join([cls.to_unicode(line) for line in value])
        elif isinstance(value, type(None)):
            string_ = Const.EMPTY
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
            list_ = list([cls.to_unicode(i) for i in value])
        elif isinstance(value, type(None)):
            list_ = []
        else:
            cls._logger.debug('conversion to list of unicode unicode strings failed with unknown type %s : %s', type(value), value)

        return list_
