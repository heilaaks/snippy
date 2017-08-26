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
        parser.add_argument('-s', '--snippet', type=str, default='', help='add command or code snippet')
        parser.add_argument('-r', '--resolve', type=str, default='', help='add troubleshooting resolution')
        parser.add_argument('-b', '--brief', type=str, default='', help='set brief description for the input')
        parser.add_argument('-c', '--category', type=str, default='', help='set a category for the input')
        parser.add_argument('-t', '--tags', nargs='*', type=str, default=[], help='set tags for the input')
        parser.add_argument('-l', '--links', type=str, default='', help='set reference links for more information')
        parser.add_argument('-f', '--find', nargs='*', type=str, default=[], help='find with all given keywords')
        parser.add_argument('-w', '--write', action='store_true', default=False, help='write input with editor')
        parser.add_argument('-d', '--delete', type=int, default=0, help='remove snippet based on storage index')
        parser.add_argument('-e', '--export', dest='export_file', type=str, default='', \
                             help='export peristed storage to file [*.yaml|json|txt]')
        parser.add_argument('-i', '--import', dest='import_file', type=str, default='', \
                             help='export peristed storage to file [*.yaml|json]')
        parser.add_argument('--ftag', type=str, help='find from tags only')
        parser.add_argument('--profiler', action='store_true', default=False, help=argparse.SUPPRESS)
        parser.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
        Arguments.args = parser.parse_args()

    @classmethod
    def get_snippet(cls):
        """Return the snippet that user gave exactly as it was."""

        cls.logger.info('parsed argument --snippet with value "%s"', cls.args.snippet)

        return cls.args.snippet

    @classmethod
    def get_resolve(cls):
        """Return the resolution that user gave exactly as it was."""

        cls.logger.info('parsed argument --resolve with value "%s"', cls.args.resolve)

        return cls.args.resolve

    @classmethod
    def get_brief(cls):
        """Return the brief description that user gave exactly as it was."""

        cls.logger.info('parsed argument --brief with value "%s"', cls.args.brief)

        return cls.args.brief

    @classmethod
    def get_category(cls):
        """Return the category that user gave exactly as it was."""

        cls.logger.info('parsed argument --category with value "%s"', cls.args.category)

        return cls.args.category

    @classmethod
    def get_tags(cls):
        """Return the tags that user gave exactly as it was."""

        cls.logger.info('parsed argument --tags with value %s', cls.args.tags)

        return cls.args.tags

    @classmethod
    def get_links(cls):
        """Return the links that user gave exactly as it was."""

        cls.logger.info('parsed argument --links with value "%s"', cls.args.links)

        return cls.args.links

    @classmethod
    def get_find(cls):
        """Return the find keywords that user gave exactly as it was."""

        cls.logger.info('parsed argument --find with value %s', cls.args.find)

        return cls.args.find

    @classmethod
    def get_delete(cls):
        """Return the index to be deleted as it was provided by the user."""

        cls.logger.info('parsed argument --delete with value %d', cls.args.delete)

        return cls.args.delete

    @classmethod
    def get_export(cls):
        """Return the export file name as it was provided by the user."""

        cls.logger.info('parsed argument --export with value "%s"', cls.args.export_file)

        return cls.args.export_file

    @classmethod
    def get_import(cls):
        """Return the import file name as it was provided by the user."""

        cls.logger.info('parsed argument --import with value "%s"', cls.args.import_file)

        return cls.args.import_file

    @classmethod
    def get_profiler(cls):
        """Return the profiler switch based on user input or from default."""

        cls.logger.info('parsed argument --profile with value %s', cls.args.profiler)

        return cls.args.profiler

    @classmethod
    def get_write(cls):
        """Return the user input from editor."""

        edited_message = ''
        if not cls.args.write:
            return edited_message

        import tempfile
        from subprocess import call

        default_editor = os.environ.get('EDITOR', 'vi')
        editor_template = ('# Commented lines will be ignored.\n'
                           '#\n' +
                           Const.EDITOR_SNIPPET_HEAD +
                           '\n' +
                           Const.EDITOR_BRIEF_HEAD +
                           '\n' +
                           Const.EDITOR_CATEGORY_HEAD +
                           '\n' +
                           Const.EDITOR_TAGS_HEAD +
                           '\n' +
                           Const.EDITOR_LINKS_HEAD +
                           '\n').encode('UTF-8')

        with tempfile.NamedTemporaryFile(prefix='snippy-edit-') as outfile:
            outfile.write(editor_template)
            outfile.flush()
            call([default_editor, outfile.name])
            outfile.seek(0)
            edited_message = outfile.read()

        return edited_message.decode('UTF-8')
