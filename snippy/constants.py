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

"""constants: Globals constants for the tool."""

import re
import sys


class Constants(object):  # pylint: disable=too-few-public-methods
    """Globals constants."""

    SPACE = ' '
    EMPTY = ''
    COMMA = ','
    NEWLINE = '\n'

    # Python 2 and 3 compatibility.
    PYTHON2 = sys.version_info.major == 2
    if PYTHON2:
        TEXT_TYPE = unicode  # noqa pylint: disable=undefined-variable
        BINARY_TYPE = str
    else:
        TEXT_TYPE = str
        BINARY_TYPE = bytes

    # Content categories.
    SNIPPET = 'snippet'
    SOLUTION = 'solution'
    REFERENCE = 'reference'
    ALL_CATEGORIES = 'all'
    UNKNOWN_CATEGORY = 'unknown'
    CATEGORIES = (SNIPPET, SOLUTION, REFERENCE)

    # Content delimiters to convert between string and tuple presentations.
    DELIMITER_DATA = NEWLINE
    DELIMITER_GROUPS = ','
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = NEWLINE

    # Default values for content fields.
    DEFAULT_GROUPS = ('default',)

    # Content formats
    CONTENT_FORMAT_NONE = 'none'
    CONTENT_FORMAT_YAML = 'yaml'
    CONTENT_FORMAT_JSON = 'json'
    CONTENT_FORMAT_TEXT = 'text'

    # Regexp patterns.
    RE_MATCH_ANSI_ESCAPE_SEQUENCES = re.compile(r'''
        \x1b[^m]*m    # Match all ANSI escape sequences.
        ''', re.VERBOSE)
