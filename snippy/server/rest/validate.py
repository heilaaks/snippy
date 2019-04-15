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

from jsonschema import Draft7Validator, RefResolver
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.logger import Logger


class Schema(object):  # pylint: disable=too-few-public-methods
    """Validate JSON document against JSON schema."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self.validator = self._get_schema_validator()

    def validate(self, media):
        """Validate media against JSON schema.

        Args:
            media (obj): JSON object that is validated against media.
        """

        validated = False
        try:
            self.validator.validate(media)
            validated = True
        except ValidationError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_BAD_REQUEST, 'json media validation failed: {}'.format(minimized))
            for error in self.validator.iter_errors(media):
                self._logger.debug('json media failure: {}'.format(error))
        except SchemaError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'json schema failure: {}'.format(minimized))

        return validated

    @staticmethod
    def _get_schema_validator():
        """Get schema validator.

        Returns:
            obj: Jsonschema draft7 validator.
        """

        schema = Config.server_schema()
        Draft7Validator.check_schema(schema)
        resolver = RefResolver(base_uri=Config.server_schema_base_uri(), referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver, format_checker=None)

        return validator


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
    _jsonschema = Schema()

    @classmethod
    def json_object(cls, request, identity=None):
        """Validate JSON API v1.0 object.

        Args:
            request (dict): JSON object received from client.
            identity (str): Partial or full message digest or UUID.

        Returns:
            tuple: List of validated resources received from client.
        """

        collection = []
        is_collection = cls._is_collection(request.media)
        if is_collection:
            collection = cls._collection(request)
        else:
            collection = cls._resource(request, identity)

        return collection

    @classmethod
    def _is_collection(cls, media):
        """Test if media is collection."""

        if 'data' in media and isinstance(media['data'], (list, tuple)):
            return True

        return False

    @classmethod
    def _resource(cls, request, identity):
        """Validate JSON API v1.0 resource.

        The identity is used to find corresponding resource from storage.
        Resource identities digest and UUID from client must be never used
        and they do not pass schema validation.

        Args:
            request (obj): JSON object received from client.
            identity (str): Partial or full message digest or UUID.

        Returns:
            tuple: Validated resources in a list.
        """

        collection = []
        if cls._jsonschema.validate(request.media):
            if cls._is_valid_data(request.media['data']):
                resource_ = request.media['data']['attributes']
                resource_['identity'] = identity
                resource_['digest'] = None
                resource_['uuid'] = None
                if (request.method.lower() == 'patch' or
                        request.get_header('x-http-method-override', default=request.method).lower() == 'patch'):
                    resource_['merge'] = True
                collection.append(resource_)
        else:
            cls._logger.debug('invalid json media for resource', request.media)

        return tuple(collection)

    @classmethod
    def _collection(cls, request):
        """Validate JSON API v1.0 collection.

        Message digest and UUID received from a client are never used.

        Args:
            request (obj): JSON object received from client.

        Returns:
            tuple: List of validated resources received from client.
        """

        collection = []
        if cls._jsonschema.validate(request.media):
            for data in request.media['data']:
                if cls._is_valid_data(data):
                    data['digest'] = None
                    data['uuid'] = None
                    collection.append(data['attributes'])
                else:
                    collection = []
                    break
        else:
            cls._logger.debug('invalid json media for collection', request.media)

        return tuple(collection)

    @staticmethod
    def _is_valid_data(data):
        """Validata top level data object.

        Args:
            data (dict): JSON top level object that contains data in a dictionary.
        """

        valid = True
        if 'id' in data:
            Cause.push(Cause.HTTP_FORBIDDEN, 'client generated resource id is not supported, remove member data.id')
            valid = False

        return valid
