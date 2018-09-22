#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

import hashlib
import re
import uuid

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.logger import Logger


class Resource(object):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
    """Persiste one resource."""

    # Database column numbers.
    DATA = 0
    BRIEF = 1
    DESCRIPTION = 2
    GROUPS = 3
    TAGS = 4
    LINKS = 5
    CATEGORY = 6
    NAME = 7
    FILENAME = 8
    VERSIONS = 9
    SOURCE = 10
    UUID = 11
    CREATED = 12
    UPDATED = 13
    DIGEST = 14
    METADATA = 15
    KEY = 16

    SOLUTION_TEMPLATE = '79e4ae470cd135798d718a668c52dbca1e614187da8bb22eca63047681f8d146'
    SNIPPET_TEMPLATE = 'b4bedc2603e3b9ea95bcf53cb7b8aa6efa31eabb788eed60fccf3d8029a6a6cc'
    REFERENCE_TEMPLATE = 'e0cd55c650ef936a66633ee29500e47ee60cc497c342212381c40032ea2850d9'
    TEMPLATES = (SNIPPET_TEMPLATE, SOLUTION_TEMPLATE, REFERENCE_TEMPLATE)

    def __init__(self, category='', timestamp=''):
        self._logger = Logger.get_logger(__name__)
        self._data = ()
        self._brief = ''
        self._description = ''
        self._groups = Const.DEFAULT_GROUPS
        self._tags = ()
        self._links = ()
        self._category = category
        self._name = ''
        self._filename = ''
        self._versions = ''
        self._source = ''
        self._uuid = str(uuid.uuid1())
        self._created = timestamp
        self._updated = timestamp
        self._metadata = ''
        self._key = ''
        self._digest = self.compute_digest()

    def __str__(self):
        """Format string from the class object."""

        return self.dump_term(index=1, ansi=True, debug=True)

    def __eq__(self, resource):
        """Compare resources if they are equal."""

        if type(resource) is type(self):
            # Resource key is defined by database and it is not compared.
            return self.data == resource.data and \
                   self.brief == resource.brief and \
                   self.description == resource.description and \
                   self.groups == resource.groups and \
                   self.tags == resource.tags and \
                   self.links == resource.links and \
                   self.category == resource.category and \
                   self.name == resource.name and \
                   self.filename == resource.filename and \
                   self.versions == resource.versions and \
                   self.source == resource.source and \
                   self.uuid == resource.uuid and \
                   self.created == resource.created and \
                   self.updated == resource.updated and \
                   self.metadata == resource.metadata and \
                   self.digest == resource.digest

        return False

    def __ne__(self, resource):
        """Compare resources if they are not equal."""

        return not self == resource

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
    def description(self):
        """Get resource description."""

        return self._description

    @description.setter
    def description(self, value):
        """Resource description."""

        self._description = value

    @property
    def groups(self):
        """Get resource groups."""

        return self._groups

    @groups.setter
    def groups(self, value):
        """Resource groups."""

        self._groups = value

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
    def name(self):
        """Get resource name."""

        return self._name

    @name.setter
    def name(self, value):
        """Resource name."""

        self._name = value

    @property
    def versions(self):
        """Get resource versions."""

        return self._versions

    @versions.setter
    def versions(self, value):
        """Resource versions."""

        self._versions = value

    @property
    def source(self):
        """Get resource source."""

        return self._source

    @source.setter
    def source(self, value):
        """Resource source."""

        self._source = value

    @property
    def uuid(self):
        """Get resource uuid."""

        return self._uuid

    @uuid.setter
    def uuid(self, value):
        """Resource uuid."""

        self._uuid = value

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

        resource_str = Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, self.data))
        resource_str = resource_str + self.brief
        resource_str = resource_str + self.description
        resource_str = resource_str + Const.DELIMITER_GROUPS.join(map(Const.TEXT_TYPE, sorted(self.groups)))
        resource_str = resource_str + Const.DELIMITER_TAGS.join(map(Const.TEXT_TYPE, sorted(self.tags)))
        resource_str = resource_str + Const.DELIMITER_LINKS.join(map(Const.TEXT_TYPE, self.links))
        resource_str = resource_str + self.category
        resource_str = resource_str + self.name
        resource_str = resource_str + self.filename
        resource_str = resource_str + self.versions
        digest = hashlib.sha256(resource_str.encode('UTF-8')).hexdigest()

        return digest

    def seal(self):
        """Seal content by updating digest and run content specific tasks.

        In case of reference content, the links are treated as content data.
        The tool has been built to expect always the data part and it was
        considered that it is more maintanable to to it like this instead
        of adding extra logic around the code.
        """

        if self.category == Const.REFERENCE:
            self.data = self.links
        else:
            self.links = tuple(sorted(self.links))

        self.digest = self.compute_digest()
        self.has_data()

    def migrate(self, source):
        """Migrate source into Resource.

        This always overrides fields that can be modified by user. Only the
        fields that can be modified by end user are updated.
        """

        self._logger.debug('migrate to resouce: %.16s', self.digest)
        self.data = source.data
        self.brief = source.brief
        self.description = source.description
        self.groups = source.groups
        self.tags = source.tags
        self.links = source.links
        self.name = source.name
        self.filename = source.filename
        self.versions = source.versions
        self.source = source.source
        self.seal()

    def merge(self, source):
        """Merge two resources.

        This overrides original resource fields only if the merged source
        fields exists. Only the fields that can be modified by end user are
        updated.
        """

        if not source:
            return None

        self._logger.debug('merge to resouce: %.16s', self.digest)
        if source.data:
            self.data = source.data
        if source.brief:
            self.brief = source.brief
        if source.description:
            self.description = source.description
        if source.groups and Const.DEFAULT_GROUPS != source.groups:
            self.groups = source.groups
        if source.tags:
            self.tags = source.tags
        if source.links:
            self.links = source.links
        if source.name:
            self.name = source.name
        if source.filename:
            self.filename = source.filename
        if source.versions:
            self.versions = source.versions
        if source.source:
            self.source = source.source

        self.seal()

        return self.digest

    def convert(self, row):
        """Convert database row into resource."""

        self.data = tuple(row[Resource.DATA].split(Const.DELIMITER_DATA))
        self.brief = row[Resource.BRIEF]
        self.description = row[Resource.DESCRIPTION]
        self.groups = tuple(row[Resource.GROUPS].split(Const.DELIMITER_GROUPS) if row[Resource.GROUPS] else [])
        self.tags = tuple(row[Resource.TAGS].split(Const.DELIMITER_TAGS) if row[Resource.TAGS] else [])
        self.links = tuple(row[Resource.LINKS].split(Const.DELIMITER_LINKS) if row[Resource.LINKS] else [])
        self.category = row[Resource.CATEGORY]
        self.name = row[Resource.NAME]
        self.filename = row[Resource.FILENAME]
        self.versions = row[Resource.VERSIONS]
        self.source = row[Resource.SOURCE]
        self.uuid = row[Resource.UUID]
        self.created = row[Resource.CREATED]
        self.updated = row[Resource.UPDATED]
        self.digest = row[Resource.DIGEST]
        self.metadata = row[Resource.METADATA]
        self.key = row[Resource.KEY]

    def is_template(self):
        """Test if resource data is empty template."""

        return True if self.digest in Resource.TEMPLATES else False

    def has_data(self):
        """Test if resource has data.

        In case of snippet and solution, the content data must be present.
        In case of references, the link must be present.
        """

        if self.category in (Const.SNIPPET, Const.SOLUTION) and not any(self.data):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field data is empty')

            return False
        if self.category == Const.REFERENCE and not any(self.links):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field links is empty')

            return False

        return True

    def is_snippet(self):
        """Test if resource is snippet."""

        return True if self.category == Const.SNIPPET else False

    def is_solution(self):
        """Test if resource is solution."""

        return True if self.category == Const.SOLUTION else False

    def is_reference(self):
        """Test if resource is reference."""

        return True if self.category == Const.REFERENCE else False

    def dump_qargs(self):
        """Convert resource for sqlite qargs.

        Links are not sorted because it is assumed that link order matter
        for the end user. For example with reference content, it is possible
        to store multiple links. It is assumed that the first link holds the
        most valuable information.
        """

        qargs = (
            Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, self.data)),
            self.brief,
            self.description,
            Const.DELIMITER_GROUPS.join(map(Const.TEXT_TYPE, sorted(self.groups))),
            Const.DELIMITER_TAGS.join(map(Const.TEXT_TYPE, sorted(self.tags))),
            Const.DELIMITER_LINKS.join(map(Const.TEXT_TYPE, self.links)),
            self.category,
            self.name,
            self.filename,
            self.versions,
            self.source,
            self.uuid,
            self.created,
            self.updated,
            self.digest,
            self.metadata,
        )

        return qargs

    def load_dict(self, dictionary):
        """Convert dictionary to resource."""

        self.data = dictionary.get('data', self.data)
        self.brief = dictionary.get('brief', self.brief)
        self.description = dictionary.get('description', self.description)
        self.groups = tuple(sorted(dictionary.get('groups', self.groups)))
        self.tags = tuple(sorted(dictionary.get('tags', self.tags)))
        self.links = tuple(dictionary.get('links', self.links))
        self.category = dictionary.get('category', self.category)
        self.name = dictionary.get('name', self.name)
        self.filename = dictionary.get('filename', self.filename)
        self.versions = dictionary.get('versions', self.versions)
        self.source = dictionary.get('source', self.source)
        self.uuid = dictionary.get('uuid', self.uuid)
        self.created = dictionary.get('created', self.created)
        self.updated = dictionary.get('updated', self.updated)
        self.digest = dictionary.get('digest', self.digest)
        self.metadata = None
        self.key = None

        self.digest = self.compute_digest()

    def dump_dict(self, remove_fields):
        """Convert resource to dictionary."""

        data = {
            'data': self.data,
            'brief': self.brief,
            'description': self.description,
            'groups': self.groups,
            'tags': self.tags,
            'links': self.links,
            'category': self.category,
            'name': self.name,
            'filename': self.filename,
            'versions': self.versions,
            'source': self.source,
            'uuid': self.uuid,
            'created': self.created,
            'updated': self.updated,
            'digest': self.digest,
        }

        # Data field in case of reference is just for internal purposes. The
        # data field is not meant to be externally visible for references.
        if self.category == Const.REFERENCE:
            data['data'] = ()

        for field in remove_fields:
            data.pop(field, None)

        return data

    def dump_text(self, templates):
        """Convert resource to text."""

        text = templates[self.category]
        text = self._add_data(text)
        text = self._add_brief(text)
        text = self._add_groups(text)
        text = self._add_tags(text)
        text = self._add_links(text)
        text = self._add_filename(text)

        return text

    def dump_term(self, index, ansi, debug):
        """Convert resource to be printed to terminal."""

        data = Const.EMPTY
        text = Const.EMPTY
        if self.is_snippet():
            text = text + self.get_snippet_text(index, ansi)
        elif self.is_solution():
            text = text + self.get_solution_text(index, ansi)
        elif self.is_reference():
            text = text + self.get_reference_text(index, ansi)
        else:
            self._logger.debug('internal error with content category: s', self.category)

        if debug:
            if self.is_reference():
                text = text + Const.EMPTY.join([Resource._terminal_reference(ansi) % (data, line)
                                                for line in self.data])
            text = text + self._terminal_description(ansi) % self.description
            text = text + self._terminal_category(ansi) % self.category
            text = text + self._terminal_name(ansi) % self.name
            text = text + self._terminal_filename(ansi) % self.filename
            text = text + self._terminal_versions(ansi) % self.versions
            text = text + self._terminal_source(ansi) % self.source
            text = text + self._terminal_uuid(ansi) % self.uuid
            text = text + self._terminal_created(ansi) % self.created
            text = text + self._terminal_updated(ansi) % self.updated
            text = text + self._terminal_digest(ansi) % (self.digest,
                                                         self.digest == self.compute_digest())
            text = text + self._terminal_metadata(ansi) % self.metadata
            text = text + self._terminal_key(ansi) % self.key
            text = text + Const.NEWLINE

        # Unicode character string must be encoded for Python 2 in order
        # to get it printed to terminal.
        if Const.PYTHON2:
            text = text.encode('utf-8')

        return text

    def get_snippet_text(self, idx, ansi=False):
        """Format snippets for terminal."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Resource._terminal_header(ansi) % (idx, self.brief,
                                                         Const.DELIMITER_GROUPS.join(self.groups),
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
        """Format solutions for terminal."""

        text = Const.EMPTY
        data = Const.EMPTY
        links = Const.EMPTY
        text = text + Resource._terminal_header(ansi) % (idx, self.brief,
                                                         Const.DELIMITER_GROUPS.join(self.groups),
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

    def get_reference_text(self, idx, ansi=False):
        """Format references for terminal."""

        text = Const.EMPTY
        links = Const.EMPTY
        text = text + Resource._terminal_header(ansi) % (idx, self.brief,
                                                         Const.DELIMITER_GROUPS.join(self.groups),
                                                         self.digest)
        text = text + Const.NEWLINE
        text = text + Const.EMPTY.join([Resource._terminal_links(ansi) % (links, link)
                                        for link in self.links])
        text = Resource._terminal_tags(ansi) % (text, Const.DELIMITER_TAGS.join(self.tags))
        text = text + Const.NEWLINE

        return text

    def _add_data(self, template):
        """Add resource data to text template."""

        data = Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, self.data))
        if data:
            if self.is_snippet():
                template = re.sub('<SNIPPY_DATA>.*<SNIPPY_DATA>', data, template, flags=re.DOTALL)
            if self.is_solution():
                template = data
        else:
            template = template.replace('<SNIPPY_DATA>', Const.EMPTY)

        return template

    def _add_brief(self, template):
        """Add resource brief to text template."""

        brief = self.brief
        template = template.replace('<SNIPPY_BRIEF>', brief)

        return template

    def _add_groups(self, template):
        """Add resource groups to text template."""

        groups = Const.DELIMITER_GROUPS.join(map(Const.TEXT_TYPE, sorted(self.groups)))
        template = template.replace('<SNIPPY_GROUPS>', groups)

        return template

    def _add_tags(self, template):
        """Add resource tags to text template."""

        tags = Const.DELIMITER_TAGS.join(map(Const.TEXT_TYPE, sorted(self.tags)))
        template = template.replace('<SNIPPY_TAGS>', tags)

        return template

    def _add_links(self, template):
        """Add resource links to text template."""

        links = Const.DELIMITER_LINKS.join(map(Const.TEXT_TYPE, self.links))
        if self.category == Const.SNIPPET:
            links = links + Const.NEWLINE  # Links is the last item in snippet template and this adds an extra newline at the end.
        template = template.replace('<SNIPPY_LINKS>', links)

        return template

    def _add_filename(self, template):
        """Add resource filename to text template."""

        filename = self.filename
        template = template.replace('<SNIPPY_FILE>', filename)

        return template

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
    def _terminal_reference(ansi=False):
        """Format reference data."""

        return '%s   \x1b[91m!\x1b[0m \x1b[2mdata\x1b[0m     : %s\n' if ansi else '   ! data     : %s\n'

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

        return '   \x1b[91m!\x1b[0m \x1b[2mcategory\x1b[0m    : %s\n' if ansi else '   ! category    : %s\n'

    @staticmethod
    def _terminal_filename(ansi=False):
        """Format content filename."""

        return '   \x1b[91m!\x1b[0m \x1b[2mfilename\x1b[0m    : %s\n' if ansi else '   ! filename    : %s\n'

    @staticmethod
    def _terminal_name(ansi=False):
        """Format content name."""

        return '   \x1b[91m!\x1b[0m \x1b[2mname\x1b[0m        : %s\n' if ansi else '   ! name        : %s\n'

    @staticmethod
    def _terminal_versions(ansi=False):
        """Format content version list."""

        return '   \x1b[91m!\x1b[0m \x1b[2mversions\x1b[0m    : %s\n' if ansi else '   ! versions    : %s\n'

    @staticmethod
    def _terminal_source(ansi=False):
        """Format content source."""

        return '   \x1b[91m!\x1b[0m \x1b[2msource\x1b[0m      : %s\n' if ansi else '   ! source      : %s\n'

    @staticmethod
    def _terminal_description(ansi=False):
        """Format content description."""

        return '   \x1b[91m!\x1b[0m \x1b[2mdescription\x1b[0m : %s\n' if ansi else '   ! description : %s\n'

    @staticmethod
    def _terminal_uuid(ansi=False):
        """Format content uuid."""

        return '   \x1b[91m!\x1b[0m \x1b[2muuid\x1b[0m        : %s\n' if ansi else '   ! uuid        : %s\n'

    @staticmethod
    def _terminal_created(ansi=False):
        """Format content creation UTC timestamp."""

        return '   \x1b[91m!\x1b[0m \x1b[2mcreated\x1b[0m     : %s\n' if ansi else '   ! created     : %s\n'

    @staticmethod
    def _terminal_updated(ansi=False):
        """Format content UTC timestamp when it was updated."""

        return '   \x1b[91m!\x1b[0m \x1b[2mupdated\x1b[0m     : %s\n' if ansi else '   ! updated     : %s\n'

    @staticmethod
    def _terminal_digest(ansi=False):
        """Format content digest."""

        return '   \x1b[91m!\x1b[0m \x1b[2mdigest\x1b[0m      : %s (%s)\n' if ansi else '   ! digest      : %s (%s)\n'

    @staticmethod
    def _terminal_metadata(ansi=False):
        """Format content metadata."""

        return '   \x1b[91m!\x1b[0m \x1b[2mmetadata\x1b[0m    : %s\n' if ansi else '   ! metadata    : %s\n'

    @staticmethod
    def _terminal_key(ansi=False):
        """Format content key."""

        return '   \x1b[91m!\x1b[0m \x1b[2mkey\x1b[0m         : %s\n' if ansi else '   ! key         : %s\n'
