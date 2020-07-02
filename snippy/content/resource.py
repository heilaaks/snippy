# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
from snippy.content.parser import Parser
from snippy.logger import Logger


class Resource(object):  # pylint: disable=too-many-public-methods,too-many-instance-attributes,too-many-lines
    """Persiste one resource."""

    # Database column numbers.
    _ID = 0
    CATEGORY = 1
    DATA = 2
    BRIEF = 3
    DESCRIPTION = 4
    NAME = 5
    GROUPS = 6
    TAGS = 7
    LINKS = 8
    SOURCE = 9
    VERSIONS = 10
    LANGUAGES = 11
    FILENAME = 12
    CREATED = 13
    UPDATED = 14
    UUID = 15
    DIGEST = 16

    SNIPPET_TEMPLATE = 'b4bedc2603e3b9ea95bcf53cb7b8aa6efa31eabb788eed60fccf3d8029a6a6cc'
    SOLUTION_TEMPLATE_TEXT = 'be2ec3ade0e984463c1d3346910a05625897abd8d3feae4b2e54bfd6aecbde2d'
    SOLUTION_TEMPLATE_MKDN = '073ea152d867cf06b2ee993fb1aded4c8ccbc618972db5c18158b5b68a5da6e4'
    REFERENCE_TEMPLATE = 'e0cd55c650ef936a66633ee29500e47ee60cc497c342212381c40032ea2850d9'
    TEMPLATES = (
        SNIPPET_TEMPLATE,
        SOLUTION_TEMPLATE_TEXT,
        SOLUTION_TEMPLATE_MKDN,
        REFERENCE_TEMPLATE,
    )

    def __init__(self, category='', timestamp='', list_=None, dict_=None):
        self._logger = Logger.get_logger(__name__)

        self._id = ''
        self._category = category
        self._data = ()
        self._brief = ''
        self._description = ''
        self._name = ''
        self._groups = Const.DEFAULT_GROUPS
        self._tags = ()
        self._links = ()
        self._source = ''
        self._versions = ()
        self._languages = ()
        self._filename = ''
        self._created = timestamp
        self._updated = timestamp
        self._uuid = ''
        self._digest = ''
        if list_ or dict_:
            self.convert(list_, dict_)

        if not self._id:
            self._id = self._get_internal_uuid()
        if not self._uuid:
            self._uuid = self._get_external_uuid()
        self._digest = self._compute_digest()

    def __str__(self):
        """Format string from the class object."""

        return self.dump_term(index=1, only_headers=False, use_ansi=True, debug_logs=True)

    def __eq__(self, resource):
        """Compare resources if they are equal."""

        if type(resource) is type(self):
            # The comparison checks only publicly visible resource fields.
            # Internal field ID is not compared since it is always unique
            # ID used for database primary key.
            return self.category == resource.category and \
                   self.data == resource.data and \
                   self.brief == resource.brief and \
                   self.description == resource.description and \
                   self.name == resource.name and \
                   self.groups == resource.groups and \
                   self.tags == resource.tags and \
                   self.links == resource.links and \
                   self.source == resource.source and \
                   self.versions == resource.versions and \
                   self.languages == resource.languages and \
                   self.filename == resource.filename and \
                   self.created == resource.created and \
                   self.updated == resource.updated and \
                   self.uuid == resource.uuid and \
                   self.digest == resource.digest

        return False

    def __ne__(self, resource):
        """Compare resources if they are not equal."""

        return not self == resource

    def copy(self):
        """Copy resource."""

        resource = type(self)()
        resource.__dict__.update(self.__dict__)

        return resource

    @property
    def category(self):
        """Get resource category."""

        return self._category

    @category.setter
    def category(self, value):
        """Resource category."""

        if value in Const.CATEGORIES:
            self._category = value
        else:
            self._logger.debug('resource category not identified: {}'.format(value))

    @property
    def data(self):
        """Get resource data."""

        return self._data

    @data.setter
    def data(self, value):
        """Resource data is stored as a tuple with one line per element.

        The value must be formatted only if it contains a value. If an empty
        string or a tuple would be passed to format_data, the result would be
        tuple that contains one empty string. The reason is that empty data is
        considered valid byte the formatter.
        """

        if not value:
            value = None

        self._data = Parser.format_data(self.category, value)

    @property
    def brief(self):
        """Get resource brief."""

        return self._brief

    @brief.setter
    def brief(self, value):
        """Resource brief."""

        self._brief = Parser.format_string(value)

    @property
    def description(self):
        """Get resource description."""

        return self._description

    @description.setter
    def description(self, value):
        """Resource description."""

        self._description = Parser.format_string(value)

    @property
    def name(self):
        """Get resource name."""

        return self._name

    @name.setter
    def name(self, value):
        """Resource name."""

        self._name = Parser.format_string(value)

    @property
    def groups(self):
        """Get resource groups."""

        return self._groups

    @groups.setter
    def groups(self, value):
        """Resource groups."""

        self._groups = Parser.format_list(value)

    @property
    def tags(self):
        """Get resource tags."""

        return self._tags

    @tags.setter
    def tags(self, value):
        """Resource tags."""

        self._tags = Parser.format_list(value)

    @property
    def links(self):
        """Get resource links."""

        return self._links

    @links.setter
    def links(self, value):
        """Resource links."""

        self._links = Parser.format_links(value)

    @property
    def source(self):
        """Get resource source."""

        return self._source

    @source.setter
    def source(self, value):
        """Resource source."""

        self._source = Parser.format_string(value)

    @property
    def versions(self):
        """Get resource versions."""

        return self._versions

    @versions.setter
    def versions(self, value):
        """Resource versions."""

        self._versions = Parser.format_list(value)

    @property
    def languages(self):
        """Get resource languages."""

        return self._languages

    @languages.setter
    def languages(self, value):
        """Resource languages."""

        self._languages = Parser.format_list(value)

    @property
    def filename(self):
        """Get resource filename."""

        return self._filename

    @filename.setter
    def filename(self, value):
        """Resource filename."""

        self._filename = Parser.format_string(value)

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
    def uuid(self):
        """Get resource uuid."""

        return self._uuid

    @uuid.setter
    def uuid(self, value):
        """Resource uuid."""

        self._uuid = value

    @property
    def digest(self):
        """Get resource digest."""

        return self._digest

    @digest.setter
    def digest(self, value):
        """Resource digest."""

        self._digest = value

    def get_template(self, category, template_format, templates):  # pylint: disable=too-many-branches
        """Return resource in a text template.

        If the resource is empty, an empty text template with examples is
        returned. If there already is a defined resource attributes, the
        content stored in the resource is transformed into a template.

        In case of an text formatted template, the mandatory fields are
        left empty for snippets and resources. The reason is that it is
        considered that filling a text template is easy and can be done
        without examples.

        In case of an Markdown formatted template, the mandatory fields
        are filled for snippets and resources. The Markdown formatted
        template is considered too difficult even for author to operate
        without examples.

        In case of a solution content, the example links are not set in
        the template because the links are automatically parsed from the
        content data.

        Args:
           category (str): Content category.
           template_format (str): Template format.
           templates (dict): Dictionary that contains content templates.

        Returns:
            str: Content template as a string.
        """

        if self._is_empty():
            if template_format == Const.CONTENT_FORMAT_MKDN:
                if category == Const.SNIPPET:
                    self.data = (Parser.EXAMPLE_DATA,)
                    if not self.links:
                        self.links = (Parser.EXAMPLE_LINKS.split(Const.DELIMITER_LINKS))
                elif category == Const.SOLUTION:
                    self.data = (
                        '## Description',
                        '',
                        '## References',
                        '',
                        '## Commands',
                        '',
                        '## Configurations',
                        '',
                        '## Solutions',
                        '',
                        '## Whiteboard'
                    )
                elif category == Const.TODO:
                    self.data = (
                        '## Todo',
                        '',
                        '   - [ ] Add todo item.',
                        '',
                        '## Whiteboard'
                    )
                elif category == Const.REFERENCE:
                    if not self.links:
                        self.links = (Parser.EXAMPLE_LINKS.split(Const.DELIMITER_LINKS))
            if not self.brief:
                self.brief = Parser.EXAMPLE_BRIEF
            if not self.description:
                self.description = Parser.EXAMPLE_DESCRIPTION
            if not self.name:
                self.name = Parser.EXAMPLE_NAME
            if Const.DEFAULT_GROUPS == self.groups:
                self.groups = (Parser.EXAMPLE_GROUPS.split(Const.DELIMITER_GROUPS))
            if not self.tags:
                self.tags = (Parser.EXAMPLE_TAGS.split(Const.DELIMITER_TAGS))
            if not self.links and category == Const.SNIPPET:
                self.links = (Parser.EXAMPLE_LINKS.split(Const.DELIMITER_LINKS))
            if not self.source:
                self.source = Parser.EXAMPLE_SOURCE
            if not self.versions:
                self.versions = (Parser.EXAMPLE_VERSIONS.split(Const.DELIMITER_VERSIONS))
            if not self.languages:
                self.languages = (Parser.EXAMPLE_LANGUAGES.split(Const.DELIMITER_LANGUAGES))
            if not self.filename:
                self.filename = Parser.EXAMPLE_FILENAME

            # In order to match is_template before and after parsing, reference
            # data must be set to links. This is done automatically after the
            # Markdown parsing.
            if category == Const.REFERENCE:
                self.data = self.links
            self.digest = self._compute_digest()
        if self._is_empty() and category == Const.SOLUTION and template_format == Const.CONTENT_FORMAT_MKDN:
            self.digest = self._compute_digest()

        template = Const.EMPTY
        if template_format == Const.CONTENT_FORMAT_MKDN:
            template = self.dump_mkdn(templates)
        elif template_format == Const.CONTENT_FORMAT_TEXT:
            template = self.dump_text(templates)

        return template

    def seal(self, validate=True):
        """Seal content by updating digest and run content specific tasks.

        In case of reference content, the links are treated as content data.
        The tool has been built to expect always the data part and it was
        considered that it is more maintanable to to it like this instead
        of adding extra logic around the code.

        Args:
           validate (bool): Defines if the content is validated.

        Returns:
            bool: If the resource sealing was successful.
        """

        if self.category == Const.REFERENCE:
            self.data = self.links
        else:
            self.links = tuple(sorted(self.links))

        # There may be cases where for example Yaml loading automatically
        # converts timestamps to datetime objects if the timestamps are
        # not surrounded by quotes. Internally the timestamps are always
        # stored in string format.
        if isinstance(self.created, datetime.datetime):
            self.created = self.created.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        if isinstance(self.updated, datetime.datetime):
            self.updated = self.updated.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

        if not self.uuid:
            self.uuid = self._get_external_uuid()

        self.digest = self._compute_digest()

        is_template = self._is_template()
        if is_template and validate:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because it was matching to an empty template')

        is_empty = self._is_empty()
        if is_empty and validate:
            if self.category in (Const.SNIPPET, Const.SOLUTION, Const.TODO):
                Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field data is empty')
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'content was not stored because mandatory content field links is empty')

        return not bool(is_empty or is_template)

    def _compute_digest(self):
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
        resource_str = resource_str + Const.DELIMITER_VERSIONS.join(map(Const.TEXT_TYPE, sorted(self.versions)))
        digest = hashlib.sha256(resource_str.encode('UTF-8')).hexdigest()

        return digest

    def migrate(self, source, validate=True):
        """Migrate source into Resource.

        This always overrides fields that can be modified by user. Only the
        fields that can be modified by end user are updated.
        """

        self._logger.debug('migrate to resouce: %.16s', self.digest)
        self.data = source.data
        self.brief = source.brief
        self.description = source.description
        self.name = source.name
        self.groups = source.groups
        self.tags = source.tags
        self.links = source.links
        self.source = source.source
        self.versions = source.versions
        self.languages = source.languages
        self.filename = source.filename

        return self.seal(validate)

    def merge(self, source, validate=True):
        """Merge two resources.

        Override resource attributes only if the merged source attributes
        have values. Only the attributes that can be modified by a client
        are updated.

        The validate flag defines if the merged resource is validated.

        Args:
           validate (bool): Defines if the content is validated.

        Returns:
            bool: If the source was merged successfully.
        """

        if not source:
            return False

        self._logger.debug('merge to resouce: %.16s', self.digest)
        if source.data:
            self.data = source.data
        if source.brief:
            self.brief = source.brief
        if source.description:
            self.description = source.description
        if source.name:
            self.name = source.name
        if source.groups and Const.DEFAULT_GROUPS != source.groups:
            self.groups = source.groups
        if source.tags:
            self.tags = source.tags
        if source.links:
            self.links = source.links
        if source.source:
            self.source = source.source
        if source.versions:
            self.versions = source.versions
        if source.languages:
            self.languages = source.languages
        if source.filename:
            self.filename = source.filename

        return self.seal(validate)

    def convert(self, list_=None, dict_=None):
        """Convert given data into a resource.

        Resource source can be database which stores resources as a list
        of attributes or a dictionary. In case of dictionary, the source
        can be any supported file format like YAML or Markdown format.

        The internal ``_id`` attribute is stored only in database and thus
        it must be generated when resource is read from external file.

        The external source file may not contain timestamps in attributes
        ``created`` or ``updated`` for example in error cases. These values
        has to be set to timestamp to prevent database INSERT failure.

        Args:
            list_ (list): Resource attributes in a list or tuple.
            dict_ (dict): Resource attributes in dictionary.
        """

        if list_:
            self._id = list_[Resource._ID]
            self.category = list_[Resource.CATEGORY]
            self.data = tuple(list_[Resource.DATA].split(Const.DELIMITER_DATA))
            self.brief = list_[Resource.BRIEF]
            self.description = list_[Resource.DESCRIPTION]
            self.name = list_[Resource.NAME]
            self.groups = tuple(list_[Resource.GROUPS].split(Const.DELIMITER_GROUPS) if list_[Resource.GROUPS] else [])
            self.tags = tuple(list_[Resource.TAGS].split(Const.DELIMITER_TAGS) if list_[Resource.TAGS] else [])
            self.links = tuple(list_[Resource.LINKS].split(Const.DELIMITER_LINKS) if list_[Resource.LINKS] else [])
            self.source = list_[Resource.SOURCE]
            self.versions = tuple(list_[Resource.VERSIONS].split(Const.DELIMITER_VERSIONS) if list_[Resource.VERSIONS] else [])
            self.languages = tuple(list_[Resource.LANGUAGES].split(Const.DELIMITER_LANGUAGES) if list_[Resource.LANGUAGES] else [])
            self.filename = list_[Resource.FILENAME]
            self.created = list_[Resource.CREATED]
            self.updated = list_[Resource.UPDATED]
            self.uuid = list_[Resource.UUID]
            self.digest = list_[Resource.DIGEST]
        elif dict_:
            self._id = self._get_internal_uuid()
            self.category = dict_.get('category')
            self.data = dict_.get('data', self.data)
            self.brief = dict_.get('brief', self.brief)
            self.description = dict_.get('description', self.description)
            self.name = dict_.get('name', self.name)
            self.groups = dict_.get('groups', self.groups)
            self.tags = dict_.get('tags', self.tags)
            self.links = dict_.get('links', self.links)
            self.source = dict_.get('source', self.source)
            self.versions = dict_.get('versions', self.versions)
            self.languages = dict_.get('languages', self.languages)
            self.filename = dict_.get('filename', self.filename)
            self.created = dict_.get('created', self.created) or self.created
            self.updated = dict_.get('updated', self.updated) or self.updated
            self.uuid = dict_.get('uuid', self.uuid)
            self.digest = dict_.get('digest', self.digest)

    def _is_template(self):
        """Test if resource data is empty template."""

        return bool(self.digest in Resource.TEMPLATES)

    def _is_empty(self):
        """Test if resource does not have mandatory data.

        In case of snippet or solution the content data must be present. In
        case of references, the link must be present.
        """

        if self.category in (Const.SNIPPET, Const.SOLUTION, Const.TODO) and not any(self.data):
            return True
        if self.category == Const.REFERENCE and not any(self.links):
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

    def is_todo(self):
        """Test if resource is todo."""

        return bool(self.category == Const.TODO)

    def is_native_mkdn_solution(self):
        """Test if resource is native Markdown formatted content.

        The Markdown content is identified simply by checking that the first
        line of the data is a second level Markdown header.
        """

        if not self.is_solution():
            return False

        try:
            match = re.compile(r'''
                ^[#]{2}\s\S+     # Match second level Markdown header at the beginning of the content data string.
                ''', re.VERBOSE).search(self.data[0])
            if match:
                return True
        except IndexError:
            pass

        return False

    def dump_qargs(self):
        """Convert resource for storage.

        Links are not sorted because it is assumed that link order matter
        for the end user. For example with reference content, it is possible
        to store multiple links. It is assumed that the first link holds the
        most valuable information.
        """

        qargs = (
            self._id,
            self.category,
            Const.DELIMITER_DATA.join(map(Const.TEXT_TYPE, self.data)),
            self.brief,
            self.description,
            self.name,
            Const.DELIMITER_GROUPS.join(map(Const.TEXT_TYPE, sorted(self.groups))),
            Const.DELIMITER_TAGS.join(map(Const.TEXT_TYPE, sorted(self.tags))),
            Const.DELIMITER_LINKS.join(map(Const.TEXT_TYPE, self.links)),
            self.source,
            Const.DELIMITER_VERSIONS.join(map(Const.TEXT_TYPE, sorted(self.versions))),
            Const.DELIMITER_LANGUAGES.join(map(Const.TEXT_TYPE, sorted(self.languages))),
            self.filename,
            self.created,
            self.updated,
            self.uuid,
            self.digest
        )

        return qargs

    def dump_dict(self, remove_fields):
        """Convert resource to dictionary."""

        data = {
            'category': self.category,
            'data': self.data,
            'brief': self.brief,
            'description': self.description,
            'name': self.name,
            'groups': self.groups,
            'tags': self.tags,
            'links': self.links,
            'source': self.source,
            'versions': self.versions,
            'languages': self.languages,
            'filename': self.filename,
            'created': self.created,
            'updated': self.updated,
            'uuid': self.uuid,
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
        text = text.replace('<category>', self.category)
        if self.data:
            try:
                text = re.sub(r'''
                    [<data>]{6}         # Match <data> tag.
                    (.*[<data>]{6})?    # Match optional closing <data> tag and all data between the tags.
                    ''', Const.DELIMITER_DATA.join([line.replace('\\', '\\\\') for line in self.data]), text, flags=re.DOTALL | re.VERBOSE)
            except (re.error, TypeError):
                self._logger.info('failed to replace content data in text template: {}'.format(traceback.format_exc()))
                self._logger.info('failed to replace content data: {}'.format(self.data))
                self._logger.info('failed to replace content template: %s', text)
        else:
            # The replacing of the data is only relevant with a text formatted
            # solution . With other cases where for example Markdown solution
            # or snippet have one <data> tag, the tag is just replaced with an
            # empty string.
            match = re.compile(r'''
                <data>          # Match opening tag for data.
                (?P<data>.*)    # Catch all the data from template.
                <data>          # Match closing tag for data.
                ''', re.DOTALL | re.VERBOSE).search(text)
            if match:
                text = re.sub(r'''
                    <data>          # Match opening tag for data.
                    (.*<data>)      # Match closing <data> tag and all data between the tags.
                    ''', match.group('data').lstrip().replace('\\', '\\\\'), text, flags=re.DOTALL | re.VERBOSE)
            else:
                text = text.replace('<data>', Const.EMPTY)
                text = text.lstrip()
        text = text.replace('<brief>', self.brief)
        text = text.replace('<description>', self.description)
        text = text.replace('<name>', self.name)
        text = text.replace('<groups>', Const.DELIMITER_GROUPS.join(self.groups))
        text = text.replace('<tags>', Const.DELIMITER_TAGS.join(self.tags))
        text = text.replace('<links>', Const.DELIMITER_LINKS.join(self.links))
        text = text.replace('<source>', self.source)
        text = text.replace('<versions>', Const.DELIMITER_VERSIONS.join(self.versions))
        text = text.replace('<languages>', Const.DELIMITER_LANGUAGES.join(self.languages))
        text = text.replace('<filename>', self.filename)
        text = text.replace('<created>', self.created)
        text = text.replace('<updated>', self.updated)
        text = text.replace('<uuid>', self.uuid)
        text = text.replace('<digest>', self.digest)

        return text

    def dump_mkdn(self, templates):
        """Convert resource to Markdown.

        Long lines are wrapped so that there are two spaces at the end of
        newline. This same approach with the trailing spaces is used with
        the metadata in the Markdown template.
        """

        mkdn = templates['mkdn'][self.category]
        mkdn = mkdn.replace('<category>', self.category)
        mkdn = mkdn.replace('<data>', self._dump_mkdn_data())
        mkdn = mkdn.replace('<brief>', self.brief)
        mkdn = mkdn.replace('<description>', textwrap.fill(self.description, 88).replace('\n', '  \n'))
        mkdn = mkdn.replace('<name>', self.name)
        mkdn = mkdn.replace('<groups>', Const.DELIMITER_GROUPS.join(self.groups))
        mkdn = mkdn.replace('<tags>', Const.DELIMITER_TAGS.join(self.tags))
        mkdn = mkdn.replace('<links>', self._dump_mkdn_links())
        mkdn = mkdn.replace('<source>', self.source)
        mkdn = mkdn.replace('<versions>', Const.DELIMITER_VERSIONS.join(self.versions))
        mkdn = mkdn.replace('<languages>', Const.DELIMITER_LANGUAGES.join(self.languages))
        mkdn = mkdn.replace('<filename>', self.filename)
        mkdn = mkdn.replace('<created>', self.created)
        mkdn = mkdn.replace('<updated>', self.updated)
        mkdn = mkdn.replace('<uuid>', self.uuid)
        mkdn = mkdn.replace('<digest>', self.digest)

        # Beautify metadata line ends with three spaces to include always two
        # spaces. If a metadata field is empty, adding it to template creates
        # three spaces. Two spaces are required by Markdown to have a newline.
        mkdn = re.sub(r'''
            \s{1}:\s{3}$      # Match empty metadata with three spaces.
            ''', ' :  ', mkdn, flags=re.MULTILINE | re.VERBOSE)

        return mkdn

    def _dump_mkdn_data(self):
        """Dump resource data to Markdown format.

        Snippet data contains commands that may have comment. Snippet comments
        are extracted from a command string and used as headers in Markdown
        formatted data.

        Solutions are quarateed to have one newline. The Markdown template has
        already one newline for the solution data. Because of this, the last
        newline from the data field is not converted to the string.

        Returns:
            str: Sring representing the resource data attribute.
        """

        data = Const.EMPTY
        if self.is_snippet():
            comments = self._snippet_has_comments(self.data)
            for command in self.data:
                match = Const.RE_CATCH_COMMAND_AND_COMMENT.search(command)
                if match:
                    if match.group('comment'):
                        data = data + "- " + match.group('comment') + Const.NEWLINE * 2
                        data = data + "    `$ " + match.group('command') + "`" + Const.NEWLINE * 2
                    else:
                        if comments:
                            data = data + "- " + Parser.SNIPPET_DEFAULT_COMMENT + Const.NEWLINE * 2
                            data = data + "    `$ " + match.group('command') + "`  " + Const.NEWLINE * 2
                        else:
                            data = data + "`$ " + match.group('command') + "`  " + Const.NEWLINE
                else:
                    self._logger.debug('command parsing failed: %s', command)
            data = data.rstrip()
        elif self.is_solution():
            if self.is_native_mkdn_solution():
                data = data + Const.DELIMITER_DATA.join(self.data[0:-1])
            else:
                data = '```\n'
                data = data + Const.DELIMITER_DATA.join(self.data[0:-1])
                data = data + '```'
        elif self.is_todo():
            data = data + Const.DELIMITER_DATA.join(self.data)

        return data

    @staticmethod
    def _snippet_has_comments(data):
        """Test if any of the snippets have comments.

        Args:
            data (tuple): Content data.

        Returns:
            bool: True if any of the commands in snipped data have a comment.
        """

        for command in data:
            match = Const.RE_CATCH_COMMAND_AND_COMMENT.search(command)
            if match and match.group('comment'):
                return True

        return False

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

    def dump_term(self, index, only_headers, use_ansi, debug_logs):  # noqa pylint: disable=too-many-statements, too-many-locals, too-many-branches
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
        links_ = self.links if self.links else ('',)  # Force the link symbol '>' if there are no links.
        if self.is_snippet():
            aligned_data = self._align_snippet_comments(self.data, use_ansi)
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            if not only_headers:
                text = text + Const.NEWLINE
                text = text + Const.EMPTY.join([data.format(indent=indent, symbol='$', line=line) for line in aligned_data])
                text = text + Const.NEWLINE
                text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
                text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in links_])
                text = text + Const.NEWLINE
        elif self.is_solution():
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            if not only_headers:
                text = text + Const.NEWLINE
                text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
                text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in links_])
                text = text + Const.NEWLINE
                text = text + Const.EMPTY.join([data.format(indent=indent, symbol=':', line=line) for line in self.data])
                text = text + Const.NEWLINE
        elif self.is_reference():
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            if not only_headers:
                text = text + Const.NEWLINE
                text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in links_])
                text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
                text = text + Const.NEWLINE
        elif self.is_todo():
            text = text + header.format(i=index, brief=self.brief, groups=Const.DELIMITER_GROUPS.join(self.groups), digest=self.digest)
            if not only_headers:
                text = text + Const.NEWLINE
                text = text + Const.EMPTY.join([data.format(indent=indent, symbol=u'\u2713', line=line) for line in self.data])
                text = text + Const.NEWLINE
                text = text + tags.format(indent=indent, tag=Const.DELIMITER_TAGS.join(self.tags))
                text = text + Const.EMPTY.join([links.format(indent=indent, link=link) for link in links_])
                text = text + Const.NEWLINE
        else:
            self._logger.debug('internal error with content category: %s', self.category)

        if debug_logs:
            if self.is_reference():
                text = text + Const.EMPTY.join([meta.format(indent=indent, key='data', align=' ' * 8, value=line) for line in self.data])
            text = text + meta.format(indent=indent, key='category', align=' ' * 4, value=self.category)
            text = text + meta.format(indent=indent, key='created', align=' ' * 5, value=self.created)
            text = text + meta.format(indent=indent, key='description', align=' ' * 1, value=self.description)
            text = text + digest.format(indent=indent, key='digest', align=' ' * 6, value=self.digest, test=self.digest == self._compute_digest())  # noqa pylint: disable=line-too-long
            text = text + meta.format(indent=indent, key='filename', align=' ' * 4, value=self.filename)
            text = text + meta.format(indent=indent, key='id', align=' ' * 10, value=self._id)
            text = text + meta.format(indent=indent, key='languages', align=' ' * 3, value=Const.DELIMITER_LANGUAGES.join(self.languages))
            text = text + meta.format(indent=indent, key='name', align=' ' * 8, value=self.name)
            text = text + meta.format(indent=indent, key='source', align=' ' * 6, value=self.source)
            text = text + meta.format(indent=indent, key='updated', align=' ' * 5, value=self.updated)
            text = text + meta.format(indent=indent, key='uuid', align=' ' * 8, value=self.uuid)
            text = text + meta.format(indent=indent, key='versions', align=' ' * 4, value=Const.DELIMITER_VERSIONS.join(self.versions))
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

    @staticmethod
    def _get_internal_uuid():
        """Get internally used UUID.

        This UUID is intended not to be visible outside of the server. The
        UUID contains physical MAC address that may reveal location of
        running server.

        Returns:
            str: UUID1 string.
        """

        return str(uuid.uuid1())
