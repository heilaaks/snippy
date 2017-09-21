#!/usr/bin/env python3

"""format.py: Data formatting and conversions."""

import re
from snippy.config import Constants as Const


class Format(object):
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
                                            for line in snippet[Const.CONTENT]])
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
                                            for line in solution[Const.CONTENT]])

        return text

    @staticmethod
    def console_header(colors=False):
        """Format content text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0;2m \x1b[0m@%s \x1b[0;2m[%.16s]\x1b[0m\n' if colors \
               else '%d. %s @%s [%.16s]\n'

    @staticmethod
    def console_snippet(colors=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m \x1b[0m%s\x1b[0m\n' if colors else '%s   $ %s\n'

    @staticmethod
    def console_solution(colors=False):
        """Format solution text."""

        return '%s   \x1b[91m:\x1b[0m \x1b[0m%s\x1b[0m\n' if colors else '%s   : %s\n'

    @staticmethod
    def console_links(colors=False):
        """Format content links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   > %s\n'

    @staticmethod
    def console_tags(colors=False):
        """Format content tags."""

        return '%s   \x1b[91m#\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   # %s\n'

    @staticmethod
    def get_content_string(content):
        """Format content data to string."""

        data = Const.DELIMITER_CONTENT.join(map(str, content[Const.CONTENT]))

        return data

    @staticmethod
    def get_brief_string(content):
        """Format content brief to string."""

        brief = content[Const.BRIEF]

        return brief

    @staticmethod
    def get_group_string(content):
        """Format content group to string."""

        # If the group is in default value, don't show it to end user
        # since it may be confusing. If there is no input for the group
        # the default is set back.
        group = Const.EMPTY
        if not content[Const.GROUP] == Const.DEFAULT_GROUP:
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

        file = Const.EMPTY
        match = re.search('## FILE  :(.*)', Format.get_content_string(content))
        if match:
            file = match.group(1)

        if '<SNIPPY_FILE>' in file:
            file = Const.EMPTY

        return file

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
