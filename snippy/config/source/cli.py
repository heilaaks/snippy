#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""cli: CLI based content management."""

from __future__ import print_function

import sys
import argparse

from snippy.constants import Constants as Const
from snippy.config.source.base import ConfigSourceBase
from snippy.content.parser import Parser
from snippy.meta import __homepage__
from snippy.meta import __version__


class Cli(ConfigSourceBase):
    """CLI argument parsing."""

    ARGS_COPYRIGHT = (
        'Snippy version ' + __version__ + ' - license GNU AGPLv3 or later',
        'Copyright 2017-2019 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
        'Homepage ' + __homepage__
    )
    ARGS_USAGE = ('snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]')
    ARGS_CATEGORY = (
        '  --snippets                    operate snippets (default)',
        '  --solutions                   operate solutions',
        '  --references                  operate references',
        '  --all                         operate all content (search only)'
    )
    ARGS_EDITOR = (
        '  -c, --content CONTENT         define example content',
        '  -b, --brief BRIEF             define content brief description',
        '  -g, --groups [GROUP,...]      define comma separated list of groups',
        '  -t, --tags [TAG,...]          define comma separated list of tags',
        '  -l, --links [LINK ...]        define space separated list of links',
        '  -d, --digest DIGEST           idenfity content with digest',
        '  -u, --uuid UUID               idenfity content with uuid',
        '  --editor                      use vi editor to manage content',
        '  --no-editor                   do not use vi editor',
    )
    ARGS_SEARCH = (
        '  --scat [CATEGORY,...]         search keywords only from categories',
        '  --sall [KW,...]               search keywords from all fields',
        '  --stag [KW,...]               search keywords only from tags',
        '  --sgrp [KW,...]               search keywords only from groups',
        '  --filter REGEXP               filter search result with regexp',
        '  --limit INT                   maximum number of search results',
        '  --no-ansi                     remove ANSI characters from output'
    )
    ARGS_MIGRATE = (
        '  -f, --file FILE               define file for operation',
        '  --defaults                    migrate category specific defaults',
        '  --template                    migrate category specific template',
    )
    ARGS_EPILOG = (
        'symbols:',
        '    $    snippet',
        '    :    solution',
        '    >    reference',
        '    @    group',
        '    #    tag',
        '',
        'examples:',
        '    Import default content.',
        '      $ snippy import --snippets --defaults',
        '      $ snippy import --solutions --defaults',
        '      $ snippy import --references --defaults',
        '',
        '    List all snippets.',
        '      $ snippy search --snippets --sall .',
        '',
        '    List more examples.',
        '      $ snippy --help examples',
        '') + ARGS_COPYRIGHT

    ARGS_EXAMPLES = (
        'examples:',
        '    Creating new content:',
        '      $ snippy create --snippets --editor',
        '      $ snippy create --snippets -c \'docker ps\' -b \'list containers\' -t docker,moby',
        '',
        '    Searching and filtering content:',
        '      $ snippy search --snippets --sall docker,moby',
        '      $ snippy search --snippets --sall .',
        '      $ snippy search --snippets --sall . --no-ansi | grep \'\\$\' | sort',
        '      $ snippy search --solutions --sall .',
        '      $ snippy search --solutions --sall . | grep -Ev \'[^\\s]+:\'',
        '      $ snippy search --all --sall . --filter \'\\$?.*docker\'',
        '      $ snippy search --all --sall . --no-ansi | grep -E \'[0-9]+\\.\\s\'',
        '',
        '    Updating content:',
        '      $ snippy update --snippets -d 44afdd0c59e17159',
        '      $ snippy update --snippets -c \'docker ps\'',
        '',
        '    Deleting content:',
        '      $ snippy delete --snippets -d 44afdd0c59e17159',
        '      $ snippy delete --snippets -c \'docker ps\'',
        '',
        '    Migrating default content:',
        '      $ snippy import --snippets --defaults',
        '      $ snippy import --solutions --defaults',
        '      $ snippy import --references --defaults',
        '',
        '    Migrating content templates:',
        '      $ snippy export --solutions --template',
        '      $ snippy import --solutions --template',
        '      $ snippy import --solutions -f solution-template.txt',
        '',
        '    Migrating specific content:',
        '      $ snippy export -d eb792f8015ace749',
        '      $ snippy import -d eb792f8015ace749 -f howto-debug-elastic-beats.mkdn',
        '',
        '    Migrating content:',
        '      $ snippy export --snippets -f snippets.yaml',
        '      $ snippy export --snippets -f snippets.json',
        '      $ snippy export --snippets -f snippets.text',
        '      $ snippy import --snippets -f snippets.yaml',
        '      $ snippy export --solutions -f solutions.yaml',
        '      $ snippy import --solutions -f solutions.yaml',
        '') + ARGS_COPYRIGHT

    def __init__(self, args):
        super(Cli, self).__init__(self.__class__.__name__)
        if args is None:
            args = []
        args = args[1:]  # Remove the first parameter that is the program name.
        parameters = Cli._parse_args(args)
        Cli._set_editor(parameters)
        Cli._set_format(parameters)
        # CLI always updates existing content if it exit exists (merge). This
        # prevents updating empty values on top of already defined content
        # attributes from the command line. The example below allows defining
        # only tags on top of existing content tag attribute.
        #
        # The merge option has relevance in API where it allows different
        # behaviour between PUT and PATCH methods.
        #
        # $ snippy update -d f3fd167c64b6f97e --tags new,tags,from,cli
        parameters['merge'] = True
        self.init_conf(parameters)

    @staticmethod
    def _parse_args(args):  # pylint: disable=too-many-statements
        """Parse command line arguments."""

        parameters = {}
        parser = argparse.ArgumentParser(
            prog='snippy',
            add_help=False,
            usage=Cli.ARGS_USAGE,
            epilog=Const.NEWLINE.join(Cli.ARGS_EPILOG),
            formatter_class=argparse.RawTextHelpFormatter
        )

        # content options
        content = parser.add_argument_group(title='content category', description=Const.NEWLINE.join(Cli.ARGS_CATEGORY))
        content_meg = content.add_mutually_exclusive_group()
        content_meg.add_argument('--snippet', '--snippets', action='store_const', dest='category', const='snippet', help=argparse.SUPPRESS)
        content_meg.add_argument('--solution', '--solutions', action='store_const', dest='category', const='solution', help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        content_meg.add_argument('--reference', '--references', action='store_const', dest='category', const='reference', help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        content_meg.add_argument('--all', action='store_const', dest='category', const='all', help=argparse.SUPPRESS)
        content_meg.set_defaults(category=Const.SNIPPET)

        # editing options
        options = parser.add_argument_group(title='edit options', description=Const.NEWLINE.join(Cli.ARGS_EDITOR))
        options.add_argument('-c', '--content', type=Parser.to_unicode, dest='data', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('-b', '--brief', type=Parser.to_unicode, default=Const.EMPTY, help=argparse.SUPPRESS)
        options.add_argument('-g', '--groups', nargs='*', type=Parser.to_unicode, default=Const.DEFAULT_GROUPS, help=argparse.SUPPRESS)
        options.add_argument('-t', '--tags', nargs='*', type=Parser.to_unicode, default=[], help=argparse.SUPPRESS)
        options.add_argument('-l', '--links', nargs='*', type=Parser.to_unicode, default=[], help=argparse.SUPPRESS)
        options.add_argument('-d', '--digest', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('-u', '--uuid', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('--editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('--no-editor', dest='no_editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('--format', nargs='?', choices=(Const.CONTENT_FORMAT_MKDN, Const.CONTENT_FORMAT_TEXT), default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long

        # search options
        search = parser.add_argument_group(title='search options', description=Const.NEWLINE.join(Cli.ARGS_SEARCH))
        search_meg = search.add_mutually_exclusive_group()
        search_meg.add_argument('--sall', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search_meg.add_argument('--stag', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--scat', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--sgrp', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--filter', type=Parser.to_unicode, dest='search_filter', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--limit', type=int, default=Cli.LIMIT_DEFAULT_CLI, help=argparse.SUPPRESS)

        # migration options
        migrat = parser.add_argument_group(title='migration options', description=Const.NEWLINE.join(Cli.ARGS_MIGRATE))
        migrat_meg = migrat.add_mutually_exclusive_group()
        migrat_meg.add_argument('-f', '--file', type=Parser.to_unicode, dest='filename', default='', help=argparse.SUPPRESS)
        migrat_meg.add_argument('--defaults', action='store_true', default=False, help=argparse.SUPPRESS)
        migrat_meg.add_argument('--template', action='store_true', default=False, help=argparse.SUPPRESS)

        # support options
        support = parser.add_argument_group(title='support options')
        support.add_argument('-v', '--version', nargs=0, action=CustomVersionAction, help=argparse.SUPPRESS)
        support.add_argument('-vv', dest='very_verbose', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('-q', dest='quiet', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--profile', dest='profiler', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--no-ansi', dest='no_ansi', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--log-json', dest='log_json', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--log-msg-max', type=int, default=Cli.DEFAULT_LOG_MSG_MAX, help=argparse.SUPPRESS)

        # server options
        server = parser.add_argument_group(title='server options')
        server.add_argument('--server-host', type=Parser.to_unicode, dest='server_host', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-minify-json', dest='server_minify_json', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--server-app-base-path', type=Parser.to_unicode, dest='server_app_base_path', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--server-ssl-cert', type=Parser.to_unicode, dest='server_ssl_cert', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--server-ssl-key', type=Parser.to_unicode, dest='server_ssl_key', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--server-ssl-ca-cert', type=Parser.to_unicode, dest='server_ssl_ca_cert', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long

        # storage options
        server.add_argument('--storage-path', type=Parser.to_unicode, dest='storage_path', default=argparse.SUPPRESS, help=argparse.SUPPRESS) # noqa pylint: disable=line-too-long
        server.add_argument('--storage-type', type=Parser.to_unicode, dest='storage_type', choices=Const.STORAGES, default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--storage-host', type=Parser.to_unicode, dest='storage_host', default=argparse.SUPPRESS, help=argparse.SUPPRESS) # noqa pylint: disable=line-too-long
        server.add_argument('--storage-user', type=Parser.to_unicode, dest='storage_user', default=argparse.SUPPRESS, help=argparse.SUPPRESS) # noqa pylint: disable=line-too-long
        server.add_argument('--storage-password', type=Parser.to_unicode, dest='storage_password', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--storage-database', type=Parser.to_unicode, dest='storage_database', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--storage-ssl-cert', type=Parser.to_unicode, dest='storage_ssl_cert', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--storage-ssl-key', type=Parser.to_unicode, dest='storage_ssl_key', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--storage-ssl-ca-cert', type=Parser.to_unicode, dest='storage_ssl_ca_cert', default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long

        # The argparse module will exit with support options help or version
        # and when argument parsing fails. The --no-ansi flag is needed before
        # custom help action. Because of this, help and positional arguments
        # are not included when the first set of options is parsed to read the
        # needed flags for help commads.
        #
        # Positional arguments are not included into the first parsing in
        # order to get the --help <option> combination to work. The <option>
        # after the --help would be parsed as positional argument and that
        # would fail the parsing.
        try:
            parameters, _ = parser.parse_known_args(args)
            parameters = vars(parameters)

            # positional arguments
            operations = ('create', 'search', 'update', 'delete', 'export', 'import')
            parser.add_argument('operation', nargs='?', choices=operations, metavar='  {create,search,update,delete,export,import}')

            # support options
            support.add_argument('-h', '--help', nargs='?', action=CustomHelpAction, no_ansi=parameters['no_ansi'], help=argparse.SUPPRESS)

            parameters = vars(parser.parse_args(args))
            parameters['failure'] = False
        except SystemExit:
            parameters['failure'] = True

        # Print help if no parameters are provided at all.
        if not args:
            parser.print_help(sys.stdout)
            parameters['failure'] = True

        return parameters

    @staticmethod
    def _set_editor(parameters):
        """Enforce editor implicitly.

        The no-editor option always prevents implicit usage of editor.
        In other cases, editor is used by default for create and update
        operations.

        Only if user provided mandatory links for reference or data for
        other content types in create operation, editor is not used by
        default.
        """

        if parameters['failure'] or parameters['no_editor']:
            parameters['editor'] = False
            return

        if parameters['operation'] in (Cli.CREATE, Cli.UPDATE):
            if parameters['category'] == Const.REFERENCE:
                if not parameters['links']:
                    parameters['editor'] = True
            else:
                if 'data' not in parameters:
                    parameters['editor'] = True

    @staticmethod
    def _set_format(parameters):
        """Enforce editor implicitly.

        The default is text format when searching content from command line.
        All other cases default to Markdown format. If user defined the format
        option, it overrides this setting.
        """

        if parameters['failure']:
            parameters['format'] = Const.CONTENT_FORMAT_MKDN
            return

        if 'format' not in parameters and parameters['operation'] == Cli.SEARCH:
            parameters['format'] = Const.CONTENT_FORMAT_TEXT
        elif 'format' not in parameters:
            parameters['format'] = Const.CONTENT_FORMAT_MKDN


class CustomHelpAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised help action."""

    def __init__(self, *args, **kwargs):
        self._no_ansi = kwargs.pop('no_ansi', False)
        super(CustomHelpAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised help."""

        if values == 'examples':
            print(Const.NEWLINE.join(Cli.ARGS_EXAMPLES))
        elif values == 'tests':
            from snippy.devel.reference import Reference

            ansi = not self._no_ansi
            test = Reference()
            test.print_tests(ansi)
        else:
            parser.print_help()

        parser.exit()


class CustomVersionAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised version action."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised version"""

        # Argparse and Python versions below 3.4 print to stderr. In order to
        # have consistent functionality between supported Python versions, the
        # version must be explicitly printed into stdout.
        print(__version__)

        parser.exit()
