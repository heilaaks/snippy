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

"""test_ut_logger: Test Logger() class."""

import json

import pytest

from snippy.logger import Logger
from tests.lib.content import Field


class TestUtLogger(object):
    """Test Logger() class."""

    @staticmethod
    def test_logger_001(logger, caplog, capsys):
        """Test logger basic usage.

        Test case verifies that default log configuration is working.
        By default only log level warning and levels above are printed.
        The logs must be text formatted lines that are not truncated.
        """

        # Test log levels.
        logger.security('testing security level')
        logger.critical('testing critical level')
        logger.error('testing error level')
        logger.warning('testing warning level')
        logger.info('testing info level')
        logger.debug('testing debug level')

        # Test log message length.
        logger.warning('abcdefghij'*100)

        out, err = capsys.readouterr()
        assert not err
        assert not out
        assert len(caplog.records[:]) == 5
        assert 'testing critical level' in caplog.text
        assert 'testing error level' in caplog.text
        assert 'testing warning level' in caplog.text
        assert max(caplog.text.split(), key=len) == 'abcdefghij'*100
        with pytest.raises(Exception):
            json.loads(out)

    @staticmethod
    def test_logger_002(logger, caplog, capsys):
        """Test logger basic usage.

        Test case verifies that debug configuration is working. In
        this case the debug level should be applied that must produce
        full length lines from all log levels.
        """

        Logger.configure({
            'debug': True,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })

        # Test log levels.
        logger.security('testing security level')
        logger.critical('testing critical level')
        logger.error('testing error level')
        logger.warning('testing warning level')
        logger.info('testing info level')
        logger.debug('testing debug level')

        # Test log message length.
        logger.warning('abcdefghij'*100)

        out, err = capsys.readouterr()
        assert not err
        assert len(out.splitlines()) == 7
        assert 'testing critical level' in out
        assert 'testing error level' in out
        assert 'testing warning level' in out
        assert 'testing info level' in out
        assert 'testing debug level' in out
        assert len(caplog.records[:]) == 7
        assert 'testing critical level' in caplog.text
        assert 'testing error level' in caplog.text
        assert 'testing warning level' in caplog.text
        assert 'testing info level' in caplog.text
        assert 'testing debug level' in caplog.text
        assert max(caplog.text.split(), key=len) == 'abcdefghij'*100
        with pytest.raises(Exception):
            json.loads(out)

    @staticmethod
    def test_logger_003(capsys, caplog):
        """Test logger basic usage.

        Test case verifies that very verbose option works for text logs.
        In this case the length of the log message must be truncated and
        the message must be in all lower case characters.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': True
        })
        logger = Logger.get_logger('snippy.' + __name__)

        logger.warning('abcdefghij'*100)
        logger.warning('VARIABLE %s', ('ABCDEFGHIJ'*100))
        logger.security('SECURITY %s', ('ABCDEFGHIJ'*100))

        out, err = capsys.readouterr()
        assert not err
        assert 'abcdefghijabcdefg...' in out
        assert 'abcdefghijabcdefgh...' in out
        assert 'variable abcdefghij' in out
        assert len(caplog.records[0].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[1].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[2].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert caplog.records[0].msg.islower()
        assert caplog.records[1].msg.islower()
        assert caplog.records[2].msg.islower()

    @staticmethod
    def test_logger_004(capsys, caplog):
        """Test logger basic usage.

        Test case verifies that debug option works with json logs.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        logger = Logger.get_logger('snippy.' + __name__)

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

    @staticmethod
    def test_logger_005(capsys, caplog):
        """Test logger basic usage.

        Test case verifies that very verbose option works with json logs.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': True
        })
        logger = Logger.get_logger('snippy.' + __name__)

        logger.warning('abcdefghij'*100)
        logger.warning('variable %s', ('abcdefghij'*100))

        out, err = capsys.readouterr()
        assert not err
        assert len(json.loads(out.splitlines()[0])['message']) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(json.loads(out.splitlines()[1])['message']) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[0].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[1].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert Field.is_iso8601(json.loads(out.splitlines()[0])['asctime'])
        assert Field.is_iso8601(json.loads(out.splitlines()[1])['asctime'])

    @staticmethod
    def test_logger_006(capsys, caplog):
        """Test logger basic usage.

        Test case verifies that quiet option works with different logger
        configuration combinations. This also verifies that the logger
        settings can be changed programmatically.
        """

        Logger.remove()

        # Cause is printed normally to stdout as is when log printing
        # is not activated by debug or very verbose options.
        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        Logger.print_status('NOK: exit cause')
        out, err = capsys.readouterr()
        assert not err
        assert out == 'NOK: exit cause\n'
        assert not caplog.records[:]

        # The quiet option prevents printing the cause as is to stdout.
        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': True,
            'very_verbose': False
        })
        Logger.print_status('NOK: exit cause')
        out, err = capsys.readouterr()
        assert not err
        assert not out
        assert not caplog.records[:]

        # Because the very verbose log printing is enabled, the cause is
        # printed only in the log string with all lower case letters.
        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': True
        })
        Logger.print_status('NOK: exit cause')
        out, err = capsys.readouterr()
        assert not err
        assert 'nok: exit cause' in out
        assert caplog.records[0].msg == 'nok: exit cause'

        # Because the debug log printing is enabled, the cause is printed
        # only in the log string exactly the same as provided.
        caplog.clear()
        Logger.configure({
            'debug': True,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': True,
            'very_verbose': False
        })
        Logger.print_status('NOK: exit cause')
        out, err = capsys.readouterr()
        assert not err
        assert 'NOK: exit cause' in out
        assert caplog.records[0].msg == 'NOK: exit cause'

    @staticmethod
    def test_logger_007(capsys, caplog):
        """Test print_status with JSON logger

        Test case verifies print_status special treatment with JSON logs.
        """

        Logger.remove()

        # Even when logs are disbled, the print_status must output the
        # log in JSON format.
        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        Logger.print_status('snippy server running at: 127.0.0.1:8080')
        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['message'] == 'snippy server running at: 127.0.0.1:8080'
        assert caplog.records[0].msg == 'snippy server running at: 127.0.0.1:8080'
        assert Field.is_iso8601(json.loads(out.splitlines()[0])['asctime'])

        # Because the debug and very_verbose options are not set, the JSON
        # log must not be printed because quiet is enabled.
        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': True,
            'very_verbose': False
        })
        Logger.print_status('snippy server running at: 127.0.0.1:8080')
        out, err = capsys.readouterr()
        assert not err
        assert not out

        # Because the debug option have precedence over the quiet option,
        # the JSON log must be printed.
        caplog.clear()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        Logger.print_status('snippy server running at: 127.0.0.1:8080')
        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['message'] == 'snippy server running at: 127.0.0.1:8080'
        assert caplog.records[0].msg == 'snippy server running at: 127.0.0.1:8080'
        assert Field.is_iso8601(json.loads(out.splitlines()[0])['asctime'])

        # Because the very_verbose option have precedence over the quiet
        # option, the JSON log must be printed.
        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': True
        })
        Logger.print_status('snippy server running at: 127.0.0.1:8080')
        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['message'] == 'snippy server running at: 127.0.0.1:8080'
        assert caplog.records[0].msg == 'snippy server running at: 127.0.0.1:8080'
        assert Field.is_iso8601(json.loads(out.splitlines()[0])['asctime'])

    @staticmethod
    def test_logger_008(capsys):
        """Test operation ID (OID).

        Test case verifies that operation ID (OID) refresh works.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        logger = Logger.get_logger('snippy.' + __name__)

        logger.warning('first message')
        Logger.refresh_oid()
        logger.warning('second message')

        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['oid'] != json.loads(out.splitlines()[1])['oid']

    @staticmethod
    def test_logger_009(capsys):
        """Test Logger debugging.

        Test case verifies that debug methods works.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        logger = Logger.get_logger('snippy.' + __name__)
        logger.warning('testing logger debug')
        Logger.debug()

        out, err = capsys.readouterr()
        assert not err
        assert 'snippy.tests.test_ut_logger' in out

    @staticmethod
    def test_logger_010(capsys):
        """Test removing snippy Logger handlers.

        Test case verifies that Logger.remove() does not delete other than
        snippy packages logging handlers.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        _ = Logger.get_logger('other.package')

        Logger.remove()  # Part of the test.
        Logger.debug()   # Part of the test.

        out, err = capsys.readouterr()
        assert not err
        assert 'Handler Stream' in out

    @staticmethod
    def test_logger_011(capsys, caplog):
        """Test logger advanced configuration.

        Test case verifies that log maximum message length can be configred
        and that the configuration can be changed. The case also tests that
        static logger fields are not changed when logger is reconfigured.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': 120,
            'quiet': False,
            'very_verbose': True
        })
        logger = Logger.get_logger('snippy.' + __name__)

        logger.warning('abcdefghij'*100)
        logger.warning('VARIABLE %s', ('ABCDEFGHIJ'*100))

        out, err = capsys.readouterr()
        assert not err
        assert 'abcdefghijabcdefg...' in out
        assert 'abcdefghijabcdefgh...' in out
        assert 'variable abcdefghij' in out
        assert len(caplog.records[0].msg) == 120
        assert len(caplog.records[1].msg) == 120
        assert caplog.records[0].appname == 'snippy'
        assert caplog.records[1].appname == 'snippy'

        caplog.clear()
        Logger.configure({
            'debug': False,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': True
        })
        logger.warning('abcdefghij'*100)
        logger.warning('VARIABLE %s', ('ABCDEFGHIJ'*100))
        out, err = capsys.readouterr()
        assert not err
        assert 'abcdefghijabcdefg...' in out
        assert 'abcdefghijabcdefgh...' in out
        assert 'variable abcdefghij' in out
        assert len(caplog.records[0].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[1].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert caplog.records[0].appname == 'snippy'
        assert caplog.records[1].appname == 'snippy'

    @staticmethod
    def test_logger_012(logger, caplog, capsys):
        """Test logger security.

        Test case verifies that debug configuration is not printing extremely
        long log messages. These are prevented for safety and security reasons.
        There must be a security event logged.
        """

        Logger.configure({
            'debug': True,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })

        logger.debug('variable%s', ('a'*(Logger.SECURITY_LOG_MSG_MAX+1000)))
        out, err = capsys.readouterr()
        assert not err
        assert len(out.splitlines()) == 2
        assert len(caplog.records[:]) == 2
        assert 'long log message detected and truncated' in caplog.text
        assert 'variableaaaaaaaa' in out
        assert len(max(caplog.text.split(), key=len)) == len('variable' + 'a'*Logger.SECURITY_LOG_MSG_MAX) - len('variable')

    @staticmethod
    def test_logger_013(logger, caplog, capsys):
        """Test logger security.

        Test case verifies that security log is not printed when log exceeds
        the limit with the very verbose ``-vv`` option. This option already
        truncates the log and there is no need to ward about long logs.

        The log message max length is also reduced in this test.
        """

        Logger.configure({
            'debug': True,
            'log_json': False,
            'log_msg_max': 30,
            'quiet': False,
            'very_verbose': True
        })

        logger.debug('variable%s', ('a'*(Logger.SECURITY_LOG_MSG_MAX+1000)))
        out, err = capsys.readouterr()
        assert not err
        assert len(out.splitlines()) == 1
        assert len(caplog.records[:]) == 1
        assert 'variableaaaaaaaaaaaaaaaaaaa...' in out

    @staticmethod
    def test_logger_014(capsys, caplog):
        """Test custom security level.

        Test case verifies that the custom ``security`` level is working.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': 120,
            'quiet': False,
            'very_verbose': True
        })
        logger = Logger.get_logger('snippy.' + __name__)

        logger.security('SECURITY %s', ('ABCDEFGHIJ'*100))

        out, err = capsys.readouterr()
        assert not err
        assert 'security abcdefghij' in out
        assert len(caplog.records[0].msg) == 120
        assert caplog.records[0].appname == 'snippy'
        assert caplog.records[0].levelname == 'security'
        assert caplog.records[0].levelno == Logger.SECURITY
        assert hasattr(caplog.records[0], 'oid')

    @staticmethod
    def test_logger_015(capsys, caplog):
        """Test failure handling.

        Test case verifies that log message length cannot exceed safety limits
        that are defined for a security reasons. Because the very verbose mode
        is used, the log messages are limited to default length.
        """

        Logger.remove()
        Logger.configure({
            'debug': False,
            'log_json': False,
            'log_msg_max': Logger.SECURITY_LOG_MSG_MAX + Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': True
        })
        logger = Logger.get_logger('snippy.' +  __name__)

        logger.warning('abcdefghij'*100)
        logger.warning('VARIABLE %s', ('ABCDEFGHIJ'*100))
        logger.security('SECURITY %s', ('ABCDEFGHIJ'*100))

        out, err = capsys.readouterr()
        assert not err
        assert 'abcdefghijabcdefg...' in out
        assert 'abcdefghijabcdefgh...' in out
        assert 'variable abcdefghij' in out
        assert 'log message length: 10080 :cannot exceed security limit: 10000' in caplog.text
        assert len(caplog.records[1].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[2].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert len(caplog.records[3].msg) == Logger.DEFAULT_LOG_MSG_MAX
        assert caplog.records[0].msg.islower()
        assert caplog.records[1].msg.islower()
        assert caplog.records[2].msg.islower()
        assert caplog.records[3].msg.islower()

    @staticmethod
    def test_logger_016(capsys):
        """Test logs from Gunicorn.

        Test case verifies that log log messages from Gunicorn are converted
        correctly to Snippy server logs. The informative logs from Gunicorn
        must be converted to debug level logs. All other log level must be
        kept the same.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        logger = Logger.get_logger('snippy.server.gunicorn')

        # Test log levels.
        logger.security('testing security level')
        logger.critical('testing critical level')
        logger.error('testing error level')
        logger.warning('testing warning level')
        logger.info('testing info level')
        logger.debug('testing debug level')

        out, err = capsys.readouterr()
        assert not err
        assert json.loads(out.splitlines()[0])['levelno'] == 60
        assert json.loads(out.splitlines()[0])['levelname'] == 'security'
        assert json.loads(out.splitlines()[1])['levelno'] == 50
        assert json.loads(out.splitlines()[1])['levelname'] == 'crit'
        assert json.loads(out.splitlines()[2])['levelno'] == 40
        assert json.loads(out.splitlines()[2])['levelname'] == 'err'
        assert json.loads(out.splitlines()[3])['levelno'] == 30
        assert json.loads(out.splitlines()[3])['levelname'] == 'warning'
        assert json.loads(out.splitlines()[4])['levelno'] == 10
        assert json.loads(out.splitlines()[4])['levelname'] == 'debug'
        assert json.loads(out.splitlines()[5])['levelno'] == 10
        assert json.loads(out.splitlines()[5])['levelname'] == 'debug'

    @staticmethod
    def test_logger_017(caplog):
        """Test pretty printing logs.

        In case of debug when JSON logs are not enabled, the logs are pretty
        printed.
        """

        Logger.remove()
        Logger.configure({
            'debug': True,
            'log_json': False,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })
        logger = Logger.get_logger('snippy.' + __name__)
        row = [(
            '0d364a0e-6b63-11e9-b176-2c4d54508088',
            'reference',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\n'
            'https://chris.beams.io/posts/git-commit/',
            'How to write commit messages',
            '',
            '',
            'git',
            'commit,git,howto,message,scm',
            'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\n'
            'https://chris.beams.io/posts/git-commit/',
            '',
            '',
            '',
            '2018-06-22T13:10:33.295299+00:00',
            '2018-06-27T10:10:16.553052+00:00',
            '33da9768-1257-4419-b6df-881e19f07bbc',
            '6d221115da7b95409c59164632893a57419666135c08151ddbf0be976f3b20a3'
        )]
        output_p3 = (
            "format database row:",
            "        [('0d364a0e-6b63-11e9-b176-2c4d54508088',",
            "          'reference',",
            "          'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\\n'",
            "          'https://chris.beams.io/posts/git-commit/',",
            "          'How to write commit messages',",
            "          '',",
            "          '',",
            "          'git',",
            "          'commit,git,howto,message,scm',",
            "          'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\\n'",
            "          'https://chris.beams.io/posts/git-commit/',",
            "          '',",
            "          '',",
            "          '',",
            "          '2018-06-22T13:10:33.295299+00:00',",
            "          '2018-06-27T10:10:16.553052+00:00',",
            "          '33da9768-1257-4419-b6df-881e19f07bbc',",
            "          '6d221115da7b95409c59164632893a57419666135c08151ddbf0be976f3b20a3')]"
        )
        output_p2 = (
            "format database row:",
            "        [('0d364a0e-6b63-11e9-b176-2c4d54508088',",
            "          'reference',",
            "          'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\\nhttps://chris.beams.io/posts/git-commit/',",
            "          'How to write commit messages',",
            "          '',",
            "          '',",
            "          'git',",
            "          'commit,git,howto,message,scm',",
            "          'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\\nhttps://chris.beams.io/posts/git-commit/',",
            "          '',",
            "          '',",
            "          '',",
            "          '2018-06-22T13:10:33.295299+00:00',",
            "          '2018-06-27T10:10:16.553052+00:00',",
            "          '33da9768-1257-4419-b6df-881e19f07bbc',",
            "          '6d221115da7b95409c59164632893a57419666135c08151ddbf0be976f3b20a3')]"
        )

        # Log is pretty printed.
        logger.debug('format database row:\n%s', row)

        assert '\n'.join(output_p3) in caplog.text or '\n'.join(output_p2) in caplog.text

        caplog.clear()
        Logger.configure({
            'debug': True,
            'log_json': True,
            'log_msg_max': Logger.DEFAULT_LOG_MSG_MAX,
            'quiet': False,
            'very_verbose': False
        })

        output = (
            "format database row:",
            "[('0d364a0e-6b63-11e9-b176-2c4d54508088', 'reference', 'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\\nhttps://chris.beams.io/posts/git-commit/', 'How to write commit messages', '', '', 'git', 'commit,git,howto,message,scm', 'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages\\nhttps://chris.beams.io/posts/git-commit/', '', '', '', '2018-06-22T13:10:33.295299+00:00', '2018-06-27T10:10:16.553052+00:00', '33da9768-1257-4419-b6df-881e19f07bbc', '6d221115da7b95409c59164632893a57419666135c08151ddbf0be976f3b20a3')]"  # noqa pylint: disable=line-too-long
        )
        # Log is not pretty printed because JSON logs are actived.
        logger.debug('format database row:\n%s', row)
        assert '\n'.join(output) in caplog.text
