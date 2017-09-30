#!/usr/bin/env python3

"""format.py: Data formatting and conversions."""

import re
import datetime
from snippy.config import Constants as Const
from snippy.content import Content


class Format(object): # pylint: disable=too-many-public-methods
    """Data formatting and conversions."""

    @staticmethod
    def get_snippet_text(snippets, colors=False):
        """Format snippets for console or pure text output."""

        text = Const.EMPTY
        content = Const.EMPTY
        links = Const.EMPTY
        for idx, snippet in enumerate(snippets, start=1):
            text = text + Format.console_header(colors) % (idx, snippet.get_brief(),
                                                           snippet.get_group(), \
                                                           snippet.get_digest())
            text = text + Const.EMPTY.join([Format.console_snippet(colors) % (content, line) \
                                            for line in snippet.get_data()])
            text = text + Const.NEWLINE
            text = Format.console_tags(colors) % (text, Const.DELIMITER_TAGS.join(snippet.get_tags()))
            text = text + Const.EMPTY.join([Format.console_links(colors) % (links, link) \
                                            for link in snippet.get_links()])
            text = text + Const.NEWLINE

        return text

    @staticmethod
    def get_solution_text(solutions, colors=False):
        """Format solutions for console or pure text output."""

        text = Const.EMPTY
        content = Const.EMPTY
        links = Const.EMPTY
        for idx, solution in enumerate(solutions, start=1):
            text = text + Format.console_header(colors) % (idx, solution.get_brief(),
                                                           solution.get_group(), \
                                                           solution.get_digest())
            text = text + Const.NEWLINE
            text = Format.console_tags(colors) % (text, Const.DELIMITER_TAGS.join(solution.get_tags()))
            text = text + Const.EMPTY.join([Format.console_links(colors) % (links, link) \
                                            for link in solution.get_links()])
            text = text + Const.NEWLINE

            text = text + Const.EMPTY.join([Format.console_solution(colors) % (content, line) \
                                            for line in solution.get_data()])

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
            content_list.append(Format._get_content_from_dictionary(entry))

        return content_list

    @staticmethod
    def get_utc_time():
        """Get UTC time."""

        utc = datetime.datetime.utcnow()

        return utc.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_dictionary(content):
        """Convert content into dictionary."""

        dictionary = {'data': content.get_data(),
                      'brief': content.get_brief(),
                      'group': content.get_group(),
                      'tags': content.get_tags(),
                      'links': content.get_links(),
                      'category': content.get_category(),
                      'filename': content.get_filename(),
                      'utc': content.get_utc(),
                      'digest': content.get_digest()}

        return dictionary

    @staticmethod
    def _get_content_from_dictionary(dictionary):
        """Convert single dictionary entry into tuple."""

        content = Content([dictionary['data'],
                           dictionary['brief'],
                           dictionary['group'],
                           dictionary['tags'],
                           dictionary['links'],
                           dictionary['category'],
                           dictionary['filename'],
                           dictionary['utc'],
                           dictionary['digest'],
                           None,  # metadata
                           None]) # key

        return content
