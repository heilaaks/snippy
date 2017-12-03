#!/usr/bin/env python3

"""cli.py: Command line argument management."""

from __future__ import print_function
import sys
import argparse
from snippy.version import __version__
from snippy.config.constants import Constants as Const
from snippy.config.source.base import ConfigSourceBase


class Cli(ConfigSourceBase):
    """Command line argument management."""

    ARGS_COPYRIGHT = ('Snippy version ' + __version__ + ' - license Apache 2.0',
                      'Copyright 2017 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                      'Homepage https://github.com/heilaaks/snippy')
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

    def __init__(self):
        super(Cli, self).__init__()
        parameters = Cli._parse_args()
        self._set_conf(parameters)
        self._set_self()

    @staticmethod
    def _parse_args():
        """Parse command line arguments."""

        parser = argparse.ArgumentParser(prog='snippy',
                                         add_help=False,
                                         usage=Cli.ARGS_USAGE,
                                         epilog=Const.NEWLINE.join(Cli.ARGS_EPILOG),
                                         formatter_class=argparse.RawTextHelpFormatter)

        # positional arguments
        operations = ('create', 'search', 'update', 'delete', 'export', 'import')
        parser.add_argument('operation', choices=operations, metavar='  {create,search,update,delete,export,import}')

        # content options
        content = parser.add_argument_group(title='content category', description=Const.NEWLINE.join(Cli.ARGS_CATEGO))
        content_meg = content.add_mutually_exclusive_group()
        content_meg.add_argument('--snippet', action='store_const', dest='cat', const='snippet', help=argparse.SUPPRESS)
        content_meg.add_argument('--solution', action='store_const', dest='cat', const='solution', help=argparse.SUPPRESS)
        content_meg.add_argument('--all', action='store_const', dest='cat', const='all', help=argparse.SUPPRESS)
        content_meg.set_defaults(cat='snippet')

        # editing options
        options = parser.add_argument_group(title='edit options', description=Const.NEWLINE.join(Cli.ARGS_EDITOR))
        options.add_argument('-e', '--editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('-c', '--content', type=str, dest='data', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('-b', '--brief', type=str, default=Const.EMPTY, help=argparse.SUPPRESS)
        options.add_argument('-g', '--group', type=str, default=Const.DEFAULT_GROUP, help=argparse.SUPPRESS)
        options.add_argument('-t', '--tags', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        options.add_argument('-l', '--links', type=str, default=Const.EMPTY, help=argparse.SUPPRESS)
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
        support.add_argument('-h', '--help', nargs=0, action=MyHelpAction, help=argparse.SUPPRESS)
        support.add_argument('-v', '--version', nargs=0, action=MyVersionAction, help=argparse.SUPPRESS)
        support.add_argument('-vv', dest='very_verbose', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('-q', dest='quiet', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--profile', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--no-ansi', dest='no_ansi', action='store_true', default=False, help=argparse.SUPPRESS)

        # server options
        server = parser.add_argument_group(title='server options')
        server.add_argument('--server', action='store_true', default=False, help=argparse.SUPPRESS)

        # Argparse will exit in case of support options like --help or --version.
        # Also in case of argument parse failures the SystemExit is made.
        parameters = vars(parser.parse_args())

        return parameters


class MyHelpAction(argparse.Action):  # pylint: disable=too-few-public-methods
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


class MyVersionAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised argparse action class to print version always to stdout."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised printing"""

        # Argparse and Python versions below 3.4 print to stderr. In order
        # to have consistent functionality between supported Python versions,
        # the version must be explicitly printed to stdout.
        if option_string == '-v' or option_string == '--version':
            print(__version__)

        parser.exit()
