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

"""base: Base class for text content parsers."""

import re

from snippy.constants import Constants as Const
from snippy.logger import Logger


class ContentParserBase(object):
    """Base class for text content parser."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def data(cls, category, value):
        """Convert content data to utf-8 encoded tuple of lines.

        Content data is stored as a tuple with one line per element.

        Solutions are trimmed only from end of the whole solution string but
        snippets and references from both sides of each line. Solutions are
        quaranteed to have one newline at the end of solution.

        Any value including empty string is considered valid data.

        Args:
            category (str): Content category.
            value (str,list): Content data in string or list.

        Returns:
            tuple: Tuple of utf-8 encoded unicode strings.
        """

        data = cls.to_unicode(value)
        if category in [Const.SNIPPET, Const.REFERENCE]:
            data = [s.strip() for s in data.rstrip().split(Const.DELIMITER_DATA)]
        elif category == Const.SOLUTION:
            data = data.rstrip().split(Const.NEWLINE) + [Const.EMPTY]

        return tuple(data)

    @classmethod
    def value(cls, value):
        """Convert content string value to utf-8 encoded string.

        Args:
            value (str,list,tuple): Content field value in string, list or tuple.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        value = cls.to_unicode(value).strip()

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
            keywords = cls.keywords(value)
            if not any(keywords):
                cls._logger.debug('all content listed because keywords were not provided')
                keywords = ('.')
        else:
            keywords = ()

        return keywords

    @classmethod
    def keywords(cls, keywords, sort_=True):
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
        list_ = []
        keywords = cls._to_list(keywords)
        for tag in keywords:
            list_ = list_ + re.findall(u'[\\w–\\-\\.]+', tag, flags=re.UNICODE)  # Python 2 and 3 compatible unicode regexp.

        if sort_:
            list_ = sorted(list_)

        return tuple(list_)

    @classmethod
    def links(cls, links):
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
            string_ = Const.NEWLINE.join([cls.to_unicode(x.rstrip()) for x in value])  # Enforce only one newline at the end.
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
        else:
            cls._logger.debug('conversion to list of unicode unicode strings failed with unknown type %s : %s', type(value), value)

        return list_
