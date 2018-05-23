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

"""api_snippets: JSON REST API for Snippets."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.api import Api
from snippy.content.snippet import Snippet
from snippy.logger import Logger
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.base import ApiContentDigestBase
from snippy.server.rest.base import ApiContentFieldBase
from snippy.server.rest.jsonapiv1 import JsonApiV1
from snippy.server.rest.validate import Validate


class ApiSnippets(ApiContentBase):
    """Process snippet collections."""

    def __init__(self, content):
        super(ApiSnippets, self).__init__(content, Const.SNIPPET)


class ApiSnippetsDigest(ApiContentDigestBase):
    """Process snippet based on digest."""

    def __init__(self, content):
        super(ApiSnippetsDigest, self).__init__(content, Const.SNIPPET)


class ApiSnippetsField(ApiContentFieldBase):
    """Process snippet based on digest and field."""

    def __init__(self, content):
        super(ApiSnippetsField, self).__init__(content, Const.SNIPPET)

