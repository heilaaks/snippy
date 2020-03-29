# -*- coding: utf-8 -*-
#
#  Snippy - Software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
#
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""test_ut_plugins: Test Plugins() class."""

from snippy.plugins import Const
from snippy.plugins import Parser
from snippy.plugins import Schema


class TestUtPlugins(object):  # pylint: disable=too-few-public-methods
    """Test Plugins() class."""

    @staticmethod
    def test_plugins_001():
        """Test plugins schema validation"""

        test = Schema()
        test.validate({})
        test = Const.SNIPPET
        _ = Parser.format_data(Const.SNIPPET, "")
