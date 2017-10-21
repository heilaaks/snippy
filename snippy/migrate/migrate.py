#!/usr/bin/env python3

"""migrate.py: Import and export management."""

from __future__ import print_function
import re
import sys
import os.path
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config


class Migrate(object):
    """Import and export management."""

    logger = None

    def __init__(self):
        Migrate.logger = Logger(__name__).get()

    @classmethod
    def print_terminal(cls, contents):
        """Print content into terminal."""

        cls.logger.debug('printing content to terminal')
        regexp = Config.get_search_filter()
        if regexp:
            # In case user provided regexp filter, the ANSI control characters for
            # colors are not used in order to make the filter work as exptected.
            text = Migrate.get_terminal_text(contents, ansi=False)
            match = re.findall(regexp, text)
            if match:
                print(Const.NEWLINE.join(match))
                print()
        else:
            text = Migrate.get_terminal_text(contents, ansi=Config.use_ansi())
            if text:
                print(text)

    @staticmethod
    def get_terminal_text(contents, ansi=False, debug=False):
        """Format content for terminal output."""

        text = Const.EMPTY
        for idx, content in enumerate(contents, start=1):
            if content.is_snippet():
                text = text + Migrate.get_snippet_text(idx, content, ansi)
            else:
                text = text + Migrate.get_solution_text(idx, content, ansi)

            if debug:
                text = text + Migrate._terminal_category(ansi) % content.get_category()
                text = text + Migrate._terminal_filename(ansi) % content.get_filename()
                text = text + Migrate._terminal_utc(ansi) % content.get_utc()
                text = text + Migrate._terminal_digest(ansi) % (content.get_digest(),
                                                                content.get_digest() == content.compute_digest())
                text = text + Migrate._terminal_metadata(ansi) % content.get_metadata()
                text = text + Migrate._terminal_key(ansi) % content.get_key()

        if contents:
            # Set only one empty line at the end of string for beautified output.
            text = text.rstrip()
            text = text + Const.NEWLINE

        return text

    @staticmethod
    def get_snippet_text(idx, snippet, ansi=False):
        """Format snippets for terminal or pure text output."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Migrate._terminal_header(ansi) % (idx, snippet.get_brief(),
                                                        snippet.get_group(),
                                                        snippet.get_digest())
        text = text + Const.EMPTY.join([Migrate._terminal_snippet(ansi) % (data, line)
                                        for line in snippet.get_data()])
        text = text + Const.NEWLINE
        text = Migrate._terminal_tags(ansi) % (text, Const.DELIMITER_TAGS.join(snippet.get_tags()))
        text = text + Const.EMPTY.join([Migrate._terminal_links(ansi) % (links, link)
                                        for link in snippet.get_links()])
        text = text + Const.NEWLINE

        return text

    @staticmethod
    def get_solution_text(idx, solution, ansi=False):
        """Format solutions for terminal or pure text output."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Migrate._terminal_header(ansi) % (idx, solution.get_brief(),
                                                        solution.get_group(),
                                                        solution.get_digest())
        text = text + Const.NEWLINE
        text = Migrate._terminal_tags(ansi) % (text, Const.DELIMITER_TAGS.join(solution.get_tags()))
        text = text + Const.EMPTY.join([Migrate._terminal_links(ansi) % (links, link)
                                        for link in solution.get_links()])
        text = text + Const.NEWLINE

        text = text + Const.EMPTY.join([Migrate._terminal_solution(ansi) % (data, line)
                                        for line in solution.get_data()])
        text = text + Const.NEWLINE

        return text

    @classmethod
    def dump(cls, contents):
        """Dump contents into file."""

        if not Config.is_supported_file_format():
            return

        filename = Config.get_operation_file()
        cls.logger.debug('exporting contents %s', filename)
        with open(filename, 'w') as outfile:
            try:
                dictionary = {'content': Migrate.get_dictionary_list(contents)}
                if Config.is_file_type_yaml():
                    import yaml

                    yaml.safe_dump(dictionary, outfile, default_flow_style=False)
                elif Config.is_file_type_json():
                    import json

                    json.dump(dictionary, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_file_type_text():
                    outfile.write(Migrate.get_terminal_text(contents, ansi=False))
                else:
                    cls.logger.info('unknown export format')
            except (TypeError, ValueError, yaml.YAMLError) as exception:
                cls.logger.exception('fatal failure to generate formatted export file "%s"', exception)
                sys.exit()

    @classmethod
    def dump_template(cls, content):
        """Dump content template into file."""

        filename = Config.get_operation_file(content_filename=content.get_filename())
        template = Config.get_content_template(content)
        cls.logger.debug('exporting content template %s', filename)
        with open(filename, 'w') as outfile:
            try:
                outfile.write(template)
            except IOError as exception:
                cls.logger.exception('fatal failure in creating snippet template file "%s"', exception)
                Cause.set_text('cannot export snippet template {}'.format(filename))

    @classmethod
    def load(cls, filename, content):
        """Load dictionary from file."""

        dictionary = {}
        if not Config.is_supported_file_format():
            return dictionary

        cls.logger.debug('importing contents from file %s', filename)
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                try:
                    if Config.is_file_type_yaml():
                        import yaml

                        dictionary = yaml.safe_load(infile)
                    elif Config.is_file_type_json():
                        import json

                        dictionary = json.load(infile)
                    elif Config.is_file_type_text():
                        contents = Config.get_file_contents(content, infile.read())
                        dictionary = {'content': Migrate.get_dictionary_list(contents)}
                    else:
                        cls.logger.info('unknown export format')
                except (TypeError, ValueError, yaml.YAMLError) as exception:
                    cls.logger.exception('fatal exception while loading the import file %s "%s"', filename, exception)
                    sys.exit()

        else:
            Cause.set_text('cannot read file {}'.format(filename))

        return dictionary

    @staticmethod
    def _terminal_header(ansi=False):
        """Format content text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0m @%s \x1b[0;2m[%.16s]\x1b[0m\n' if ansi \
               else '%d. %s @%s [%.16s]\n'

    @staticmethod
    def _terminal_snippet(ansi=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m %s\n' if ansi else '%s   $ %s\n'

    @staticmethod
    def _terminal_solution(ansi=False):
        """Format solution text."""

        return '%s   \x1b[91m:\x1b[0m %s\n' if ansi else '%s   : %s\n'

    @staticmethod
    def _terminal_tags(ansi=False):
        """Format content tags."""

        return '%s   \x1b[91m#\x1b[0m \x1b[2m%s\x1b[0m\n' if ansi else '%s   # %s\n'

    @staticmethod
    def _terminal_links(ansi=False):
        """Format content links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if ansi else '%s   > %s\n'

    @staticmethod
    def _terminal_category(ansi=False):
        """Format content category."""

        return '   \x1b[91m!\x1b[0m \x1b[2mcategory\x1b[0m : %s\n' if ansi else '   ! category : %s\n'

    @staticmethod
    def _terminal_filename(ansi=False):
        """Format content filename."""

        return '   \x1b[91m!\x1b[0m \x1b[2mfilename\x1b[0m : %s\n' if ansi else '   ! filename : %s\n'

    @staticmethod
    def _terminal_utc(ansi=False):
        """Format content utc."""

        return '   \x1b[91m!\x1b[0m \x1b[2mutc\x1b[0m      : %s\n' if ansi else '   ! utc      : %s\n'

    @staticmethod
    def _terminal_digest(ansi=False):
        """Format content digest."""

        return '   \x1b[91m!\x1b[0m \x1b[2mdigest\x1b[0m   : %s (%s)\n' if ansi else '   ! digest   : %s (%s)\n'

    @staticmethod
    def _terminal_metadata(ansi=False):
        """Format content metadata."""

        return '   \x1b[91m!\x1b[0m \x1b[2mmetadata\x1b[0m : %s\n' if ansi else '   ! metadata : %s\n'

    @staticmethod
    def _terminal_key(ansi=False):
        """Format content key."""

        return '   \x1b[91m!\x1b[0m \x1b[2mkey\x1b[0m      : %s\n' if ansi else '   ! key      : %s\n'

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
