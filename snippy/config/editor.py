#!/usr/bin/env python3

"""editor.py: Editor based configuration."""

from snippy.config import Constants as Const
from snippy.logger import Logger


class Editor(object): # pylint: disable-all
    """Editor based configuration."""

    def __init__(self):
        Config.logger = Logger(__name__).get()

    @classmethod
    def _get_edited_data(cls, message, form):
        """Return content data from editor."""

        lines = ()
        if form == Const.SNIPPET:
            lines = Config._get_user_tuple(message, Const.EDITED_CONTENT)
        else:
            lines = tuple(map(lambda s: s.strip(), message.rstrip().split(Const.NEWLINE)))

        return lines

    @classmethod
    def _get_edited_brief(cls, message, form):
        """Return content brief from editor."""

        brief = Const.EMPTY
        if form == Const.SNIPPET:
            brief = Config._get_user_string(message, Const.EDITED_BRIEF)
        else:
            match = re.search('## BRIEF :(.*)$', message)
            if match:
                brief = match.group(1).strip()

        cls.config['content']['brief'] = brief
        cls.logger.debug('configured value from editor for brief as "%s"', cls.config['content']['brief'])

    @classmethod
    def _get_edited_group(cls, message, form):
        """Return content group from editor."""

        group = Const.EMPTY
        if form == Const.SNIPPET:
            group = Config._get_user_string(message, Const.EDITED_GROUP)
        else:
            match = re.search('## GROUP :(.*)$', message)
            if match:
                group = match.group(1).strip()

        cls.config['content']['group'] = group
        cls.logger.debug('configured value from editor for group as "%s"', cls.config['content']['group'])

    @classmethod
    def _get_edited_tags(cls, message, form):
        """Return content tags from editor."""

        tags = Const.EMPTY
        if form == Const.SNIPPET:
            tags = Config._get_user_string(message, Const.EDITED_TAGS)
        else:
            match = re.search('## TAGS  :(.*)$', message)
            if match:
                tags = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.DELIMITER_TAGS)))

        cls.config['content']['tags'] = tags
        cls.logger.debug('configured value from editor for tags as "%s"', cls.config['content']['tags'])

