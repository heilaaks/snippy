#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""cli: CLI based content management."""

from __future__ import print_function

import sys
import argparse

from snippy.constants import Constants as Const
from snippy.config.source.base import ConfigSourceBase
from snippy.logger import Logger
from snippy.meta import __homepage__
from snippy.meta import __version__


class Cli(ConfigSourceBase):
    """CLI argument management."""

    ARGS_COPYRIGHT = (
        'Snippy version ' + __version__ + ' - license GNU AGPLv3 or later',
        'Copyright 2017-2018 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
        'Homepage ' + __homepage__
    )
    ARGS_USAGE = ('snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]')
    ARGS_CATEGORY = (
        '  --snippet                     operate snippets (default)',
        '  --solution                    operate solutions',
        '  --all                         operate all content (search only)'
    )
    ARGS_EDITOR = (
        '  -e, --editor                  use vi editor to add content',
        '  -c, --content CONTENT         define example content',
        '  -b, --brief BRIEF             define content brief description',
        '  -g, --group GROUP             define content group',
        '  -t, --tags [TAG,...]          define comma separated list of tags',
        '  -l, --links [LINK ...]        define space separated list of links',
        '  -d, --digest DIGEST           idenfity content with digest'
    )
    ARGS_SEARCH = (
        '  --sall [KW,...]               search keywords from all fields',
        '  --stag [KW,...]               search keywords only from tags',
        '  --sgrp [KW,...]               search keywords only from groups',
        '  --filter REGEXP               filter search output with regexp',
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
        '    @    group',
        '    #    tag',
        '    >    url',
        '',
        'examples:',
        '    Import default content.',
        '      $ snippy import --snippet --defaults',
        '      $ snippy import --solution --defaults',
        '',
        '    List all snippets.',
        '      $ snippy search --snippet --sall .',
        '',
        '    List more examples.',
        '      $ snippy --help examples',
        '') + ARGS_COPYRIGHT

    ARGS_EXAMPLES = (
        'examples:',
        '    Creating new content:',
        '      $ snippy create --snippet --editor',
        '      $ snippy create --snippet -c \'docker ps\' -b \'list containers\' -t docker,moby',
        '',
        '    Searching and filtering content:',
        '      $ snippy search --snippet --sall docker,moby',
        '      $ snippy search --snippet --sall .',
        '      $ snippy search --snippet --sall . --no-ansi | grep \'\\$\' | sort',
        '      $ snippy search --solution --sall .',
        '      $ snippy search --solution --sall . | grep -Ev \'[^\\s]+:\'',
        '      $ snippy search --all --sall . --filter \'.*(\\$\\s.*)\'',
        '      $ snippy search --all --sall . --no-ansi | grep -E \'[0-9]+\\.\\s\'',
        '',
        '    Updating content:',
        '      $ snippy update --snippet -d 44afdd0c59e17159',
        '      $ snippy update --snippet -c \'docker ps\'',
        '',
        '    Deleting content:',
        '      $ snippy delete --snippet -d 44afdd0c59e17159',
        '      $ snippy delete --snippet -c \'docker ps\'',
        '',
        '    Migrating default content:',
        '      $ snippy import --snippet --defaults',
        '      $ snippy import --solution --defaults',
        '',
        '    Migrating content templates:',
        '      $ snippy export --solution --template',
        '      $ snippy import --solution --template',
        '      $ snippy import --solution -f solution-template.txt',
        '',
        '    Migrating specific content:',
        '      $ snippy export -d 76a1a02951f6bcb4',
        '      $ snippy import -d 76a1a02951f6bcb4 -f howto-debug-elastic-beats.txt',
        '',
        '    Migrating content:',
        '      $ snippy export --snippet -f snippets.yaml',
        '      $ snippy export --snippet -f snippets.json',
        '      $ snippy export --snippet -f snippets.text',
        '      $ snippy import --snippet -f snippets.yaml',
        '      $ snippy export --solution -f solutions.yaml',
        '      $ snippy import --solution -f solutions.yaml',
        '') + ARGS_COPYRIGHT

    def __init__(self, args):
        super(Cli, self).__init__()
        if args is None:
            args = []
        args = args[1:]  # Remove the first parameter that is the program name.
        parameters = Cli._parse_args(args)
        Cli._set_editor(parameters)
        self.set_conf(parameters)

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
        content_meg.add_argument('--snippet', action='store_const', dest='category', const='snippet', help=argparse.SUPPRESS)
        content_meg.add_argument('--solution', action='store_const', dest='category', const='solution', help=argparse.SUPPRESS)
        content_meg.add_argument('--all', action='store_const', dest='category', const='all', help=argparse.SUPPRESS)
        content_meg.set_defaults(category='snippet')

        # editing options
        options = parser.add_argument_group(title='edit options', description=Const.NEWLINE.join(Cli.ARGS_EDITOR))
        options.add_argument('-e', '--editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('-c', '--content', type=str, dest='data', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('-b', '--brief', type=str, default=Const.EMPTY, help=argparse.SUPPRESS)
        options.add_argument('-g', '--group', type=str, default=Const.DEFAULT_GROUP, help=argparse.SUPPRESS)
        options.add_argument('-t', '--tags', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        options.add_argument('-l', '--links', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        options.add_argument('-d', '--digest', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('--merge', action='store_true', default=False, help=argparse.SUPPRESS)

        # search options
        search = parser.add_argument_group(title='search options', description=Const.NEWLINE.join(Cli.ARGS_SEARCH))
        search_meg = search.add_mutually_exclusive_group()
        search_meg.add_argument('--sall', nargs='*', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search_meg.add_argument('--stag', nargs='*', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--sgrp', nargs='*', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--filter', type=str, dest='regexp', default=Const.EMPTY, help=argparse.SUPPRESS)

        # migration options
        migrat = parser.add_argument_group(title='migration options', description=Const.NEWLINE.join(Cli.ARGS_MIGRATE))
        migrat_meg = migrat.add_mutually_exclusive_group()
        migrat_meg.add_argument('-f', '--file', type=str, dest='filename', default='', help=argparse.SUPPRESS)
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
        support.add_argument('--log-msg-max', nargs=1, type=int, default=Logger.DEFAULT_LOG_MSG_MAX, help=argparse.SUPPRESS)

        # server options
        server = parser.add_argument_group(title='server options')
        server.add_argument('--server', action='store_true', default=False, help=argparse.SUPPRESS)
        server.add_argument('--base-path-app', type=str, dest='base_path_app', default=Cli.BASE_PATH_APP, help=argparse.SUPPRESS)
        server.add_argument('--ip', type=str, dest='server_ip', default=Cli.SERVER_IP, help=argparse.SUPPRESS)
        server.add_argument('--port', type=str, dest='server_port', default=Cli.SERVER_PORT, help=argparse.SUPPRESS)
        server.add_argument('--compact-json', dest='compact_json', action='store_true', default=False, help=argparse.SUPPRESS)
        server.add_argument('--ssl-cert', type=str, dest='ssl_cert', default=None, help=argparse.SUPPRESS)
        server.add_argument('--ssl-key', type=str, dest='ssl_key', default=None, help=argparse.SUPPRESS)
        server.add_argument('--ssl-ca-cert', type=str, dest='ssl_ca_cert', default=None, help=argparse.SUPPRESS)

        # storage options
        server.add_argument('--storage-path', type=str, dest='storage_path', default=Const.EMPTY, help=argparse.SUPPRESS)

        # The argparse module will exit with support options help or version
        # and when argument parsing fails. The --no-ansi flag is needed before
        # custom help action. Because of this, help and positional arguments
        # are not included when the first set of options is parsed.
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
        """Enforce editor usage for some operations for better usability."""

        if parameters['failure']:
            return

        if parameters['category'] == Const.SNIPPET and parameters['operation'] == Cli.UPDATE:
            parameters['editor'] = True

        if parameters['category'] == Const.SOLUTION and (Cli.CREATE or Cli.UPDATE in parameters['operation']):
            parameters['editor'] = True


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
