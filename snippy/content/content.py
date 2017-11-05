#!/usr/bin/env python3

"""content.py: Store content."""

import re
import hashlib
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.config.config import Config


class Content(object):
    """Manage content."""

    def __init__(self, content=None, category=None):
        self.logger = Logger(__name__).get()
        if content is None:
            self.content = (Config.get_content_data(),
                            Config.get_content_brief(),
                            Config.get_content_group(),
                            Config.get_content_tags(),
                            Config.get_content_links(),
                            Config.get_category(),
                            Config.get_filename(),
                            None,  # utc
                            None,  # digest
                            None,  # metadata
                            None)  # key
        else:
            self.content = content

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

    def is_snippet(self):
        """Test if content is snippet."""

        return True if self.content[Const.CATEGORY] == Const.SNIPPET else False

    def is_solution(self):
        """Test if content is solution."""

        return True if self.content[Const.CATEGORY] == Const.SOLUTION else False

    def has_data(self):
        """Test if content has data defined."""

        return True if self.content[Const.DATA] else False

    def is_data_template(self, edited=None):
        """Test if content data is empty template."""

        template = Config.get_content_template(Content(content=None, category=self.get_category()))
        if not edited:
            content = self.get_data(form=Const.STRING_CONTENT)
        else:
            content = edited
        template = re.sub(r'## DATE  :.*', '## DATE  :', template)
        content = re.sub(r'## DATE  :.*', '## DATE  :', content)

        return True if content == template else False

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

    def get_utc(self, form=Const.NATIVE_CONTENT):  # pylint: disable=unused-argument
        """Return content UTC."""

        return self.content[Const.UTC]

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
        self.content = (content[Const.DATA],
                        content[Const.BRIEF],
                        content[Const.GROUP],
                        content[Const.TAGS],
                        content[Const.LINKS],
                        content[Const.CATEGORY],
                        content[Const.FILENAME],
                        content[Const.UTC],
                        content[Const.DIGEST],
                        content[Const.METADATA],
                        content[Const.KEY])

    def _update_category(self, category):
        """Update content categor."""

        content = self.get_list()
        content[Const.CATEGORY] = category
        self.content = (content[Const.DATA],
                        content[Const.BRIEF],
                        content[Const.GROUP],
                        content[Const.TAGS],
                        content[Const.LINKS],
                        content[Const.CATEGORY],
                        content[Const.FILENAME],
                        content[Const.UTC],
                        content[Const.DIGEST],
                        content[Const.METADATA],
                        content[Const.KEY])

    def get_string(self):
        """Convert content into one string."""

        content_str = self.get_data(Const.STRING_CONTENT)
        content_str = content_str + self.get_brief(Const.STRING_CONTENT)
        content_str = content_str + self.get_group(Const.STRING_CONTENT)
        content_str = content_str + self.get_tags(Const.STRING_CONTENT)
        content_str = content_str + self.get_links(Const.STRING_CONTENT)
        content_str = content_str + self.get_category(Const.STRING_CONTENT)
        content_str = content_str + self.get_filename(Const.STRING_CONTENT)

        return content_str

    def get_list(self):
        """Convert content into mutable list."""

        content = [self.get_data(),
                   self.get_brief(),
                   self.get_group(),
                   self.get_tags(),
                   self.get_links(),
                   self.get_category(),
                   self.get_filename(),
                   self.get_utc(),
                   self.get_digest(),
                   self.get_metadata(),
                   self.get_key()]

        return content

    def migrate_edited(self, contents):
        """Migrate edited content."""

        # Only the content that can be directly modified by user is migrated.
        if contents:
            migrated = contents[0]
            content = self.get_list()
            content[Const.DATA] = migrated.get_data()
            content[Const.BRIEF] = migrated.get_brief()
            content[Const.GROUP] = migrated.get_group()
            content[Const.TAGS] = migrated.get_tags()
            content[Const.LINKS] = migrated.get_links()
            content[Const.FILENAME] = migrated.get_filename()
            content[Const.UTC] = migrated.get_utc()
            self.content = (content[Const.DATA],
                            content[Const.BRIEF],
                            content[Const.GROUP],
                            content[Const.TAGS],
                            content[Const.LINKS],
                            content[Const.CATEGORY],
                            content[Const.FILENAME],
                            content[Const.UTC],
                            content[Const.DIGEST],
                            content[Const.METADATA],
                            content[Const.KEY])

    @classmethod
    def load(cls, dictionary):
        """Load contents from dictionary."""

        contents = ()

        if 'content' in dictionary:
            contents = Content._get_contents(dictionary['content'])

        return contents

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

        content = Content([dictionary['data'],
                           dictionary['brief'],
                           dictionary['group'],
                           dictionary['tags'],
                           dictionary['links'],
                           dictionary['category'],
                           dictionary['filename'],
                           dictionary['utc'],
                           dictionary['digest'],
                           None,   # metadata
                           None])  # key

        return content
