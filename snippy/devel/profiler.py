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

"""profiler: Profile code."""

from __future__ import print_function

import cProfile
import pstats
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class Profiler(object):
    """Profile code."""

    _profiler = None
    _is_enabled = False

    @classmethod
    def enable(cls, profiled):
        """Enable profiler."""

        if profiled:
            cls._profiler = cProfile.Profile()
            cls._profiler.enable()
            cls._is_enabled = True

    @classmethod
    def disable(cls):
        """Disable profiler."""

        if cls._is_enabled:
            cls._profiler.disable()
            output_string = StringIO()
            cls._profiler = pstats.Stats(cls._profiler, stream=output_string).sort_stats('cumulative')
            cls._profiler.print_stats()
            cls._is_enabled = False
            print(output_string.getvalue())
