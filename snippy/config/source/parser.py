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

import re
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger


class Parser(object):
    """Parse configuration source parameters."""

    _logger = Logger(__name__).get()

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
            string_ = Const.NEWLINE.join([x.strip() for x in value])  # Enforce only one newline at the end.
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
