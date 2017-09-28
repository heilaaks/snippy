#!/usr/bin/env python3

"""format.py: Data formatting and conversions."""

import re
import hashlib
import datetime
from snippy.config import Constants as Const


class Format(object): # pylint: disable=too-many-public-methods
    """Data formatting and conversions."""

    @staticmethod
    def get_snippet_text(snippets, colors=False):
        """Format snippets for console or pure text output."""

        text = Const.EMPTY
        content = Const.EMPTY
        links = Const.EMPTY
        for idx, snippet in enumerate(snippets, start=1):
            text = text + Format.console_header(colors) % (idx, snippet[Const.BRIEF],
                                                           snippet[Const.GROUP], \
                                                           snippet[Const.DIGEST])
            text = text + Const.EMPTY.join([Format.console_snippet(colors) % (content, line) \
                                            for line in snippet[Const.DATA]])
            text = text + Const.NEWLINE
            text = Format.console_tags(colors) % (text, Const.DELIMITER_TAGS.join(snippet[Const.TAGS]))
            text = text + Const.EMPTY.join([Format.console_links(colors) % (links, link) \
                                            for link in snippet[Const.LINKS]])
            text = text + Const.NEWLINE

        return text

    @staticmethod
    def get_solution_text(solutions, colors=False):
        """Format solutions for console or pure text output."""

        text = Const.EMPTY
        content = Const.EMPTY
        links = Const.EMPTY
        for idx, solution in enumerate(solutions, start=1):
            text = text + Format.console_header(colors) % (idx, solution[Const.BRIEF],
                                                           solution[Const.GROUP], \
                                                           solution[Const.DIGEST])
            text = text + Const.NEWLINE
            text = Format.console_tags(colors) % (text, Const.DELIMITER_TAGS.join(solution[Const.TAGS]))
            text = text + Const.EMPTY.join([Format.console_links(colors) % (links, link) \
                                            for link in solution[Const.LINKS]])
            text = text + Const.NEWLINE

            text = text + Const.EMPTY.join([Format.console_solution(colors) % (content, line) \
                                            for line in solution[Const.DATA]])

        return text

    @staticmethod
    def console_header(colors=False):
        """Format content text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0m @%s \x1b[0;2m[%.16s]\x1b[0m\n' if colors \
               else '%d. %s @%s [%.16s]\n'

    @staticmethod
    def console_snippet(colors=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m %s\n' if colors else '%s   $ %s\n'

    @staticmethod
    def console_solution(colors=False):
        """Format solution text."""

        return '%s   \x1b[91m:\x1b[0m %s\n' if colors else '%s   : %s\n'

    @staticmethod
    def console_links(colors=False):
        """Format content links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   > %s\n'

    @staticmethod
    def console_tags(colors=False):
        """Format content tags."""

        return '%s   \x1b[91m#\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   # %s\n'

    @staticmethod
    def get_db_data(content):
        """Format content data for database storage."""

        data = Const.DELIMITER_DATA.join(map(str, content[Const.DATA]))

        return data

    @staticmethod
    def get_db_brief(content):
        """Format content brief for database storage."""

        brief = content[Const.BRIEF]

        return brief

    @staticmethod
    def get_db_group(content):
        """Format content group for database storage."""

        group = content[Const.GROUP]

        return group

    @staticmethod
    def get_db_tags(content):
        """Format content tags for database storage."""

        # The map is sorted because it seems that this somehow randomly changes
        # the order of tags in the string. This seems to happen only in Python 2.7.
        tags = Const.DELIMITER_TAGS.join(map(str, sorted(content[Const.TAGS])))

        return tags

    @staticmethod
    def get_db_links(content):
        """Format content links for database storage."""

        # The map is sorted because it seems that this somehow randomly changes
        # the order of tags in the string. This seems to happen only in Python 2.7.
        links = Const.DELIMITER_LINKS.join(map(str, sorted(content[Const.LINKS])))

        return links

    @staticmethod
    def get_db_category(content):
        """Format content category for database storage."""

        category = content[Const.CATEGORY]

        return category

    @staticmethod
    def get_db_filename(content):
        """Format content filename for database storage."""

        filename = content[Const.FILENAME]

        return filename

    @staticmethod
    def get_data_string(content):
        """Format content data to string."""

        data = Const.DELIMITER_DATA.join(map(str, content[Const.DATA]))

        return data

    @staticmethod
    def get_brief_string(content):
        """Format content brief to string."""

        brief = content[Const.BRIEF]

        return brief

    @staticmethod
    def get_group_string(content):
        """Format content group to string."""

        group = content[Const.GROUP]

        return group

    @staticmethod
    def get_tags_string(content):
        """Format content tags to string."""

        tags = Const.DELIMITER_TAGS.join(map(str, content[Const.TAGS]))

        return tags

    @staticmethod
    def get_links_string(content):
        """Format content links to string."""

        links = Const.DELIMITER_NEWLINE.join(map(str, content[Const.LINKS]))

        return links

    @staticmethod
    def get_file_string(content):
        """Format content file to string."""

        filename = Const.EMPTY
        match = re.search(r'## FILE  :\s+(\S+)', Format.get_data_string(content))
        if match:
            filename = match.group(1)

        if '<SNIPPY_FILE>' in filename:
            filename = Const.EMPTY

        return filename

    @classmethod
    def get_keywords(cls, keywords):
        """Preprocess the user given keyword list. The keywords are for example the
        user provided tags or the search keywords. The user may use various formats
        so each item in a list may be for example a string of comma separated tags.

        The dot is a special case. It is allowed for the regexp to match and print
        all records."""

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t dockertesting', container-managemenet', cleanup_testing
        #           6. --sall '.'
        kw_list = []
        for tag in keywords:
            kw_list = kw_list + re.findall(r"[\w\-\.]+", tag)

        sorted_list = sorted(kw_list)

        return tuple(sorted_list)


    @staticmethod
    def get_dictionary(contents):
        """Convert content to dictionary format."""

        content_list = []
        for entry in contents:
            content_list.append(Format._get_dictionary(entry))

        return content_list

    @staticmethod
    def get_storage(contents):
        """Convert content from dictionary format."""

        content_list = []
        for entry in contents:
            content_list.append(Format._get_tuple_from_dictionary(entry))

        return content_list

    @staticmethod
    def calculate_digest(content):
        """Calculate digest for the content and timestamp."""

        data_string = Format._get_string(content)
        digest = hashlib.sha256(data_string.encode('UTF-8')).hexdigest()

        return digest

    @staticmethod
    def get_utc_time():
        """Get UTC time."""

        utc = datetime.datetime.utcnow()

        return utc.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_string(content):
        """Convert content into one string."""

        content_str = Const.EMPTY.join(map(str, content[Const.DATA]))
        content_str = content_str + Const.EMPTY.join(content[Const.BRIEF:Const.TAGS])
        content_str = content_str + Const.EMPTY.join(sorted(content[Const.TAGS]))
        content_str = content_str + Const.EMPTY.join(sorted(content[Const.LINKS]))
        content_str = content_str + content[Const.CATEGORY]
        content_str = content_str + content[Const.FILENAME]

        return content_str

    @staticmethod
    def _get_dictionary(content):
        """Convert content into dictionary."""

        dictionary = {'content': content[Const.DATA],
                      'brief': content[Const.BRIEF],
                      'group': content[Const.GROUP],
                      'tags': content[Const.TAGS],
                      'links': content[Const.LINKS],
                      'category': content[Const.CATEGORY],
                      'filename': content[Const.FILENAME],
                      'utc': content[Const.UTC],
                      'digest': content[Const.DIGEST]}

        return dictionary

    @staticmethod
    def _get_tuple_from_dictionary(dictionary):
        """Convert single dictionary entry into tuple."""

        content = [dictionary['data'],
                   dictionary['brief'],
                   dictionary['group'],
                   dictionary['tags'],
                   dictionary['links'],
                   dictionary['category'],
                   dictionary['filename'],
                   dictionary['utc'],
                   dictionary['digest']]
        digest = Format.calculate_digest(content)
        content.append(digest)

        return tuple(content)
