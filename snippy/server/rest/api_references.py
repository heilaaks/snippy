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

"""api_refenrecens: JSON REST API for ``reference`` category."""

from snippy.constants import Constants as Const
from snippy.server.rest.base import ApiResource
from snippy.server.rest.base import ApiResourceId
from snippy.server.rest.base import ApiResourceIdField


class ApiReferences(ApiResource):
    """Query references."""

    def __init__(self, content):
        super(ApiReferences, self).__init__(content)


class ApiReferencesId(ApiResourceId):
    """Query references based on resource ID."""

    def __init__(self, content):
        super(ApiReferencesId, self).__init__(content)


class ApiReferencesIdField(ApiResourceIdField):
    """Query references with resource ID and attribute."""

    def __init__(self, content):
        super(ApiReferencesIdField, self).__init__(content)
