Development
===========

Quick Start
-----------

For the development, you can clone the repository and run the setup
for Python virtual environment like below:

.. code:: bash

    git clone https://github.com/heilaaks/snippy.git
    mkvirtualenv snippy
    make dev

The basic commands to run and test are:

.. code:: bash

    python3 runner create -c 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -t docker,container,cleanup
    make test
    make lint
    make coverage
    make docs
    make clean

Python Virtual Environment
--------------------------

You can install the Python virtual environment wrapper like below:

.. code:: bash

    mkdir -p ${HOME}/devel/python-virtualenvs
    sudo pip3 install virtualenvwrapper
    virtualenv --version
    export WORKON_HOME=${HOME}/devel/python-virtualenvs # Add to ~/.bashrc
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3    # Add to ~/.bashrc
    source /usr/bin/virtualenvwrapper.sh                # Add to ~/.bashrc
    mkvirtualenv snippy

Example commands to operate the virtual environment are below. More
information can be found from the Python virtualenvwrapper_ command
reference documentation.

.. code:: bash

    lssitepackages
    lsvirtualenv
    deactivate
    workon snippy
    rmvirtualenv snippy

Pylint
------

The Pylint rc file can be generated for the very first time like:

.. code:: bash

    pylint --generate-rcfile > tests/pylint/pylint-snippy.rc

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html

.. include:: releasing.rst

Modules
-------

snippy.logger
~~~~~~~~~~~~~

**Service**

Logger class offers logger for each caller based on the given module name. The
configuration is controlled by global settings that are inherited by every
logger.

The effective log level for all the loggers created under the 'snippy' logger
namespace is inherited from the root logger which controls the log level. This
relies on that the module level logger does not set the level and it remains
as NOTSET. This causes module level logger to propagate the log record to parent
where it eventually reaches the 'snippy' top level namespace that is just below
the 'root' logger.

**Behaviour**

By default, there are no logs printed to the users. This applies also to error
logs.

There are two levels of logging verbosity. All logs are printed in full length
without filters with the --debug option. The -vv (very verbose) option prints
limited length log messages in lower case letters.

There are two formats for logs: text (default) and JSON. JSON logs can be enabled
with --log-json option. A JSON log has more information fields than text formatted
log. When -vv option is used with JSON logs, it truncates log message in the same
way as with text logs.

Timestamps are in local time with text formatted logs. In case of JSON logs, the
timestamp is in GMT time zone and it follows strictly the ISO8601 format. Both
timestamps are in millisecond granularity.

The log levels are are from Python logger but they follow severity level names
from `RFC 5424 <https://en.wikipedia.org/wiki/Syslog#Severity_level>`_. There is
a custom security level reserved only for security events.

All logs include operation ID that uniquely identifies all logs within specific
operation. The operation ID must be refreshed by logger user after each operation
is completed or the method must be wrapped with @Logger.timeit decorator which
takes care of the OID refreshing.

All logs including Gunicorn server logs, are formatted to match format defined in
this logger.

All logs are printed to stdout.

**Security**

There is a custom security level above critical level. This log level must be
used only when there is a suspected security related event.

There is a hard maximum for log messages length for safety and security reasons.
This tries to prevent extremely long log messages which may cause problems for
the server.

**Rules**

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

**Examples**

   .. code-block:: text

      # Variable printed at the end of log message is separated with colon.
      2018-06-03 19:20:54.838 snippy[5756] [d] [b339bab5]: configured option server: true

      # Variable printed in the middle of log message is separated colons and
      # space from both sides. The purpose is to provide possibility to allow
      # log message post processing and to parse variables from log messages.
      2018-06-03 19:20:54.838 snippy[5756] [d] [b339bab5]: server ip: 127.0.0.1 :and port: 8080

.. autoclass:: snippy.logger.Logger
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
