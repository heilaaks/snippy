#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""test_api_healthcheck: Test server healthcheck."""

from snippy.cause import Cause
from snippy.snip import Snippy

class TestApiHealthcheck(object):  # pylint: disable=too-few-public-methods
    """Test server in healtcheck."""

    @staticmethod
    def test_api_healthcheck_001(capsys, osenviron, healthcheck):
        """Run API healtcheck."""

        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        snippy = Snippy(['snippy', '--server-healthcheck'])
        cause = snippy.run()
        healthcheck.assert_called_once_with('127.0.0.1:8081', timeout=2)
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == ''
        assert not err
