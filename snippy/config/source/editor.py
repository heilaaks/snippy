#!/usr/bin/env python3

"""editor.py: Editor based configuration."""

import re
import os.path
import datetime
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause


class Editor(object):
    """Editor based configuration."""

    # Editor inputs
    SOLUTION_BRIEF = '## BRIEF :'
    SOLUTION_DATE = '## DATE  :'
    SOLUTION_GROUP = '## GROUP :'
    DATA_HEAD = '# Add mandatory snippet below.\n'
    DATA_TAIL = '# Add optional brief description below.\n'
    BRIEF_HEAD = '# Add optional brief description below.\n'
    BRIEF_TAIL = '# Add optional single group below.\n'
    GROUP_HEAD = '# Add optional single group below.\n'
    GROUP_TAIL = '# Add optional comma separated list of tags below.\n'
    TAGS_HEAD = '# Add optional comma separated list of tags below.\n'
    TAGS_TAIL = '# Add optional links below one link per line.\n'
    LINKS_HEAD = '# Add optional links below one link per line.\n'
    LINKS_TAIL = '.'

    def __init__(self, content, utc, edited=Const.EMPTY):
        self.logger = Logger(__name__).get()
        self.content = content
        self.edited = edited
        self.is_snippet = self.get_edited_category() == Const.SNIPPET
        self.is_solution = self.get_edited_category() == Const.SOLUTION
        self.utc = utc

    def read_content(self):
        """Read the content from editor."""

        template = self.get_template()
        self.edited = self.call_editor(template)
        self.is_snippet = self.get_edited_category() == Const.SNIPPET
        self.is_solution = self.get_edited_category() == Const.SOLUTION

    def get_template(self):
        """Get template for editor."""

        template = self.read_template()
        template = self.set_template_data(template)
        template = self.set_template_brief(template)
        template = self.set_template_date(template)
        template = self.set_template_group(template)
        template = self.set_template_tags(template)
        template = self.set_template_links(template)
        template = self.set_template_filename(template)

        return template

    def is_content_identified(self):
        """Test if content category is identified."""

        identified = False
        if self.get_edited_category() == Const.SNIPPET or self.get_edited_category() == Const.SOLUTION:
            identified = True

        return identified

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
                Cause.set_text('required editor %s not installed %s' % (editor, exception))

        return message

    def get_edited_data(self):
        """Return content data from editor."""

        data = ()
        if self.is_snippet:
            match = re.search('%s(.*)%s' % (Editor.DATA_HEAD, Editor.DATA_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                data = tuple([s.strip() for s in match.group(1).rstrip().split(Const.NEWLINE)])
        else:
            # Remove unnecessary newlines at the end and make sure there is one at the end.
            data = tuple(self.edited.rstrip().split(Const.NEWLINE) + [Const.EMPTY])
        self.logger.debug('parsed content data from editor "%s"', data)

        return data

    def get_edited_brief(self):
        """Return content brief from editor."""

        brief = Const.EMPTY
        if self.is_snippet:
            match = re.search('%s(.*)%s' % (Editor.BRIEF_HEAD, Editor.BRIEF_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple([s.strip() for s in match.group(1).rstrip().split(Const.DELIMITER_SPACE)])
                brief = Const.DELIMITER_SPACE.join(lines)
        else:
            match = re.search(r'## BRIEF :\s*?(.*|$)', self.edited, re.MULTILINE)
            if match:
                brief = match.group(1).strip()
        self.logger.debug('parsed content brief from editor "%s"', brief)

        return brief

    def get_edited_date(self):
        """Return content date from editor."""

        # Read the time from 1) content or 2) time set for the object or from template.
        # The first two time stamps are used because it can be that user did not set
        # the date and time correctly to ISO 8601.
        if self.content.get_utc():
            date = self.content.get_utc()
        else:
            date = self.utc
        if self.is_solution:
            match = re.search(r'## DATE  :\s*?(.*|$)', self.edited, re.MULTILINE)
            if match:
                try:
                    datetime.datetime.strptime(match.group(1).strip(), '%Y-%m-%d %H:%M:%S')
                    date = match.group(1).strip()
                except ValueError:
                    self.logger.info('incorrect date and time format "%s"', match.group(1))

        self.logger.debug('parsed content date from editor "%s"', date)

        return date

    def get_edited_group(self):
        """Return content group from editor."""

        group = Const.EMPTY
        if self.is_snippet:
            match = re.search('%s(.*)%s' % (Editor.GROUP_HEAD, Editor.GROUP_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                lines = tuple([s.strip() for s in match.group(1).rstrip().split(Const.DELIMITER_SPACE)])
                group = Const.DELIMITER_SPACE.join(lines)
        else:
            match = re.search(r'## GROUP :\s*?(\S+|$)', self.edited, re.MULTILINE)
            if match:
                group = match.group(1).strip()
        self.logger.debug('parsed content group from editor "%s"', group)

        return group

    def get_edited_tags(self):
        """Return content tags from editor."""

        tags = ()
        if self.is_snippet:
            match = re.search('%s(.*)%s' % (Editor.TAGS_HEAD, Editor.TAGS_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                tags = Editor.get_keywords([match.group(1)])
        else:
            match = re.search(r'## TAGS  :\s*?(.*|$)', self.edited, re.MULTILINE)
            if match:
                tags = tuple([s.strip() for s in match.group(1).rstrip().split(Const.DELIMITER_TAGS)])
        self.logger.debug('parsed content tags from editor "%s"', tags)

        return tags

    def get_edited_links(self):
        """Return content links from editor."""

        # In case of solution, the links are read from the whole content data.
        links = ()
        if self.is_snippet:
            match = re.search('%s(.*)%s' % (Editor.LINKS_HEAD, Editor.LINKS_TAIL), self.edited, re.DOTALL)
            if match and not match.group(1).isspace():
                links = tuple([s.strip() for s in match.group(1).rstrip().split(Const.NEWLINE)])
        else:
            links = tuple(re.findall('> (http.*)', self.edited))
        self.logger.debug('parsed content links from editor "%s"', links)

        return links

    def get_edited_category(self):
        """Return content category based on edited content."""

        category = Const.UNKNOWN_CONTENT

        if Editor.DATA_HEAD in self.edited and Editor.BRIEF_HEAD:
            category = Const.SNIPPET
        elif Editor.SOLUTION_BRIEF in self.edited and Editor.SOLUTION_DATE:
            category = Const.SOLUTION

        return category

    def get_edited_filename(self):
        """Return solution filename from editor."""

        # Only solutions use the optional file variable.
        filename = Const.EMPTY
        if self.is_solution:
            match = re.search(r'## FILE  :\s*?(\S+|$)', self.edited, re.MULTILINE)
            if match and match.group(1):
                filename = match.group(1)
        self.logger.debug('parsed content filename from editor "%s"', filename)

        return filename

    def set_template_data(self, template):
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

    def set_template_brief(self, template):
        """Update template content brief."""

        brief = self.content.get_brief(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_BRIEF>', brief)

        return template

    def set_template_date(self, template):
        """Update template content date."""

        if '<SNIPPY_DATE>' in template:
            template = template.replace('<SNIPPY_DATE>', self.utc)
        else:
            match = re.search(r'(## DATE  :\s*?$)', template, re.MULTILINE)
            if match and self.content.get_utc():
                match.group(1).rstrip()
                template = template.replace(match.group(1), match.group(1) + Const.SPACE + self.content.get_utc())

        return template

    def set_template_group(self, template):
        """Update template content group."""

        group = self.content.get_group(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_GROUP>', group)

        return template

    def set_template_tags(self, template):
        """Update template content tags."""

        tags = self.content.get_tags(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_TAGS>', tags)

        return template

    def set_template_links(self, template):
        """Update template content links."""

        links = self.content.get_links(Const.STRING_CONTENT)
        links = links + Const.NEWLINE  # Links is the last item in snippet template and this adds extra newline at the end.
        template = template.replace('<SNIPPY_LINKS>', links)

        return template

    def set_template_filename(self, template):
        """Update template content file."""

        filename = self.content.get_filename(Const.STRING_CONTENT)
        template = template.replace('<SNIPPY_FILE>', filename)

        return template

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

    def read_template(self):
        """Return content template."""

        template = Const.EMPTY
        if self.content.is_snippet():
            filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), 'snippet-template.txt')
        else:
            filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/template'), 'solution-template.txt')

        with open(filename, 'r') as infile:
            template = infile.read()

        return template

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
