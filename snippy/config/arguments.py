#!/usr/bin/env python3

"""arguments.py: Command line argument management."""

import os
import argparse
from snippy.config import Constants as Const
from snippy.logger import Logger
from pkg_resources import get_distribution


class Arguments(object):
    """Command line argument management."""

    args = {}
    logger = {}
    version = get_distribution('snippy').version

    ARGS_MANAGE = ('snippy [-v, --version] [-h, --help] <command> [<options>] [--debug]')
    ARGS_EDITOR = ('  --snippet                     operate snippets [default: true]',
                   '  --resolution                  operate resolutions [default: false]',
                   '  -e, --editor                  use vi editor to add content',
                   '  -f, --file FILE               use input file to add content',
                   '  -c, --content CONTENT         define example content',
                   '  -b, --brief BRIEF             define content brief description',
                   '  -l, --link LINK               define content reference link',
                   '  -g, --group GROUP             define content category',
                   '  -t, --tags [TAGS ...]         define tags for content',
                   '  -d, --digest DIGEST           idenfity content with digest')
    ARGS_SEARCH = ('  --sall                        search from all fields',
                   '  --stag                        search only from tags',
                   '  --sgrp                        search only from groups')
    ARGS_EPILOG = ('symbols:',
                   '    $    command',
                   '    >    url',
                   '    #    tag',
                   '    @    category',
                   '',
                   'examples:',
                   '    Creating new snippets.',
                   '      $ snippy create --editor',
                   '      $ snippy create --snippet --editor',
                   '      $ snippy create -c \'docker ps\' -b \'list containers\' -t docker,moby',
                   '',
                   '    Search snippets with keyword list.',
                   '      $ snippy search --snippet -sall docker,moby',
                   '',
                   '    Delete snippet with message digest.',
                   '      $ snippy delete --snippet -d 2dcbecd10330ac4d',
                   '',
                   '    Export all snippets in yaml format.',
                   '      $ snippy export --snippet -f snippets.yaml',
                   '',
                   'Snippy version ' + get_distribution('snippy').version + ' - license MIT',
                   'Copyright 2017 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                   'Homepage https://github.com/heilaaks/snippy',
                   '')

    def __init__(self):
        Arguments.logger = Logger(__name__).get()

        #parser = argparse.ArgumentParser(prog='snippy', add_help=False,
        #                                 usage=Arguments.ARGS_MANAGE,
        #                                 epilog=Const.NEWLINE.join(Arguments.ARGS_EPILOG),
        #                                 formatter_class=argparse.RawTextHelpFormatter)

        ## positional arguments
        #commands = ('create', 'search', 'update', 'delete', 'export', 'import')
        #parser.add_argument('command', choices=commands, metavar='  {create,search,update,delete,export,import}')

        ## content options
        #content = parser.add_mutually_exclusive_group()
        #content.add_argument('--snippet', action='store_true', help=argparse.SUPPRESS)
        #content.add_argument('--resolution', action='store_true', help=argparse.SUPPRESS)

        ## editing arguments
        #options = parser.add_argument_group(title='edit options', description=Const.NEWLINE.join(Arguments.ARGS_EDITOR))
        #options.add_argument('-e', '--editor', action='store_true', default=False, help=argparse.SUPPRESS)
        #options.add_argument('-f', '--file', type=str, default='', help=argparse.SUPPRESS)
        #options.add_argument('-d', '--digest', type=str, default='', help=argparse.SUPPRESS)
        #options.add_argument('-c', '--content', type=str, default='', help=argparse.SUPPRESS)
        #options.add_argument('-b', '--brief', type=str, default='', help=argparse.SUPPRESS)
        #options.add_argument('-g', '--group', type=str, default='', help=argparse.SUPPRESS)
        #options.add_argument('-t', '--tags', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        #options.add_argument('-l', '--links', type=str, default='', help=argparse.SUPPRESS)

        ## search options
        #search = parser.add_argument_group(title='search options', description=Const.NEWLINE.join(Arguments.ARGS_SEARCH))
        #search.add_argument('--sany', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        #search.add_argument('--stag', nargs='*', type=str, default=[], help=argparse.SUPPRESS)
        #search.add_argument('--sgrp', nargs='*', type=str, default=[], help=argparse.SUPPRESS)

        ## support options
        #support = parser.add_argument_group(title='support options')
        #support.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
        #support.add_argument('-v', '--version', action='version', version=Arguments.version, help=argparse.SUPPRESS)
        #support.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        #support.add_argument('--profile', action='store_true', default=False, help=argparse.SUPPRESS)
        #support.add_argument('-q', dest='quiet', action='store_true', default=False, help=argparse.SUPPRESS)

        #Arguments.args = parser.parse_args()
        #print("test %s" % Arguments.args)

        parser = argparse.ArgumentParser()
        job_roles = ['snippet', 'resolve']
        jobs = ['create', 'search', 'update', 'delete', 'import', 'export']
        job_type = parser.add_argument_group('MANDATORY JOB OPTIONS')
        job_type.add_argument('-r', '--role', type=str, choices=job_roles, default=job_roles[0], help='define job role')
        job_type.add_argument('-j', '--job', type=str, choices=jobs, default=jobs[0], help='define job')

        job_service = parser.add_argument_group('OPTIONAL SERVICES')
        job_service.add_argument('--editor', action='store_true', default=False, help='use default editor')
        job_service.add_argument('--file', type=str, default='', help='use input file')
        job_service.add_argument('--id', type=str, default='', help='set identity of an item')

        job_args = parser.add_argument_group('OPTIONAL ARGUMENTS')
        job_args.add_argument('-i', '--input', dest='content', type=str, default='', help='input content')
        job_args.add_argument('-b', '--brief', type=str, default='', help='brief description ot the input')
        job_args.add_argument('-c', '--category', type=str, default='', help='category for the input')
        job_args.add_argument('-t', '--tags', nargs='*', type=str, default=[], help='tags for the input')
        job_args.add_argument('-l', '--links', type=str, default='', help='links for more information')

        job_search = parser.add_argument_group('SEARCH OPTIONS')
        job_search.add_argument('-s', '--search', nargs='*', type=str, default=[], help='search with keywords')

        parser.add_argument('--profile', action='store_true', default=False, help=argparse.SUPPRESS)
        parser.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        Arguments.args = parser.parse_args()

    @classmethod
    def get_job(cls):
        """Return the job that user defined."""

        cls.logger.info('parsed argument --job with value "%s"', cls.args.job)

        return cls.args.job

    @classmethod
    def get_job_role(cls):
        """Return the job role that user defined."""

        cls.logger.info('parsed argument --role with value "%s"', cls.args.role)

        return cls.args.role

    @classmethod
    def get_editor(cls):
        """Return the usage of supplementary editor for the job."""

        return cls.args.editor

    @classmethod
    def get_editor_content(cls, snippet):
        """Return the edited content."""

        import tempfile
        from subprocess import call

        edited_message = ''
        content = snippet['content'] + Const.NEWLINE
        brief = snippet['brief'] + Const.NEWLINE
        category = snippet['category'] + Const.NEWLINE
        tags = Const.DELIMITER_TAGS.join(snippet['tags']) + Const.NEWLINE
        links = Const.DELIMITER_NEWLINE.join(snippet['links']) + Const.NEWLINE
        default_editor = os.environ.get('EDITOR', 'vi')
        editor_template = ('# Commented lines will be ignored.\n'
                           '#\n' +
                           Const.EDITOR_SNIPPET_HEAD +
                           content + '\n' +
                           Const.EDITOR_BRIEF_HEAD +
                           brief + '\n' +
                           Const.EDITOR_CATEGORY_HEAD +
                           category + '\n' +
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
    def get_file(cls):
        """Return the supplementary file for the job."""

        cls.logger.info('parsed argument --file with value "%s"', cls.args.file)

        return cls.args.file

    @classmethod
    def get_id(cls):
        """Return the supplementary if for the job."""

        cls.logger.info('parsed argument --id with value "%s"', cls.args.id)

        return cls.args.id

    @classmethod
    def get_content(cls):
        """Return supplementary content for the job."""

        cls.logger.info('parsed argument --input with value "%s"', cls.args.content)

        return cls.args.content

    @classmethod
    def get_brief(cls):
        """Return supplementary brief description."""

        cls.logger.info('parsed argument --brief with value "%s"', cls.args.brief)

        return cls.args.brief

    @classmethod
    def get_category(cls):
        """Return supplementary category for the job."""

        cls.logger.info('parsed argument --category with value "%s"', cls.args.category)

        return cls.args.category

    @classmethod
    def get_tags(cls):
        """Return supplementary tags."""

        cls.logger.info('parsed argument --tags with value %s', cls.args.tags)

        return cls.args.tags

    @classmethod
    def get_links(cls):
        """Return supplementary links."""

        cls.logger.info('parsed argument --links with value "%s"', cls.args.links)

        return cls.args.links

    @classmethod
    def get_search(cls):
        """Return the search keywords."""

        cls.logger.info('parsed argument --search with value %s', cls.args.search)

        return cls.args.search
