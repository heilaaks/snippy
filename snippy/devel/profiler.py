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

"""profiler: Profiler wrapper."""

from __future__ import print_function

import cProfile
import pstats
import sys
from signal import signal, getsignal, SIGPIPE, SIG_DFL
from snippy.config.constants import Constants as Const
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
    from StringIO import StringIO  # pylint: disable=import-error


class Profiler(object):
    """Profiler wrapper."""

    profiler = None
    is_enabled = False

    @classmethod
    def enable(cls):
        """Enable profiler."""

        if '--profile' in sys.argv:
            cls.profiler = cProfile.Profile()
            cls.profiler.enable()
            cls.is_enabled = True

    @classmethod
    def disable(cls):
        """Disable profiler."""

        if cls.is_enabled:
            cls.profiler.disable()
            output_string = StringIO()
            cls.profiler = pstats.Stats(cls.profiler, stream=output_string).sort_stats('cumulative')
            cls.profiler.print_stats()
            cls.is_enabled = False
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(output_string.getvalue())
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)
