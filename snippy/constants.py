# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
    PYTHON37 = bool(sys.version_info >= (3, 7))

    # Windows
    WINDOWS = sys.platform == 'win32'  # This applies also to win64.

    # Content categories.
    CODE = 'code'
    SNIPPET = 'snippet'
    SOLUTION = 'solution'
    REFERENCE = 'reference'
    TODO = 'todo'
    ALL_CATEGORIES = 'all'
    UNKNOWN_CATEGORY = 'unknown'
    CATEGORIES = (SNIPPET, SOLUTION, REFERENCE)

    # Field categories.
    GROUPS = 'groups'
    TAGS = 'tags'
    FIELD_CATEGORIES = (GROUPS, TAGS)

    # Content delimiters to convert between string and tuple presentations.
    DELIMITER_DATA = NEWLINE
    DELIMITER_GROUPS = ','
    DELIMITER_LINKS = NEWLINE
    DELIMITER_TAGS = ','
    DELIMITER_VERSIONS = ','
    DELIMITER_LANGUAGES = ','

    # Separate snippet data from optional comment.
    SNIPPET_COMMENT = '  #  '
    SNIPPET_COMMENT_COLOR = '  \x1b[91m#\x1b[0m  '

    # Default values for content fields.
    DEFAULT_GROUPS = ('default',)

    # Content formats
    CONTENT_FORMAT_DICT = 'dict'
    CONTENT_FORMAT_JSON = 'json'
    CONTENT_FORMAT_MKDN = 'mkdn'
    CONTENT_FORMAT_TEXT = 'text'
    CONTENT_FORMAT_YAML = 'yaml'
    CONTENT_FORMAT_NONE = 'none'

    # Storage backends and databases.
    DB_SQLITE = 'sqlite'
    DB_POSTGRESQL = 'postgresql'
    DB_COCKROACHDB = 'cockroachdb'
    DB_IN_MEMORY = 'in-memory'
    STORAGES = (DB_SQLITE, DB_POSTGRESQL, DB_COCKROACHDB, DB_IN_MEMORY)

    # Regexp patterns.
    RE_MATCH_ANSI_ESCAPE_SEQUENCES = re.compile(r'''
        \x1b[^m]*m    # Match all ANSI escape sequences.
        ''', re.VERBOSE)

    RE_CATCH_COMMAND_AND_COMMENT = re.compile(r'''
        (?P<command>[\s\S]+?)     # Catch command untill following separator.
        (:?\s{1,}[#]{1}\s{1,}|$)  # Match optional separator between command and comment or end of the line.
        (?P<comment>[\s\S]+|$)    # Catch optional comment. This regexp forces empty string instead of None in optional group.
        ''', re.VERBOSE)

    RE_DO_NOT_MATCH_ANYTHING = re.compile(r'''
        \A(?!x)x  # Never match anything.
        ''', re.VERBOSE)

    RE_MATCH_NEWLINES = re.compile(u'''             # Unicode regexp compatible with Python 2 and 3.
        (:?[\\r\\n\\x0B\\x0C\u0085\u2028\u2029]+)   # Match all newlines inluding Unicode line break characters.
        ''', re.UNICODE | re.VERBOSE)               # https://stackoverflow.com/a/34936253

    RE_MATCH_MULTIPE_WHITESPACES = re.compile(r'''
        (:?[\s]{2,})  # Match multiple whitespaces.
        ''', re.VERBOSE)
