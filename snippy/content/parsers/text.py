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

"""base: Parse content from text templates."""

import re

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.parsers.base import ContentParserBase
from snippy.logger import Logger


class ContentParserText(ContentParserBase):
    """Parse content from text template."""

    DATA = {}
    DATA[Const.SNIPPET] = '# Add mandatory snippet below.\n'
    DATA[Const.REFERENCE] = DATA[Const.SNIPPET]
    DATA[Const.SOLUTION] = '## BRIEF  :'

    BRIEF = {}
    BRIEF[Const.SNIPPET] = '# Add optional brief description below.\n'
    BRIEF[Const.REFERENCE] = BRIEF[Const.SNIPPET]
    BRIEF[Const.SOLUTION] = '## BRIEF  :'

    DESCRIPTION = {}
    DESCRIPTION[Const.SNIPPET] = '# Add optional description below.\n'
    DESCRIPTION[Const.REFERENCE] = DESCRIPTION[Const.SNIPPET]
    DESCRIPTION[Const.SOLUTION] = '## DESCRIPTION  :'

    NAME = {}
    NAME[Const.SNIPPET] = '# Add optional name below.\n'
    NAME[Const.REFERENCE] = NAME[Const.SNIPPET]

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

    SOURCE = {}
    SOURCE[Const.SNIPPET] = '# Add optional source reference below.\n'
    SOURCE[Const.REFERENCE] = SOURCE[Const.SNIPPET]

    VERSIONS = {}
    VERSIONS[Const.SNIPPET] = '# Add optional comma separated list of key-value versions below.\n'
    VERSIONS[Const.REFERENCE] = VERSIONS[Const.SNIPPET]

    LANGUAGES = {}
    LANGUAGES[Const.SNIPPET] = '# Add optional comma separated list of languages below.\n'
    LANGUAGES[Const.REFERENCE] = LANGUAGES[Const.SNIPPET]

    FILENAME = {}
    FILENAME[Const.SNIPPET] = '# Add optional filename below.\n'
    FILENAME[Const.REFERENCE] = FILENAME[Const.SNIPPET]
    FILENAME[Const.SOLUTION] = '## FILE   :'

    REGEXP = {}
    REGEXP['data'] = {}
    REGEXP['data'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference data header.
        (?P<data>[\s\S]*?)      # Catch multiline data untill next match.
        (?:\n{2}|[#]\sAdd\s)    # Match newlines or next header indicated by hash and 'Add' tag from template.
        ''' % (re.escape(DATA[Const.SNIPPET]), re.escape(DATA[Const.REFERENCE])), re.MULTILINE | re.VERBOSE)
    REGEXP['data'][Const.REFERENCE] = REGEXP['data'][Const.SNIPPET]
    REGEXP['data'][Const.SOLUTION] = re.compile(r'''
        (?:[#]{2}\sFILE.*?\n[#]{70,}\s+)    # Match the header that is not part of data.
        (?P<data>.*?)                       # Catch all the content to data till the metadata.
        (?:$|[#]{70,}\n[#]{2}\sMeta)        # Match end of string or content metadata.
        ''', re.DOTALL | re.VERBOSE)

    REGEXP['brief'] = {}
    REGEXP['brief'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference brief.
        (?P<brief>.*?)          # Catch brief.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(BRIEF[Const.SNIPPET]), re.escape(BRIEF[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['brief'][Const.REFERENCE] = REGEXP['brief'][Const.SNIPPET]
    REGEXP['brief'][Const.SOLUTION] = re.compile(r'''
        %s\s*?                  # Match solution brief header.
        (?P<brief>.*|$)         # Catch brief.
        ''' % re.escape(BRIEF[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    REGEXP['description'] = {}
    REGEXP['description'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference description.
        (?P<description>.*?)    # Catch description.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the line.
        ''' % (re.escape(DESCRIPTION[Const.SNIPPET]), re.escape(DESCRIPTION[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['description'][Const.REFERENCE] = REGEXP['description'][Const.SNIPPET]
    REGEXP['description'][Const.SOLUTION] = re.compile(r'''
        (?:\#\#\s+[dD]escription\n(?:[#]+\n)?)  # Match solution description header. The description can be text or Markdown header.
        (?P<description>.*?)                    # Catch description.
        (?:\n{2}|[#]{2,}|$)                     # Match newlines or next header indicated by hashes or end of the string.
        ''', re.DOTALL | re.VERBOSE)

    REGEXP['name'] = {}
    REGEXP['name'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference name.
        (?P<name>.*?)           # Catch name.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(NAME[Const.SNIPPET]), re.escape(NAME[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['name'][Const.REFERENCE] = REGEXP['name'][Const.SNIPPET]
    REGEXP['name'][Const.SOLUTION] = re.compile(r'''
        name                    # Match metadata key at the beginning of line.
        \s+[:]{1}\s             # Match spaces and column between key and value.
        (?P<name>.*$)           # Catch metadata value till end of the line.
        ''', re.MULTILINE | re.VERBOSE)

    REGEXP['groups'] = {}
    REGEXP['groups'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference groups.
        (?P<groups>.*?)         # Catch groups.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(GROUPS[Const.SNIPPET]), re.escape(GROUPS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['groups'][Const.REFERENCE] = REGEXP['groups'][Const.SNIPPET]
    REGEXP['groups'][Const.SOLUTION] = re.compile(r'''
        %s\s*?                  # Match groups tag from solution.
        (?P<groups>.*|$)        # Catch groups.
        ''' % re.escape(GROUPS[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    REGEXP['tags'] = {}
    REGEXP['tags'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference tags.
        (?P<tags>.*?)           # Catch tags.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(TAGS[Const.SNIPPET]), re.escape(TAGS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['tags'][Const.REFERENCE] = REGEXP['tags'][Const.SNIPPET]
    REGEXP['tags'][Const.SOLUTION] = re.compile(r'''
        %s\s*?                  # Match tags tag from solution.
        (?P<tags>.*|$)          # Catch tags.
        ''' % re.escape(TAGS[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    REGEXP['links'] = {}
    REGEXP['links'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference links.
        (?P<links>.*?)          # Catch links.
        (?:[\n]{2}|[#]|$)       # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(LINKS[Const.SNIPPET]), re.escape(LINKS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['links'][Const.REFERENCE] = REGEXP['links'][Const.SNIPPET]
    REGEXP['links'][Const.SOLUTION] = re.compile(r'''
        \s+[>]{1}\s             # Match only links that contain fixed tag preceding the link.
        (?P<links>http.*)       # Catch link.
        ''', re.MULTILINE | re.VERBOSE)

    REGEXP['source'] = {}
    REGEXP['source'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference source.
        (?P<source>.*?)         # Catch source.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(SOURCE[Const.SNIPPET]), re.escape(SOURCE[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['source'][Const.REFERENCE] = REGEXP['source'][Const.SNIPPET]
    REGEXP['source'][Const.SOLUTION] = re.compile(r'''
        source                  # Match metadata key at the beginning of line.
        \s+[:]{1}\s             # Match spaces and column between key and value.
        (?P<source>.*$)         # Catch metadata value till end of the line.
        ''', re.MULTILINE | re.VERBOSE)

    REGEXP['versions'] = {}
    REGEXP['versions'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference versions.
        (?P<versions>.*?)       # Catch versions.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(VERSIONS[Const.SNIPPET]), re.escape(VERSIONS[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['versions'][Const.REFERENCE] = REGEXP['versions'][Const.SNIPPET]
    REGEXP['versions'][Const.SOLUTION] = re.compile(r'''
        versions                # Match metadata key at the beginning of line.
        \s+[:]{1}\s             # Match spaces and column between key and value.
        (?P<versions>.*$)       # Catch metadata value till end of the line.
        ''', re.MULTILINE | re.VERBOSE)

    REGEXP['languages'] = {}
    REGEXP['languages'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference languages.
        (?P<languages>.*?)      # Catch languages.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(LANGUAGES[Const.SNIPPET]), re.escape(LANGUAGES[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['languages'][Const.REFERENCE] = REGEXP['languages'][Const.SNIPPET]
    REGEXP['languages'][Const.SOLUTION] = re.compile(r'''
        languages               # Match metadata key at the beginning of line.
        \s+[:]{1}\s             # Match spaces and column between key and value.
        (?P<languages>.*$)      # Catch metadata value till end of the line.
        ''', re.MULTILINE | re.VERBOSE)

    REGEXP['filename'] = {}
    REGEXP['filename'][Const.SNIPPET] = re.compile(r'''
        (?:%s|%s)               # Match snippet or reference filename.
        (?P<filename>.*?)       # Catch filename.
        (?:\n{2}|[#]|$)         # Match newlines or next header indicated by hash or end of the string.
        ''' % (re.escape(FILENAME[Const.SNIPPET]), re.escape(FILENAME[Const.REFERENCE])), re.DOTALL | re.VERBOSE)
    REGEXP['filename'][Const.REFERENCE] = REGEXP['filename'][Const.SNIPPET]
    REGEXP['filename'][Const.SOLUTION] = re.compile(r'''
        %s\s*?                  # Match filename tag from solution.
        (?P<filename>.*|$)      # Catch filename.
        ''' % re.escape(FILENAME[Const.SOLUTION]), re.MULTILINE | re.VERBOSE)

    def __init__(self, timestamp, text, collection):
        """
        Args:
            timestamp (str): IS8601 timestamp used with created resources.
            text (str): Source text that is parsed.
            collection (:obj:`Collection`): Collection where the content is stored.
        """

        self._logger = Logger.get_logger(__name__)
        self._timestamp = timestamp
        self._text = text
        self._collection = collection

    def read_collection(self):
        """Read collection from the given text source."""

        resources = []
        contents = self._split_contents()
        for content in contents:
            category = self._read_category(content)
            resources.append({
                'category': category,
                'data': self._read_data(category, content),
                'brief': self._read_brief(category, content),
                'description': self._read_description(category, content),
                'name': self._read_name(category, content),
                'groups': self._read_groups(category, content),
                'tags': self._read_tags(category, content),
                'links': self._read_links(category, content),
                'source': self._read_source(category, content),
                'versions': self._read_versions(category, content),
                'languages': self._read_languages(category, content),
                'filename': self._read_filename(category, content),
                'created': self.read_meta_value(category, 'created', content),
                'updated': self.read_meta_value(category, 'updated', content),
                'uuid': self.read_meta_value(category, 'uuid', content),
                'digest': self.read_meta_value(category, 'digest', content),
            })
        self._collection.convert(resources, self._timestamp)

    def _split_contents(self):
        """Split source text to multiple contents.

        This method parses a single text string and extracts a list of text
        contents from it.

        All line numbers with a content specific ``head tag`` are scanned. The
        head tag is the first field description in a content specific template.
        The whole text string is then split based on scanned line numbers where
        a head tag was found.

        An offset is substracted from the line number where a ``head tag`` was
        found. The offset is coming from informative description field of a
        text template that has few lines before the head tag.

        If the source test string contains template tags or examples, those are
        removed from each returned content.

        Returns:
            list: List of text contents.
        """

        contents = []
        category = self._read_category(self._text)
        if category == Const.SNIPPET:
            offset = 2  # Two lines in the text template before the head tag.
            tag = '# Add mandatory snippet below'
        elif category == Const.SOLUTION:
            offset = 1  # One line in the text template before the content starts.
            tag = self.BRIEF[Const.SOLUTION]
        elif category == Const.REFERENCE:
            offset = 2  # Two lines in the text template before the head tag.
            tag = '# Add mandatory links below one link per line'
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'could not identify content category - please keep template tags in place')

            return contents

        lines = self._text.split(Const.NEWLINE)
        line_numbers = [i for i, line in enumerate(lines) if line.startswith(tag)]
        line_numbers[:] = [max(x-offset, 0) for x in line_numbers]
        if line_numbers:
            head = line_numbers.pop(0)
            for line in line_numbers:
                contents.append(Const.NEWLINE.join(lines[head:line]))
                head = line
            contents.append(self.remove_template_fillers(Const.NEWLINE.join(lines[head:])))

        return contents

    def _read_category(self, text):
        """Read content category from a text string.

        Args:
            text (str): Source text where the category is determined.

        Returns:
            str: Content category.
        """

        category = Const.UNKNOWN_CATEGORY

        if self.DATA[Const.SNIPPET] in text and self.BRIEF[Const.SNIPPET]:
            category = Const.SNIPPET
        elif self.BRIEF[Const.SOLUTION] in text and self.FILENAME[Const.SOLUTION] in text:
            category = Const.SOLUTION
        elif self.LINKS[Const.REFERENCE] in text:
            category = Const.REFERENCE

        return category

    def _read_data(self, category, text):
        """Read content data from text string.

        Each content data line is stored in element in a tuple. Solution
        content data is stored only by trimming the trailing newlines at the
        end of the data. In case of snippet content, each line is trimmed.

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

        match = self.REGEXP['data'][category].search(text)
        if match:
            data = self.format_data(category, match.group(1))
            self._logger.debug('parsed content data: %s', data)
        else:
            self._logger.debug('parser did not find content for data: {}'.format(text))

        # Format snippet command comments to internal format.
        if category == Const.SNIPPET:
            commands = []
            for command in data:
                match = Const.RE_CATCH_COMMAND_AND_COMMENT.search(command)
                if match and match.group('comment'):
                    commands.append('{}{}{}'.format(match.group('command'), Const.SNIPPET_COMMENT, match.group('comment')))
                else:
                    commands.append(command)
            data = commands

        return self.format_data(category, data)

    def _read_brief(self, category, text):
        """Read content brief from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode brief string.
        """

        brief = ''
        if category not in Const.CATEGORIES:
            return self.format_string(brief)

        match = self.REGEXP['brief'][category].search(text)
        if match:
            brief = match.group('brief')
            self._logger.debug('parsed content brief: %s', brief)
        else:
            self._logger.debug('parser did not find content for brief: {}'.format(text))

        return self.format_string(brief)

    def _read_description(self, category, text):
        """Read content description from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode description string.
        """

        description = ''
        if category not in Const.CATEGORIES:
            return self.format_string(description)

        match = self.REGEXP['description'][category].search(text)
        if match:
            description = match.group('description')
            self._logger.debug('parsed content description: %s', description)
        else:
            self._logger.debug('parser did not find content for description: {}'.format(text))

        # Remove comment marks from each line in case of solution description.
        description = re.sub(r'''
            ^\s*[#]{1}\s    # Match start of each line (MULTILINE) with optional whitespaces in front of one hash.
            ''', '', description, flags=re.MULTILINE | re.VERBOSE)

        # Remove newlines, tabs and replace multiple spaces with one space.
        description = re.sub(r'\s+', ' ', description).strip()

        return self.format_string(description)

    def _read_name(self, category, text):
        """Read content name from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode name string.
        """

        name = ''
        if category not in Const.CATEGORIES:
            return self.format_string(name)

        match = self.REGEXP['name'][category].search(text)
        if match:
            name = match.group('name')
            self._logger.debug('parsed content name: %s', name)
        else:
            self._logger.debug('parser did not find content for name: {}'.format(text))

        return self.format_string(name)

    def _read_groups(self, category, text):
        """Read content groups from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        return self.parse_groups(category, self.REGEXP['groups'].get(category, None), text)

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

        match = self.REGEXP['tags'][category].search(text)
        if match:
            tags = [match.group('tags')]
            self._logger.debug('parsed content tags: %s', tags)
        else:
            self._logger.debug('parser did not find content for tags: {}'.format(text))

        return self.format_list(tags)

    def _read_links(self, category, text):
        """Read content links from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        return self.parse_links(category, self.REGEXP['links'].get(category, None), text)

    def _read_source(self, category, text):
        """Read content source from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode source string.
        """

        source = ''
        if category not in Const.CATEGORIES:
            return self.format_string(source)

        match = self.REGEXP['source'][category].search(text)
        if match:
            source = match.group('source')
            self._logger.debug('parsed content source: %s', source)
        else:
            self._logger.debug('parser did not find content for source: {}'.format(text))

        return self.format_string(source)

    def _read_versions(self, category, text):
        """Read content versions from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded versions.
        """

        return self.parse_versions(category, self.REGEXP['versions'].get(category, None), text)

    def _read_languages(self, category, text):
        """Read content tags from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded languages.
        """

        languages = ()
        if category not in Const.CATEGORIES:
            return self.format_list(languages)

        match = self.REGEXP['languages'][category].search(text)
        if match:
            languages = [match.group('languages')]
            self._logger.debug('parsed content languages: %s', languages)
        else:
            self._logger.debug('parser did not find content for languages: {}'.format(text))

        return self.format_list(languages)

    def _read_filename(self, category, text):
        """Read content filename from text string.

        Args:
            category (str): Content category.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode filename string.
        """

        filename = ''
        if category not in Const.CATEGORIES:
            return self.format_string(filename)

        match = self.REGEXP['filename'][category].search(text)
        if match:
            filename = match.group('filename')
            self._logger.debug('parsed content filename: %s', filename)
        else:
            self._logger.debug('parser did not find content for filename: {}'.format(text))

        return self.format_string(filename)
