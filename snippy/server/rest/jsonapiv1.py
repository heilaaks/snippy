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

"""jsonapiv10: Format to JSON API v1.0."""

import json
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.logger import Logger


class JsonApiV1(object):
    """Format according to JSON API v1.0 specifications."""

    _logger = Logger(__name__).logger

    @classmethod
    def resource(cls, category, contents, uri, add_meta=False):
        """Format JSON API v1.0 resource from content list."""

        resource_ = {
            'data': {},
            'links': {}
        }
        for content in contents['data']:
            if 'digest' in content:
                uri = urljoin(uri, content['digest'][:16])
                resource_['links'] = {'self': uri}
            type_ = 'snippets' if category == Const.SNIPPET else 'solutions'
            resource_['data'] = {'type': type_,
                                 'id': content['digest'],
                                 'attributes': content}
            break

        if add_meta:
            resource_['meta'] = {}
            resource_['meta']['count'] = 1  # There is always one resource.
            resource_['meta']['limit'] = Config.search_limit
            resource_['meta']['offset'] = Config.search_offset
            resource_['meta']['total'] = contents['meta']['total']

        if not resource_['data']:
            resource_ = json.loads('{"links": {"self": "' + uri + '"}, "data": null}')

        return cls.dumps(resource_)

    @classmethod
    def collection(cls, category, contents, add_meta=False):
        """Format JSON API v1.0 collection from content list."""

        collection = {
            'data': []
        }
        for content in contents['data']:
            type_ = 'snippets' if category == Const.SNIPPET else 'solutions'
            digest = content['digest']
            if 'digest' in Config.filter_fields:
                content.pop('digest', None)
            collection['data'].append({'type': type_,
                                       'id': digest,
                                       'attributes': content})
        if add_meta:
            collection['meta'] = {}
            collection['meta']['count'] = len(collection['data'])
            collection['meta']['limit'] = Config.search_limit
            collection['meta']['offset'] = Config.search_offset
            collection['meta']['total'] = contents['meta']['total']

        return cls.dumps(collection)

    @classmethod
    def error(cls, causes):
        """Format JSON API v1.0 error."""

        # Follow CamelCase in field names because expected usage is from
        # Javascript that uses CamelCase.
        errors = {
            'errors': [],
            'meta': {}
        }
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

        return cls.dumps(errors)

    @staticmethod
    def dumps(response):
        """Create string from json structure."""

        # Python 2 and Python 3 have different defaults for separators and
        # thus they have to be defined here. In case of Python 2, there is
        # whitespace after the comma which is not there with the Python 3.
        kwargs = {'indent': 4, 'sort_keys': True, 'separators': (',', ': ')}
        if Config.compact_json:
            kwargs = {}

        return json.dumps(response, **kwargs)
