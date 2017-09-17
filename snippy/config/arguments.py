#!/usr/bin/env python3

"""arguments.py: Command line argument management."""

import os
import argparse
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.version import __version__


class Arguments(object):
    """Command line argument management."""

    args = {}
    logger = {}

    ARGS_USAGE = ('snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]')
    ARGS_CONTENT = ('  --snippet                     operate snippets (default)',
                    '  --solution                    operate solutions',
                    '  --all                         operate all content')
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
                   '  --sgrp [KW,...]               search keywords only from groups')
    ARGS_IMPEXP = ('  -f, --file FILE               define file for operation',
                   '  --template FILE               create template for defined content')
    ARGS_EPILOG = ('symbols:',
                   '    $    command',
                   '    >    url',
                   '    #    tag',
                   '    @    group',
                   '',
                   'examples:',
                   '    Creating new snippets.',
                   '      $ snippy create --snippet --editor',
                   '      $ snippy create -c \'docker ps\' -b \'list containers\' -t docker,moby',
                   '',
                   '    Search snippets with keyword list.',
                   '      $ snippy search --snippet --sall docker,moby',
                   '',
                   '    Export all snippets in yaml format.',
                   '      $ snippy export --snippet -f snippets.yaml',
                   '',
                   '    Delete snippet with message digest.',
                   '      $ snippy delete --snippet -d b26daeda142cf1ed',
                   '',
                   'Snippy version ' + __version__ + ' - license Apache 2.0',
                   'Copyright 2017 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                   'Homepage https://github.com/heilaaks/snippy',
                   '')

    def __init__(self):
        Arguments.logger = Logger(__name__).get()

        parser = argparse.ArgumentParser(prog='snippy', add_help=False,
                                         usage=Arguments.ARGS_USAGE,
                                         epilog=Const.NEWLINE.join(Arguments.ARGS_EPILOG),
                                         formatter_class=argparse.RawTextHelpFormatter)

        # positional arguments
        operations = ('create', 'search', 'update', 'delete', 'export', 'import')
        parser.add_argument('operation', choices=operations, metavar='  {create,search,update,delete,export,import}')

        # content options
        content = parser.add_argument_group(title='content options', description=Const.NEWLINE.join(Arguments.ARGS_CONTENT))
        content_meg = content.add_mutually_exclusive_group()
        content_meg.add_argument('--snippet', action='store_const', dest='type', const='snippet', help=argparse.SUPPRESS)
        content_meg.add_argument('--solution', action='store_const', dest='type', const='solution', help=argparse.SUPPRESS)
        content_meg.add_argument('--all', action='store_const', dest='type', const='all', help=argparse.SUPPRESS)
        content_meg.set_defaults(type='snippet')

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

        # import/export options
        template = parser.add_argument_group(title='export options', description=Const.NEWLINE.join(Arguments.ARGS_IMPEXP))
        template.add_argument('--template', type=argparse.FileType('w'), help=argparse.SUPPRESS)

        # support options
        support = parser.add_argument_group(title='support options')
        support.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
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
    def get_content_type(cls):
        """Return content type."""

        cls.logger.info('parsed content type with value "%s"', cls.args.type)

        return cls.args.type

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
    def get_operation_digest(cls):
        """Return digest identifying the operation target."""

        cls.logger.info('parsed argument --digest with value "%s"', cls.args.digest)

        return cls.args.digest

    @classmethod
    def get_search_all(cls):
        """Return keywords to search from all fields."""

        cls.logger.info('parsed argument --sall with value %s', cls.args.sall)

        return cls.args.sall

    @classmethod
    def get_search_grp(cls):
        """Return keywords to search only from groups."""

        cls.logger.info('parsed argument --sgrp with value %s', cls.args.sgrp)

        return cls.args.sgrp

    @classmethod
    def get_search_tag(cls):
        """Return keywords to search only from tags."""

        cls.logger.info('parsed argument --stag with value %s', cls.args.stag)

        return cls.args.stag

    @classmethod
    def get_editor(cls):
        """Return the usage of editor for the operation."""

        return cls.args.editor

    @classmethod
    def get_editor_content(cls, snippet):
        """Return the edited content from editor."""

        import tempfile
        from subprocess import call

        # If the group is in default value, don't show it to end user
        # since it may be confusing. If there is no input for the group
        # the default is set back.
        edited_message = Const.EMPTY
        content = Const.DELIMITER_CONTENT.join(map(str, snippet[Const.SNIPPET_CONTENT]))
        brief = snippet[Const.SNIPPET_BRIEF] + Const.NEWLINE
        if snippet[Const.SNIPPET_GROUP] == Const.DEFAULT_GROUP:
            group = Const.EMPTY + Const.NEWLINE
        else:
            group = snippet[Const.SNIPPET_GROUP] + Const.NEWLINE
        tags = Const.DELIMITER_TAGS.join(snippet[Const.SNIPPET_TAGS]) + Const.NEWLINE
        links = Const.DELIMITER_NEWLINE.join(snippet[Const.SNIPPET_LINKS]) + Const.NEWLINE
        default_editor = os.environ.get('EDITOR', 'vi')
        editor_template = ('# Commented lines will be ignored.\n'
                           '#\n' +
                           Const.EDITOR_CONTENT_HEAD +
                           content + Const.NEWLINE * 2 +
                           Const.EDITOR_BRIEF_HEAD +
                           brief + '\n' +
                           Const.EDITOR_GROUP_HEAD +
                           group + '\n' +
                           Const.EDITOR_TAGS_HEAD +
                           tags + '\n' +
                           Const.EDITOR_LINKS_HEAD +
                           links + '\n').encode('UTF-8')

        with tempfile.NamedTemporaryFile(prefix='snippy-edit-') as outfile:
            outfile.write(editor_template)
            outfile.flush()
            call([default_editor, outfile.name])
            outfile.seek(0)
            edited_message = outfile.read()

        return edited_message.decode('UTF-8')

    @classmethod
    def get_operation_file(cls):
        """Return file for operation."""

        cls.logger.info('parsed argument --file with value "%s"', cls.args.file)

        return cls.args.file
