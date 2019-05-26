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

"""generate: Generate a body for HTTP REST API response."""

import gzip
import json
import math
import operator
import re
from collections import OrderedDict

try:
    import StringIO  # Only in Python 2.
except ImportError:
    pass
try:
    from urllib.parse import urljoin
    from urllib.parse import urlparse, urlunparse
    from urllib.parse import quote_plus
except ImportError:
    from urlparse import urljoin, urlparse, urlunparse
    from urllib import quote_plus  # pylint: disable=ungrouped-imports

from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.logger import Logger


class Generate(object):
    """Generate a body for HTTP REST API response."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def resource(cls, collection, request, response, identity, field=Const.EMPTY, pagination=False):
        """Create HTTP response body with a resource.

        The links ``self`` and data ``id`` attributes are always created from
        the resource digest attribute. The digest is considered as a main ID.

        The ``self`` attribute cannot contain the URI from the request. If
        content is updated, the request URI is not correct after the resource
        update when digest in URI is used.

        The resource digest attributes changes when the resource changes. This
        should work with HTTP caching. The caching works so that the URI and
        response are cached. If URI contains an UUID which does not change, the
        cached result could be incorrect. But when the link with digest changes
        with the content, the cached result should be always correct. [1]

        [1] This is something that the author is not too confident.

        Args:
            collection (Collection()): Collection with resources to be send in HTTP response.
            request (object): HTTP request.
            response (object): HTTP response.
            identity (str): Partial or full message digest or UUID.
            field (str): Content field attribute that was used in the HTTP request URL.
            pagination (bool): Define if pagination is used.

        Returns:
            body: JSON body as a string or compressed bytes.

        """

        data = {
            'data': {},
            'links': {}
        }
        for resource in collection.resources():
            uri = list(urlparse(request.uri))
            uri[2] = uri[2][:uri[2].index(identity)]  # Remove everything before resource ID.
            uri = urlunparse(uri)
            uri = urljoin(uri, resource.uuid)
            if field:
                uri = urljoin(uri + '/', field)
            data['links'] = {'self': uri}
            data['data'] = {
                'type': resource.category,
                'id': resource.uuid,
                'attributes': resource.dump_dict(Config.remove_fields)
            }

            break

        if pagination:
            data['meta'] = {}
            data['meta']['count'] = 1
            data['meta']['limit'] = Config.search_limit
            data['meta']['offset'] = Config.search_offset
            data['meta']['total'] = collection.total

        if not data['data']:
            data = json.loads('{"links": {"self": "' + request.uri + '"}, "data": null}')

        return cls.compress(request, response, cls.dumps(data))

    @classmethod
    def collection(cls, collection, request, response, pagination=False):  # pylint: disable=too-many-locals,too-many-branches
        """Generate HTTP body with multiple resources.

        Created body follows the JSON API specification.

        Args:
            collection (Collection()): Collection that has resources to be send in HTTP response.
            request (object): HTTP request.
            response (object): HTTP response.
            pagination (bool): Define if pagination is used.

        Returns:
            body: JSON body as a string or compressed bytes.

        """

        data = {
            'data': []
        }
        for resource in collection.resources():
            data['data'].append({
                'type': resource.category,
                'id': resource.uuid,
                'attributes': resource.dump_dict(Config.remove_fields)
            })
        if pagination:
            data['meta'] = {}
            data['meta']['count'] = len(collection)
            data['meta']['limit'] = Config.search_limit
            data['meta']['offset'] = Config.search_offset
            data['meta']['total'] = collection.total

            # Rules
            #
            # 1. No pagination needed: add only self, first and last which are all the same.
            # 2. First page with offset zero: do not add previous link.
            # 3. Last page: do not add next link.
            # 4. Sort resulted uri query string in links to get deterministic results for testing.
            # 5. Add links only when offset parameter is defined. Pagination makes sense only with offset.
            # 6. In case search limit is zero, only meta is requested and no links are needed.
            if request.get_param('offset', default=None) and Config.search_limit:
                data['links'] = {}
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
                        data['links']['prev'] = prev_link

                    if Config.search_offset + Config.search_limit < collection.total:
                        # next: o+l<t            ==> o=o+l  (less)
                        # next: o+l<t-l && o+l<t ==> o=o+l  (last)
                        # next: o+l=t            ==> N/A    (even)
                        # next: o+l>t            ==> N/A    (over)
                        next_offset = Config.search_offset+Config.search_limit
                        next_link = re.sub(r'offset=\d+', 'offset='+str(next_offset), url)
                        data['links']['next'] = next_link
                    # last: o+l<=t-l             ==> o=ceil(t/l)xl-l (less)
                    # last: o+l<t-l && o+l<t     ==> o=o+l           (last)
                    # last: o+l=t                ==> o=o             (even)
                    # last: o+l>t                ==> o=t-l           (over)
                    if Config.search_offset+Config.search_limit <= collection.total-Config.search_limit:
                        # Explicit float casting is needed for Python 2.7 to
                        # get floating point result for ceil.
                        last_offset = int(math.ceil(float(collection.total)/float(Config.search_limit))*Config.search_limit-Config.search_limit)  # noqa pylint: disable=line-too-long
                    elif collection.total-Config.search_limit < Config.search_offset+Config.search_limit < collection.total:  # noqa pylint: disable=line-too-long
                        last_offset = Config.search_offset+Config.search_limit
                    elif Config.search_offset+Config.search_limit == collection.total:
                        last_offset = self_offset
                    else:
                        last_offset = self_offset
                    first_offset = 0

                self_link = re.sub(r'offset=\d+', 'offset='+str(self_offset), url)
                first_link = re.sub(r'offset=\d+', 'offset='+str(first_offset), url)
                last_link = re.sub(r'offset=\d+', 'offset='+str(last_offset), url)
                data['links']['self'] = self_link
                data['links']['first'] = first_link
                data['links']['last'] = last_link

        return cls.compress(request, response, cls.dumps(data))

    @classmethod
    def fields(cls, attribute, uniques, request, response):
        """Generate HTTP body for fields API endpoints.

        Created body follows the JSON API specification.

        Args:
            attribute (str): Resource attribute which unique values are sent
            uniques (dict): Unique values for the field.

        Returns:
            body: JSON body as a string or compressed bytes.
        """

        # Follow CamelCase in field names because expected usage is from
        # Javascript that uses CamelCase.
        fields = {}
        for field in uniques:
            fields[field[0]] = field[1]
        fields = OrderedDict(sorted(fields.items(), key=operator.itemgetter(1), reverse=True))
        data = {
            'data': {},
        }
        data['data'] = {
            'type': attribute,
            'attributes': {
                attribute: fields
            }
        }

        return cls.compress(request, response, cls.dumps(data))

    @classmethod
    def error(cls, causes):
        """Generate HTTP body with an error.

        Created body follows the JSON API specification.

        Args:
            cause (Cause()): Cause that is used to build the error response.

        Returns:
            body: JSON body as a string or compressed bytes.
        """

        # Follow CamelCase in field names because expected usage is from
        # Javascript that uses CamelCase.
        data = {
            'errors': [],
            'meta': {}
        }
        for cause in causes['errors']:
            data['errors'].append({
                'status': str(cause['status']),
                'statusString': cause['status_string'],
                'title': cause['title'],
                'module': cause['module']
            })

        if not data['errors']:
            data = {
                'errors': [{
                    'status': '500',
                    'statusString': '500 Internal Server Error',
                    'title': 'Internal errors not found when error detected.'
                }]
            }
        data['meta'] = causes['meta']

        return cls.dumps(data)

    @classmethod
    def dumps(cls, body):
        """Create string presentation from a JSON body.

        The JSON body is converted to a string presentation from the data
        structure.

        By default the body is pretty printed to help readability. Optionally
        it can be minified by removing all whitespaces from the string.

        Args:
            body (dict): HTTP JSON response body in a dictionary.

        Returns:
            string: JSON string presentation from the HTTP response body.
        """

        # Python 2 and Python 3 have different defaults for separators and
        # thus they have to be defined here. In case of Python 2, there is
        # whitespace after the comma which is not there with the Python 3.
        kwargs = {'indent': 4, 'sort_keys': True, 'separators': (',', ': ')}
        if Config.server_minify_json:
            kwargs = {}

        return json.dumps(body, **kwargs)

    @classmethod
    def compress(cls, request, response, body):
        """Compress the HTTP response body.

        The response headers are updated if the response body is compressed.

        Args:
            request (object): Received HTTP request.
            response (object): HTTP response which headers may be updated.
            body (str): String presentation from HTTP response body.

        Returns:
            string|bytes: Body compressed to bytes or original JSON string.
        """

        if 'gzip' not in request.get_header('accept-encoding', default='').lower():
            return body

        response.set_header('content-encoding', 'gzip')
        if Const.PYTHON2:
            outfile = StringIO.StringIO()
            gzip_file = gzip.GzipFile(fileobj=outfile, mode="wb")
            gzip_file.write(body.encode('utf-8'))
            gzip_file.close()
            return outfile.getvalue()

        return gzip.compress(body.encode('utf-8'), compresslevel=9)  # slowest with most compression.
