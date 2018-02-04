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

"""validate.py - Validate REST API input."""

from snippy.logger.logger import Logger


class Validate(object):  # pylint: disable=too-few-public-methods
    """Validate REST API input."""

    _logger = Logger(__name__).get()

    @classmethod
    def collection(cls, media):
        """Return media as collection of content."""

        collection = []
        try:
            if 'data' in media and isinstance(media['data'], (list, tuple)):
                for data in media['data']:
                    if 'attributes' in data:
                        collection.append(data['attributes'])
            elif 'data' in media and isinstance(media['data'], dict):
                if 'attributes' in media['data']:
                    collection.append(media['data']['attributes'])
            else:
                cls._logger.info('media ignored because of unknown type %s', media)
        except ValueError:
            cls._logger.info('media collection validation failed and it was ignored %s', media)

        return tuple(collection)

    @classmethod
    def resource(cls, media, digest):
        """Return media as specific resource with digest."""

        resource_ = {}
        try:
            if 'data' in media and isinstance(media['data'], dict):
                if 'attributes' in media['data']:
                    resource_ = media['data']['attributes']
                    resource_['digest'] = digest
            else:
                cls._logger.info('media ignored because of unknown type %s', media)
        except ValueError:
            cls._logger.info('media resource validation failed and it was ignored %s', media)

        return resource_
