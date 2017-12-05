#!/usr/bin/env python3

"""falcon_helper.py: Helper methods Falcon testing."""

import sys
import unittest
import pytest
from falcon import testing
from snippy.snip import Snippy


class FalconHelper(unittest.TestCase):
    """Helper methods for Falcon REST API testing."""

    @staticmethod
    @pytest.fixture()
    def client():
        """Testing client."""

        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        # def snippy_teardown():
        #     """Release database."""
        #     snippy.release()
        #     snippy = None
        #     Database.delete_storage()
        # request.addfinalizer(snippy_teardown)

        return testing.TestClient(snippy.server.api)
