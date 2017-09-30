#!/usr/bin/env python3

"""editor.py: Editor based configuration."""

import re
import os.path
import pkg_resources
from snippy.config import Constants as Const
from snippy.logger import Logger


class Editor(object): # pylint: disable-all
    """Editor based configuration."""

    def __init__(self, content, utc):
        self.logger = Logger(__name__).get()
        self.content = content
        self.edited = Const.EMPTY
        self.utc = utc

    def read_content(self):
        """Read the content from editor."""

        import tempfile
        from subprocess import call

        template = self.read_template()
        template = self._set_template_data(template)
        template = self._set_template_brief(template)
        template = self._set_template_date(template)
        template = self._set_template_group(template)
        template = self._set_template_tags(template)
        template = self._set_template_links(template)
        template = self._set_template_filename(template)
        template = template.encode('UTF-8')

        editor = os.environ.get('EDITOR', 'vi')
        self.logger.info('using editor %s', editor)
        with tempfile.NamedTemporaryFile(prefix='snippy-edit-') as outfile:
            outfile.write(template)
            outfile.flush()
            call([editor, outfile.name])
            outfile.seek(0)
            message = outfile.read()

        self.edited = message.decode('UTF-8')

    def read_template(self):
        """Return content template."""

        template = Const.EMPTY
        if self.content.is_snippet():
            file = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), 'snippet-template.txt')
        else:
            file = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), 'solution-template.txt')

        with open(file, 'r') as infile:
            template = infile.read()

        return template

    def get_edited_data(self):
        """Return content data from editor."""

        data = ()
        if self.content.is_snippet():
            match = re.search('%s(.*)%s' % (Const.EDITOR_DATA_HEAD, Const.EDITOR_DATA_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                data = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.NEWLINE)))
        else:
            data = tuple(self.edited.rstrip().split(Const.NEWLINE))
        self.logger.debug('parsed content data from editor "%s"', data)

        return data

    def get_edited_brief(self):
        """Return content brief from editor."""

        brief = Const.EMPTY
        if self.content.is_snippet():
            match = re.search('%s(.*)%s' % (Const.EDITOR_BRIEF_HEAD, Const.EDITOR_BRIEF_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.DELIMITER_SPACE)))
                brief = Const.DELIMITER_SPACE.join(lines)
        else:
            match = re.search('## BRIEF :\s*(.*)', self.edited)
            if match:
                brief = match.group(1).strip()
        self.logger.debug('parsed content brief from editor "%s"', brief)

        return brief

    def get_edited_group(self):
        """Return content group from editor."""

        group = Const.EMPTY
        if self.content.is_snippet():
            match = re.search('%s(.*)%s' % (Const.EDITOR_GROUP_HEAD, Const.EDITOR_GROUP_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.DELIMITER_SPACE)))
                group = Const.DELIMITER_SPACE.join(lines)

        else:
            match = re.search('## GROUP :\s*(.*)', self.edited)
            if match:
                group = match.group(1).strip()
        self.logger.debug('parsed content group from editor "%s"', group)

        return group

    def get_edited_tags(self):
        """Return content tags from editor."""

        tags = ()
        if self.content.is_snippet():
            match = re.search('%s(.*)%s' % (Const.EDITOR_TAGS_HEAD, Const.EDITOR_TAGS_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                tags = Editor.get_keywords([match.group(1)])
        else:
            match = re.search('## TAGS  :\s*(.*)', self.edited)
            if match:
                tags = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.DELIMITER_TAGS)))
        self.logger.debug('parsed content tags from editor "%s"', tags)

        return tags

    def get_edited_links(self):
        """Return content links from editor."""

        # In case of solution, the links are read from the whole content data.
        links = ()
        if self.content.is_snippet():
            match = re.search('%s(.*)%s' % (Const.EDITOR_LINKS_HEAD, Const.EDITOR_LINKS_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                links = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.NEWLINE)))
        else:
            links = tuple(re.findall('> (http.*)', self.edited))
        self.logger.debug('parsed content links from editor "%s"', links)

        return links

    def get_edited_filename(self):
        """Return solution filename from editor."""

        # Only solutions use the optional file variable.
        filename = Const.EMPTY
        if self.content.get_category() == Const.SOLUTION:
            match = re.search(r'## FILE  :\s+(\S+)', self.edited)
            if match:
                filename = match.group(1)
        self.logger.debug('parsed content filename from editor "%s"', filename)

        return filename

    @staticmethod
    def get_keywords(keywords):
        """Preprocess the user given keyword list. The keywords are for example the
        user provided tags or the search keywords. The user may use various formats
        so each item in a list may be for example a string of comma separated tags.

        The dot is a special case. It is allowed for the regexp to match and print
        all records."""

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t dockertesting', container-managemenet', cleanup_testing
        #           6. --sall '.'
        kw_list = []
        for tag in keywords:
            kw_list = kw_list + re.findall(r"[\w\-\.]+", tag)

        sorted_list = sorted(kw_list)

        return tuple(sorted_list)

    def _set_template_data(self, template):
        """Update template content data."""

        data = self.content.get_data(Const.STRING_CONTENT)
        if data:
            if self.content.get_category() == Const.SOLUTION:
                template = data
            else:
                template = re.sub('<SNIPPY_DATA>.*<SNIPPY_DATA>', data, template, flags=re.DOTALL)
        else:
            template = template.replace('<SNIPPY_DATA>', Const.EMPTY)

        return template

    def _set_template_brief(self, template):
        """Update template content brief."""

        brief = self.content.get_brief(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_BRIEF>', brief)

        return template

    def _set_template_date(self, template):
        """Update template content date."""

        template = template.replace('<SNIPPY_DATE>', self.utc)

        return template

    def _set_template_group(self, template):
        """Update template content group."""

        group = self.content.get_group(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_GROUP>', group)

        return template

    def _set_template_tags(self, template):
        """Update template content tags."""

        tags = self.content.get_tags(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_TAGS>', tags)

        return template

    def _set_template_links(self, template):
        """Update template content links."""

        links = self.content.get_links(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_LINKS>', links)

        return template

    def _set_template_filename(self, template):
        """Update template content file."""

        filename = self.content.get_filename(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_FILE>', filename)

        return template

    @classmethod
    def _get_user_string(cls, edited_string, constants):
        """Parse string type value from editor input."""

        value_list = cls._get_user_tuple(edited_string, constants)

        return constants['delimiter'].join(value_list)

    @classmethod
    def _get_user_tuple(cls, edited_string, constants):
        """Parse list type value from editor input."""

        user_answer = re.search('%s(.*)%s' % (constants['head'], constants['tail']), edited_string, re.DOTALL)
        if user_answer and not user_answer.group(1).isspace():
            value_list = tuple(map(lambda s: s.strip(), user_answer.group(1).rstrip().split(constants['delimiter'])))

            return value_list

        return Const.EMPTY_TUPLE
