#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

import io
import os.path
import re

import pkg_resources


class Helper(object):  # pylint: disable=too-few-public-methods
    """Generic helpers testing.

    This class intentionally copies some of the implementation from the
    code. The intention is to avoid dependencies in this module to be
    able to import this module anywhere.
    """

    EXPORT_TIME = '2018-02-02T02:02:02.000001+0000'
    IMPORT_TIME = '2018-03-02T02:02:02.000001+0000'
    EXPORT_TEMPLATE = '2017-10-14T19:56:31.000001+0000'

    RE_MATCH_ANSI_ESCAPE_SEQUENCES = re.compile(r'''
        \x1b[^m]*m    # Match all ANSI escape sequences.
        ''', re.VERBOSE)

    @staticmethod
    def read_template(filename):
        """Get default content template in text format.

        The returned template must be in the same format where external editor
        like vi gets the default template. This means that all the tags are
        removed and the group tag is replaced with 'default' group.

        Args:
            filename (str): Template filename as stored in data/templates.

        Returns:
            str: Empty template in the same format as for external editor.
        """

        template = ''
        filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/templates'), filename)
        with io.open(filename, encoding='utf-8') as infile:
            template = infile.read()

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

    @staticmethod
    def remove_ansi(message):
        """Remove all ANSI escape codes from given string.

        Args:
            message (str): Message which ANSI escape codes are removed.

        Returns:
            str: Same message but without ANSI escape sequences.
        """

        return Helper.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', message)
