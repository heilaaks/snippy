#!/usr/bin/env python3

"""migrate.py: Import and export management."""

import re
import sys
import os.path
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config
from snippy.content import Content


class Migrate(object):
    """Import and export management."""

    logger = None

    def __init__(self):
        Migrate.logger = Logger(__name__).get()

    @classmethod
    def print_terminal(cls, contents):
        """Print content into terminal."""

        # In case user provided regexp filter, the ANSI color codes are removed
        # from the content in order to make the filter work as exptected.
        cls.logger.debug('printing content to terminal')
        text = Migrate.get_terminal_text(contents, colors=True)
        regexp = Config.get_search_filter()
        if regexp:
            ansi_escape = re.compile(r'\x1b[^m]*m')
            text = ansi_escape.sub('', text)
            match = re.findall(regexp, text)
            if match:
                print(Const.NEWLINE.join(match))
                print()
        else:
            print(text)

    @staticmethod
    def get_terminal_text(contents, colors=False):
        """Format content for terminal output."""

        text = Const.EMPTY
        for idx, content in enumerate(contents, start=1):
            if content.is_snippet():
                text = text + Migrate.get_snippet_text(idx, content, colors)
            else:
                text = text + Migrate.get_solution_text(idx, content, colors)

        return text

    @staticmethod
    def get_snippet_text(idx, snippet, colors=False):
        """Format snippets for console or pure text output."""


        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Migrate._console_header(colors) % (idx, snippet.get_brief(),
                                                         snippet.get_group(), \
                                                         snippet.get_digest())
        text = text + Const.EMPTY.join([Migrate._console_snippet(colors) % (data, line) \
                                        for line in snippet.get_data()])
        text = text + Const.NEWLINE
        text = Migrate._console_tags(colors) % (text, Const.DELIMITER_TAGS.join(snippet.get_tags()))
        text = text + Const.EMPTY.join([Migrate._console_links(colors) % (links, link) \
                                        for link in snippet.get_links()])
        text = text + Const.NEWLINE

        return text

    @staticmethod
    def get_solution_text(idx, solution, colors=False):
        """Format solutions for console or pure text output."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Migrate._console_header(colors) % (idx, solution.get_brief(),
                                                         solution.get_group(), \
                                                         solution.get_digest())
        text = text + Const.NEWLINE
        text = Migrate._console_tags(colors) % (text, Const.DELIMITER_TAGS.join(solution.get_tags()))
        text = text + Const.EMPTY.join([Migrate._console_links(colors) % (links, link) \
                                        for link in solution.get_links()])
        text = text + Const.NEWLINE

        text = text + Const.EMPTY.join([Migrate._console_solution(colors) % (data, line) \
                                        for line in solution.get_data()])

        return text

    @classmethod
    def dump(cls, contents):
        """Dump contents into file."""

        export_file = Config.get_operation_file()
        cls.logger.debug('exporting contents to file %s', export_file)
        with open(export_file, 'w') as outfile:
            try:
                dictionary_list = {'content': Migrate.get_dictionary_list(contents)}
                if Config.is_file_type_yaml():
                    import yaml

                    yaml.dump(dictionary_list, outfile, default_flow_style=False)
                elif Config.is_file_type_json():
                    import json

                    json.dump(dictionary_list, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_file_type_text():
                    outfile.write(Migrate.get_terminal_text(contents, colors=False))
                else:
                    cls.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                cls.logger.exception('fatal failure to generate formatted export file "%s"', exception)
                sys.exit()

    @classmethod
    def load(cls, filename):
        """Load dictionary to import contents."""

        snippets = ()
        dictionary = {}
        cls.logger.debug('importing contents from file %s', filename)
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                try:
                    if Config.is_file_type_yaml():
                        import yaml

                        dictionary = yaml.load(infile)
                    elif Config.is_file_type_json():
                        import json

                        dictionary = json.load(infile)
                    else:
                        cls.logger.info('unknown export format')
                except (yaml.YAMLError, TypeError) as exception:
                    cls.logger.exception('fatal exception while loading the import file %s "%s"', filename, exception)
                    sys.exit()

            snippets = Migrate._get_contents(dictionary['content'])
        else:
            Config.set_cause('cannot read file %s' % filename)

        return snippets

    @staticmethod
    def _console_header(colors=False):
        """Format content text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0m @%s \x1b[0;2m[%.16s]\x1b[0m\n' if colors \
               else '%d. %s @%s [%.16s]\n'

    @staticmethod
    def _console_snippet(colors=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m %s\n' if colors else '%s   $ %s\n'

    @staticmethod
    def _console_solution(colors=False):
        """Format solution text."""

        return '%s   \x1b[91m:\x1b[0m %s\n' if colors else '%s   : %s\n'

    @staticmethod
    def _console_links(colors=False):
        """Format content links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   > %s\n'

    @staticmethod
    def _console_tags(colors=False):
        """Format content tags."""

        return '%s   \x1b[91m#\x1b[0m \x1b[2m%s\x1b[0m\n' if colors else '%s   # %s\n'

    @staticmethod
    def get_dictionary_list(contents):
        """Convert content to dictionary format."""

        dictionary_list = []
        for entry in contents:
            dictionary_list.append(Migrate._get_dict_entry(entry))

        return dictionary_list

    @staticmethod
    def _get_dict_entry(content):
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
    def _get_contents(dictionary):
        """Convert dictionary to content tupe."""

        contents = []
        for entry in dictionary:
            contents.append(Migrate._get_content(entry))

        return tuple(contents)

    @staticmethod
    def _get_content(dictionary):
        """Convert single dictionary entry into Content object."""

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
