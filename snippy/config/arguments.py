#!/usr/bin/env python3

"""arguments.py: Command line argument management."""

import sys
import argparse
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.version import __version__


class Arguments(object):
    """Command line argument management."""

    args = {}
    logger = {}

    ARGS_COPYRIGHT = ('Snippy version ' + __version__ + ' - license Apache 2.0',
                      'Copyright 2017 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                      'Homepage https://github.com/heilaaks/snippy')
    ARGS_USAGE = ('snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]')
    ARGS_CATEGO = ('  --snippet                     operate snippets (default)',
                   '  --solution                    operate solutions',
                   '  --all                         operate all content (search only)')
    ARGS_EDITOR = ('  -e, --editor                  use vi editor to add content',
                   '  -f, --file FILE               define file for operation',
                   '  -c, --content CONTENT         define example content',
                   '  -b, --brief BRIEF             define content brief description',
                   '  -g, --group GROUP             define content group',
                   '  -t, --tags [TAG,...]          define comma separated list of tags',
                   '  -l, --links [LINK ...]        define space separated list of links',
                   '  -d, --digest DIGEST           idenfity content with digest')
    ARGS_SEARCH = ('  --sall [KW,...]               search keywords from all fields',
                   '  --stag [KW,...]               search keywords only from tags',
                   '  --sgrp [KW,...]               search keywords only from groups',
                   '  --filter REGEXP               filter search output with regexp')
    ARGS_MIGRAT = ('  -f, --file FILE               define file for operation',
                   '  --template FILE               create template for defined content')
    ARGS_EPILOG = ('symbols:',
                   '    $    snippet',
                   '    :    solution',
                   '    @    group',
                   '    #    tag',
                   '    >    url',
                   '',
                   'examples:',
                   '    Import default content.',
                   '      $ snippy import --snippet -f defaults',
                   '      $ snippy import --solution -f defaults',
                   '',
                   '    List all snippets.',
                   '      $ snippy search --snippet --sall .',
                   '',
                   '    List more examples.',
                   '      $ snippy --help examples',
                   '') + ARGS_COPYRIGHT

    ARGS_EXAMPLES = ('examples:',
                     '    Creating new content.',
                     '      $ snippy create --snippet --editor',
                     '      $ snippy create --snippet -c \'docker ps\' -b \'list containers\' -t docker,moby',
                     '',
                     '    Searching and filtering content.',
                     '      $ snippy search --snippet --sall docker,moby',
                     '      $ snippy search --snippet --sall .',
                     '      $ snippy search --snippet --sall . | grep --color=never \'\\$\'',
                     '      $ snippy search --solution --sall .',
                     '      $ snippy search --solution --sall . | grep -Ev \'[^\\s]+:\'',
                     '      $ snippy search --all --sall . --filter \'.*(\\$\\s.*)\'',
                     '',
                     '    Updating content.',
                     '      $ snippy update --snippet -d b26daeda142cf1ed',
                     '      $ snippy update --snippet -c \'docker rm --volumes $(docker ps --all --quiet)\'',
                     '',
                     '    Deleting content.',
                     '      $ snippy delete --snippet -d b26daeda142cf1ed',
                     '      $ snippy delete --snippet -c \'docker rm --volumes $(docker ps --all --quiet)\'',
                     '',
                     '    Migrating content.',
                     '      $ snippy export --snippet -f snippets.yaml',
                     '      $ snippy export --snippet -f snippets.json',
                     '      $ snippy export --snippet -f snippets.text',
                     '      $ snippy import --snippet -f snippets.yaml',
                     '      $ snippy export --solution -f contents.yaml',
                     '      $ snippy import --solution -f contents.yaml',
                     '') + ARGS_COPYRIGHT

    def __init__(self):
        Arguments.logger = Logger(__name__).get()

        parser = argparse.ArgumentParser(prog='snippy',
                                         add_help=False,
                                         usage=Arguments.ARGS_USAGE,
                                         epilog=Const.NEWLINE.join(Arguments.ARGS_EPILOG),
                                         formatter_class=argparse.RawTextHelpFormatter)

        # positional arguments
        operations = ('create', 'search', 'update', 'delete', 'export', 'import')
        parser.add_argument('operation', choices=operations, metavar='  {create,search,update,delete,export,import}')

        # content options
        content = parser.add_argument_group(title='content category', description=Const.NEWLINE.join(Arguments.ARGS_CATEGO))
        content_meg = content.add_mutually_exclusive_group()
        content_meg.add_argument('--snippet', action='store_const', dest='cat', const='snippets', help=argparse.SUPPRESS)
        content_meg.add_argument('--solution', action='store_const', dest='cat', const='solutions', help=argparse.SUPPRESS)
        content_meg.add_argument('--all', action='store_const', dest='cat', const='all', help=argparse.SUPPRESS)
        content_meg.set_defaults(cat='snippets')

        # editing options
        options = parser.add_argument_group(title='edit options', description=Const.NEWLINE.join(Arguments.ARGS_EDITOR))
        options.add_argument('-e', '--editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('-f', '--file', type=str, default='', help=argparse.SUPPRESS)
        options.add_argument('-c', '--content', type=str, default='', help=argparse.SUPPRESS)
        options.add_argument('-b', '--brief', type=str, default='', help=argparse.SUPPRESS)
        options.add_argument('-g', '--group', type=str, default=Const.DEFAULT_GROUP, help=argparse.SUPPRESS)
        options.add_argument('-t', '--tags', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        options.add_argument('-l', '--links', type=str, default='', help=argparse.SUPPRESS)
        options.add_argument('-d', '--digest', type=str, default='', help=argparse.SUPPRESS)

        # search options
        search = parser.add_argument_group(title='search options', description=Const.NEWLINE.join(Arguments.ARGS_SEARCH))
        search_meg = search.add_mutually_exclusive_group()
        search_meg.add_argument('--sall', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        search_meg.add_argument('--stag', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        search_meg.add_argument('--sgrp', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        search.add_argument('--filter', type=str, dest='regexp', default='', help=argparse.SUPPRESS)

        # migration options
        migrat = parser.add_argument_group(title='migration options', description=Const.NEWLINE.join(Arguments.ARGS_MIGRAT))
        migrat.add_argument('--template', type=argparse.FileType('w'), help=argparse.SUPPRESS)

        # support options
        support = parser.add_argument_group(title='support options')
        support.add_argument('-h', '--help', nargs=0, action=MyHelpAction, help=argparse.SUPPRESS)
        support.add_argument('-v', '--version', action='version', version=__version__, help=argparse.SUPPRESS)
        support.add_argument('-vv', dest='very_verbose', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('-q', dest='quiet', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        support.add_argument('--profile', action='store_true', default=False, help=argparse.SUPPRESS)

        Arguments.args = parser.parse_args()

    @classmethod
    def get_operation(cls):
        """Return the requested operation for the content."""

        cls.logger.info('parsed positional argument with value "%s"', cls.args.operation)

        return cls.args.operation

    @classmethod
    def get_content_category(cls):
        """Return content category."""

        cls.logger.info('parsed content category with value "%s"', cls.args.cat)

        return cls.args.cat

    @classmethod
    def get_content_data(cls):
        """Return content data."""

        cls.logger.info('parsed argument --content with value "%s"', cls.args.content)

        return cls.args.content

    @classmethod
    def get_content_brief(cls):
        """Return content brief description."""

        cls.logger.info('parsed argument --brief with value "%s"', cls.args.brief)

        return cls.args.brief

    @classmethod
    def get_content_group(cls):
        """Return content group."""

        cls.logger.info('parsed argument --group with value "%s"', cls.args.group)

        return cls.args.group

    @classmethod
    def get_content_tags(cls):
        """Return content tags."""

        cls.logger.info('parsed argument --tags with value %s', cls.args.tags)

        return cls.args.tags

    @classmethod
    def get_content_links(cls):
        """Return content reference links."""

        cls.logger.info('parsed argument --links with value "%s"', cls.args.links)

        return cls.args.links

    @classmethod
    def get_content_digest(cls):
        """Return digest identifying the content."""

        cls.logger.info('parsed argument --digest with value "%s"', cls.args.digest)

        return cls.args.digest

    @classmethod
    def get_search_all(cls):
        """Return keywords to search from all fields."""

        cls.logger.info('parsed argument --sall with value %s', cls.args.sall)

        return cls.args.sall

    @classmethod
    def get_search_tag(cls):
        """Return keywords to search only from tags."""

        cls.logger.info('parsed argument --stag with value %s', cls.args.stag)

        return cls.args.stag

    @classmethod
    def get_search_grp(cls):
        """Return keywords to search only from groups."""

        cls.logger.info('parsed argument --sgrp with value %s', cls.args.sgrp)

        return cls.args.sgrp

    @classmethod
    def get_search_filter(cls):
        """Return regexp filter for search output."""

        cls.logger.info('parsed argument --filter with value %s', cls.args.regexp)

        return cls.args.regexp

    @classmethod
    def get_editor(cls):
        """Return the usage of editor for the operation."""

        return cls.args.editor

    @classmethod
    def get_operation_file(cls):
        """Return file for operation."""

        cls.logger.info('parsed argument --file with value "%s"', cls.args.file)

        return cls.args.file


class MyHelpAction(argparse.Action): # pylint: disable=too-few-public-methods
    """Customised argparse help to print examples."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised example printing to override positional arguments."""

        if option_string == '-h' or option_string == '--help':
            if 'examples' not in sys.argv:
                parser.print_help()
            else:
                print(Const.NEWLINE.join(Arguments.ARGS_EXAMPLES))

        parser.exit()
