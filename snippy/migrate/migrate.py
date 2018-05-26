#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""migrate: Import and export management."""

from __future__ import print_function

import json
import os.path
import re
import sys
from signal import signal, getsignal, SIGPIPE, SIG_DFL

import yaml

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger
from snippy.meta import __homepage__
from snippy.meta import __version__


class Migrate(object):
    """Import and export management."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def content(cls, contents, content_type):
        """Migrate content into requested format."""

        migrated = Const.EMPTY
        cls._logger.debug('migrate content: %s', content_type)
        filtered = Migrate.apply_filters(contents)
        if content_type == Const.CONTENT_TYPE_TEXT:
            migrated = Migrate.terminal(filtered)
        elif content_type == Const.CONTENT_TYPE_JSON:
            migrated = Migrate.get_dictionary_list(filtered)
        elif content_type == Const.CONTENT_TYPE_YAML:
            migrated = Migrate.get_dictionary_list(filtered)

        return migrated

    @classmethod
    def apply_filters(cls, contents):
        """Apply regexp filter to content."""

        regexp = Config.search_filter

        if regexp and contents:
            cls._logger.debug('apply regexp filter to query response: %s', regexp)

        return contents

    @classmethod
    def terminal(cls, contents):
        """Print content into terminal."""

        text = Const.EMPTY
        if not contents:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')

        regexp = Config.search_filter
        if regexp:
            # In case user provided regexp filter, the ANSI control characters for
            # colors are not used in order to make the filter work as expected.
            text = Migrate.get_terminal_text(contents, ansi=False)
            match = re.findall(regexp, text)
            if match:
                text = Const.NEWLINE.join(match) + Const.NEWLINE
                Migrate.print_stdout(text)
        else:
            text = Migrate.get_terminal_text(contents, ansi=Config.use_ansi, debug=Config.debug_logs)
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
        if text:
            cls._logger.debug('printing content to terminal stdout')
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
                text = text + Migrate._terminal_created(ansi) % content.get_created()
                text = text + Migrate._terminal_updated(ansi) % content.get_updated()
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
    def dump(cls, collection, filename):
        """Dump collection into file."""

        if not Config.is_supported_file_format():
            cls._logger.debug('file format not supported for file %s', filename)

            return

        if not collection.size():
            cls._logger.debug('no content to be exported')

            return

        cls._logger.debug('exporting contents %s', filename)
        with open(filename, 'w') as outfile:
            try:
                dictionary = {'meta': {'updated': Config.utcnow(),
                                       'version': __version__,
                                       'homepage': __homepage__},
                              'content': collection.dump_json(Config.filter_fields)}
                if Config.is_operation_file_text:
                    for resource in collection.resources():
                        template = resource.dump_text(Config.templates)
                        outfile.write(template)
                        outfile.write(Const.NEWLINE)
                elif Config.is_operation_file_json:
                    json.dump(dictionary, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_operation_file_yaml:
                    yaml.safe_dump(dictionary, outfile, default_flow_style=False)
                else:
                    cls._logger.debug('unknown export file format')
            except (IOError, TypeError, ValueError, yaml.YAMLError) as exception:
                cls._logger.exception('fatal failure to generate formatted export file "%s"', exception)
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while exporting content to file')

    @classmethod
    def dump_template(cls, category):
        """Dump content template into file."""

        filename = Config.get_operation_file()
        resource = Collection.get_resource(category, Config.utcnow())
        template = resource.dump_text(Config.templates)
        cls._logger.debug('exporting content template %s', filename)
        with open(filename, 'w') as outfile:
            try:
                outfile.write(template)
            except IOError as exception:
                cls._logger.exception('fatal failure in creating %s template file "%s"', category, exception)
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while exporting template {}'.format(filename))

    @classmethod
    def load(cls, filename):
        """Load dictionary from file."""

        collection = Collection()
        if not Config.is_supported_file_format():
            cls._logger.debug('file format not supported for file %s', filename)

            return collection

        cls._logger.debug('importing contents from file %s', filename)
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                try:
                    if Config.is_operation_file_text:
                        collection = Config.get_collection(source=infile.read())
                    elif Config.is_operation_file_json:
                        dictionary = json.load(infile)
                        collection.load_dict(dictionary)
                    elif Config.is_operation_file_yaml:
                        dictionary = yaml.safe_load(infile)
                        collection.load_dict(dictionary)
                    else:
                        cls._logger.debug('unknown import file format')
                except (TypeError, ValueError, yaml.YAMLError) as exception:
                    cls._logger.exception('fatal exception while loading file "%s"', exception)
                    Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while importing content from file')

        else:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot read file {}'.format(filename))

        return collection

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
    def _terminal_created(ansi=False):
        """Format content creation UTC timestamp."""

        return '   \x1b[91m!\x1b[0m \x1b[2mcreated\x1b[0m  : %s\n' if ansi else '   ! created  : %s\n'

    @staticmethod
    def _terminal_updated(ansi=False):
        """Format content UTC timestamp when it was updated."""

        return '   \x1b[91m!\x1b[0m \x1b[2mupdated\x1b[0m  : %s\n' if ansi else '   ! updated  : %s\n'

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
                      'created': content.get_created(),
                      'updated': content.get_updated(),
                      'digest': content.get_digest()}

        # Digest is always needed when JSON REST API response is constructed.
        # Because of this, the digest is not removed in here but just before
        # constructing the JSON API response.
        for field in Config.filter_fields:
            if field != 'digest':
                dictionary.pop(field, None)

        return dictionary
