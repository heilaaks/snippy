# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""editor: Text editor based content management."""

import os

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.parser import Parser
from snippy.logger import Logger


class Editor(object):  # pylint: disable=too-few-public-methods
    """Text editor based content management."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def read(cls, timestamp, template_format, template, collection):
        """Read content from editor.

        Args:
            timestamp (str): IS8601 timestamp to be used with created collection.
            template_format (str): Template format.
            template (str): Default template for editor.
            collection (Collection()): Collection to store parsed content.
        """

        text = cls._call_editor(template)
        Parser(template_format, timestamp, text, collection).read()
        if not collection:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'edited: {} :content could not be read - please keep template tags in place'.format(template_format))  # noqa pylint: disable=line-too-long

    @classmethod
    def _call_editor(cls, template):
        """Run editor session."""

        import tempfile
        from subprocess import call

        # External dependencies are isolated in this method to ease
        # testing. This method is mocked to return the edited text.
        message = Const.EMPTY
        template = template.encode('UTF-8')
        editor = cls._get_editor()
        cls._logger.debug('using %s as editor', editor)
        with tempfile.NamedTemporaryFile(prefix='snippy-edit-') as outfile:
            outfile.write(template)
            outfile.flush()
            try:
                call([editor, outfile.name])
                outfile.seek(0)
                message = outfile.read()
                message = message.decode('UTF-8')
            except OSError as error:
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'required editor %s not installed %s' % (editor, error))

        return message

    @classmethod
    def _get_editor(cls):
        """Try to resolve the editor in a secure way."""

        # Running code blindly from environment variable is not safe because
        # the call would execute any command from environment variable.
        editor = os.environ.get('EDITOR', 'vi')

        # Avoid usage other than supported editors as of now for security
        # and functionality reasons. What is the safe way to check the
        # environment variables? What is the generic way to use editor in
        # Windows and Mac?
        if editor != 'vi':
            cls._logger.debug('enforcing vi as default editor instead of %s', editor)
            editor = 'vi'

        return editor
