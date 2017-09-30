#!/usr/bin/env python3

"""content.py: Store content."""

import hashlib
from snippy.config import Constants as Const
from snippy.logger import Logger


class Content(object):
    """Store content."""

    def __init__(self, content):
        self.logger = Logger(__name__).get()
        self.content = content

    def get(self):
        """Get content."""

        return self.content

    def set(self, content):
        """Set content."""

        self.content = content

    def is_snippet(self):
        """Test if content is snippet."""

        return True if self.content[Const.CATEGORY] == Const.SNIPPET else False

    def has_data(self):
        """Test if content has data defined."""

        return True if self.content[Const.DATA] else False

    def get_data(self, form=Const.NATIVE_CONTENT):
        """Return content data."""

        if form == Const.STRING_CONTENT:
            data = Const.DELIMITER_DATA.join(map(str, self.content[Const.DATA]))
        else:
            data = self.content[Const.DATA]

        return data

    def get_brief(self, form=Const.NATIVE_CONTENT): # pylint: disable=unused-argument
        """Return content brief."""

        return self.content[Const.BRIEF]

    def get_group(self, form=Const.NATIVE_CONTENT): # pylint: disable=unused-argument
        """Return content group."""

        return self.content[Const.BRIEF]

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
