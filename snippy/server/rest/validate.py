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

"""validate: Validate REST API request."""

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

from snippy.cause import Cause
from snippy.logger import Logger


class Validate(object):
    """Validate REST API input.

    Description
    ===========

    This class validates JSON REST API request. The validattion rules are
    from the JSON API v1.0 specification.

    Implemented Rules
    =================

    1. Single invalid resource will invalidate whole requst. This aims to
       simplify error logic and amount of code.

    2. "A server MUST return 403 Forbidden in response to an unsupported
        request to create a resource with a client-generated ID." [1]

    [1] http://jsonapi.org/format/
    """

    _logger = Logger.get_logger(__name__)

    @classmethod
    def collection(cls, request):
        """Return media as collection of content."""

        collection = []
        if JsonSchema.validate(JsonSchema.COLLECTION, request.media):
            if isinstance(request.media['data'], (list, tuple)):
                for data in request.media['data']:
                    if cls.is_valid_data(data):
                        collection.append(data['attributes'])
                    else:
                        collection = []
                        break
            elif isinstance(request.media['data'], dict):
                if cls.is_valid_data(request.media['data']):
                    collection.append(request.media['data']['attributes'])
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'invalid request with unknown top level data object: {}'.format(type(request.media['data'])))  # noqa: E501 # pylint: disable=line-too-long

        return tuple(collection)

    @classmethod
    def resource(cls, request, digest):
        """Return media as specific resource with digest."""

        resource_ = {}
        if JsonSchema.validate(JsonSchema.RESOURCE, request.media):
            if isinstance(request.media['data'], dict):
                if cls.is_valid_data(request.media['data']):
                    resource_ = request.media['data']['attributes']
                    resource_['digest'] = digest
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'invalid request with unknown top level data object: {}'.format(type(request.media['data'])))  # noqa: E501 # pylint: disable=line-too-long

        if request.method.lower() == 'patch' or request.get_header('x-http-method-override', default='post').lower() == 'patch':
            resource_['merge'] = True

        return resource_

    @staticmethod
    def is_valid_data(data):
        """Validata top level data object."""

        valid = True
        if 'id' in data:
            Cause.push(Cause.HTTP_FORBIDDEN, 'client generated resource id is not supported, remove member data.id')
            valid = False

        return valid


class JsonSchema(object):  # pylint: disable=too-few-public-methods
    """Validate JSON media against schema."""

    CONTENT = {
        "type": "object",
        "properties": {
            "type": {"enum": ["snippet", "solution"]},
            "attributes": {
                "type": "object",
                "properties": {
                    "data": {"type": ["string", "array"]},
                    "brief": {"type": "string"}
                },
                "required": ["data"]
            }
        },
        "required": ["type"]
    }

    RESOURCE = {
        "type": "object",
        "properties": {
            "data": CONTENT
        },
        "required": ["data"]
    }
    COLLECTION = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": CONTENT,
                "minItems": 1,
                "maxItems": 100
            }
        },
        "required": ["data"]
    }

    @classmethod
    def validate(cls, schema, media):
        """Validate media against JSON schema."""

        validated = False
        try:
            validate(media, schema)
            validated = True
        except ValidationError as exception:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'json media validation failed: {}'.format(exception))
        except SchemaError as exception:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'json schema failure: {}'.format(exception))

        return validated
