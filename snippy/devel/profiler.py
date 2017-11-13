#!/usr/bin/env python3

"""profiler.py: Profiler wrapper."""

from __future__ import print_function
import cProfile
import pstats
import sys
from snippy.config.constants import Constants as Const
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error

class Profiler(object):
    """Profiler wrapper."""

    profiler = None
    is_enabled = False

    @classmethod
    def enable(cls):
        """The profiler enabling is read directly from the system arguments because
        the value is needed before the Config() object gets initialized."""

        if '--profile' in sys.argv:
            cls.profiler = cProfile.Profile()
            cls.profiler.enable()
            cls.is_enabled = True

    @classmethod
    def disable(cls):
        """Disable the profiler and print the results."""

        if cls.is_enabled:
            cls.profiler.disable()
            output_string = StringIO()
            cls.profiler = pstats.Stats(cls.profiler, stream=output_string).sort_stats('cumulative')
            cls.profiler.print_stats()
            cls.is_enabled = False
            print(output_string.getvalue())
