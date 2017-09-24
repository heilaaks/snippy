#!/usr/bin/env python3

"""editor.py: Editor based configuration."""

import re
import os.path
import datetime
import pkg_resources
from snippy.config import Constants as Const
from snippy.logger import Logger
from snippy.format import Format


class Editor(object): # pylint: disable-all
    """Editor based configuration."""

    def __init__(self, content, form):
        self.logger = Logger(__name__).get()
        self.content = content
        self.edited = Const.EMPTY
        self.form = form

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
        template = self._set_template_file(template)
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
        if self.form == Const.SNIPPET:
            file = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), 'snippet-template.txt')
        else:
            file = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), 'solution-template.txt')

        with open(file, 'r') as infile:
            template = infile.read()

        return template

    def get_edited_data(self):
        """Return content data from editor."""

        data = ()
        if self.form == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (Const.EDITOR_CONTENT_HEAD, Const.EDITOR_CONTENT_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                data = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.NEWLINE)))
        else:
            data = tuple(self.edited.rstrip().split(Const.NEWLINE))
        self.logger.debug('parsed content data from editor "%s"', data)

        return data

    def get_edited_brief(self):
        """Return content brief from editor."""

        brief = Const.EMPTY
        if self.form == Const.SNIPPET:
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
        if self.form == Const.SNIPPET:
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
        if self.form == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (Const.EDITOR_TAGS_HEAD, Const.EDITOR_TAGS_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                tags = Format.get_keywords([match.group(1)])
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
        if self.form == Const.SNIPPET:
            match = re.search('%s(.*)%s' % (Const.EDITOR_LINKS_HEAD, Const.EDITOR_LINKS_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                links = tuple(map(lambda s: s.strip(), match.group(1).rstrip().split(Const.NEWLINE)))
        else:
            links = tuple(re.findall('> (http.*)', self.edited))
        self.logger.debug('parsed content links from editor "%s"', links)
        
        return links

    def _set_template_data(self, template):
        """Update template content data."""

        data = Format.get_content_string(self.content)
        if data:
            if self.form == Const.SOLUTION:
                template = data
            else:
                template = re.sub('<SNIPPY_DATA>.*<SNIPPY_DATA>', data, template, flags=re.DOTALL)
        else:
            template = template.replace('<SNIPPY_DATA>', Const.EMPTY)

        return template

    def _set_template_brief(self, template):
        """Update template content brief."""

        brief = Format.get_brief_string(self.content)
        template = template.replace('<SNIPPY_BRIEF>', brief)

        return template

    def _set_template_date(self, template):
        """Update template content date."""

        utc = datetime.datetime.utcnow()
        template = template.replace('<SNIPPY_DATE>', utc.strftime("%Y-%m-%d %H:%M:%S"))

        return template

    def _set_template_group(self, template):
        """Update template content group."""

        group = Format.get_group_string(self.content)
        template = template.replace('<SNIPPY_GROUP>', group)

        return template

    def _set_template_tags(self, template):
        """Update template content tags."""

        tags = Format.get_tags_string(self.content)
        template = template.replace('<SNIPPY_TAGS>', tags)

        return template

    def _set_template_links(self, template):
        """Update template content links."""

        links = Format.get_links_string(self.content)
        template = template.replace('<SNIPPY_LINKS>', links)

        return template

    def _set_template_file(self, template):
        """Update template content file."""

        file = Format.get_file_string(self.content)
        template = template.replace('<SNIPPY_FILE>', file)

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