#!/usr/bin/env python3

"""migrate.py: Import and export management."""

import sys
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.config import Config
from snippy.format import Format


class Migrate(object):
    """Import and export management."""

    logger = None

    def __init__(self):
        Migrate.logger = Logger(__name__).get()

    @classmethod
    def print_terminal(cls, content):
        """Print content into console."""

        cls.logger.debug('printing content to console')
        print(content)

    @classmethod
    def print_file(cls, category, content):
        """Print content into file."""

        export_file = Config.get_operation_file()
        cls.logger.debug('export storage into file %s', export_file)
        with open(export_file, 'w') as outfile:
            try:
                if Config.is_file_type_yaml():
                    import yaml

                    content_dict = {'content': Format.get_dictionary(content)}
                    yaml.dump(content_dict, outfile, default_flow_style=False)
                elif Config.is_file_type_json():
                    import json

                    content_dict = {'content': Format.get_dictionary(content)}
                    json.dump(content_dict, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_file_type_text() and category == Const.SNIPPET:
                    outfile.write(Format.get_snippet_text(content, colors=False))
                elif Config.is_file_type_text() and category == Const.SOLUTION:
                    outfile.write(Format.get_solution_text(content, colors=False))
                else:
                    cls.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                cls.logger.exception('fatal failure to generate formatted export file "%s"', exception)
                sys.exit()

    @classmethod
    def load_dictionary(cls, contents):
        """Create dictionary from content loaded from a file."""

        content_dict = {}

        cls.logger.debug('loading content dictionary from file')
        with open(contents, 'r') as infile:
            try:
                if Config.is_file_type_yaml():
                    import yaml

                    content_dict = yaml.load(infile)
                elif Config.is_file_type_json():
                    import json

                    content_dict = json.load(infile)
                else:
                    cls.logger.info('unknown export format')
            except (yaml.YAMLError, TypeError) as exception:
                cls.logger.exception('fatal exception while loading the import file %s "%s"', contents, exception)
                sys.exit()

        return content_dict
