#!/usr/bin/env python3

"""arguments.py: Command line argument management."""

import os
import argparse
from snippy.config import Constants as Const
from snippy.logger import Logger


class Arguments(object):
    """Command line argument management."""

    args = {}
    logger = {}

    def __init__(self):
        Arguments.logger = Logger(__name__).get()
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
