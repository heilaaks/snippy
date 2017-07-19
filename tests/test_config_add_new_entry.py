"""test module."""
from itertools import product
from unittest import mock

import pytest


class TestAddNewConfigurationEntry(object):

    def test_init(self):
        from cuma.config import Config
        obj = Config()
        print("object %s" % obj)

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
