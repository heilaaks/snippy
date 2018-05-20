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
import math
import re
try:
    from urllib.parse import urljoin
    from urllib.parse import urlparse, urlunparse
    from urllib.parse import quote_plus
except ImportError:
    from urlparse import urljoin, urlparse, urlunparse
    from urllib import quote_plus  # pylint: disable=ungrouped-imports

from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.logger import Logger


class JsonApiV1(object):
    """Format according to JSON API v1.0 specifications."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def resource(cls, collection, request, digest, field=Const.EMPTY, pagination=False):
        """Format JSON API v1.0 resource from content list.

        The contents is a list but there can be only one resources.
        """

        json = {
            'data': {},
            'links': {}
        }
        for resource in collection.resources():
            # Digest must be always the 16 octet digest, not the one provided
            # by user in URL. User may have used digest with any length.
            uri = list(urlparse(request.uri)[:])
            uri[2] = uri[2][:uri[2].index(digest)]  # Remove all after digest.
            uri = urlunparse(uri)
            uri = urljoin(uri, resource.digest[:16])
            if field:
                uri = urljoin(uri + '/', field)
            json['links'] = {'self': uri}
            json['data'] = {
                'type': resource.category,
                'id': resource.digest,
                'attributes': resource.dump_json(Config.filter_fields)
            }

            break

        if pagination:
            json['meta'] = {}
            json['meta']['count'] = 1
            json['meta']['limit'] = Config.search_limit
            json['meta']['offset'] = Config.search_offset
            json['meta']['total'] = collection.total

        if not json['data']:
            json = json.loads('{"links": {"self": "' + uri + '"}, "data": null}')

        return cls.dumps(json)

    @classmethod
    def collection(cls, collection, request, pagination=False):  # pylint: disable=too-many-locals,too-many-branches
        """Format JSON API v1.0 collection from content list."""

        json = {
            'data': []
        }
        for resource in collection.resources():
            json['data'].append({
                 'type': resource.category,
                 'id': resource.digest,
                 'attributes': resource.dump_json(Config.filter_fields)
            })
        if pagination:
            json['meta'] = {}
            json['meta']['count'] = collection.count()
            json['meta']['limit'] = Config.search_limit
            json['meta']['offset'] = Config.search_offset
            json['meta']['total'] = collection.total

            # Rules
            #
            # 1. No pagination needed: add only self, first and last which are all the same.
            # 2. First page with offset zero: do not add previous link.
            # 3. Last page: do not add next link.
            # 4. Sort resulted uri query string in links to get deterministic results for testing.
            # 5. Add links only when offset parameter is defined. Pagination makes sense only with offset.
            # 6. In case search limit is zero, only meta is requested and no links are needed.
            if request.get_param('offset', default=None) and Config.search_limit:
                json['links'] = {}
                self_offset = Config.search_offset

                # Sort query parameter in link URL to have deterministic URL
                # for testing.
                url = re.sub(request.query_string, Const.EMPTY, request.uri)
                for param in sorted(request.params):
                    url = url + param + '=' + quote_plus(request.get_param(param)) + '&'
                url = url[:-1]  # Remove last ambersand.

                # Set offset of links.
                if Config.search_offset == 0 and Config.search_limit >= collection.total:
                    last_offset = self_offset
                    first_offset = self_offset
                else:
                    if Config.search_offset != 0:
                        # prev: o-l <0           ==> o=0    (less)
                        # prev: o-l>=0           ==> o=o-l  (over)
                        # prev: o-l >t           ==> o=t-l  (over) (N/P)
                        prev_offset = Config.search_offset-Config.search_limit if Config.search_offset-Config.search_limit > 0 else 0
                        prev_link = re.sub(r'offset=\d+', 'offset='+str(prev_offset), url)
                        json['links']['prev'] = prev_link

                    if Config.search_offset + Config.search_limit < collection.total:
                        # next: o+l<t            ==> o=o+l  (less)
                        # next: o+l<t-l && o+l<t ==> o=o+l  (last)
                        # next: o+l=t            ==> N/A    (even)
                        # next: o+l>t            ==> N/A    (over)
                        next_offset = Config.search_offset+Config.search_limit
                        next_link = re.sub(r'offset=\d+', 'offset='+str(next_offset), url)
                        json['links']['next'] = next_link
                    # last: o+l<=t-l             ==> o=ceil(t/l)xl-l (less)
                    # last: o+l<t-l && o+l<t     ==> o=o+l           (last)
                    # last: o+l=t                ==> o=o             (even)
                    # last: o+l>t                ==> o=t-l           (over)
                    if Config.search_offset+Config.search_limit <= collection.total-Config.search_limit:
                        # Explicit float casting is needed for Python 2.7 to
                        # get floating point result for ceil.
                        last_offset = int(math.ceil(float(collection.total)/float(Config.search_limit))*Config.search_limit-Config.search_limit)  # noqa: E501 # pylint: disable=line-too-long
                    elif collection.total-Config.search_limit < Config.search_offset+Config.search_limit < collection.total:  # noqa: E501 # pylint: disable=line-too-long
                        last_offset = Config.search_offset+Config.search_limit
                    elif Config.search_offset+Config.search_limit == collection.total:
                        last_offset = self_offset
                    else:
                        last_offset = self_offset
                    first_offset = 0

                self_link = re.sub(r'offset=\d+', 'offset='+str(self_offset), url)
                first_link = re.sub(r'offset=\d+', 'offset='+str(first_offset), url)
                last_link = re.sub(r'offset=\d+', 'offset='+str(last_offset), url)
                json['links']['self'] = self_link
                json['links']['first'] = first_link
                json['links']['last'] = last_link

        return cls.dumps(json)

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
