#!/usr/bin/env python3

"""arguments_helper.py: Helper methods for command line arguments testing."""

import sys


class ArgumentsHelper(object): # pylint: disable=too-few-public-methods
    """Helper methods for arguments testing."""

    def reset(self):
        """Reset command line arguments."""

        sys.argv = ['snippy']
