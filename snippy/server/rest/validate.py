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

import json
import jsonschema

from snippy.cause.cause import Cause
from snippy.logger.logger import Logger


class Validate(object):  # pylint: disable=too-few-public-methods
    """Validate REST API input."""

    _logger = Logger(__name__).get()

    @classmethod
    def collection(cls, media):
        """Return media as collection of content."""

        print(media)
        collection = []
#        schema = {
#            "$schema": "http://json-schema.org/draft-04/schema#",
#            "title": "Schema for Snippet content",
#            "$ref": "#/definitions/Collection",
#              "definitions": {
#                "Resource": {
#                  "type": "object",
#                  "properties": {
#                    "links": {
#                      "$ref": "#/definitions/Links"
#                    },
#                    "data": {
#                      "$ref": "#/definitions/Data"
#                    }
#                  },
#                  "required": [
#                    "data"
#                  ]
#                },
#                "Collection": {
#                  "type": "object",
#                  "properties": {
#                    "data": {
#                      "type": "array",
#                      "items": {
#                        "$ref": "#/definitions/Data"
#                      }
#                    }
#                  },
#                  "required": [
#                    "data"
#                  ]
#                },
#                "Links": {
#                  "type": "object",
#                  "properties": {
#                    "self": {
#                      "type": "string",
#                      "description": "Link pointing to resource."
#                    }
#                  }
#                },
#                "Data": {
#                  "type": "object",
#                  "properties": {
#                    "type": {
#                      "type": "string",
#                      "enum": [
#                        "snippet",
#                        "solution"
#                      ]
#                    },
#                    "id": {
#                      "type": "string"
#                    },
#                    "attributes": {
#                      "$ref": "#/definitions/Attributes"
#                    }
#                  },
#                  "required": [
#                    "type",
#                    "attributes"
#                  ]
#                },
#                "Attributes": {
#                  "type": "object",
#                  "properties": {
#                    "data": {
#                      "type": "array",
#                      "items": {
#                        "type": "string"
#                      },
#                      "description": "Mandatory content data in list context with one line per element."
#                    },
#                    "brief": {
#                      "type": "string",
#                      "description": "Optional brief description of the content."
#                    },
#                    "group": {
#                      "type": "string",
#                      "description": "Optional group to which the content belongs.",
#                      "default": "default"
#                    },
#                    "tags": {
#                      "type": "array",
#                      "items": {
#                        "type": "string"
#                      },
#                      "description": "Optional list of tags."
#                    },
#                    "links": {
#                      "type": "array",
#                      "items": {
#                        "type": "string"
#                      },
#                      "description": "Optional list of refrence links."
#                    },
#                    "category": {
#                      "type": "string",
#                      "enum": [
#                        "snippet",
#                        "solution"
#                      ],
#                      "description": "Automatically assigned content category."
#                    },
#                    "filename": {
#                      "type": "string",
#                      "description": "Optional filename that that defines automatically used filename when content is exported."
#                    },
#                    "runalias": {
#                      "type": "string",
#                      "description": "Optional alias to run the content."
#                    },
#                    "versions": {
#                      "type": "string",
#                      "description": "Optional list of services and versions related to the snippet."
#                    },
#                    "utc": {
#                      "type": "string",
#                      "description": "Optional UTC timestamp in ISO 8601 format that is automatically assigned if left out."
#                    },
#                    "digest": {
#                      "type": "string",
#                      "description": "Automatically assigned message digest that uniquely identifies the content."
#                    }
#                  },
#                  "required": [
#                    "data"
#                  ]
#                },
#                "Errors": {
#                  "type": "object",
#                  "properties": {
#                    "meta": {
#                      "$ref": "#/definitions/Meta"
#                    },
#                    "errors": {
#                      "type": "array",
#                      "items": {
#                        "$ref": "#/definitions/Error"
#                      }
#                    }
#                  },
#                  "required": [
#                    "meta",
#                    "errors"
#                  ]
#                },
#                "Meta": {
#                  "type": "object",
#                  "properties": {
#                    "version": {
#                      "type": "string",
#                      "description": "Server version"
#                    },
#                    "homepage": {
#                      "type": "string",
#                      "description": "Server homepage URL"
#                    }
#                  },
#                  "required": [
#                    "version",
#                    "homepage"
#                  ]
#                },
#                "Error": {
#                  "type": "object",
#                  "properties": {
#                    "status": {
#                      "type": "string",
#                      "description": "HTTP status code"
#                    },
#                    "statusString": {
#                      "type": "string",
#                      "description": "HTTP status as text string"
#                    },
#                    "module": {
#                      "type": "string",
#                      "description": "Location of error"
#                    },
#                    "title": {
#                      "type": "string",
#                      "description": "Message describing the error."
#                    }
#                  },
#                  "required": [
#                    "status",
#                    "statusString",
#                    "module",
#                    "title"
#                  ]
#                }
#              }
#            }

       # schema = {
       #     "$schema": "http://json-schema.org/draft-04/schema#",
       #     "title": "Schema for a recording",
       #     "type": "object",
       #       "properties": {
       #         "links": {"type" : "string"},
       #         "data": {"type" : "object"}
       #       },
       #       "required": ["data"]
       #     }

        #with open('./collection.json') as schema_file:
            #return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)
        ###data = json.load(open('./collection.json'))
        ###data = json.load(open('../snippy/server/rest/collection.json'))
        #data = json.load(open('./snippy/data/schema/collection.json'))
        #jsonschema.RefResolver('file://' + base_dir + '/' + 'Fields/Ranges.json', schema)
        #print(data)

        #data = json.load(open('./snippy/data/schema/collection.json'))
        #try:
        #    jsonschema.validate(media, data)
        #    print("VALID")
        #except jsonschema.exceptions.ValidationError as exception:
        #    print("NON VALID")
        #    cls._logger.exception('fatal failure to generate formatted export file "%s"', exception)

        try:
            if 'data' in media and isinstance(media['data'], (list, tuple)):
                for data in media['data']:
                    if 'attributes' in data:
                        collection.append(data['attributes'])
            elif 'data' in media and isinstance(media['data'], dict):
                if 'attributes' in media['data']:
                    collection.append(media['data']['attributes'])
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'request ignored because top level data member missing')
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
