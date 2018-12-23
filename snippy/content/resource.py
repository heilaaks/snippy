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

import datetime
import hashlib
import re
import textwrap
import traceback
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

    SNIPPET_TEMPLATE = 'b4bedc2603e3b9ea95bcf53cb7b8aa6efa31eabb788eed60fccf3d8029a6a6cc'
    SOLUTION_TEMPLATE = '79e4ae470cd135798d718a668c52dbca1e614187da8bb22eca63047681f8d146'
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
        self._uuid = self._get_external_uuid()
        self._created = timestamp
        self._updated = timestamp
        self._metadata = ''
        self._key = None
        self._digest = self.compute_digest()

    def __str__(self):
        """Format string from the class object."""

        return self.dump_term(index=1, use_ansi=True, debug_logs=True)

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

        Returns:
            bool: If the resource sealing was successful.
        """

        if self.category == Const.REFERENCE:
            self.data = self.links
        else:
            self.links = tuple(sorted(self.links))

        # There may be case where for example Yaml loading automatically
        # converts timestamps to datetime objects if the timestamps are
        # not surrounded by quotes. Internally the timestamps are stored
        # as strings.
        if isinstance(self.created, datetime.datetime):
            self.created = self.created.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        if isinstance(self.updated, datetime.datetime):
            self.updated = self.updated.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

        if not self.uuid:
            self.uuid = self._get_external_uuid()

        self.digest = self.compute_digest()

        is_empty = self.is_empty()
        is_template = self.is_template()

        return not bool(is_empty or is_template)

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

        return self.seal()

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

        return self.seal()

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

        if bool(self.digest in Resource.TEMPLATES):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because it was matching to an empty template')

        return bool(self.digest in Resource.TEMPLATES)

    def is_empty(self):
        """Test if resource does not have mandatory data.

        In case of snippet and solution, the content data must be present.
        In case of references, the link must be present.
        """

        if self.category in (Const.SNIPPET, Const.SOLUTION) and not any(self.data):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field data is empty')

            return True
        if self.category == Const.REFERENCE and not any(self.links):
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field links is empty')

            return True

        return False

    def is_snippet(self):
        """Test if resource is snippet."""

        return bool(self.category == Const.SNIPPET)

    def is_solution(self):
        """Test if resource is solution."""

        return bool(self.category == Const.SOLUTION)

    def is_reference(self):
        """Test if resource is reference."""

        return bool(self.category == Const.REFERENCE)

    def dump_qargs(self):
        """Convert resource for storage.

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

        # Each line is replaced with escape characters so that the user
        # defined special character combinations like \n for new line
        # are not interpolated.
        text = templates['text'][self.category]
        if self.data:
            try:
                text = re.sub(r'''
                    [<data>]{6}         # Match <data> tag.
                    (.*[<data>]{6})?    # Match optional closing <data> tag and all data between the tags.
                    ''', Const.DELIMITER_DATA.join([line.replace('\\', '\\\\') for line in self.data]), text, flags=re.DOTALL | re.VERBOSE)
            except (re.error, TypeError):
                self._logger.info('failed to replace content data in text template: {}'.format(traceback.format_exc()))
                self._logger.info('failed to replace content data: {}'.format(self.data))
                self._logger.info('failed to replace content template: {}'.format(text))
        else:
            text = text.replace('<data>', Const.EMPTY)
            text = text.lstrip()
        text = text.replace('<brief>', self.brief)
        text = text.replace('<description>', self.description)
        text = text.replace('<groups>', Const.DELIMITER_GROUPS.join(self.groups))
        text = text.replace('<tags>', Const.DELIMITER_TAGS.join(self.tags))
        text = text.replace('<links>', Const.DELIMITER_LINKS.join(self.links))
        text = text.replace('<filename>', self.filename)

        return text

    def dump_mkdn(self, templates):
        """Convert resource to Markdown.

        Long lines are wrapped so that there are two spaces at the end of
        newline. This same approach with the trailing spaces is used with
        the metadata in the Markdown template.
        """

        mkdn = templates['mkdn'][self.category]
        mkdn = mkdn.replace('<data>', self._dump_mkdn_data())
        mkdn = mkdn.replace('<brief>', self.brief)
        mkdn = mkdn.replace('<description>', textwrap.fill(self.description, 88).replace('\n', '  \n'))
        mkdn = mkdn.replace('<groups>', Const.DELIMITER_GROUPS.join(self.groups))
        mkdn = mkdn.replace('<tags>', Const.DELIMITER_TAGS.join(self.tags))
        mkdn = mkdn.replace('<links>', self._dump_mkdn_links())
        mkdn = mkdn.replace('<category>', self.category)
        mkdn = mkdn.replace('<name>', self.name)
        mkdn = mkdn.replace('<filename>', self.filename)
        mkdn = mkdn.replace('<versions>', self.versions)
        mkdn = mkdn.replace('<source>', self.source)
        mkdn = mkdn.replace('<uuid>', self.uuid)
        mkdn = mkdn.replace('<created>', self.created)
        mkdn = mkdn.replace('<updated>', self.updated)
        mkdn = mkdn.replace('<digest>', self.digest)

        return mkdn

    def _dump_mkdn_data(self):
        """Dump resource data to Markdown format.

        Snippet data contains commands that may have comment. The comment
        is extracted from the command string and used as a header in the
        Markdown formatted data.
        """

        data = Const.EMPTY
        if self.is_snippet():
            for command in self.data:
                match = re.compile(r'''
                    (?P<command>.*?)                # Catch mandatory command.
                    (?:\s+[#]\s+(?P<comment>.*)|$)  # Catch optional comment.
                    ''', re.VERBOSE).search(command)
                if match:
                    if match.group('comment'):
                        data = data + "- " + match.group('comment') + Const.NEWLINE * 2
                        data = data + "    `$ " + match.group('command') + "`" + Const.NEWLINE * 2
                    else:
                        data = data + "`$ " + match.group('command') + "`" + Const.NEWLINE
                else:
                    self._logger.debug('command parsing failed: %s', command)
            data = data.rstrip()
        elif self.is_solution():
            data = '```\n'
            data = data + Const.DELIMITER_DATA.join(self.data)
            data = data + '```'

        return data

    def _dump_mkdn_links(self):
        """Dump resource links to Markdown format.

        Extra spaces at the end of link is needed to get the Markdown syntax
        with multiple links to wrap correctly for every link.
        """

        links = Const.EMPTY
        for i, link in enumerate(self.links, start=1):
            links = links + "[%s] " % i + link + '  ' + Const.NEWLINE
        links = links.rstrip()

        return links

    def dump_term(self, index, use_ansi, debug_logs):  # noqa pylint: disable=too-many-statements
        """Convert resource for terminal output."""

        # In order to print unicode characters in Python 2, the strings
        # below must be defined as unicode strings with u''.
        indent = Const.SPACE * (2 + len(str(index)))

        if use_ansi:
            header = u'\x1b[96;1m{i}. \x1b[1;92m{brief}\x1b[0m @{groups} \x1b[0;2m[{digest:.16}]\x1b[0m\n'
            tags = u'{indent}\x1b[91m#\x1b[0m \x1b[2m{tag}\x1b[0m\n'
            links = u'{indent}\x1b[91m>\x1b[0m \x1b[2m{link}\x1b[0m\n'
            data = u'{indent}\x1b[91m{symbol}\x1b[0m {line}\n'
            meta = u'{indent}\x1b[91m!\x1b[0m \x1b[2m{key}\x1b[0m{align}: {value}\n'
            digest = u'{indent}\x1b[91m!\x1b[0m \x1b[2m{key}\x1b[0m{align}: {value} ({test})\n'
        else:
            header = u'{i}. {brief} @{groups} [{digest:.16}]\n'
            tags = u'{indent}# {tag}\n'
            links = u'{indent}> {link}\n'
            data = u'{indent}{symbol} {line}\n'
            meta = u'{indent}! {key}{align}: {value}\n'
            digest = u'{indent}! {key}{align}: {value} ({test})\n'

        text = Const.EMPTY
        if self.is_snippet():
            aligned_data = self._align_snippet_comments(self.data, use_ansi)
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            text = text + Const.NEWLINE
            text = text + Const.EMPTY.join([data.format(indent=indent, symbol='$', line=line) for line in aligned_data])
            text = text + Const.NEWLINE
            text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
            text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in self.links])
            text = text + Const.NEWLINE
        elif self.is_solution():
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            text = text + Const.NEWLINE
            text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
            text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in self.links])
            text = text + Const.NEWLINE
            text = text + Const.EMPTY.join([data.format(indent=indent, symbol=':', line=line) for line in self.data])
            text = text + Const.NEWLINE
        elif self.is_reference():
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            text = text + Const.NEWLINE
            text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in self.links])
            text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
            text = text + Const.NEWLINE
        else:
            self._logger.debug('internal error with content category: %s', self.category)

        if debug_logs:
            if self.is_reference():
                text = text + Const.EMPTY.join([meta.format(indent=indent, key='data', align=' ' * 8, value=line) for line in self.data])
            text = text + meta.format(indent=indent, key='category', align=' ' * 4, value=self.category)
            text = text + meta.format(indent=indent, key='created', align=' ' * 5, value=self.created)
            text = text + meta.format(indent=indent, key='description', align=' ' * 1, value=self.description)
            text = text + digest.format(indent=indent, key='digest', align=' ' * 6, value=self.digest, test=self.digest == self.compute_digest())  # noqa pylint: disable=line-too-long
            text = text + meta.format(indent=indent, key='filename', align=' ' * 4, value=self.filename)
            text = text + meta.format(indent=indent, key='key', align=' ' * 9, value=self.key)
            text = text + meta.format(indent=indent, key='metadata', align=' ' * 4, value=self.metadata)
            text = text + meta.format(indent=indent, key='name', align=' ' * 8, value=self.name)
            text = text + meta.format(indent=indent, key='source', align=' ' * 6, value=self.source)
            text = text + meta.format(indent=indent, key='updated', align=' ' * 5, value=self.updated)
            text = text + meta.format(indent=indent, key='uuid', align=' ' * 8, value=self.uuid)
            text = text + meta.format(indent=indent, key='versions', align=' ' * 4, value=self.versions)
            text = text + Const.NEWLINE

        # Unicode character string must be encoded for Python 2 in order
        # to get it printed to terminal.
        if Const.PYTHON2:
            text = text.encode('utf-8')

        return text

    def _align_snippet_comments(self, data, use_ansi):
        """Align comments in multiple lines of snippet data.

        Alignment is made only based on commands which have comment. This
        avoids too long lines in case the snippet without comment is very
        long.

        Original order of commands must not be changed.
        """

        max_len = 0
        aligned = ()
        snippets = []
        for command in data:
            match = Const.RE_CATCH_COMMAND_AND_COMMENT.search(command)
            if match:
                snippets.append({'command': match.group('command').strip(), 'comment': match.group('comment').strip()})
                if match.group('comment'):
                    max_len = max(max_len, len(match.group('command')))
            else:
                self._logger.debug('parser did not match command for comment alignment: %s', command)
                snippets.append({'command': command, 'comment': Const.EMPTY})

        separator = Const.SNIPPET_COMMENT
        if use_ansi:
            separator = Const.SNIPPET_COMMENT_COLOR
        for snippet in snippets:
            if snippet['comment']:
                aligned = aligned + ('{:<{len}}{}{}'.format(snippet['command'], separator, snippet['comment'], len=max_len), )
            else:
                aligned = aligned + (snippet['command'],)

        return aligned

    @staticmethod
    def _get_external_uuid():
        """Get externally used UUID.

        This UUID is intended to be visible outside the REST API server. The
        UUID must not contain hardware addresses like MAC address used in
        UUID1. The reason is that this would reveal hardware MAC address and
        possibly the physical location of the server.

        UUID4 is used in order to allocate pseudo-random UUID that does not
        contain physical identities like MAC.

        Returns:
            str: UUID4 string.
        """

        return str(uuid.uuid4())
