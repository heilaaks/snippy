#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""api_refenrecens: JSON REST API for References."""

from snippy.constants import Constants as Const
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.base import ApiContentDigestBase
from snippy.server.rest.base import ApiContentFieldBase


class ApiReferences(ApiContentBase):
    """Query references."""

    def __init__(self, content):
        super(ApiReferences, self).__init__(content, Const.REFERENCE)


class ApiReferencesDigest(ApiContentDigestBase):
    """Query references based on digest."""

    def __init__(self, content):
        super(ApiReferencesDigest, self).__init__(content, Const.REFERENCE)


class ApiReferencesField(ApiContentFieldBase):
    """Query references based on digest and specified field."""

    def __init__(self, content):
        super(ApiReferencesField, self).__init__(content, Const.REFERENCE)
