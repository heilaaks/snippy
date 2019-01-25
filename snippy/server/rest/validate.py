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

"""validate: Validate REST API request."""

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

from snippy.cause import Cause
from snippy.logger import Logger


class Validate(object):  # pylint: disable=too-few-public-methods
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
    def json_object(cls, request, digest=None):
        """Validate JSON API v1.0 object.

        Args:
            request (dict): JSON object received from client.
            digest (str): Message digest or part of it.

        Returns:
            tuple: List of validated resources received from client.
        """

        collection = []
        is_collection = JsonSchema.is_collection(request.media)
        schema = cls._get_schema(request, is_collection)
        if is_collection:
            collection = Validate._collection(request, schema)
        else:
            collection = Validate._resource(request, digest, schema)

        return collection

    @classmethod
    def _resource(cls, request, digest, schema):
        """Validate JSON API v1.0 resource.

        Args:
            request (dict): JSON object received from client.
            digest (str): Message digest or part of it.
            schema (str): JSON schema to validate the request.

        Returns:
            tuple: Validated resources in a list.
        """

        collection = []
        if JsonSchema.validate(schema, request.media):
            if cls._is_valid_data(request.media['data']):
                resource_ = request.media['data']['attributes']
                resource_['digest'] = digest
                if (request.method.lower() == 'patch' or
                        request.get_header('x-http-method-override', default=request.method).lower() == 'patch'):
                    resource_['merge'] = True
                collection.append(resource_)
        else:
            cls._logger.debug('invalid json media for resource', request.media)

        return tuple(collection)

    @classmethod
    def _collection(cls, request, schema):
        """Validate JSON API v1.0 collection.

        Args:
            request (dict): JSON object received from client.

        Returns:
            tuple: List of validated resources received from client.
        """

        collection = []
        if JsonSchema.validate(schema, request.media):
            for data in request.media['data']:
                if cls._is_valid_data(data):
                    collection.append(data['attributes'])
                else:
                    collection = []
                    break
        else:
            cls._logger.debug('invalid json media for collection', request.media)

        return tuple(collection)

    @staticmethod
    def _is_valid_data(data):
        """Validata top level data object."""

        valid = True
        if 'id' in data:
            Cause.push(Cause.HTTP_FORBIDDEN, 'client generated resource id is not supported, remove member data.id')
            valid = False

        return valid

    @classmethod
    def _get_schema(cls, request, is_collection):
        """Get correct schema for the request.

        If a new content is created with POST or the content is replaced
        with PUT request, the mandatory fields must be present. Otherwise
        the request is considered as update and the mandatory fields may
        be missing.

        Args:
            request (dict): JSON object received from client.
            is_collection (bool): Defines if the request is collection
        """

        create = False
        if (request.method.lower() == "post" and request.get_header("x-http-method-override", default=request.method).lower() == "post") \
           or \
           (request.method.lower() == "put" or request.get_header("x-http-method-override", default=request.method).lower() == "put"):
            create = True

        if is_collection:
            if create:
                schema = JsonSchema.COLLECTION_CREATE
            else:
                schema = JsonSchema.COLLECTION_UPDATE
        else:
            if create:
                schema = JsonSchema.RESOURCE_CREATE
            else:
                schema = JsonSchema.RESOURCE_UPDATE

        return schema


class JsonSchema(object):  # pylint: disable=too-few-public-methods
    """Validate JSON media against schema.

    In case of creating content, the content data or links are mandatory. In
    case of content updates, it is possible to leave data and links fields
    out from REST API request.
    """

    CONTENT_CREATE = {
        "type": "object",
        "properties": {
            "type": {"enum": ["snippet", "solution", "reference"]},
            "attributes": {
                "type": "object",
                "properties": {
                    "data": {"type": ["string", "array"]},
                    "brief": {"type": ["string", "null"]},
                    "links": {"type": ["string", "array", "null"]}
                },
                "anyOf": [{
                    "required": ["data"]
                }, {
                    "required": ["links"]
                }]
            }
        },
        "required": ["type"]
    }

    CONTENT_UPDATE = {
        "type": "object",
        "properties": {
            "type": {"enum": ["snippet", "solution", "reference"]},
            "attributes": {
                "type": "object",
                "properties": {
                    "data": {"type": ["string", "array"]},
                    "brief": {"type": ["string", "null"]},
                    "links": {"type": ["string", "array", "null"]}
                }
            }
        },
        "required": ["type"]
    }

    RESOURCE_CREATE = {
        "type": "object",
        "properties": {
            "data": CONTENT_CREATE
        },
        "required": ["data"]
    }

    RESOURCE_UPDATE = {
        "type": "object",
        "properties": {
            "data": CONTENT_UPDATE
        },
        "required": ["data"]
    }

    COLLECTION_CREATE = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": CONTENT_CREATE,
                "minItems": 1,
                "maxItems": 100
            }
        },
        "required": ["data"]
    }

    COLLECTION_UPDATE = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": CONTENT_UPDATE,
                "minItems": 1,
                "maxItems": 100
            }
        },
        "required": ["data"]
    }

    IS_COLLECTION = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
            }
        }
    }

    @classmethod
    def is_collection(cls, media):
        """Test if media is collection."""

        collection = False
        try:
            validate(media, JsonSchema.IS_COLLECTION)
            collection = True
        except ValidationError:
            pass

        return collection

    @classmethod
    def validate(cls, schema, media):
        """Validate media against JSON schema."""

        validated = False
        try:
            validate(media, schema)
            validated = True
        except ValidationError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_BAD_REQUEST, 'json media validation failed: {}'.format(minimized))
        except SchemaError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'json schema failure: {}'.format(minimized))

        return validated
