# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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
from snippy.constants import Constants as Const
from snippy.config.config import Config
from snippy.logger import Logger


class Schema(object):  # pylint: disable=too-few-public-methods
    """Validate JSON document against JSON schema."""

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self.validator = self._get_schema_validator()

    def validate(self, document):
        """Validate document against JSON schema.

        Args:
            document (obj): JSON document that is validated.

        Returns:
            bool: True if the document is valid.
        """

        validated = False
        try:
            self.validator.validate(document)
            validated = True
        except ValidationError as error:
            minimized = ' '.join(str(error).split())
            Cause.push(Cause.HTTP_BAD_REQUEST, 'json media validation failed: {}'.format(minimized))
            for error in self.validator.iter_errors(document):
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
        resolver = RefResolver(base_uri=Config.schema_base_uri(), referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver, format_checker=None)

        return validator


class Validate(object):  # pylint: disable=too-few-public-methods
    """Validate REST API input.

    Description
    ===========

    This class validates JSON REST API request. The validattion rules are
    from the JSON API v1.1 specification.

    Implemented Rules
    =================

    1. Single invalid resource will invalidate whole requst. This aims to
       simplify error logic and amount of code.

    2. "A server MUST return 403 Forbidden in response to an unsupported
        request to create a resource with a client-generated ID." [1]

    3. All schema validations failures cause 400 Bad Request.

    [1] https://jsonapi.org/format/1.1/
    """

    _logger = Logger.get_logger(__name__)
    _schema = Schema()

    @classmethod
    def json_object(cls, request, identity=None):
        """Validate JSON API v1.0 object.

        Args:
            request (dict): JSON resource received from a client.
            identity (str): Full length UUID or partial or full digest.

        Returns:
            tuple: List of validated resources received from client.
        """

        collection = []
        merge = False
        if (request.method.lower() == 'patch' or
                request.get_header('x-http-method-override', default=request.method).lower() == 'patch'):
            merge = True

        if cls._schema.validate(request.media):
            for data in cls._to_list(request.media['data']):
                if cls._is_valid_data(data, request):
                    resource_ = data['attributes']
                    resource_['identity'] = identity
                    resource_['digest'] = None
                    resource_['uuid'] = None
                    resource_['merge'] = merge
                    collection.append(resource_)
                else:
                    collection = []
                    break
        else:
            cls._logger.debug('invalid json media for resource', request.media)

        return collection

    @classmethod
    def _to_list(cls, data):
        """Transform resource data to list.

        A client can send resource or collection in HTTP request. This method
        always converts the top level ``data`` object to a list of resources.

        Args:
            data (dict): Top level JSON ``data`` property.

        Returns:
            tuple: List of attributes
        """

        if not isinstance(data, (list, tuple)):
            return (data,)

        return tuple(data)

    @classmethod
    def _is_valid_data(cls, data, request):
        """Validata top level resource data.

        Additional validation on top of JSON schema validation is done to be
        able to generate other than 400 Bad Request HTTP response. The 400 is
        the only HTTP error generated from JSON schema validation failures.

        JSON API specification requires that the 403 Forbidden response if
        client tried to generate a resource ID.

        Because resources are processed one by one, the mandatory attibutes
        are must checked for the whole HTTP request in here. The ``data`` or
        ``links`` attributes are mandatory only when new resource is created.

        Args:
            data (dict): Top level JSON ``data`` property.
            request (dict): JSON resource received from a client.

        Returns:
            bool: True if the data is valid.
        """

        if 'id' in data:
            Cause.push(Cause.HTTP_FORBIDDEN, 'client generated resource id is not supported, remove member data.id')
            return False

        if cls._is_resource_created(request):
            if 'data' in data['attributes'] and not data['attributes']['data'] and data['type'] in (Const.SNIPPET, Const.SOLUTION):
                Cause.push(Cause.HTTP_BAD_REQUEST, 'mandatory attribute data for {} is empty'.format(data['type']))
                return False

            if 'links' in data['attributes'] and not data['attributes']['links'] and data['type'] == Const.REFERENCE:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'mandatory attribute links for {} is empty'.format(data['type']))
                return False

        return True

    @staticmethod
    def _is_resource_created(request):
        """Test if new resource is created.

        Args:
            request (dict): JSON resource received from a client.

        Returns:
            bool: True if a new resource is created.
        """

        method = request.method.lower()
        override = request.get_header("x-http-method-override", default=method)
        if (method == 'post' or override == 'post') or (method == 'put' or override == 'put'):
            return True

        return False
