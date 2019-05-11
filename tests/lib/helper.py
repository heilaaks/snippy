#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""helper: Generic helpers testing."""

from __future__ import print_function

import io
import os.path
import re
import sys

import json
import pkg_resources

from jsonschema import Draft7Validator, RefResolver


class Helper(object):
    """Generic helpers testing.

    This class intentionally copies some of the implementation from the
    production code. The purpose is to avoid dependencies in this module
    to be able to import this module anywhere.
    """

    EXPORT_TIME = '2018-02-02T02:02:02.000001+00:00'
    IMPORT_TIME = '2018-03-02T02:02:02.000001+00:00'
    EXPORT_TEMPLATE = '2017-10-14T19:56:31.000001+00:00'

    DB_SQLITE = 'sqlite'
    DB_POSTGRESQL = 'postgresql'
    DB_COCKROACHDB = 'cockroachdb'
    DB_IN_MEMORY = 'in-memory'
    STORAGES = (DB_SQLITE, DB_POSTGRESQL, DB_COCKROACHDB, DB_IN_MEMORY)

    COLOR_OK = '\033[32m'
    COLOR_END = '\033[0m'

    # All resource attributes that can be sent in HTTP request.
    REQUEST_ATTRIBUTES = (
        'data',
        'brief',
        'description',
        'name',
        'groups',
        'tags',
        'links',
        'source',
        'versions',
        'filename'
    )

    RE_MATCH_ANSI_ESCAPE_SEQUENCES = re.compile(r'''
        \x1b[^m]*m    # Match all ANSI escape sequences.
        ''', re.VERBOSE)

    @classmethod
    def read_template(cls, filename):
        """Get default content template in text format.

        The returned template must be in the same format where external editor
        like vi gets the default template. This means that all the tags are
        removed and the group tag is replaced with 'default' group.

        Args:
            filename (str): Template filename as stored in data/templates.

        Returns:
            str: Empty template in the same format as for external editor.
        """

        template = cls._read_resource('data/templates', filename)
        template = re.sub(r'''
            <groups>    # Match groups tag.
            ''', 'default', template, flags=re.VERBOSE)

        template = re.sub(r'''
            [<]\S+[>]   # Match any tag in the template.
            ''', '', template, flags=re.VERBOSE)

        # In case of the solution template, there is a <data> tag that leaves
        # empty fist line. Since all templates start from the first line, the
        # whitespaces can be removed from left of the string.
        template = template.lstrip()

        return template

    @classmethod
    def read_completion(cls, filename):
        """Get shell completion script.

        Args
            filename (str): Name of the shell completion file.
        """

        return cls._read_resource('data/completion', filename)

    @staticmethod
    def remove_ansi(message):
        """Remove all ANSI escape codes from given string.

        Args:
            message (str): Message which ANSI escape codes are removed.

        Returns:
            str: Same message but without ANSI escape sequences.
        """

        return Helper.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', message)

    @classmethod
    def get_schema_validator(cls):
        """Get JSON schema validator for REST API response.

        Returns:
            obj: Jsonschema draft7 validator.
        """

        response_resource = json.loads(cls._read_resource('data/server/openapi/schema', 'responseresource.json'))
        response_collection_get = json.loads(cls._read_resource('data/server/openapi/schema', 'responsecollectionget.json'))
        response_collection_post = json.loads(cls._read_resource('data/server/openapi/schema', 'responsecollectionpost.json'))
        response_errors = json.loads(cls._read_resource('data/server/openapi/schema', 'responseerrors.json'))
        response_hello = json.loads(cls._read_resource('data/server/openapi/schema', 'responsehello.json'))
        schema = {
            'oneOf': [
                response_collection_get,
                response_collection_post,
                response_errors,
                response_hello,
                response_resource
            ]
        }

        filepath = pkg_resources.resource_filename('snippy', 'data/server/openapi/schema/')
        if not os.path.isdir(filepath):
            print('NOK: cannot run test because server api response schema base uri is not accessible: {}'.format(filepath))
            sys.exit(1)
        server_schema_base_uri = 'file:' + filepath
        Draft7Validator.check_schema(schema)
        resolver = RefResolver(base_uri=server_schema_base_uri, referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver, format_checker=None)

        return validator

    @staticmethod
    def _read_resource(path, filename):
        """Read resource file.

        Args:
            path (str): Relative path under snippy project.
            filename (str): Resource filename.

        Returns:
            str: File read into a string.
        """

        filename = os.path.join(pkg_resources.resource_filename('snippy', path), filename)
        if not os.path.isfile(filename):
            print('NOK: cannot run tests because snippy resource file is not accessible: {}'.format(filename))
            sys.exit(1)

        resource_file = ''
        with io.open(filename, encoding='utf-8') as infile:
            resource_file = infile.read()

        return resource_file


class Classproperty(object):  # pylint: disable=too-few-public-methods
    """Implement classproperty.

    Implement decorator that mimics object property. See [1] for more
    details.

    [1] https://stackoverflow.com/a/3203659
    """

    def __init__(self, getter):
        self._getter = getter

    def __get__(self, _, owner):
        """Get property of a class."""

        return self._getter(owner)
