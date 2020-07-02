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

"""base: Base class for content parsers."""

import re
from collections import OrderedDict

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.logger import Logger


class ContentParserBase(object):
    """Base class for text content parser."""

    # Regexp patterns.
    RE_MATCH_TODO_TIMELINE = re.compile(r'''
        (?:
            No\sTimelin |               # Match timeline special string.
            Today |                     # Match timeline special string.
            Tomorrow |                  # Match timeline special string.
            \d{4}-\d{2}-\d{2}           # Match simplified ISO8601 date.
            (?:
                T                       # Match simplified ISO8601 date and time separator.
                \d{2}\:\d{2}\:\d{2}     # Match Simplified ISO8601 time.
                (?:
                    [+-]\d{2}\:\d{2}    # Match timezone offset.
                    |
                    Z                   # Match UTC timezone.
                )
                |
                $
            )
        )
        ''', re.VERBOSE)

    RE_CATCH_TODO_ITEMS = re.compile(r'''
        \s*                         # Match optional spaces before item.
        [-]*\s*                     # Match optional hyphen followed by optional space.
        [\[]{1}                     # Match mandatory opening bracket.
        (?P<done>[xX\s]{0,1})       # Catch done status.
        [\]\s]+                     # Match closing bracket for done status.
        (?P<item>\s.*)              # Catch todo item.
        ''', re.VERBOSE)

    # Defined in subclasses.
    REGEXP = {}

    # Content template tags.
    TEXT_TAG_DATA = '<data>'
    TEXT_TAG_BRIEF = '<brief>'
    TEXT_TAG_DESCRIPTION = '<description>'
    TEXT_TAG_NAME = '<name>'
    TEXT_TAG_GROUPS = '<groups>'
    TEXT_TAG_TAGS = '<tags>'
    TEXT_TAG_LINKS = '<links>'
    TEXT_TAG_SOURCE = '<source>'
    TEXT_TAG_VERSIONS = '<versions>'
    TEXT_TAG_LANGUAGES = '<languages>'
    TEXT_TAG_FILENAME = '<filename>'

    # Match content template tags.
    RE_MATCH_TEMPLATE_TAGS = re.compile(r'''
         %s  # Match content data.
        |%s  # Match brief.
        |%s  # Match description.
        |%s  # Match name.
        |%s  # Match groups.
        |%s  # Match tags.
        |%s  # Match links.
        |%s  # Match source.
        |%s  # Match versions.
        |%s  # Match languages.
        |%s  # Match filename.
        ''' % (re.escape(TEXT_TAG_DATA),
               re.escape(TEXT_TAG_BRIEF),
               re.escape(TEXT_TAG_DESCRIPTION),
               re.escape(TEXT_TAG_NAME),
               re.escape(TEXT_TAG_GROUPS),
               re.escape(TEXT_TAG_TAGS),
               re.escape(TEXT_TAG_LINKS),
               re.escape(TEXT_TAG_SOURCE),
               re.escape(TEXT_TAG_VERSIONS),
               re.escape(TEXT_TAG_LANGUAGES),
               re.escape(TEXT_TAG_FILENAME)
               ), re.VERBOSE)  # pylint: disable=bad-continuation

    # Content template example content.
    #
    # Do not add a dot at the end of the example ``brief``. This value
    # used in Markdown formatted template and using a dot with the
    # brief line, which also has the group field, does not look good.
    EXAMPLE_DATA = 'Markdown commands are defined between backtics and prefixed by a dollar sign'  # Used only with Markdown template.
    EXAMPLE_BRIEF = 'Add brief title for content'
    EXAMPLE_DESCRIPTION = 'Add a description that defines the content in one chapter.'
    EXAMPLE_NAME = 'example content handle'
    EXAMPLE_GROUPS = 'groups'
    EXAMPLE_TAGS = 'example,tags'
    EXAMPLE_LINKS = 'https://www.example.com/add-links-here.html'
    EXAMPLE_SOURCE = 'https://www.example.com/source.md'
    EXAMPLE_VERSIONS = 'example=3.9.0,python>=3'
    EXAMPLE_LANGUAGES = 'example-language'
    EXAMPLE_FILENAME = 'example-content.md'

    # Match content template texamples with the exception of groups.
    RE_MATCH_TEMPLATE_EXAMPLES = re.compile(r'''
        [`$\s]{3}%s[`]{1}\n    # Match data in Markdown surrounded by `$ `.
        |%s                    # Match brief.
        |%s                    # Match description.
        |%s                    # Match name.
        |%s                    # Match tags.
        |(?:[\[\d\]\s]{4})?%s  # Match links that are optionally prefixed by '[1] ' in case of Markdown template.
        |%s                    # Match source.
        |%s                    # Match versions.
        |%s                    # Match languages.
        |%s                    # Match filename.
        ''' % (re.escape(EXAMPLE_DATA),
               re.escape(EXAMPLE_BRIEF),
               re.escape(EXAMPLE_DESCRIPTION),
               re.escape(EXAMPLE_NAME),
               re.escape(EXAMPLE_TAGS),
               re.escape(EXAMPLE_LINKS),
               re.escape(EXAMPLE_SOURCE),
               re.escape(EXAMPLE_VERSIONS),
               re.escape(EXAMPLE_LANGUAGES),
               re.escape(EXAMPLE_FILENAME)
               ), re.VERBOSE)  # pylint: disable=bad-continuation

    TITLE_TEXT_GROUPS = '# Add optional comma separated list of groups below.\n'
    RE_MATCH_TEXT_GROUPS_EXAMPLES = re.compile(r'''
        %s  # Match groups title in text template.
        %s  # Match example groups.
        ''' % (re.escape(TITLE_TEXT_GROUPS),
               re.escape(EXAMPLE_GROUPS)
               ), re.VERBOSE)  # pylint: disable=bad-continuation
    RE_MATCH_MKDN_GROUPS_EXAMPLES = re.compile(r'''
        @groups$
        ''', re.MULTILINE | re.VERBOSE)

    # Temporary placeholder to align snippets in Markdown format. This
    # is used with snippets that have multiple commands when only part
    # of the commands have an user comment. This is used in editor when
    # content is updated or when it is exporeted in Markdown format.
    SNIPPET_DEFAULT_COMMENT = '<not documented>'

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

        data = []
        if value is None:
            return tuple(data)

        if category in [Const.SNIPPET, Const.REFERENCE]:
            data = cls.to_unicode(value).rstrip().split(Const.DELIMITER_DATA)
        elif category == Const.TODO:
            data = cls.to_unicode(value, strip_lines=False).split(Const.DELIMITER_DATA)
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
    def format_list(cls, keywords, unique=True, sort_=True):
        """Convert list of keywords to utf-8 encoded list of strings.

        Parse user provided keyword list. The keywords are for example groups,
        tags, search all keywords or versions.

        It is possible to use string or list context for the given keywords.
        In case of list context, each element in the list is still split
        separately.

        The keywords are split in word boundaries.

        A dot is a special case. It is allowed for a regexp to match and
        search all records. The dot is also used in cases wuhere user wants
        to search strings with "docker.stop". This matches to "docker stop"
        and it does not search separated words "docker" or "stop".

        Content versions field must support specific mathematical operators
        that do not split the keyword.

        Args:
            keywords (str,list,tuple): Keywords in string, list or tuple.
            unique (bool): Return unique keyword values.
            sort_ (bool): Return sorted keywords.

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
        #           7. --sall 'docker.stop'
        #           8. kafka==1.0.0
        #           9. kafka~1.0.0
        #          10. kafka>=1.0.0
        #          11. kafka<=1.0.0
        #          12. kafka!=1.0.0
        list_ = []
        keywords = cls._to_list(keywords)
        for tag in keywords:
            list_ = list_ + re.findall(u'''
                [\\w–\\-\\.\\=\\<\\>\\!\\~]+   # Python 2 and 3 compatible unicode regexp.
                ''', tag, re.UNICODE | re.VERBOSE)
        if unique:
            list_ = list(OrderedDict.fromkeys(list_))  # Must retain original order.
        if sort_:
            list_ = sorted(list_)

        return tuple(list_)

    @classmethod
    def format_links(cls, links, unique=True):
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
            links (str,list,tuple): Links in a string, list or tuple.
            unique (bool): Return unique keyword values.

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

        if unique:
            list_ = list(OrderedDict.fromkeys(list_))  # Must retain original order.

        return tuple(list_)

    @classmethod
    def format_filenames(cls, filenames):
        """Convert filenames to utf-8 encoded list of filenames.

        Parse user provided list of filenames. The filenames are separated with
        whitespaces. The filenames can contain any characters, even whitespaces.
        Because of this, the given filenames must be a list of filenames where
        each file can contain whitespaces.

        Args:
            filenames (list,tuple): Filenames in a list or tuple.

        Returns:
            tuple: Tuple of utf-8 encoded filenames.
        """

        list_ = []
        for filename in filenames:
            list_.append(cls.to_unicode(filename))
        list_ = list(filter(None, list_))

        return tuple(list_)

    @classmethod
    def format_versions(cls, versions):
        """Convert versions to utf-8 encoded list of version.

        Only specific operators between key value versions are allowed.

        Args:
            versions (str,list,tuple): Versions in a string, list or tuple.

        Returns:
            tuple: Tuple of utf-8 encoded versions.
        """

        versions_ = []
        versions = cls._to_list(versions)

        # Order of operators matter for the code logic. If operators < or >
        # are before >= and <=, the version is split into three values. Add
        # the longest match first into the operators.
        operators = ('>=', '<=', '!=', '==', '>', '<', '~')
        for version in versions:
            value = re.split('|'.join(operators), version)
            if len(value) == 2 and value[0] and value[1]:
                versions_.append(version)
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST,
                           'version: {} did not have key value pair with any of the supported operators: {}'.format(version, operators))

        return tuple(versions_)

    @classmethod
    def parse_groups(cls, category, regexp, text):
        """Parse content groups from text string.

        There is always a default group added into the content group field.

        Args:
            category (str): Content category.
            regexp (re): Compiled regexp to search groups.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        groups = Const.DEFAULT_GROUPS
        if category not in Const.CATEGORIES:
            return cls.format_list(groups)

        match = regexp.search(text)
        if match:
            groups = cls.format_list([match.group('groups')])
            if not groups:
                groups = Const.DEFAULT_GROUPS
            cls._logger.debug('parsed content groups: %s', groups)
        else:
            cls._logger.debug('parser did not find content for groups')

        return cls.format_list(groups)

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
            return cls.format_links(links)

        match = regexp.findall(text)
        if match:
            links = cls.format_links(match)
            cls._logger.debug('parsed content links: %s', links)
        else:
            cls._logger.debug('parser did not find content for links: %s', text)

        return links

    @classmethod
    def parse_versions(cls, category, regexp, text):
        """Parse content versions from text string.

        Version strings are validated. Only versions which pass the validation
        rules are stored. The rules allow only specific operators between key
        value pairs.

        Args:
            category (str): Content category.
            regexp (re): Compiled regexp to search versions.
            text (str): Content text string.

        Returns:
            tuple: Tuple of utf-8 encoded versions.
        """

        versions = ()
        if category not in Const.CATEGORIES:
            return cls.format_list(versions)

        match = regexp.search(text)
        if match:
            versions = cls.format_list([match.group('versions')])
            cls._logger.debug('parsed content versions: %s', versions)
        else:
            cls._logger.debug('parser did not find content for versions: %s', text)

        return cls.format_versions(versions)

    @classmethod
    def remove_template_fillers(cls, content):
        """Remove tags and examples from content.

        There are examples and tags in content templates that need to be
        removed before further processing the content. This method removes
        all the unnecessary tags and examples that are set to help user to
        fill a content template.

        The received content can be text for Markdown based.

        Args:
            content (str): Content text or Markdown string.

        Returns:
            str: String without content fillers.
        """

        content = cls.RE_MATCH_TEMPLATE_TAGS.sub('', content)
        content = cls.RE_MATCH_TEMPLATE_EXAMPLES.sub('', content)
        content = cls.RE_MATCH_TEXT_GROUPS_EXAMPLES.sub(cls.TITLE_TEXT_GROUPS + Const.DELIMITER_GROUPS.join(Const.DEFAULT_GROUPS), content)
        content = cls.RE_MATCH_MKDN_GROUPS_EXAMPLES.sub('@' + Const.DELIMITER_GROUPS.join(Const.DEFAULT_GROUPS), content)

        return content

    @classmethod
    def to_unicode(cls, value, strip_lines=True):
        """Convert value to utf-8 coded unicode string.

        If the give value is already an unicode character, it is assumed that
        it is a valid utf-8 encoded unicode character.

        The conversion quarantees one newline at the end of string.

        Args:
            value (str,list,tuple): Value in a string, list or tuple.
            strip_lines (bool): Defines if all lines are stripped in list.

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
    def to_bytes(cls, value):
        """Convert utf-8 encoded unicode string to byte string.

        Args:
            value (str): Value as a utf-8 encoded unicode string.

        Returns:
            str: Byte presentation from the utf-8 envoded unicode string.
        """

        if Const.PYTHON2:
            string_ = value.encode('utf-8')
        else:
            string_ = value

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

    def read_brief(self, category, text):
        """Read content ``brief`` attribute.

        Args:
            category (str): Content category.
            text (str): Content string.

        Returns:
            str: Utf-8 encoded unicode brief string.
        """

        brief = Const.EMPTY
        if category not in Const.CATEGORIES:
            return self.format_string(brief)

        match = self.REGEXP['brief'][category].search(text)
        if match:
            brief = match.group('brief')
            brief = Const.RE_MATCH_NEWLINES.sub(Const.SPACE, brief)
            brief = Const.RE_MATCH_MULTIPE_WHITESPACES.sub(Const.SPACE, brief)
            self._logger.debug('parsed content brief: %s', brief)
        else:
            self._logger.debug('parser did not find brief attribute: %s', text)

        return self.format_string(brief)

    def read_description(self, category, text):
        """Read content ``description`` attribute.

        Args:
            category (str): Content category.
            text (str): Content string.

        Returns:
            str: Utf-8 encoded unicode description string.
        """

        description = Const.EMPTY
        if category not in Const.CATEGORIES:
            return self.format_string(description)

        match = self.REGEXP['description'][category].search(text)
        if match:
            description = match.group('description')
            description = re.sub(r'''
                ^\s*[#]{1}\s    # Match start of each line (MULTILINE) with optional whitespaces in front of one hash.
                ''', Const.EMPTY, description, flags=re.MULTILINE | re.VERBOSE)
            description = Const.RE_MATCH_NEWLINES.sub(Const.SPACE, description)
            description = Const.RE_MATCH_MULTIPE_WHITESPACES.sub(Const.SPACE, description)
            self._logger.debug('parsed content description: %s', description)
        else:
            self._logger.debug('parser did not find content for description: %s', text)

        return self.format_string(description)

    def read_groups(self, category, text):
        """Read content ``groups`` attribute.

        Args:
            category (str): Content category.
            text (str): Content string.

        Returns:
            tuple: Tuple of utf-8 encoded groups.
        """

        return self.parse_groups(category, self.REGEXP['groups'].get(category, None), text)

    def read_links(self, category, text):
        """Read content ``links`` attribute.

        Args:
            category (str): Content category.
            text (str): Content string.

        Returns:
            tuple: Tuple of utf-8 encoded links.
        """

        return self.parse_links(category, self.REGEXP['links'].get(category, None), text)

    def read_versions(self, category, text):
        """Read content ``versions`` attribute.

        Args:
            category (str): Content category.
            text (str): Content string.

        Returns:
            tuple: Tuple of utf-8 encoded versions.
        """

        return self.parse_versions(category, self.REGEXP['versions'].get(category, None), text)

    def read_meta_value(self, category, key, text):
        """Read content metadata value from a text string.

        Args:
            category (str): Content category.
            metadata (str): Metadata to be read.
            text (str): Content text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        meta = ''
        if category not in Const.CATEGORIES:
            return self.format_string(meta)

        match = re.compile(r'''
            ^%s                 # Match metadata key at the beginning of line.
            \s+[:]{1}\s*?       # Match spaces and column between key and value or end of line immediately after column.
            (?P<value>.*$)      # Catch metadata value till end of the line it it exist.
            ''' % re.escape(key), re.MULTILINE | re.VERBOSE).search(text)
        if match:
            meta = match.group('value')
            self._logger.debug('parsed content metadata: %s : with value: %s', key, text)
        else:
            self._logger.debug('parser did not find content for key: %s :from metadata: %s', key, text)

        return self.format_string(meta)
