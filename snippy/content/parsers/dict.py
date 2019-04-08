#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""base: Parse content from dictionary."""

from snippy.logger import Logger


class ContentParserDict(object):  # pylint: disable=too-few-public-methods
    """Parse content from dictionary."""

    def __init__(self, timestamp, dictionary, collection):
        """
        Args:
            timestamp (str): IS8601 timestamp used with created resources.
            dictionary (dict): Dictionary where the content is read.
            collection (Collection()): Collection where the content is stored.
        """

        self._logger = Logger.get_logger(__name__)
        self._timestamp = timestamp
        self._dictionary = dictionary
        self._collection = collection

    def read_collection(self):
        """Read collection from the given dictionary source."""

        if 'data' in self._dictionary:
            self._collection.convert(self._dictionary['data'], self._timestamp)
        else:
            self._logger.debug('structured content format not indentified: %s', self._dictionary)
