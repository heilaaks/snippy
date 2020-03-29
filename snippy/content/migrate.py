# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""migrate: Import and export management."""

from __future__ import print_function

import io
import json
import os.path
import traceback

import yaml

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.logger import Logger
from snippy.meta import __homepage__
from snippy.meta import __version__


class Migrate(object):
    """Import and export management."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def dump(cls, collection, filename):
        """Dump collection into file."""

        if not Config.is_supported_file_format():
            cls._logger.debug('file format not supported for file %s', filename)

            return

        if not collection:
            Cause.push(Cause.HTTP_NOT_FOUND, 'no content found to be exported')

            return

        cls._logger.debug('exporting contents %s', filename)
        with io.open(filename, mode='w', encoding='utf-8') as outfile:
            try:
                dictionary = {'meta': {'updated': Config.utcnow(),
                                       'version': __version__,
                                       'homepage': __homepage__},
                              'data': collection.dump_dict(Config.remove_fields)}
                if Config.is_operation_file_text:
                    outfile.write(collection.dump_text(Config.templates))
                elif Config.is_operation_file_json:
                    json.dump(dictionary, outfile)
                    outfile.write(Const.NEWLINE)
                elif Config.is_operation_file_mkdn:
                    outfile.write(collection.dump_mkdn(Config.templates))
                elif Config.is_operation_file_yaml:
                    yaml.safe_dump(dictionary, outfile, default_flow_style=False)
                else:
                    cls._logger.debug('unknown export file format')
            except (IOError, TypeError, ValueError, yaml.YAMLError) as error:
                cls._logger.exception('fatal failure to generate formatted export file "%s"', error)
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while exporting content to file')

    @classmethod
    def dump_template(cls, category):
        """Dump content template into file."""

        filename = Config.get_operation_file()
        resource = Collection.get_resource(category, Config.utcnow())
        template = resource.get_template(
            category,
            Config.template_format,
            Config.templates
        )
        cls._logger.debug('exporting content template %s', filename)
        with io.open(filename, mode='w', encoding='utf-8') as outfile:
            try:
                outfile.write(template)
            except IOError as error:
                cls._logger.exception('fatal failure in creating %s template file "%s"', category, error)
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while exporting template {}'.format(filename))

    @classmethod
    def dump_completion(cls, complete):
        """Dump shell completion script into a file.

        Args:
            complete (str): Name of the shell for completion.
        """

        filename = Config.get_operation_file()
        path, _ = os.path.split(filename)
        cls._logger.debug('exporting: %s :completion: %s', Config.complete, filename)
        if not os.path.exists(path) or not os.access(path, os.W_OK):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot export: {} :completion file because path is not writable: {}'.format(
                complete,
                filename
            ))
            return

        with io.open(filename, mode='w', encoding='utf-8') as outfile:
            try:
                outfile.write(Config.completion[Config.complete])
            except IOError as error:
                cls._logger.exception('fatal failure when creating {} shell completion file: {}', filename, error)
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while exporting shell completion {}'.format(filename))

    @classmethod
    def load(cls, filename):
        """Load dictionary from file."""

        collection = Collection()
        if not Config.is_supported_file_format():
            cls._logger.debug('file format not supported for file %s', filename)

            return collection

        cls._logger.debug('importing contents from file %s', filename)
        if os.path.isfile(filename):
            with io.open(filename, mode='r', encoding='utf-8') as infile:
                try:
                    timestamp = Config.utcnow()
                    if Config.is_operation_file_text:
                        collection.load_text(timestamp, infile.read())
                    elif Config.is_operation_file_mkdn:
                        collection.load_mkdn(timestamp, infile.read())
                    elif Config.is_operation_file_json:
                        dictionary = json.load(infile)
                        collection.load_dict(timestamp, dictionary)
                    elif Config.is_operation_file_yaml:
                        dictionary = yaml.safe_load(infile)
                        collection.load_dict(timestamp, dictionary)
                    else:
                        cls._logger.debug('unknown import file format')
                except (TypeError, ValueError, yaml.YAMLError) as error:
                    cls._logger.exception('fatal exception while loading file "%s"', error)
                    Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'fatal failure while importing content from file')

        else:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot read file {}'.format(filename))

        return collection

    @classmethod
    def import_hook(cls):
        """Import content from external plugin.

        Returns:
            obj: Imported notes in a ``Collection`` object.
        """

        notes = {}
        collection = Collection()
        try:
            notes = Config.hooks['import'](Logger.get_logger('snippy.plugin.import'), Config.get_plugin_uri())
        except KeyboardInterrupt:
            cls._logger.debug('user interrupted import plugin: {}'.format(traceback.format_exc()))
            Cause.push(Cause.HTTP_METHOD_NOT_ALLOWED, 'user interrupted import plugin')
        except Exception:  # pylint: disable=broad-except
            cls._logger.debug('failed to call import plugin: {}'.format(traceback.format_exc()))
            Cause.push(Cause.HTTP_FORBIDDEN, 'failed to call import plugin - enable --debug logs')

        if not notes:
            Cause.push(Cause.HTTP_NOT_FOUND, 'no imported notes found')
            return collection

        try:
            if len(notes) > 10000:
                Cause.push(Cause.HTTP_FORBIDDEN, 'too many imported notes')
                return collection
        except TypeError:
            Cause.push(Cause.HTTP_FORBIDDEN, 'failed to read the number of imported notes - implement len() for the plugin iterator')
            return collection

        try:
            timestamp = Config.utcnow()
            data = {
                'data': notes
            }
            collection.load_dict(timestamp, data)
        except Exception:  # pylint: disable=broad-except
            cls._logger.debug('failed to import content from plugin: {}'.format(traceback.format_exc()))
            Cause.push(Cause.HTTP_FORBIDDEN, 'failed to call import plugin - enable --debug logs')

        return collection
