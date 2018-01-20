#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""editor.py: Text editor based content management."""

import os.path
from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.logger.logger import Logger


class Editor(object):
    """Editor based configuration."""

    # Editor inputs
    SOLUTION_BRIEF = '## BRIEF :'
    SOLUTION_DATE = '## DATE  :'
    DATA_HEAD = '# Add mandatory snippet below.\n'
    DATA_TAIL = '# Add optional brief description below.\n'
    BRIEF_HEAD = '# Add optional brief description below.\n'
    BRIEF_TAIL = '# Add optional single group below.\n'

    def __init__(self, content, utc, edited=Const.EMPTY):
        self.logger = Logger(__name__).get()
        self.content = content
        self.edited = edited
        self.utc = utc

    def read_content(self, content):
        """Read the content from editor."""

        template = content.convert_text()
        source = self.call_editor(template)
        category = Parser.content_category(source)
        if category == Const.SNIPPET or category == Const.SOLUTION:
            content.set((Parser.content_data(category, source),
                         Parser.content_brief(category, source),
                         Parser.content_group(category, source),
                         Parser.content_tags(category, source),
                         Parser.content_links(category, source),
                         content.get_category(),
                         Parser.content_filename(category, source),
                         content.get_runalias(),
                         content.get_versions(),
                         content.get_utc(),
                         content.get_digest(),
                         content.get_metadata(),
                         content.get_key()))
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'could not identify edited content category - please keep tags in place')

        return content

    def call_editor(self, template):
        """Run editor session."""

        import tempfile
        from subprocess import call

        # External dependencies are isolated in this method to ease
        # testing. This method is mocked to return the edited text.
        message = Const.EMPTY
        template = template.encode('UTF-8')
        editor = self._get_editor()
        self.logger.info('using %s as editor', editor)
        with tempfile.NamedTemporaryFile(prefix='snippy-edit-') as outfile:
            outfile.write(template)
            outfile.flush()
            try:
                call([editor, outfile.name])
                outfile.seek(0)
                message = outfile.read()
                message = message.decode('UTF-8')
            except OSError as exception:
                Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'required editor %s not installed %s' % (editor, exception))

        return message

    def _get_editor(self):
        """Try to resolve the editor in a secure way."""

        # Running code blindly from environment variable is not safe because
        # the call would execute any command from environment variable.
        editor = os.environ.get('EDITOR', 'vi')

        # Avoid usage other than supported editors as of now for security
        # and functionality reasons. What is the safe way to check the
        # environment variables? What is the generic way to use editor in
        # Windows and Mac?
        if editor != 'vi':
            self.logger.info('enforcing vi as default editor instead of %s', editor)
            editor = 'vi'

        return editor

    def is_content_identified(self):
        """Test if content category is identified."""

        identified = False
        if self.get_edited_category() == Const.SNIPPET or self.get_edited_category() == Const.SOLUTION:
            identified = True

        return identified

    def get_edited_data(self):
        """Return content data from editor."""

        category = self.get_edited_category()
        content_data = Parser.content_data(category, self.edited)

        return content_data

    def get_edited_brief(self):
        """Return content brief from editor."""

        category = self.get_edited_category()
        content_brief = Parser.content_brief(category, self.edited)

        return content_brief

    def get_edited_date(self):
        """Return content date from editor."""

        # Read the time from 1) content or 2) time set for the object or from template.
        # The first two time stamps are used because it can be that user did not set
        # the date and time correctly to ISO 8601.
        if self.content.get_utc():
            timestamp = self.content.get_utc()
        else:
            timestamp = self.utc
        category = self.get_edited_category()
        content_date = Parser.content_date(category, self.edited, timestamp)

        return content_date

    def get_edited_group(self):
        """Return content group from editor."""

        category = self.get_edited_category()
        content_group = Parser.content_group(category, self.edited)

        return content_group

    def get_edited_tags(self):
        """Return content tags from editor."""

        category = self.get_edited_category()
        content_tags = Parser.content_tags(category, self.edited)

        return content_tags

    def get_edited_links(self):
        """Return content links from editor."""

        category = self.get_edited_category()
        content_links = Parser.content_links(category, self.edited)

        return content_links

    def get_edited_filename(self):
        """Return solution filename from editor."""

        category = self.get_edited_category()
        content_filename = Parser.content_filename(category, self.edited)

        return content_filename

    def get_edited_category(self):
        """Return content category based on edited content."""

        category = Const.UNKNOWN_CONTENT

        if Editor.DATA_HEAD in self.edited and Editor.BRIEF_HEAD:
            category = Const.SNIPPET
        elif Editor.SOLUTION_BRIEF in self.edited and Editor.SOLUTION_DATE:
            category = Const.SOLUTION

        return category
