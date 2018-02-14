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

"""cli.py: CLI based content management."""

from __future__ import print_function
import sys
import argparse
from snippy.meta import __version__
from snippy.meta import __homepage__
from snippy.config.constants import Constants as Const
from snippy.config.source.base import ConfigSourceBase


class Cli(ConfigSourceBase):
    """CLI argument management."""

    ARGS_COPYRIGHT = ('Snippy version ' + __version__ + ' - license GNU AGPLv3',
                      'Copyright 2017-2018 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                      'Homepage ' + __homepage__)
    ARGS_USAGE = ('snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]')
    ARGS_CATEGO = ('  --snippet                     operate snippets (default)',
                   '  --solution                    operate solutions',
                   '  --all                         operate all content (search only)')
    ARGS_EDITOR = ('  -e, --editor                  use vi editor to add content',
                   '  -c, --content CONTENT         define example content',
                   '  -b, --brief BRIEF             define content brief description',
                   '  -g, --group GROUP             define content group',
                   '  -t, --tags [TAG,...]          define comma separated list of tags',
                   '  -l, --links [LINK ...]        define space separated list of links',
                   '  -d, --digest DIGEST           idenfity content with digest')
    ARGS_SEARCH = ('  --sall [KW,...]               search keywords from all fields',
                   '  --stag [KW,...]               search keywords only from tags',
                   '  --sgrp [KW,...]               search keywords only from groups',
                   '  --filter REGEXP               filter search output with regexp',
                   '  --no-ansi                     remove ANSI characters from output')
    ARGS_MIGRAT = ('  -f, --file FILE               define file for operation',
                   '  --defaults                    migrate category specific defaults',
                   '  --template                    migrate category specific template',)
    ARGS_EPILOG = ('symbols:',
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

    ARGS_EXAMPLES = ('examples:',
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
    def _parse_args(args):
        """Parse command line arguments."""

        parser = argparse.ArgumentParser(prog='snippy',
                                         add_help=False,
                                         usage=Cli.ARGS_USAGE,
                                         epilog=Const.NEWLINE.join(Cli.ARGS_EPILOG),
                                         formatter_class=argparse.RawTextHelpFormatter)

        # positional arguments
        operations = ('create', 'search', 'update', 'delete', 'export', 'import')
        parser.add_argument('operation', nargs='?', choices=operations, metavar='  {create,search,update,delete,export,import}')

        # content options
        content = parser.add_argument_group(title='content category', description=Const.NEWLINE.join(Cli.ARGS_CATEGO))
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

        # search options
        search = parser.add_argument_group(title='search options', description=Const.NEWLINE.join(Cli.ARGS_SEARCH))
        search_meg = search.add_mutually_exclusive_group()
        search_meg.add_argument('--sall', nargs='*', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search_meg.add_argument('--stag', nargs='*', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--sgrp', nargs='*', type=str, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--filter', type=str, dest='regexp', default=Const.EMPTY, help=argparse.SUPPRESS)

        # migration options
        migrat = parser.add_argument_group(title='migration options', description=Const.NEWLINE.join(Cli.ARGS_MIGRAT))
        migrat_meg = migrat.add_mutually_exclusive_group()
        migrat_meg.add_argument('-f', '--file', type=str, dest='filename', default='', help=argparse.SUPPRESS)
        migrat_meg.add_argument('--defaults', action='store_true', default=False, help=argparse.SUPPRESS)
        migrat_meg.add_argument('--template', action='store_true', default=False, help=argparse.SUPPRESS)

        # support options
        support = parser.add_argument_group(title='support options')
        support.add_argument('-h', '--help', nargs=0, action=CustomHelpAction, help=argparse.SUPPRESS)
        support.add_argument('-v', '--version', nargs=0, action=CustomVersionAction, help=argparse.SUPPRESS)
        support.add_argument('-vv', dest='very_verbose', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('-q', dest='quiet', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--profile', dest='profiler', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--no-ansi', dest='no_ansi', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--json-logs', dest='json_logs', action='store_true', default=False, help=argparse.SUPPRESS)

        # server options
        server = parser.add_argument_group(title='server options')
        server.add_argument('--server', action='store_true', default=False, help=argparse.SUPPRESS)
        server.add_argument('--base-path', type=str, dest='base_path', default=Cli.BASE_PATH, help=argparse.SUPPRESS)
        server.add_argument('--ip', type=str, dest='server_ip', default=Cli.SERVER_IP, help=argparse.SUPPRESS)
        server.add_argument('--port', type=str, dest='server_port', default=Cli.SERVER_PORT, help=argparse.SUPPRESS)

        # storage options
        server.add_argument('--storage-path', type=str, dest='storage_path', default=Const.EMPTY, help=argparse.SUPPRESS)

        # Argparse will exit with support options like --help or --version and
        # when argument parsing fails. Catching the exception here allows the
        # tool to exit in controlled manner and release pending resources.
        parameters = {}
        try:
            parameters = vars(parser.parse_args(args))
            parameters['exit'] = False
        except SystemExit:
            parameters['exit'] = True

        return parameters

    @staticmethod
    def _set_editor(parameters):
        """Enforce editor usage for some operations for better usability."""

        if parameters['exit']:
            return

        if parameters['category'] == Const.SNIPPET and parameters['operation'] == Cli.UPDATE:
            parameters['editor'] = True

        if parameters['category'] == Const.SOLUTION and (Cli.CREATE or Cli.UPDATE in parameters['operation']):
            parameters['editor'] = True


class CustomHelpAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised argparse help to print examples."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised example printing to override positional arguments."""

        if option_string == '-h' or option_string == '--help':
            if 'examples' in sys.argv:
                print(Const.NEWLINE.join(Cli.ARGS_EXAMPLES))
            elif 'tests' in sys.argv:
                from snippy.devel.reference import Reference
                ansi = True if '--no-ansi' not in sys.argv else False
                test = Reference()
                test.print_tests(ansi)
            else:
                parser.print_help()

        parser.exit()


class CustomVersionAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised argparse action class to print version always to stdout."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised printing"""

        # Argparse and Python versions below 3.4 print to stderr. In order
        # to have consistent functionality between supported Python versions,
        # the version must be explicitly printed to stdout.
        if option_string == '-v' or option_string == '--version':
            print(__version__)

        parser.exit()
