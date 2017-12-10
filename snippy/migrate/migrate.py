#!/usr/bin/env python3

"""migrate.py: Import and export management."""

from __future__ import print_function
import os.path
import re
import sys
from signal import signal, getsignal, SIGPIPE, SIG_DFL
from snippy.version import __version__
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config


class Migrate(object):
    """Import and export management."""

    logger = None

    def __init__(self):
        if not Migrate.logger:
            Migrate.logger = Logger(__name__).get()

    @classmethod
    def content(cls, contents, content_type):
        """Migrate content into requested format."""

        migrated = Const.EMPTY
        filtered = Migrate.apply_filters(contents)
        if content_type == Const.CONTENT_TYPE_TEXT:
            migrated = Migrate.terminal(filtered)
        elif content_type == Const.CONTENT_TYPE_JSON:
            import json

            dictionary = Migrate.get_dictionary_list(filtered)
            migrated = json.dumps(dictionary)
        elif content_type == Const.CONTENT_TYPE_YAML:
            import yaml

            dictionary = Migrate.get_dictionary_list(filtered)
            migrated = yaml.safe_dump(dictionary, default_flow_style=False)

        return migrated

    @classmethod
    def apply_filters(cls, contents):
        """Apply filter, limit and sorting parameters to content."""

        regexp = Config.get_search_filter()
        limit = Config.get_search_limit()
        sorting = Config.get_search_sorting()

        # The design is that the first regexp query is applied to reduce the
        # content list. Then the remaining contents are first sorted and then
        # limited. That is, all the content reduction parameters are applied
        # first, then sort and the limit is always the last.
        #
        # Sorting with multiple parameters is complicated and not fully understood.
        # Based on /1/ the logic is to reverse the order of parameters given by
        # user and then run the sort for each column in reversed order. This seems
        # to work but currently cannot be quaranteed to be 100% correct.
        #
        # /1/ https://stackoverflow.com/a/4233482
        if regexp and contents:
            cls.logger.debug('apply search regexp filter to search query')
        if sorting and contents:
            cls.logger.debug('apply search sorting filters to search query')
            for sort_column in reversed(sorting['order']):
                contents = contents[0].sort_contents(contents, sort_column, sorting['value'][sort_column])
        if limit and contents:
            cls.logger.debug('apply search limit %d filter to search query', limit)
            contents = contents[:limit]

        return contents

    @classmethod
    def terminal(cls, contents):
        """Print content into terminal."""

        text = Const.EMPTY
        if not contents:
            Cause.set_text('cannot find content with given search criteria')

        regexp = Config.get_search_filter()
        if regexp:
            # In case user provided regexp filter, the ANSI control characters for
            # colors are not used in order to make the filter work as exptected.
            text = Migrate.get_terminal_text(contents, ansi=False)
            match = re.findall(regexp, text)
            if match:
                text = Const.NEWLINE.join(match) + Const.NEWLINE
                Migrate.print_stdout(text)
        else:
            text = Migrate.get_terminal_text(contents, ansi=Config.use_ansi(), debug=Config.is_debug())
            Migrate.print_stdout(text)

        return text

    @classmethod
    def print_stdout(cls, text):
        """Print tool output to stdout."""

        # The signal handler manipulation and flush setting below prevents 'broken
        # pipe' errors with grep. For example incorrect parameter usage in grep may
        # cause this. See below listed references /1,2/ and examples that fail
        # without this correction.
        #
        # /1/ https://stackoverflow.com/a/16865106
        # /2/ https://stackoverflow.com/a/26738736
        #
        # $ snippy search --sall '--all' --filter crap | grep --all
        # $ snippy search --sall 'test' --filter test -vv | grep --all
        if text and Config.is_print():
            cls.logger.debug('printing content to terminal stdout')
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(text)
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)

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
                text = text + Migrate._terminal_runalias(ansi) % content.get_runalias()
                text = text + Migrate._terminal_versions(ansi) % content.get_versions()
                text = text + Migrate._terminal_utc(ansi) % content.get_utc()
                text = text + Migrate._terminal_digest(ansi) % (content.get_digest(),
                                                                content.get_digest() == content.compute_digest())
                text = text + Migrate._terminal_metadata(ansi) % content.get_metadata()
                text = text + Migrate._terminal_key(ansi) % content.get_key()
                text = text + Const.NEWLINE

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
    def dump(cls, contents, filename):
        """Dump contents into file."""

        if not Config.is_supported_file_format():
            cls.logger.debug('file format not supported for file %s', filename)

            return

        if not contents:
            cls.logger.debug('no content to be exported')

            return

        cls.logger.debug('exporting contents %s', filename)
        with open(filename, 'w') as outfile:
            try:
                dictionary = {'metadata': {'utc': Config.get_utc_time(),
                                           'version': __version__,
                                           'homepage': 'https://github.com/heilaaks/snippy'},
                              'content': Migrate.get_dictionary_list(contents)}
                if Config.is_file_type_text():
                    for content in contents:
                        template = Config.get_content_template(content)
                        outfile.write(template)
                        outfile.write(Const.NEWLINE)
                elif Config.is_file_type_json():
                    import json

                    json.dump(dictionary, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_file_type_yaml():
                    import yaml

                    yaml.safe_dump(dictionary, outfile, default_flow_style=False)
                else:
                    cls.logger.info('unknown export file format')
            except (IOError, TypeError, ValueError, yaml.YAMLError) as exception:
                cls.logger.exception('fatal failure to generate formatted export file "%s"', exception)
                Cause.set_text('fatal failure while exporting content to file')

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
                Cause.set_text('fatal failure while exporting template {}'.format(filename))

    @classmethod
    def load(cls, filename, content):
        """Load dictionary from file."""

        dictionary = {}
        if not Config.is_supported_file_format():
            cls.logger.debug('file format not supported for file %s', filename)

            return dictionary

        cls.logger.debug('importing contents from file %s', filename)
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                try:
                    if Config.is_file_type_text():
                        contents = Config.get_text_contents(content, infile.read())
                        dictionary = {'content': Migrate.get_dictionary_list(contents)}
                    elif Config.is_file_type_json():
                        import json

                        dictionary = json.load(infile)
                    elif Config.is_file_type_yaml():
                        import yaml

                        dictionary = yaml.safe_load(infile)
                    else:
                        cls.logger.info('unknown import file format')
                except (TypeError, ValueError, yaml.YAMLError) as exception:
                    cls.logger.exception('fatal exception while loading file "%s"', exception)
                    Cause.set_text('fatal failure while importing content from file')

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
    def _terminal_runalias(ansi=False):
        """Format content runalias."""

        return '   \x1b[91m!\x1b[0m \x1b[2mrunalias\x1b[0m : %s\n' if ansi else '   ! runalias : %s\n'

    @staticmethod
    def _terminal_versions(ansi=False):
        """Format content version list."""

        return '   \x1b[91m!\x1b[0m \x1b[2mversions\x1b[0m : %s\n' if ansi else '   ! versions : %s\n'

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
                      'runalias': content.get_runalias(),
                      'versions': content.get_versions(),
                      'utc': content.get_utc(),
                      'digest': content.get_digest()}

        columns = Config.get_search_removed_columns()
        for column in columns:
            dictionary.pop(column)

        return dictionary
