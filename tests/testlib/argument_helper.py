#!/usr/bin/env python3

"""argument_helper.py: Helper methods for command line argument testing."""

import sys


class ArgumentHelper(object): # pylint: disable=too-few-public-methods
    """Helper methods for arguments testing."""

    def reset(self):
        """Reset command line arguments."""

        sys.argv = ['snippy']
