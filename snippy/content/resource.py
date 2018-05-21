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

"""resource: Single resource."""

import re
import hashlib

from snippy.config.constants import Constants as Const # TODO REMOVE
from snippy.logger import Logger


class Resource(object):  # pylint: disable=too-many-public-methods
    """Persiste one resource."""

    # Resource categories.
    SNIPPET = 'snippet'
    SOLUTION = 'solution'

    # Data delimiters
    DELIMITER_DATA = '\n'
    DELIMITER_TAGS = ','
    DELIMITER_LINKS = '\n'

    SOLUTION_TEMPLATE = '844d0d37738ff2d20783f97690f771bb47d81ef3a4bda4ee9d022a17919fd271'
    SNIPPET_TEMPLATE = 'b4bedc2603e3b9ea95bcf53cb7b8aa6efa31eabb788eed60fccf3d8029a6a6cc'
    TEMPLATES = (SNIPPET_TEMPLATE, SOLUTION_TEMPLATE)

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._data = ()
        self._brief = ''
        self._group = ''
        self._tags = ()
        self._links = ()
        self._category = ''
        self._filename = ''
        self._runalias = ''
        self._versions = ''
        self._created = ''
        self._updated = ''
        self._digest = self.compute_digest()

    def __str__(self):
        """Format string from the class object."""

        return self.convert_term(index=1, ansi=True, debug=True)

    @property
    def data(self):
        """Get resource data."""

        return self._data

    @data.setter
    def data(self, value):
        """Resource data is stored as a tuple with one line per element."""

        self._data = value

    @property
    def brief(self):
        """Get resource brief."""

        return self._brief

    @brief.setter
    def brief(self, value):
        """Resource brief."""

        self._brief = value

    @property
    def group(self):
        """Get resource group."""

        return self._group

    @group.setter
    def group(self, value):
        """Resource group."""

        self._group = value

    @property
    def tags(self):
        """Get resource tags."""

        return self._tags

    @tags.setter
    def tags(self, value):
        """Resource tags."""

        self._tags = value

    @property
    def links(self):
        """Get resource links."""

        return self._links

    @links.setter
    def links(self, value):
        """Resource links."""

        self._links = value

    @property
    def category(self):
        """Get resource category."""

        return self._category

    @category.setter
    def category(self, value):
        """Resource category."""

        self._category = value

    @property
    def filename(self):
        """Get resource filename."""

        return self._filename

    @filename.setter
    def filename(self, value):
        """Resource filename."""

        self._filename = value

    @property
    def runalias(self):
        """Get resource runalias."""

        return self._runalias

    @runalias.setter
    def runalias(self, value):
        """Resource runalias."""

        self._runalias = value

    @property
    def versions(self):
        """Get resource versions."""

        return self._versions

    @versions.setter
    def versions(self, value):
        """Resource versions."""

        self._versions = value

    @property
    def created(self):
        """Get resource created time."""

        return self._created

    @created.setter
    def created(self, value):
        """Resource created."""

        self._created = value

    @property
    def updated(self):
        """Get resource updated time."""

        return self._updated

    @updated.setter
    def updated(self, value):
        """Resource updated."""

        self._updated = value

    @property
    def digest(self):
        """Get resource digest."""

        return self._digest

    @digest.setter
    def digest(self, value):
        """Resource digest."""

        self._digest = value

    @property
    def metadata(self):
        """Get resource metadata."""

        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """Resource metadata."""

        self._metadata = value

    @property
    def key(self):
        """Get resource key."""

        return self._key

    @key.setter
    def key(self, value):
        """Resource key."""

        self._key = value

    def compute_digest(self):
        """Compute digest from the content."""

        resource_str = Resource.DELIMITER_DATA.join(map(str, self.data))
        resource_str = resource_str + self.brief
        resource_str = resource_str + self.group
        resource_str = resource_str + Resource.DELIMITER_TAGS.join(map(str, sorted(self.tags)))
        resource_str = resource_str + Resource.DELIMITER_LINKS.join(map(str, sorted(self.links)))
        resource_str = resource_str + self.category
        resource_str = resource_str + self.filename
        resource_str = resource_str + self.runalias
        resource_str = resource_str + self.versions
        digest = hashlib.sha256(resource_str.encode('UTF-8')).hexdigest()

        return digest

    def migrate(self, source):
        """Migrate source into Resource."""

        # TODO: Remove when refactoring done.
        from snippy.content.content import Content

        if isinstance(source, Content):
            self.data = source.get_data()
            self.brief = source.get_brief()
            self.group = source.get_group()
            self.tags = source.get_tags()
            self.links = source.get_links()
            self.category = source.get_category()
            self.filename = source.get_filename()
            self.runalias = source.get_runalias()
            self.versions = source.get_versions()
            self.created = source.get_created()
            self.updated = source.get_updated()
            self.digest = source.get_digest()
            self.metadata = source.get_metadata()
            self.key = source.get_key()
        elif isinstance(source, (list,tuple)):
            self.data = tuple(source[0].split(Resource.DELIMITER_DATA))
            self.brief = source[1]
            self.group = source[2]
            self.tags = tuple(source[3].split(Resource.DELIMITER_TAGS) if source[3] else [])
            self.links = tuple(source[4].split(Resource.DELIMITER_LINKS) if source[4] else [])
            self.category = source[5]
            self.filename = source[6]
            self.runalias = source[7]
            self.versions = source[8]
            self.created = source[9]
            self.updated = source[10]
            self.digest = source[11]
            self.metadata = source[12]
            self.key = source[13]

    def merge(self, source):
        """Merge two resource.

        This overrides original resource fields only if the merged source
        fields exists.
        """

        if source:
            if source.data:
                self.data = source.data
            if source.brief:
                self.brief = source.brief
            if source.tags:
                self.tags = source.tags
            if source.links:
                self.links = source.links
            self.digest = self.compute_digest()

    def is_template(self):
        """Test if resource data is empty template."""

        return True if self.digest in Resource.TEMPLATES else False

    def has_data(self):
        """Test if content has data defined."""

        return True if self.data or any(self.data) else False

    def is_snippet(self):
        """Test if resource is snippet."""

        return True if self.category == Resource.SNIPPET else False

    def dump_qargs(self):
        """Convert resource for sqlite qargs."""

        qargs = (
            Resource.DELIMITER_DATA.join(map(str, self.data)),
            self.brief,
            self.group,
            Resource.DELIMITER_TAGS.join(map(str, sorted(self.tags))),
            Resource.DELIMITER_LINKS.join(map(str, sorted(self.links))),
            self.category,
            self.filename,
            self.runalias,
            self.versions,
            self.created,
            self.updated,
            self.digest,
            self.metadata,
        )

        return qargs

    def dump_json(self, remove_fields):
        """Convert resource to json."""

        json = {
            'data': self.data,
            'brief': self.brief,
            'group': self.group,
            'tags': self.tags,
            'links': self.links,
            'category': self.category,
            'filename': self.filename,
            'runalias': self.runalias,
            'versions': self.versions,
            'created': self.created,
            'updated': self.updated,
            'digest': self.digest
        }

        for field in remove_fields:
            json.pop(field, None)

        return json

    def dump_text(self, templates):
        """Convert resource to text."""

        text = templates[self.category]
        text = self._add_data(text)
        text = self._add_brief(text)
        text = self._add_group(text)
        text = self._add_tags(text)
        text = self._add_links(text)
        text = self._add_filename(text)

        return text

    def _add_data(self, template):
        """Add resource data to text template."""

        data = Resource.DELIMITER_DATA.join(map(str, self.data))
        if data:
            if self.is_snippet():
                template = re.sub('<SNIPPY_DATA>.*<SNIPPY_DATA>', data, template, flags=re.DOTALL)
            else:
                template = data
        else:
            template = template.replace('<SNIPPY_DATA>', Const.EMPTY)

        return template

    def _add_brief(self, template):
        """Add resource brief to text template."""

        brief = self.brief
        template = template.replace('<SNIPPY_BRIEF>', brief)

        return template

    def _add_group(self, template):
        """Add resource group to text template."""

        group = self.group
        template = template.replace('<SNIPPY_GROUP>', group)

        return template

    def _add_tags(self, template):
        """Add resource tags to text template."""

        tags = Resource.DELIMITER_TAGS.join(map(str, self.tags))
        template = template.replace('<SNIPPY_TAGS>', tags)

        return template

    def _add_links(self, template):
        """Add resource links to text template."""

        links = Resource.DELIMITER_LINKS.join(map(str, self.links))
        links = links + Const.NEWLINE  # Links is the last item in snippet template and this adds extra newline at the end.
        template = template.replace('<SNIPPY_LINKS>', links)

        return template

    def _add_filename(self, template):
        """Add resource filename to text template."""

        filename = self.filename
        template = template.replace('<SNIPPY_FILE>', filename)

        return template

    def convert_term(self, index, ansi, debug):
        """Convert resource to be printed to terminal."""

        text = Const.EMPTY
        if self.is_snippet():
            text = text + self.get_snippet_text(index, ansi)
        else:
            text = text + self.get_solution_text(index, ansi)

        if debug:
            text = text + self._terminal_category(ansi) % self.category
            text = text + self._terminal_filename(ansi) % self.filename
            text = text + self._terminal_runalias(ansi) % self.runalias
            text = text + self._terminal_versions(ansi) % self.versions
            text = text + self._terminal_created(ansi) % self.created
            text = text + self._terminal_updated(ansi) % self.updated
            text = text + self._terminal_digest(ansi) % (self.digest,
                                                         self.digest == self.compute_digest())
            text = text + self._terminal_metadata(ansi) % self.metadata
            text = text + self._terminal_key(ansi) % self.key
            text = text + Const.NEWLINE

        return text

    def get_snippet_text(self, idx, ansi=False):
        """Format snippets for terminal or pure text output."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Resource._terminal_header(ansi) % (idx, self.brief,
                                                        self.group,
                                                        self.digest)
        text = text + Const.EMPTY.join([Resource._terminal_snippet(ansi) % (data, line)
                                        for line in self.data])
        text = text + Const.NEWLINE
        text = Resource._terminal_tags(ansi) % (text, Const.DELIMITER_TAGS.join(self.tags))
        text = text + Const.EMPTY.join([Resource._terminal_links(ansi) % (links, link)
                                        for link in self.links])
        text = text + Const.NEWLINE

        return text

    def get_solution_text(self, idx, ansi=False):
        """Format solutions for terminal or pure text output."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Resource._terminal_header(ansi) % (idx, self.brief,
                                                        self.group,
                                                        self.digest)
        text = text + Const.NEWLINE
        text = Resource._terminal_tags(ansi) % (text, Const.DELIMITER_TAGS.join(self.tags))
        text = text + Const.EMPTY.join([Resource._terminal_links(ansi) % (links, link)
                                        for link in self.links])
        text = text + Const.NEWLINE

        text = text + Const.EMPTY.join([Resource._terminal_solution(ansi) % (data, line)
                                        for line in self.data])
        text = text + Const.NEWLINE

        return text

    @staticmethod
    def _terminal_header(ansi=False):
        """Format content text header."""

        return '\x1b[96;1m%d. \x1b[1;92m%s\x1b[0m @%s \x1b[0;2m[%.16s]\x1b[0m\n' if ansi \
               else '%d. %s @%s [%.16s]\n'

    @staticmethod
    def _terminal_snippet(ansi=False):
        """Format snippet text."""

        return '%s   \x1b[91m$\x1b[0m %s\n' if ansi else '%s   $ %s\n'

    @staticmethod
    def _terminal_solution(ansi=False):
        """Format solution text."""

        return '%s   \x1b[91m:\x1b[0m %s\n' if ansi else '%s   : %s\n'

    @staticmethod
    def _terminal_tags(ansi=False):
        """Format content tags."""

        return '%s   \x1b[91m#\x1b[0m \x1b[2m%s\x1b[0m\n' if ansi else '%s   # %s\n'

    @staticmethod
    def _terminal_links(ansi=False):
        """Format content links."""

        return '%s   \x1b[91m>\x1b[0m \x1b[2m%s\x1b[0m\n' if ansi else '%s   > %s\n'

    @staticmethod
    def _terminal_category(ansi=False):
        """Format content category."""

        return '   \x1b[91m!\x1b[0m \x1b[2mcategory\x1b[0m : %s\n' if ansi else '   ! category : %s\n'

    @staticmethod
    def _terminal_filename(ansi=False):
        """Format content filename."""

        return '   \x1b[91m!\x1b[0m \x1b[2mfilename\x1b[0m : %s\n' if ansi else '   ! filename : %s\n'

    @staticmethod
    def _terminal_runalias(ansi=False):
        """Format content runalias."""

        return '   \x1b[91m!\x1b[0m \x1b[2mrunalias\x1b[0m : %s\n' if ansi else '   ! runalias : %s\n'

    @staticmethod
    def _terminal_versions(ansi=False):
        """Format content version list."""

        return '   \x1b[91m!\x1b[0m \x1b[2mversions\x1b[0m : %s\n' if ansi else '   ! versions : %s\n'

    @staticmethod
    def _terminal_created(ansi=False):
        """Format content creation UTC timestamp."""

        return '   \x1b[91m!\x1b[0m \x1b[2mcreated\x1b[0m  : %s\n' if ansi else '   ! created  : %s\n'

    @staticmethod
    def _terminal_updated(ansi=False):
        """Format content UTC timestamp when it was updated."""

        return '   \x1b[91m!\x1b[0m \x1b[2mupdated\x1b[0m  : %s\n' if ansi else '   ! updated  : %s\n'

    @staticmethod
    def _terminal_digest(ansi=False):
        """Format content digest."""

        return '   \x1b[91m!\x1b[0m \x1b[2mdigest\x1b[0m   : %s (%s)\n' if ansi else '   ! digest   : %s (%s)\n'

    @staticmethod
    def _terminal_metadata(ansi=False):
        """Format content metadata."""

        return '   \x1b[91m!\x1b[0m \x1b[2mmetadata\x1b[0m : %s\n' if ansi else '   ! metadata : %s\n'

    @staticmethod
    def _terminal_key(ansi=False):
        """Format content key."""

        return '   \x1b[91m!\x1b[0m \x1b[2mkey\x1b[0m      : %s\n' if ansi else '   ! key      : %s\n'

    @staticmethod
    def get_dictionary_list(contents):
        """Convert content to dictionary format."""

        dictionary_list = []
        for entry in contents:
            dictionary_list.append(Migrate._get_dict_entry(entry))

        return dictionary_list

    @staticmethod
    def _get_dict_entry(content):
        """Convert content into dictionary."""

        dictionary = {'data': content.get_data(),
                      'brief': content.get_brief(),
                      'group': content.get_group(),
                      'tags': content.get_tags(),
                      'links': content.get_links(),
                      'category': content.get_category(),
                      'filename': content.get_filename(),
                      'runalias': content.get_runalias(),
                      'versions': content.get_versions(),
                      'created': content.get_created(),
                      'updated': content.get_updated(),
                      'digest': content.get_digest()}

        # Digest is always needed when JSON REST API response is constructed.
        # Because of this, the digest is not removed in here but just before
        # constructing the JSON API response.
        for field in Config.filter_fields:
            if field != 'digest':
                dictionary.pop(field, None)

        return dictionary
