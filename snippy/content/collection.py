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

"""collection: Store list of contents in collection."""

from __future__ import print_function

import re
import sys
from collections import OrderedDict
from signal import signal, getsignal, SIGPIPE, SIG_DFL

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.resource import Resource
from snippy.logger import Logger


class Collection(object):  # pylint: disable=too-many-public-methods
    """Store list of contents in collection."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self._data = self._init()

    def __str__(self):
        """Format string from the class object."""

        text = Const.EMPTY
        for i, resource in enumerate(self.resources(), start=1):
            text = text + resource.dump_term(index=i, ansi=True, debug=True)
            text = text + '   \x1b[91m!\x1b[0m \x1b[2mcollection-meta-digest\x1b[0m : %s (%s)\n\n' % (
                self[resource.digest]['meta']['digest'],
                resource.digest == self[resource.digest]['meta']['digest']
            )

        text = text + '\x1b[96;1m# \x1b[1;92mcollection meta\x1b[0m\n'
        text = text + '   \x1b[91m!\x1b[0m \x1b[2mtotal\x1b[0m : %d\n' % self.data['meta']['total']

        return text

    def __eq__(self, collection):
        """Compare collections if they are equal."""

        # See [1] and [2] for details how to override comparisons.
        #
        # [1] https://stackoverflow.com/a/30676267
        # [2] https://stackoverflow.com/a/390640
        if type(collection) is type(self):
            if self.size() != collection.size():
                return False

            for digest in self.keys():
                if digest in collection and self[digest] != collection[digest]:
                    return False

            return True

        return False

    def __ne__(self, collection):
        """Compare collections if they are not equal."""

        return not self == collection

    def __getitem__(self, digest):
        return self.data['data'][digest]

    def __iter__(self):
        return iter(self.data['data'])

    def size(self):
        """Return count of resources in collection."""

        return len(self.data['data'])

    def empty(self):
        """Test if collection is empty."""

        return True if self.size() == 0 else False

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

    @classmethod
    def get_resource(cls, category, timestamp):
        """Return new source."""

        return Resource(category, timestamp)

    def migrate(self, source):
        """Migrate resource or collection.

        Add new resources or override the originals if they exist.
        """

        if isinstance(source, Collection):
            for resource in source.resources():
                if resource.digest not in self.data['data']:
                    self.data['meta']['total'] = self.data['meta']['total'] + 1
                resource.seal()
                self.data['data'][resource.digest] = {}
                self.data['data'][resource.digest]['data'] = resource
                self.data['data'][resource.digest]['meta'] = {}
                self.data['data'][resource.digest]['meta']['digest'] = resource.digest
        elif isinstance(source, Resource):
            if source.digest not in self.data['data']:
                self.data['meta']['total'] = self.data['meta']['total'] + 1
            source.seal()
            self.data['data'][source.digest] = {}
            self.data['data'][source.digest]['data'] = source
            self.data['data'][source.digest]['meta'] = {}
            self.data['data'][source.digest]['meta']['digest'] = source.digest

    def merge(self, source):
        """Merge resource.

        Merge content into existing resource.
        """

        digest = None
        if not source:
            return digest

        if source.digest in self:
            digest = self[source.digest].merge(source)
        else:
            self.migrate(source)
            digest = source.digest

        return digest

    def convert(self, rows):
        """Convert database rows into collection."""

        for row in rows:
            resource = Resource()
            resource.convert(row)
            self.migrate(resource)

    def load_dict(self, dictionary):
        """Convert dictionary to collection."""

        if 'data' in dictionary:
            for content in dictionary['data']:
                resource = Resource()
                resource.load_dict(content)
                self.migrate(resource)
        else:
            self._logger.debug('json format not indentified: %s', dictionary)

    def dump_dict(self, remove_fields):
        """Convert collection to dictionary."""

        data = []
        for resource in self.resources():
            data.append(resource.dump_dict(remove_fields))

        return data

    def dump_text(self, digest, category, timestamp, templates):
        """Convert collection to text.

        Conversion is made from specific resource or from empty template for
        defined category.
        """

        if digest:
            text = self[digest]['data'].dump_text(templates)
        else:
            text = self.get_resource(category, timestamp).dump_text(templates)

        return text

    def dump_term(self, use_ansi, debug_logs, search_filter):
        """Convert collection for terminal."""

        if not self.size():
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')

        # In case user provided regexp filter, the ANSI control characters for
        # colors are not used in order to make the filter work as expected.
        ansi = use_ansi
        if search_filter:
            ansi = False

        text = Const.EMPTY
        for i, resource in enumerate(self.resources(), start=1):
            text = text + resource.dump_term(index=i, ansi=ansi, debug=debug_logs)
        # Set only one empty line at the end of string for beautified output.
        if self.size():
            text = text.rstrip()
            text = text + Const.NEWLINE

        if search_filter:
            match = re.findall(search_filter, text)
            if match:
                text = Const.NEWLINE.join(match) + Const.NEWLINE
            else:
                text = Const.EMPTY

        self._logger.debug('printing content to terminal stdout')
        self._print_stdout(text)

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

        return self.data['meta']['total']

    @total.setter
    def total(self, value):
        """Total amount of resources without filters."""

        self.data['meta']['total'] = value

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

    @classmethod
    def _print_stdout(cls, text):
        """Print tool output to stdout."""

        # The signal handler manipulation and flush setting below prevents 'broken
        # pipe' errors with grep. For example incorrect parameter usage in grep may
        # cause this. See below listed references /1,2/ and examples that fail
        # without this correction.
        #
        # /1/ https://stackoverflow.com/a/16865106
        # /2/ https://stackoverflow.com/a/26738736
        #
        # $ snippy search --sall '--all' --filter crap | grep --all
        # $ snippy search --sall 'test' --filter test -vv | grep --all
        if text:
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(text)
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)
