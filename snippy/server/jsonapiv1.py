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

"""jsonapiv10.py - Format JSON API v1.0."""

import json

from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger


class JsonApiV1(object):  # pylint: disable=too-few-public-methods
    """Format to JSON API v1.0."""

    _logger = Logger(__name__).get()

    @classmethod
    def format_resource(cls, contents, uri):
        """Format JSON API v1.0 resource from content."""

        resource_ = {'links': {'self': uri}, 'data': 'null'}
        for content in json.loads(contents):
            type_ = 'snippets' if content['category'] == Const.SNIPPET else 'solutions'
            resource_ = {'links': {'self': uri},
                         'data': {'type': type_,
                                  'id': '1',
                                  'attributes': content}}
            break

        return json.dumps(resource_)

#    @classmethod
#    def format_collection(cls, contents):
#        """Format JSON API v1.0 collection from content."""
#
