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

"""parser.py: Parse config source parameters."""

import re


class Parser(object):
    """Parse configuration source parameters."""

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
        #           1. -l link1 link2
        #           2. -l link1| link2| link3
        #           3. -l link1|link2|link3
        #           4. -l 'link1 link2 link3'
        #           5. -l 'link1| link2| link3'
        #           6. -l 'link1|link2|link3'
        #           7. -l '.'
        list_ = []
        for link in links:
            list_ = list_ + re.split(r'\s+|\|', link)
        sorted_list = sorted(list_)

        return tuple(sorted_list)
