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

"""content: Store content."""

import re
import hashlib
from snippy.config.constants import Constants as Const
from snippy.config.config import Config
from snippy.logger import Logger


class Content(object):  # pylint: disable=too-many-public-methods
    """Store content."""

    def __init__(self, content=None, category=None):
        self._logger = Logger(__name__).logger
        if content is None:
            self.content = tuple(Content.get_empty(category).get_list())
        else:
            self.set(content)

        if category:
            self._update_category(category)

    def __str__(self):
        """Format string from the class object."""

        from snippy.migrate.migrate import Migrate

        return Migrate.get_terminal_text((self,), ansi=True, debug=True)

    def get(self):
        """Get content."""

        return self.content

    def set(self, content):
        """Set content."""

        self.content = content
        self.update_digest()

    def convert_text(self):
        """Content content to text."""

        template = self._content_template(self.get_category())
        template = self._add_data(template)
        template = self._add_brief(template)
        template = self._add_date(template)
        template = self._add_group(template)
        template = self._add_tags(template)
        template = self._add_links(template)
        template = self._add_filename(template)

        return template

    def is_template(self):
        """Test if content data is empty template."""

        # Date and group fields are masked out. The date can change and the
        # tool enforces default group only after the content is saved and
        # user did not give change the group field value in template.
        template = Content.get_empty(self.get_category(), mask=True).convert_text()
        content = self.convert_text()
        template = re.sub(r'## DATE  :.*', '## DATE  : ', template)
        content = re.sub(r'## DATE  :.*', '## DATE  : ', content)
        content = re.sub(r'## GROUP :.*', '## GROUP : ', content)
        template = re.sub(r'## GROUP :.*', '## GROUP : ', template)
        content = re.sub(r'# Add optional single group below.\ndefault', '# Add optional single group below.\n', content)
        template = re.sub(r'# Add optional single group below.\ndefault', '# Add optional single group below.\n', template)

        return True if content == template else False

    @staticmethod
    def _content_template(category):
        """Return content template."""

        template = Const.EMPTY
        if category == Const.SNIPPET:
            template = Config.snippet_template
        else:
            template = Config.solution_template

        return template

    def _add_data(self, template):
        """Add content data to template."""

        data = self.get_data(Const.STRING_CONTENT)
        if data:
            if self.is_snippet():
                template = re.sub('<SNIPPY_DATA>.*<SNIPPY_DATA>', data, template, flags=re.DOTALL)
            else:
                template = data
        else:
            template = template.replace('<SNIPPY_DATA>', Const.EMPTY)

        return template

    def _add_brief(self, template):
        """Add content brief to template."""

        brief = self.get_brief(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_BRIEF>', brief)

        return template

    def _add_date(self, template):
        """Add content date to template."""

        # Only solution template contains the date field. When the field is
        # replaced with a timestamp, the template has been just created and
        # thus the creation date can be used.
        if '<SNIPPY_DATE>' in template:
            template = template.replace('<SNIPPY_DATE>', self.get_created())
        else:
            match = re.search(r'(## DATE  :\s*?$)', template, re.MULTILINE)
            if match and self.get_created():
                match.group(1).rstrip()
                template = template.replace(match.group(1), match.group(1) + Const.SPACE + self.get_created())

        return template

    def _add_group(self, template):
        """Add content group to template."""

        group = self.get_group(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_GROUP>', group)

        return template

    def _add_tags(self, template):
        """Add content tags to template."""

        tags = self.get_tags(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_TAGS>', tags)

        return template

    def _add_links(self, template):
        """Add content links to template."""

        links = self.get_links(Const.STRING_CONTENT)
        links = links + Const.NEWLINE  # Links is the last item in snippet template and this adds extra newline at the end.
        template = template.replace('<SNIPPY_LINKS>', links)

        return template

    def _add_filename(self, template):
        """Add content filename to template."""

        filename = self.get_filename(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_FILE>', filename)

        return template

    def is_snippet(self):
        """Test if content is snippet."""

        return True if self.content[Const.CATEGORY] == Const.SNIPPET else False

    def has_data(self):
        """Test if content has data defined."""

        return False if not self.content[Const.DATA] or not any(self.content[Const.DATA]) else True

    def get_data(self, form=Const.NATIVE_CONTENT):
        """Return content data."""

        if form == Const.STRING_CONTENT:
            data = Const.DELIMITER_DATA.join(map(str, self.content[Const.DATA]))
        else:
            data = self.content[Const.DATA]

        return data

    def get_brief(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content brief."""

        return self.content[Const.BRIEF]

    def get_group(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content group."""

        return self.content[Const.GROUP]

    def get_tags(self, form=Const.NATIVE_CONTENT):
        """Return content tags."""

        if form == Const.STRING_CONTENT:
            tags = Const.DELIMITER_TAGS.join(map(str, sorted(self.content[Const.TAGS])))
        else:
            tags = self.content[Const.TAGS]

        return tags

    def get_links(self, form=Const.NATIVE_CONTENT):
        """Return content links."""

        if form == Const.STRING_CONTENT:
            links = Const.DELIMITER_LINKS.join(map(str, sorted(self.content[Const.LINKS])))
        else:
            links = self.content[Const.LINKS]

        return links

    def get_category(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content category."""

        return self.content[Const.CATEGORY]

    def get_filename(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content filename."""

        return self.content[Const.FILENAME]

    def get_runalias(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content runalias."""

        return self.content[Const.RUNALIAS]

    def get_versions(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content version list."""

        return self.content[Const.VERSIONS]

    def get_created(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return UTC timestamp when content was created."""

        return self.content[Const.CREATED]

    def get_updated(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return UTC timestamp when content was updated."""

        return self.content[Const.UPDATED]

    def get_digest(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content digest."""

        return self.content[Const.DIGEST]

    def get_metadata(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content metadata."""

        return self.content[Const.METADATA]

    def get_key(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content key."""

        return self.content[Const.KEY]

    def compute_digest(self):
        """Compute digest for the content."""

        data_string = self.get_string()
        digest = hashlib.sha256(data_string.encode('UTF-8')).hexdigest()

        return digest

    def update_digest(self):
        """Update content message digest."""

        content = self.get_list()
        content[Const.DIGEST] = self.compute_digest()
        self.content = (
            content[Const.DATA],
            content[Const.BRIEF],
            content[Const.GROUP],
            content[Const.TAGS],
            content[Const.LINKS],
            content[Const.CATEGORY],
            content[Const.FILENAME],
            content[Const.RUNALIAS],
            content[Const.VERSIONS],
            content[Const.CREATED],
            content[Const.UPDATED],
            content[Const.DIGEST],
            content[Const.METADATA],
            content[Const.KEY]
        )

    def update_updated(self):
        """Update content update timestamp."""

        # Does not require recalculation of digest because the time is not
        # part of it.
        content = self.get_list()
        content[Const.UPDATED] = Config.get_utc_time()
        self.content = (
            content[Const.DATA],
            content[Const.BRIEF],
            content[Const.GROUP],
            content[Const.TAGS],
            content[Const.LINKS],
            content[Const.CATEGORY],
            content[Const.FILENAME],
            content[Const.RUNALIAS],
            content[Const.VERSIONS],
            content[Const.CREATED],
            content[Const.UPDATED],
            content[Const.DIGEST],
            content[Const.METADATA],
            content[Const.KEY]
        )

    def _update_category(self, category):
        """Update content categor."""

        content = self.get_list()
        content[Const.CATEGORY] = category
        self.content = (
            content[Const.DATA],
            content[Const.BRIEF],
            content[Const.GROUP],
            content[Const.TAGS],
            content[Const.LINKS],
            content[Const.CATEGORY],
            content[Const.FILENAME],
            content[Const.RUNALIAS],
            content[Const.VERSIONS],
            content[Const.CREATED],
            content[Const.UPDATED],
            content[Const.DIGEST],
            content[Const.METADATA],
            content[Const.KEY]
        )

    def get_string(self):
        """Convert content into one string."""

        content_str = self.get_data(Const.STRING_CONTENT)
        content_str = content_str + self.get_brief(Const.STRING_CONTENT)
        content_str = content_str + self.get_group(Const.STRING_CONTENT)
        content_str = content_str + self.get_tags(Const.STRING_CONTENT)
        content_str = content_str + self.get_links(Const.STRING_CONTENT)
        content_str = content_str + self.get_category(Const.STRING_CONTENT)
        content_str = content_str + self.get_filename(Const.STRING_CONTENT)
        content_str = content_str + self.get_runalias(Const.STRING_CONTENT)
        content_str = content_str + self.get_versions(Const.STRING_CONTENT)

        return content_str

    def get_list(self):
        """Convert content into mutable list."""

        content = [
            self.get_data(),
            self.get_brief(),
            self.get_group(),
            self.get_tags(),
            self.get_links(),
            self.get_category(),
            self.get_filename(),
            self.get_runalias(),
            self.get_versions(),
            self.get_created(),
            self.get_updated(),
            self.get_digest(),
            self.get_metadata(),
            self.get_key()
        ]

        return content

    def migrate(self, sources):
        """Migrate content.

        Content fields that can be directly modified by user are migrated.
        The 'created' and 'updated' timestamps are read from the migrated
        source.

        This overrides always the original content field.
        """

        if sources:
            migrated = sources[0]
            content = self.get_list()
            content[Const.DATA] = migrated.get_data()
            content[Const.BRIEF] = migrated.get_brief()
            content[Const.GROUP] = migrated.get_group()
            content[Const.TAGS] = migrated.get_tags()
            content[Const.LINKS] = migrated.get_links()
            content[Const.FILENAME] = migrated.get_filename()
            content[Const.RUNALIAS] = migrated.get_runalias()
            content[Const.VERSIONS] = migrated.get_versions()
            content[Const.CREATED] = migrated.get_created()
            content[Const.UPDATED] = migrated.get_updated()
            self.set((
                content[Const.DATA],
                content[Const.BRIEF],
                content[Const.GROUP],
                content[Const.TAGS],
                content[Const.LINKS],
                content[Const.CATEGORY],
                content[Const.FILENAME],
                content[Const.RUNALIAS],
                content[Const.VERSIONS],
                content[Const.CREATED],
                content[Const.UPDATED],
                content[Const.DIGEST],
                content[Const.METADATA],
                content[Const.KEY]
            ))

    def merge(self, source):
        """Merge content.

        Content fields that can be directly modified by user are merged.

        This overrides original content field only if the merged source does
        not exist.
        """

        if source:
            content = self.get_list()
            if source.get_data():
                content[Const.DATA] = source.get_data()
            if source.get_brief():
                content[Const.BRIEF] = source.get_brief()
            if source.get_tags():
                content[Const.TAGS] = source.get_tags()
            if source.get_links():
                content[Const.LINKS] = source.get_links()
            self.set((
                content[Const.DATA],
                content[Const.BRIEF],
                content[Const.GROUP],
                content[Const.TAGS],
                content[Const.LINKS],
                content[Const.CATEGORY],
                content[Const.FILENAME],
                content[Const.RUNALIAS],
                content[Const.VERSIONS],
                content[Const.CREATED],
                content[Const.UPDATED],
                content[Const.DIGEST],
                content[Const.METADATA],
                content[Const.KEY]
            ))

    @classmethod
    def sort_contents(cls, contents, column, reversed_sort):
        """Sort all contents by defined column."""

        sorted_contents = sorted(contents, key=lambda x: x.content[column], reverse=reversed_sort)

        return sorted_contents

    @classmethod
    def load(cls, dictionary):
        """Load contents from dictionary."""

        contents = ()

        if 'content' in dictionary:
            contents = Content._get_contents(dictionary['content'])

        return contents

    @classmethod
    def get_empty(cls, category, mask=False):
        """Get empty content."""

        if mask:
            timestamp = Const.EMPTY
        else:
            timestamp = Config.get_utc_time()
        content = (
            Const.EMPTY_TUPLE,
            Const.EMPTY,
            Const.DEFAULT_GROUP,
            Const.EMPTY_TUPLE,
            Const.EMPTY_TUPLE,
            category,
            Const.EMPTY,
            Const.EMPTY,
            Const.EMPTY,
            timestamp,  # created
            timestamp,  # updated
            None,  # digest
            None,  # metadata
            None   # key
        )

        return Content(content)

    @staticmethod
    def _get_contents(dictionary):
        """Convert dictionary to content tupe."""

        contents = []
        for entry in dictionary:
            contents.append(Content._get_content(entry))

        return tuple(contents)

    @staticmethod
    def _get_content(dictionary):
        """Convert single dictionary entry into Content object."""

        content = Content([
            dictionary['data'],
            dictionary['brief'],
            dictionary['group'],
            dictionary['tags'],
            dictionary['links'],
            dictionary['category'],
            dictionary['filename'],
            dictionary['runalias'],
            dictionary['versions'],
            dictionary['created'],
            dictionary['updated'],
            dictionary['digest'],
            None,  # metadata
            None   # key
        ])

        return content
