# -*- coding: utf-8 -*-
#
#  Snippy - Software development and maintenance notes manager.
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
#
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""plugins: Wrappers around services needed by plugins."""

from jsonschema import Draft7Validator, RefResolver
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

from snippy.constants import Constants as SnippyConst
from snippy.content.parsers.base import ContentParserBase as SnippyParser
from snippy.cause import Cause
from snippy.config.config import Config
from snippy.logger import Logger


class Const(object):  # pylint: disable=too-few-public-methods
    """Constants for plugins."""

    SPACE = SnippyConst.SPACE
    NEWLINE = SnippyConst.NEWLINE
    TEXT_TYPE = SnippyConst.TEXT_TYPE

    CODE = SnippyConst.CODE
    SNIPPET = SnippyConst.SNIPPET
    SOLUTION = SnippyConst.SOLUTION
    REFERENCE = SnippyConst.REFERENCE
    TODO = SnippyConst.TODO
    CATEGORIES = SnippyConst.CATEGORIES

    DEFAULT_GROUPS = SnippyConst.DEFAULT_GROUPS
    SNIPPET_COMMENT = SnippyConst.SNIPPET_COMMENT

    RE_MATCH_NEWLINES = SnippyConst.RE_MATCH_NEWLINES
    RE_MATCH_MULTIPE_WHITESPACES = SnippyConst.RE_MATCH_MULTIPE_WHITESPACES


class Parser(object):
    """Content attribute parsers for plugins.

    This parser returns attribuytes in format that are suitable for JSON
    schema validation. This is the reason why lists are used instead of
    tuples as return values.
    """

    _logger = Logger.get_logger(__name__)

    @classmethod
    def format_data(cls, category, value):
        """Format content ``data`` attribute.

        Format a list of strings in value parameter to format that is accepted
        by the Snippy tool.

        Args:
            category (str): Content category.
            value (list): Content ``data`` in a list of strings.

        Returns:
            list: List of utf-8 encoded unicode strings.
        """

        data = []
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for data attrubute parser: %s', category)
            return list(SnippyParser.format_data(Const.SNIPPET, data))

        if not isinstance(value, (list, tuple)):
            cls._logger.debug('invalid instance type for data attrubute parser: %s', type(value))
            return list(SnippyParser.format_data(Const.SNIPPET, data))

        return list(SnippyParser.format_data(category, value))

    @classmethod
    def format_brief(cls, category, value):
        """Format content ``brief`` attribute.

        Format a string that contains the ``brief`` attribute to format that
        is accepted by the Snippy tool.

        Args:
            category (str): Content category.
            value (str): Content ``brief`` in a string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        brief = ''
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for brief attrubute parser: %s', category)
            return SnippyParser.format_string(brief)

        brief = cls._format_string(value)

        return SnippyParser.format_string(brief)

    @classmethod
    def format_description(cls, category, value):
        """Format content ``description`` attribute.

        Format a string that contains the ``description`` attribute to format
        that is accepted by the Snippy tool.

        Args:
            category (str): Content category.
            value (str): Content ``description`` in a string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        description = ''
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for description attrubute parser: %s', category)
            return SnippyParser.format_string(description)

        description = cls._format_string(value)

        return SnippyParser.format_string(description)

    @classmethod
    def format_name(cls, category, value):
        """Format content ``name`` attribute.

        Format a string that contains the ``name`` attribute to format that
        is accepted by the Snippy tool.

        Args:
            category (str): Content category.
            value (str): Content ``name`` in a string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        name = ''
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for name attrubute parser: %s', category)
            return SnippyParser.format_string(name)

        name = cls._format_string(value)

        return SnippyParser.format_string(name)

    @classmethod
    def format_groups(cls, category, value):
        """Format content ``groups`` attribute.

        Format a string that contains the ``groups`` attribute to format that
        is accepted by the Snippy tool.

        Args:
            category (str): Content category.
            value (str): Content ``groups`` in a string.

        Returns:
            list: List of utf-8 encoded groups.
        """

        groups = []
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for groups attrubute parser: %s', category)
            return list(SnippyParser.format_list(groups))

        if not value:
            value = Const.DEFAULT_GROUPS

        return list(SnippyParser.format_list(value))

    @classmethod
    def format_tags(cls, category, value):
        """Format content ``tags`` attribute.

        Format a string that contains the ``tags`` attribute to format that
        is accepted by the Snippy tool.

        Args:
            category (str): Content category.
            value (str): Content ``tags`` in a string.

        Returns:
            list: List of utf-8 encoded tags.
        """

        tags = ''
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for tags attrubute parser: %s', category)
            return SnippyParser.format_string(tags)

        return list(SnippyParser.format_list(value))

    @classmethod
    def format_links(cls, category, value):
        """Format content ``links`` attribute.

        Format a string that contains the ``links`` attribute to format that
        is accepted by the Snippy tool.

        Args:
            category (str): Content category.
            value (str): Content ``links`` in a string.

        Returns:
            list: List of utf-8 encoded links.
        """

        links = ''
        if category not in Const.CATEGORIES:
            cls._logger.debug('invalid content category for links attrubute parser: %s', category)
            return SnippyParser.format_string(links)

        return list(SnippyParser.format_links(value))

    @staticmethod
    def _format_string(value):
        """Format content attributes in string format.

        The method removes all newlines and additional whitespaces from the
        given string. This allows post-processing string formatted data to
        other layouts. For example the ``description`` attribute is one long
        string that can be formatted to text or Markdown content in different
        templates.

        Args:
            value (str): A string which is beautified.

        Returns:
            str: String that is formatted for the plugin specific ways.
        """

        value = Const.RE_MATCH_NEWLINES.sub(Const.SPACE, value)
        value = Const.RE_MATCH_MULTIPE_WHITESPACES.sub(Const.SPACE, value)

        return value


class Schema(object):  # pylint: disable=too-few-public-methods
    """Content attributres JSON schema validator for plugins."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._schema = self._get_schema_validator()

    def validate(self, document):
        """Validate content attributes against JSON schema.

        Args:
            document (obj): JSON document that is validated.

        Returns:
            bool: True if the document is valid.
        """

        validated = False
        try:
            self._schema.validate(document)
            validated = True
        except ValidationError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content attributes validation failed: {}'.format(minimized))
            for error in self._schema.iter_errors(document):
                self._logger.debug('content attributes failure: {}'.format(error))
        except SchemaError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'json schema failure: {}'.format(minimized))

        return validated

    @staticmethod
    def _get_schema_validator():
        """Get JSON schema validator for plugins.

        Returns:
            obj: Jsonschema draft7 validator.
        """

        schema = Config.content_schema()
        Draft7Validator.check_schema(schema)
        resolver = RefResolver(base_uri=Config.schema_base_uri(), referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver, format_checker=None)

        return validator
