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

"""api_solutions: JSON REST API for Solutions."""

from snippy.constants import Constants as Const
from snippy.server.rest.base import ApiContentBase
from snippy.server.rest.base import ApiContentDigestBase
from snippy.server.rest.base import ApiContentDigestFieldBase


class ApiSolutions(ApiContentBase):
    """Query solutions."""

    def __init__(self, content):
        super(ApiSolutions, self).__init__(content, Const.SOLUTION)


class ApiSolutionsDigest(ApiContentDigestBase):
    """Query solutions based on digest."""

    def __init__(self, content):
        super(ApiSolutionsDigest, self).__init__(content, Const.SOLUTION)


class ApiSolutionsField(ApiContentDigestFieldBase):
    """Query solution based on digest and specified field."""

    def __init__(self, content):
        super(ApiSolutionsField, self).__init__(content, Const.SOLUTION)
