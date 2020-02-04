# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""base: Parse content from Markdown templates."""

import re

from snippy.constants import Constants as Const
from snippy.content.parsers.base import ContentParserBase
from snippy.logger import Logger


class ContentParserMkdn(ContentParserBase):
    """Parse content from Markdown template."""

    # Example 1: Capture optional comment and mandatory command for content data.
    #
    #            - Remove all exited containers
    #
    #              `$ docker rm $(docker ps --all -q -f status=exited)`
    REGEXP = {}
    REGEXP['data'] = {}
    REGEXP['data'][Const.SNIPPET] = re.compile(r'''
        (
            (?:-\s+.*$\n\s*\n)?     # Catch one line optional comment followed by one empty line.
            \s.*`\$.*`              # Catch one line mandatory command indicated by dollar sign between grave accents (`).
                                    # It is not possible to loosen this because the command may contain quotation marks or
                                    # backtics (grave accents). The `$ ` combination is needed to reliably identiy command.
        ){1}                        # Catch only one optional command and mandatory command.
        ''', re.MULTILINE | re.VERBOSE)
    REGEXP['data'][Const.SOLUTION] = re.compile(r'''
        (?=[`]{3}|[#]{2}\s.*?)      # Lookahead for code block or first second level header.
        (?P<data>.*?)               # Catch solution data till the Meta header.
        (?=[#]{2}\sMeta)            # Lookahead for second level Meta header.
        ''', re.DOTALL | re.VERBOSE)
    REGEXP['data'][Const.REFERENCE] = re.compile(r'''
        \A(?!x)x'       # Never match anything because there is no data in the content.
        ''', re.VERBOSE)

    REGEXP['brief'] = {}
    REGEXP['brief'][Const.SNIPPET] = re.compile(r'''
        [#\s]+          # Match leading comment before brief.
        (?P<brief>.*)   # Catch brief.
        \s+[@]{1}       # Match string between brief and groups.
        ''', re.DOTALL | re.VERBOSE)
    REGEXP['brief'][Const.SOLUTION] = REGEXP['brief'][Const.SNIPPET]
    REGEXP['brief'][Const.REFERENCE] = REGEXP['brief'][Const.SNIPPET]

    REGEXP['description'] = {}
    REGEXP['description'][Const.SNIPPET] = re.compile(r'''
        [#\s]+.*[@].*                        # Match headline that contains always brief and groups.
        \n\s*\n                              # Match one empty line.
        [>\s]?(?P<description>[\S\s\d\n]*?)  # Catch optional description after greater than (>) sign.
        \n\s*\n                              # Match one empty line.
        ''', re.VERBOSE)
    REGEXP['description'][Const.SOLUTION] = REGEXP['description'][Const.SNIPPET]
    REGEXP['description'][Const.REFERENCE] = REGEXP['description'][Const.SNIPPET]

    REGEXP['groups'] = {}
    REGEXP['groups'][Const.SNIPPET] = re.compile(r'''
        [#\s]+          # Match leading comment before brief.
        .*              # Match brief before groups.
        \s+[@]{1}       # Match string between brief and groups.
        (?P<groups>.*)  # Catch groups.
        ''', re.VERBOSE)
    REGEXP['groups'][Const.SOLUTION] = REGEXP['groups'][Const.SNIPPET]
    REGEXP['groups'][Const.REFERENCE] = REGEXP['groups'][Const.SNIPPET]

    REGEXP['links'] = {}
    REGEXP['links'][Const.SNIPPET] = re.compile(r'''
        [\[\d\]\\\s]{4,}    # Match link reference number before the link.
        (?P<links>http.*)   # Catch link.
        ''', re.VERBOSE)
    REGEXP['links'][Const.SOLUTION] = re.compile(r'''
        \s+[>]{1}\s             # Match only links that contain fixed tag preceding the link.
        (?P<links>http.*)       # Catch link.
        ''', re.MULTILINE | re.VERBOSE)
    REGEXP['links'][Const.REFERENCE] = REGEXP['links'][Const.SNIPPET]

    REGEXP['versions'] = {}
    REGEXP['versions'][Const.SNIPPET] = re.compile(r'''
        ^versions           # Match versions metadata key at the beginning of line.
        \s+[:]{1}\s         # Match spaces and column between key and value.
        (?P<versions>.*$)   # Catch versions value till end of the line.
        ''', re.MULTILINE | re.VERBOSE)
    REGEXP['versions'][Const.SOLUTION] = REGEXP['versions'][Const.SNIPPET]
    REGEXP['versions'][Const.REFERENCE] = REGEXP['versions'][Const.SNIPPET]

    REGEXP['languages'] = {}
    REGEXP['languages'][Const.SNIPPET] = re.compile(r'''
        ^languages          # Match languages metadata key at the beginning of line.
        \s+[:]{1}\s         # Match spaces and column between key and value.
        (?P<languages>.*$)  # Catch languages value till end of the line.
        ''', re.MULTILINE | re.VERBOSE)
    REGEXP['languages'][Const.SOLUTION] = REGEXP['languages'][Const.SNIPPET]
    REGEXP['languages'][Const.REFERENCE] = REGEXP['languages'][Const.SNIPPET]

    def __init__(self, timestamp, text, collection):
        """
        Args:
            timestamp (str): IS8601 timestamp used with created resources.
            text (str): Source text that is parsed.
            collection (Collection()): Collection where the content is stored.
        """

        self._logger = Logger.get_logger(__name__)
        self._timestamp = timestamp
        self._text = text
        self._collection = collection

    def read_collection(self):
        """Read collection from the given Markdown source.

        The content is split based on reserved syntax. The reserved syntax to
        separate two different contents is a string '---' that must be at the
        beginning of a (multiline) string and have a newline immediately after
        the reserved string.
        """

        resources = []
        contents = re.split('^[-]{3}$', self._text, flags=re.MULTILINE)
        for content in contents:
            content = self.remove_template_fillers(content)
            category = self._read_category(content)
            resources.append({
                'category': category,
                'data': self._read_data(category, content),
                'brief': self.read_brief(category, content),
                'description': self.read_description(category, content),
                'name': self.read_meta_value(category, 'name', content),
                'groups': self.read_groups(category, content),
                'tags': self._read_tags(category, content),
                'links': self.read_links(category, content),
                'source': self.read_meta_value(category, 'source', content),
                'versions': self.read_versions(category, content),
                'languages': self._read_languages(category, content),
                'filename': self.read_meta_value(category, 'filename', content),
                'created': self.read_meta_value(category, 'created', content),
                'updated': self.read_meta_value(category, 'updated', content),
                'uuid': self.read_meta_value(category, 'uuid', content),
                'digest': self.read_meta_value(category, 'digest', content),
            })
        self._collection.convert(resources, self._timestamp)

    def _read_category(self, text):
        """Read content category from text string.

        Returns:
            str: Content category.
        """

        category = Const.UNKNOWN_CATEGORY
        match = re.compile(r'''
            [>\s]{2}category\s+:\s   # Match category metadata field.
            (?P<category>.*|$)       # Catch category.
            ''', re.VERBOSE).search(text)
        if match:
            category = self.format_string(match.group('category'))
            self._logger.debug('parsed content category: %s', category)
        else:
            self._logger.debug('parser did not find content category')

        if category not in Const.CATEGORIES:
            self._logger.debug('parser read invalid category: %s', category)
            category = Const.UNKNOWN_CATEGORY

        return category

    def _read_data(self, category, text):
        """Read content data from text string.

        Each content data line is stored in own element in a tuple.

        References do not have data field. In case of references, the links
        are considered as a data.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded content data.
        """

        data = ()
        if category not in Const.CATEGORIES or category == Const.REFERENCE:
            return self.format_data(category, data)

        match = self.REGEXP['data'][category].findall(text)
        if match:
            if category == Const.SNIPPET:
                data = self._snippet_data(match)
            elif category == Const.SOLUTION:
                data = match[0].strip()
                if data.startswith("```") and data.endswith("```"):
                    data = data[3:-3]
                data = data.strip()
            self._logger.debug('parsed content data: %s', data)
        else:
            self._logger.debug('parser did not find content for data: {}'.format(text))

        return self.format_data(category, data)

    def _snippet_data(self, text):
        """Parse snippet data from Markdown formatted string.

        Args:
            text (str): Whole snippet data section as a string.

        Returns:
            tuple: List of commands with optional comments.
        """

        data = []
        for command in text:
            match = re.compile(r'''
                (?:                             # Match optional comment inside non-capturing set.
                    -\s+                        # Match hyphen and spaces before comment
                    (?P<comment>.*$)            # Catch optional one line comment and skip one empty line before command.
                    \n\s*\n                     # Match empty line.
                )?                              # Comment may be matched 0 times.
                \s+                             # Match spaces in the beginning of the line which has the command.
                [`$\s]{3}(?P<command>.*)[`]     # Catch one line command indicated by dollar sign between grave accents (`).
                ''', re.MULTILINE | re.VERBOSE).search(command)
            if match:
                if match.group('comment') and match.group('comment') != ContentParserMkdn.SNIPPET_DEFAULT_COMMENT:
                    data.append(match.group('command') + Const.SNIPPET_COMMENT + match.group('comment'))
                else:
                    data.append(match.group('command'))
                self._logger.debug('parsed snippet data: %s', data)
            else:
                self._logger.debug('parser did not find snippet data data: %s', command)

        return tuple(data)

    def _read_tags(self, category, text):
        """Read content tags from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded tags.
        """

        tags = ()
        if category not in Const.CATEGORIES:
            return self.format_list(tags)

        match = self.read_meta_value(category, 'tags', text)
        if match:
            tags = [match]
            self._logger.debug('parsed content tags: %s', tags)
        else:
            self._logger.debug('parser did not find content for tags: {}'.format(text))

        return self.format_list(tags)

    def _read_languages(self, category, text):
        """Read content languages from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded languages.
        """

        languages = ()
        if category not in Const.CATEGORIES:
            return self.format_list(languages)

        match = self.read_meta_value(category, 'languages', text)
        if match:
            languages = [match]
            self._logger.debug('parsed content languages: %s', languages)
        else:
            self._logger.debug('parser did not find content for languages: {}'.format(text))

        return self.format_list(languages)
