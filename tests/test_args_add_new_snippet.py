"""test module."""

import sys
from itertools import product
from unittest import mock
#from mock import patch

import pytest


class TestArgsAddNewSnippet(object):

    def test_no_value(self):
        from cuma.config import Arguments
        obj = Arguments()
        assert obj.get_argument('add') is None

    def test_valid_value_no_tags(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)'"
        sys.argv = ["cuma", "-s", command]
        obj = Arguments()
        assert obj.get_argument('snippet') is command

    def test_valid_value_one_tag(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)', docker"
        sys.argv = ["cuma", "-s", command]
        obj = Arguments()
        assert obj.get_argument('snippet') is command

    def test_valid_value_with_tags(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)' docker, cleanup"
        sys.argv = ["cuma", "-s", command]
        obj = Arguments()
        assert obj.get_argument('snippet') is command
