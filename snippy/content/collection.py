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

import sys
from collections import OrderedDict
from signal import signal, getsignal, SIGPIPE, SIG_DFL

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.content.parser import Parser
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
            text = text + resource.dump_term(index=i, use_ansi=True, debug_logs=True)

        text = text + '\x1b[96;1m# \x1b[1;92mcollection meta\x1b[0m\n'
        text = text + '   \x1b[91m!\x1b[0m \x1b[2mtotal\x1b[0m : %d\n' % self._data['meta']['total']

        return text

    def __eq__(self, collection):
        """Compare collections if they are equal."""

        # See [1] and [2] for details how to override comparisons.
        #
        # [1] https://stackoverflow.com/a/30676267
        # [2] https://stackoverflow.com/a/390640
        if type(collection) is type(self):
            if len(self) != len(collection):
                return False
            for digest in self.keys():
                if not (digest in collection.keys() and self[digest] == collection[digest]):
                    return False

            return True

        return False

    def __ne__(self, collection):
        """Compare collections if they are not equal."""

        return not self == collection

    def __len__(self):
        """Return length of the collection."""

        return len(self._data['data'])

    def __iter__(self):
        """Return iterable resources from object."""

        return iter([self[digest] for digest in self.keys()])

    def __getitem__(self, digest):
        """Return item from object based on message digest."""

        return self._data['data'][digest]['data']

    def keys(self):
        """Return list of digests in collection."""

        return list(self._data['data'].keys())

    def values(self):
        """Return list of resources in collection."""

        return list([self[digest] for digest in self.keys()])

    def resources(self):
        """Return generator for resources in collection."""

        for digest in self.keys():
            yield self[digest]

    @classmethod
    def get_resource(cls, category, timestamp):
        """Return new source."""

        return Resource(category, timestamp)

    def category_list(self):
        """Return list of categories in collection.

        Returns:
            tuple: List of unique categories in the collection.
        """

        categories = {}
        for resource in self.resources():
            categories[resource.category] = resource.category

        return tuple(categories.keys())

    def migrate(self, source):
        """Migrate resource or collection to collection.

        Add new resources or override originals if they exist.

        Args:
           source (content): Resource or Collection that is migrated.
        """

        if isinstance(source, Collection):
            for resource in source.resources():
                self.migrate(resource)
        elif isinstance(source, Resource):
            if source.category in Const.CATEGORIES:
                if source.digest not in self.keys():
                    self._data['meta']['total'] = self._data['meta']['total'] + 1
                source.seal()
                self._data['data'][source.digest] = {}
                self._data['data'][source.digest]['data'] = source
            else:
                self._logger.debug('migrate to collection failed due to unknown category: {}'.format(Logger.remove_ansi(str(source))))

    def merge(self, source):
        """Merge a resource to collection.

        Merge content into existing resource and return new message digest
        from the content merger. If the content source does not exist it
        causes a migrage operation. In case of migrate, the source digest
        is always correct and it can be directy returned.

        This method cannot merge a collection because so far there has been
        no need for it.

        Args:
           source (Resource): Resource to be merged to collection.

        Returns:
            str: The new message digest after merging the resource.
        """

        digest = None
        if not source or not isinstance(source, Resource):
            self._logger.debug('source was not merged to collection: {}'.format(Logger.remove_ansi(str(source))))

            return digest

        if source.digest in self.keys():
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

    def load(self, content_format, timestamp, content):
        """Load content into collection.

        Args:
           content_format (Enum): Content format.
           timestamp (str): IS8601 timestamp used with created resources.
           content (str): Content to be read.
        """

        if content_format == Const.CONTENT_FORMAT_MKDN:
            self.load_mkdn(timestamp, content)
        elif content_format == Const.CONTENT_FORMAT_TEXT:
            self.load_text(timestamp, content)

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

    def load_text(self, timestamp, text):
        """Load content from Markdown file.

        Args:
           text (str): Text formatted string.
        """

        Parser(Const.CONTENT_FORMAT_TEXT, timestamp, text, self).read()

    def dump_text(self, templates):
        """Convert collection to text format.

        All resources inside the collection are converted to text format.

        Args:
           templates (dict): Dictionary that contains text templates.

        Returns:
            string: Collection in text format.
        """

        if not self:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')

        text = Const.EMPTY
        for resource in self.resources():
            text = text + resource.dump_text(templates)
            text = text + Const.NEWLINE

        return text

    def load_mkdn(self, timestamp, mkdn):
        """Load content from Markdown file.

        Args:
           mkdn (str): Markdown formatted string.
        """

        Parser(Const.CONTENT_FORMAT_MKDN, timestamp, mkdn, self).read()

    def dump_mkdn(self, templates):
        """Convert collection to Markdown format.

        All resources inside the collection are converted to Markdown.

        Args:
           templates (dict): Dictionary that contains text templates.

        Returns:
            string: Collection in Markdown format.
        """

        if not self:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')

        text = Const.EMPTY
        for resource in self.resources():
            text = text + resource.dump_mkdn(templates)
            text = text + '\n---\n\n'
        text = text[:-6]  # Remove last separator added by the loop.

        return text

    def dump_term(self, use_ansi, debug_logs):
        """Convert collection for terminal."""

        if not self:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')

        text = Const.EMPTY
        for i, resource in enumerate(self.resources(), start=1):
            text = text + resource.dump_term(index=i, use_ansi=use_ansi, debug_logs=debug_logs)

        # Set one empty line at the end of string for beautified output.
        if self:
            text = text.rstrip()
            text = text + Const.NEWLINE

        self._logger.debug('printing content to terminal stdout')
        self._print_stdout(text)

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
