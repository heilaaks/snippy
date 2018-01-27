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

"""jsonapiv10.py - Format to JSON API v1.0."""

import json

from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger


class JsonApiV1(object):
    """Format to JSON API v1.0."""

    _logger = Logger(__name__).get()

    @classmethod
    def resource(cls, category, contents, uri):
        """Format JSON API v1.0 resource from content."""

        resource_ = {}
        for content in contents:
            type_ = 'snippets' if category == Const.SNIPPET else 'solutions'
            resource_ = {'links': {'self': uri},
                         'data': {'type': type_,
                                  'id': '1',
                                  'attributes': content}}
            break

        if not resource_:
            resource_ = json.loads('{"links": {"self": "' + uri + '"}, "data": null}')

        return json.dumps(resource_)

    @classmethod
    def collection(cls, category, contents):
        """Format JSON API v1.0 collection from content."""

        collection = {'data': []}
        for idx, content in enumerate(contents, start=1):
            type_ = 'snippets' if category == Const.SNIPPET else 'solutions'
            collection['data'].append({'type': type_,
                                       'id': str(idx),
                                       'attributes': content})

        return json.dumps(collection)

    @classmethod
    def error(cls, causes):
        """Format JSON API v1.0 error."""

        # Follow CamelCase in field names because expected usage is from
        # Javascript that uses CamelCase.
        errors = {'errors': [], 'meta': {}}
        for cause in causes['errors']:
            errors['errors'].append({'status': str(cause['status']),
                                     'statusString': cause['status_string'],
                                     'title': cause['title'],
                                     'module': cause['module']})

        if not errors['errors']:
            errors = {'errors': [{'status': '500',
                                  'statusString': '500 Internal Server Error',
                                  'title': 'Internal errors not found when error detected.'}]}
        errors['meta'] = causes['meta']

        return json.dumps(errors)
