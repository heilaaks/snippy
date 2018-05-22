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

"""collection: Store list of contents in collection."""

from collections import OrderedDict

from snippy.content.resource import Resource
from snippy.logger import Logger


class Collection(object):  # pylint: disable=too-many-public-methods
    """Store list of contents in collection."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._data = self._init()

    def __str__(self):
        """Format string from the class object."""

        text = ''
        for i, resource in enumerate(self.resources(), start=1):
            text = text + resource.convert_term(index=i, ansi=True, debug=True)

        return text

    def __getitem__(self, digest):
        return self.data['data'][digest]

    def __iter__(self):
        return iter(self.data['data'])

    def size(self):
        """Return count of resources in collection."""

        return len(self.data['data'])

    def keys(self):
        """Iterate over keys stored in collection."""

        return self.data['data'].keys()

    def items(self):
        """Iterate over items stored in collection."""

        return self.data['data'].items()

    def values(self):
        """Iterate over values stored in collection."""

        return self.data['data'].values()

    def resources(self):
        """Iterate over resources stored in collection."""

        for digest in self.keys():
            yield self.data['data'][digest]['data']

    def init(self):
        """Initialize collection."""

        self._init()

    def migrate(self, source):
        """Migrate Resource of Collections.

        Add new resources or override the original resources if they exist.
        """

        if isinstance(source, Collection):
            for resource in source.resources():
                self.data['data'][resource.digest] = OrderedDict()
                self.data['data'][resource.digest]['data'] = resource
                self.data['data'][resource.digest]['meta'] = OrderedDict()
                self.data['data'][resource.digest]['meta']['digest'] = resource.digest
        elif isinstance(source, Resource):
                self.data['data'][source.digest] = OrderedDict()
                self.data['data'][source.digest]['data'] = source
                self.data['data'][source.digest]['meta'] = OrderedDict()
                self.data['data'][source.digest]['meta']['digest'] = source.digest

    def merge(self, source):
        """Migrate two collections to one.

        Add new resources or override the original resource fields if the
        source collection resource fields are defined.
        """

    def convert(self, source):
        """Convert source into Collection()."""

        for content in source:
            resource = Resource()
            resource.migrate(content)
            self.migrate(resource)

    def dump_json(self, filter_fields):
        """Convert collection to json."""

        json = []
        for resource in source.resources():
            json.append(resource.dump_json)

        return json

    @property
    def data(self):
        """Get collection data."""

        return self._data

    @data.setter
    def data(self, value):
        """Collection data contains resources with metadata."""

        self._data = value

    @property
    def total(self):
        """Get total amount of resources without filters."""

        return self._data['meta']['total']

    @total.setter
    def total(self, value):
        """Total amount of resources without filters."""

        self._data['meta']['total'] = value

    def _init(self):
        """Wrap content list with metadata."""

        self._logger.debug('initialize new collection')
        meta_content = {
            'data': OrderedDict(),
            'meta': {
                'total': 0,  # Total amount of search results without filters.
            }
        }

        return meta_content
