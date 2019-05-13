Development
===========

Installation
------------

The instructions are tested with Fedora and Bash shell. Similar command
likely work with other Linux distributions.

.. note::

   Install docker-ce to be able to run test with read container. Make sure
   that the user who runs the Snippy tests is able to run docker commands.

.. note::

   The PostgreSQL adapters used with the server are installed by compiling
   them. This require working gcc toolchain.

.. code:: bash

    # Clone the project.
    mkdir ~/devel && cd $_
    git clone git@github.com:heilaaks/snippy.git

    # Install CPython versions.
    sudo dnf install -y \
        python27 \
        python34 \
        python35 \
        python36 \
        python37 \
        python38 \
        python3-devel \
        python2-devel

    # Install PyPy3 versions.
    sudo dnf install -y \
        pypy2 \
        pypy3 \
        pypy2-devel \
        pypy3-devel \
        postgresql-devel

    # Install Python virtual environments.
    pip install --user \
        pipenv \
        virtualenv \
        virtualenvwrapper
    export PATH=${PATH}:~/.local/bin

    # Configure virtualenv wrapper.
    vi ~/.bashrc
       export WORKON_HOME=~/devel/.virtualenvs
       source ~/.local/bin/virtualenvwrapper.sh
    source ~/.bashrc

    # Create virtual environments for each Python version.
    mkvirtualenv --python /usr/bin/python2.7 p27-snippy
    mkvirtualenv --python /usr/bin/python3.4 p34-snippy
    mkvirtualenv --python /usr/bin/python3.5 p35-snippy
    mkvirtualenv --python /usr/bin/python3.6 p36-snippy
    mkvirtualenv --python /usr/bin/python3.7 p37-snippy
    mkvirtualenv --python /usr/bin/python3.8 p38-snippy
    mkvirtualenv --python /usr/bin/pypy2 pypy2-snippy
    mkvirtualenv --python /usr/bin/pypy3 pypy3-snippy

    # Repeat for all virtual environments.
    for VENV in p27-snippy \
                p34-snippy \
                p35-snippy \
                p36-snippy \
                p37-snippy \
                p38-snippy \
                pypy2-snippy \
                pypy3-snippy
    do
        workon $VENV
        make upgrade-wheel
        make install-devel
        deactivate
    done

    # Compile Docker image for Docker tests.
    make docker

    # Run standard feature and refactoring test suite.
    make test

    # Run all tests against PostgreSQL.
    sudo docker run -d --name postgres -e POSTGRES_PASSWORD= -p 5432:5432 -d postgres
    make test-postgresql

    # Run all tests with server.
    make docker
    make test-server

    # Run all tests with Docker image.
    make docker
    make test-docker

    # Run all tests.
    make test-all

    # Install Bash complete
    python runner export --complete bash
    sudo cp snippy.bash-completion /etc/bash_completion.d/snippy.bash-completion

Workflow
--------

.. code:: bash

    # Run tests.
    make test

    # Run lint.
    make lint

    # Clean all generated files.
    make clean-all

    # Run test coverage.
    make coverage

    # Create documents.
    make docs

Heroku app
----------

.. code:: bash

    # Install Heroku command line application.
    curl https://cli-assets.heroku.com/install.sh | sh

    # Run Heroku app locally.
    heroku login
    heroku local web -f Procfile
    heroku logs -a snippy-server

    # Login
    https://snippy-server.herokuapp.com/api/snippets?sall=docker&limit=5

Modules
-------

snippy.logger
~~~~~~~~~~~~~

Description
```````````

Logger class offers logger for each caller based on the given module name. The
configuration is controlled by global settings that are inherited by every
logger.

The effective log level for all the loggers created under the 'snippy' logger
namespace is inherited from the root logger which controls the log level. This
relies on that the module level logger does not set the level and it remains
as ``NOTSET``. This causes module level logger to propagate the log record to
parent where it eventually reaches the ``snippy`` top level namespace that is
just below the ``root`` logger.

Design
``````

.. note::

   This chapter describes the Snippy logging design and rules, not the Logger
   class behaviour.

.. note::

   The are the logging rules that must be followed.

   #. Only OK or NOK with cause text must be printed with default settings.
   #. There must be no logs printed to user.
   #. There must be no exceptions printed to user.
   #. Exceptions logs are printed as INFO and all other logs as DEBUG.
   #. Variables printed in logs must be separated with colon.
   #. All other than error logs must be printed as lower case string.
   #. The --debug option must print logs without filters in full-length.
   #. The -vv option must print logs in lower case and one log per line.
   #. All external libraries must follow the same log format.
   #. All logs must be printed to stdout.

**Overview**

There are two levels of logging verbosity. All logs are printed in full length
without modifications with the ``--debug`` option unless the maximum log message
length for safety and security reason is exceeded. The very verbose option ``-vv``
prints limited length log messages with all lower case letters.

There are two formats for logs: text (default) and JSON. JSON logs can be enabled
with the ``--log-json`` option. A JSON log has more information fields than the
text formatted log. When the ``-vv`` option is used with JSON logs, it truncates
log message in the same way as with the text logs.

All logs including Gunicorn server logs, are formatted to match format defined in
this logger.

All logs are printed to stdout with the exception of command line parse failures
that are printed to stdout.

Text logs are optimized for a local development done by for humans and JSON logs
for automation and analytics.

There are no logs printed to users by default. This applies also to error logs.

**Timestamps**

Timestamps are in local time with text formatted logs. In case of JSON logs, the
timestamp is in GMT time zone and it follows strictly the ISO8601 format. Text
log timestamp is presented in millisecond granularity and JSON log in microsecond
granularity.

Python 2 does not support timezone parsing. The ``%z`` directive is available only
from Python 3.2 onwards. From Python 3.7 and onwards, the datetime ``strptime`` is
able to parse timezone in format that includes colon delimiter in UTC offset.

>>> import datetime
>>>
>>> timestamp = '2018-02-02T02:02:02.000001+00:00'
>>>
>>> # Python 3.7 and later
>>> datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
>>>
>>> # Python 3 before 3.7
>>> timestamp = timestamp.replace('+00:00', '+0000')
>>> datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
>>>
>>> # Python 2.7
>>> timestamp = timestamp[:-6]  # Remove last '+00:00'.
>>> datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')

**Log levels**

The log levels are are from Python logger but they follow severity level names
from `RFC 5424 <https://en.wikipedia.org/wiki/Syslog#Severity_level>`_. There is
a custom security level reserved only for security events.

**Operation ID (OID)**

All logs include operation ID that uniquely identifies all logs within specific
operation. The operation ID must be refreshed by logger user after each operation
is completed or the method must be wrapped with the ``@Logger.timeit`` decorator
which takes care of the OID refreshing.

Security
````````

There is a custom security level above critical level. This log level must be
used only when there is a suspected security related event.

There is a hard maximum for log messages length for safety and security reasons.
This tries to prevent extremely long log messages which may cause problems for
the server.

Examples
````````

.. code-block:: text

  # Variable printed at the end of log message is separated with colon.
  2018-06-03 19:20:54.838 snippy[5756] [d] [b339bab5]: configured option server: true

  # Variable printed in the middle of log message is separated colons and
  # space from both sides. The purpose is to provide possibility to allow
  # log message post processing and to parse variables from log messages.
  2018-06-03 19:20:54.838 snippy[5756] [d] [b339bab5]: server ip: 127.0.0.1 :and port: 8080

.. automodule:: snippy.logger
   :members:
   :member-order: bysource

snippy.cause
~~~~~~~~~~~~

**Service**

Cause class offers storage services for normal and error causes. The causes are
stored in a list where user can get all the failues that happened for example
during the operation.

All causes are operated with predefind constants for HTTP causes and short
descriptions of the event.

.. autoclass:: snippy.cause.Cause
   :members:
   :member-order: bysource

snippy.config
~~~~~~~~~~~~~

**Service**

Global configuration.

.. autoclass:: snippy.config.config.Config
   :members:
   :member-order: bysource

snippy.config.source.cli
~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

Command line configuration source.

.. autoclass:: snippy.config.source.cli.Cli
   :members:
   :member-order: bysource

snippy.config.source.api
~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

REST API configuration source.

.. autoclass:: snippy.config.source.api.Api
   :members:
   :member-order: bysource

snippy.config.source.base
~~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

Configuration source base class.

.. autoclass:: snippy.config.source.base.ConfigSourceBase
   :members:
   :member-order: bysource

snippy.content.parser
~~~~~~~~~~~~~~~~~~~~~

**Service**

Parser class offers a parser to extract content fields from text source.

.. autoclass:: snippy.content.parser.Parser
   :members:
   :member-order: bysource

snippy.content.parsers.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

Content parser base class offers basic parsing methods.

.. autoclass:: snippy.content.parsers.base.ContentParserBase
   :members:
   :member-order: bysource

snippy.content.parsers.text
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

Content parser for text content.

.. autoclass:: snippy.content.parsers.text.ContentParserText
   :members:
   :member-order: bysource


snippy.content.parsers.mkdn
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

Content parser for Markdown content.

.. autoclass:: snippy.content.parsers.mkdn.ContentParserMkdn
   :members:
   :member-order: bysource

snippy.content.parsers.dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Service**

Content parser for YAML and JSON content.

.. autoclass:: snippy.content.parsers.dict.ContentParserDict
   :members:
   :member-order: bysource

snippy.storage.storage
~~~~~~~~~~~~~~~~~~~~~~

**Service**

Storage class offers database agnosting storage services. This abstracts the
actual database solution from rest of the implementation.

.. autoclass:: snippy.storage.storage.Storage
   :members:
   :member-order: bysource

snippy.storage.database
~~~~~~~~~~~~~~~~~~~~~~~

**Service**

SqliteDb class offers database implementation for the Storage class.

.. autoclass:: snippy.storage.database
   :members:
   :member-order: bysource
