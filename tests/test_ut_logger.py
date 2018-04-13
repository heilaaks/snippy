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

"""test_ut_logger: Test Logger() class."""

import json

import pytest

from snippy.logger import Logger
from tests.testlib.content import Field


class TestUtLogger(object):
    """Test Logger() class."""

    def test_logger_001(self, logger, caplog, capsys):
        """Test logger basic usage

        Test case verifies that default log configuration is working.
        By default only log level warning and levels above are printed.
        The logs must be text formatted lines that are not truncated.
        """

        # Log levels
        logger.critical('testing critical level')
        logger.error('testing error level')
        logger.warning('testing warning level')
        logger.info('testing info level')
        logger.debug('testing debug level')

        # Log length
        logger.warning('abcdefghij'*100)

        out, err = capsys.readouterr()
        assert not err
        assert not out
        assert len(caplog.records[:]) == 4
        assert 'testing critical level' in caplog.text
        assert 'testing error level' in caplog.text
        assert 'testing warning level' in caplog.text
        assert max(caplog.text.split(), key=len) == 'abcdefghij'*100
        with pytest.raises(Exception):
            json.loads(out)

    def test_logger_002(self, logger, caplog, capsys):
        """Test logger basic usage

        Test case verifies that debug configuration is working. In
        this case the debug level should be applied that must produce
        full length lines from all log levels.
        """

        Logger.configure({
            'debug': True,
            'very_verbose': False,
            'quiet': False,
            'json_logs': False
        })

        # Log levels
        logger.critical('testing critical level')
        logger.error('testing error level')
        logger.warning('testing warning level')
        logger.info('testing info level')
        logger.debug('testing debug level')

        # Log length
        logger.warning('abcdefghij'*100)

        out, err = capsys.readouterr()
        assert not out
        assert not err
        assert len(caplog.records[:]) == 6
        assert 'testing critical level' in caplog.text
        assert 'testing error level' in caplog.text
        assert 'testing warning level' in caplog.text
        assert 'testing info level' in caplog.text
        assert 'testing debug level' in caplog.text
        assert max(caplog.text.split(), key=len) == 'abcdefghij'*100
        with pytest.raises(Exception):
            json.loads(out)

    def test_logger_003(self, capsys, caplog):
        """Test logger basic usage

        Test case verifies that very verbose option works for text logs.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'very_verbose': True,
            'quiet': False,
            'json_logs': False
        })
        logger = Logger('snippy.' + __name__).logger

        # Log length
        logger.warning('abcdefghij'*100)
        logger.warning('variable %s', ('abcdefghij'*100))

        out, err = capsys.readouterr()
        assert not err
        assert 'abcdefghijabcdefg...' in out
        assert 'abcdefghijabcdefgh...' in out
        assert len(caplog.records[0].msg) == Logger.MSG_MAX
        assert len(caplog.records[1].msg) == Logger.MSG_MAX

    def test_logger_004(self, capsys, caplog):
        """Test logger basic usage

        Test case verifies that debug option works with json logs.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'very_verbose': False,
            'quiet': False,
            'json_logs': True
        })
        logger = Logger('snippy.' + __name__).logger

        # Log length
        logger.warning('abcdefghij'*100)
        logger.warning('variable %s', ('abcdefghij'*100))

        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['message'] == 'abcdefghij'*100
        assert json.loads(out.splitlines()[1])['message'] == 'variable %s' % ('abcdefghij'*100)
        assert caplog.records[0].msg == 'abcdefghij'*100
        assert caplog.records[1].msg == 'variable %s' % ('abcdefghij'*100)
        assert Field.is_iso8601(json.loads(out.splitlines()[0])['asctime'])
        assert Field.is_iso8601(json.loads(out.splitlines()[1])['asctime'])

    def test_logger_005(self, capsys, caplog):
        """Test logger basic usage.

        Test case verifies that very verbose option works with json logs.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'very_verbose': True,
            'quiet': False,
            'json_logs': True
        })
        logger = Logger('snippy.' + __name__).logger

        # Log length
        logger.warning('abcdefghij'*100)
        logger.warning('variable %s', ('abcdefghij'*100))

        out, err = capsys.readouterr()
        assert not err
        assert len(json.loads(out.splitlines()[0])['message']) == Logger.MSG_MAX
        assert len(json.loads(out.splitlines()[1])['message']) == Logger.MSG_MAX
        assert len(caplog.records[0].msg) == Logger.MSG_MAX
        assert len(caplog.records[1].msg) == Logger.MSG_MAX
        assert Field.is_iso8601(json.loads(out.splitlines()[0])['asctime'])
        assert Field.is_iso8601(json.loads(out.splitlines()[1])['asctime'])

    def test_logger_006(self, capsys):
        """Test operation ID (OID)

        Test case verifies that operation ID (OID) refresh works.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'very_verbose': False,
            'quiet': False,
            'json_logs': True
        })
        logger = Logger('snippy.' + __name__).logger

        # Log length
        logger.warning('first message')
        Logger.refresh_oid()
        logger.warning('second message')

        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['oid'] != json.loads(out.splitlines()[1])['oid']
