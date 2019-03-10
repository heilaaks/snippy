Development
===========

Quick Start
-----------

For the development, you can clone the repository and run the setup
for Python virtual environment like below:

.. code:: bash

    git clone https://github.com/heilaaks/snippy.git
    mkvirtualenv snippy
    make devel

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

Apache Bench
------------

.. code:: bash

    # Install testing tools.
    dnf install httpd-tools
    go get -u github.com/rakyll/hey
    
    # Generate TLS server certificates
    openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 356 -subj "/C=US/O=Snippy/CN=127.0.0.1"

    # Run HTTP server with sqlite backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy:latest --server-host 127.0.0.1:8080 --defaults
    ab -n 10000 -c 1 -k http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests


    Server Software:        gunicorn/19.9.0
    Server Hostname:        127.0.0.1
    Server Port:            8080

    Document Path:          /snippy/api/app/v1/snippets?limit=20
    Document Length:        31914 bytes

    Concurrency Level:      1
    Time taken for tests:   45.854 seconds
    Complete requests:      10000
    Failed requests:        0
    Keep-Alive requests:    0
    Total transferred:      320920000 bytes
    HTML transferred:       319140000 bytes
    Requests per second:    218.08 [#/sec] (mean)
    Time per request:       4.585 [ms] (mean)
    Time per request:       4.585 [ms] (mean, across all concurrent requests)
    Transfer rate:          6834.73 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     4    5   0.5      4      15
    Waiting:        4    5   0.5      4      15
    Total:          4    5   0.5      4      15
    WARNING: The median and mean for the processing time are not within a normal deviation
            These results are probably not that reliable.
    WARNING: The median and mean for the waiting time are not within a normal deviation
            These results are probably not that reliable.
    WARNING: The median and mean for the total time are not within a normal deviation
            These results are probably not that reliable.

    Percentage of the requests served within a certain time (ms)
      50%      4
      66%      4
      75%      4
      80%      4
      90%      5
      95%      5
      98%      6
      99%      7
     100%     15 (longest request)

    # Run HTTP server with sqlite backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy:latest --server-host 127.0.0.1:8080 --defaults
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20

    Summary:
      Total:        45.1121 secs
      Slowest:      0.0142 secs
      Fastest:      0.0044 secs
      Average:      0.0045 secs
      Requests/sec: 221.6700

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.004 [1]     |
      0.005 [9974]  |
      0.006 [6]     |
      0.007 [6]     |
      0.008 [3]     |
      0.009 [3]     |
      0.010 [4]     |
      0.011 [2]     |
      0.012 [0]     |
      0.013 [0]     |
      0.014 [1]     |


    Latency distribution:
      10% in 0.0045 secs
      25% in 0.0045 secs
      50% in 0.0045 secs
      75% in 0.0045 secs
      90% in 0.0046 secs
      95% in 0.0046 secs
      99% in 0.0048 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0044 secs, 0.0142 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0044 secs, 0.0043 secs, 0.0140 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0004 secs

    Status code distribution:
      [200] 10000 responses

    # Run HTTPS server with sqlite backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    python runner --server-host 127.0.0.1:8080 --server-ssl-cert ./server.crt --server-ssl-key ./server.key --defaults
    /root/go/bin/hey -n 10000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20

    Summary:
      Total:        90.7888 secs
      Slowest:      0.0161 secs
      Fastest:      0.0088 secs
      Average:      0.0091 secs
      Requests/sec: 110.1457

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.009 [1]     |
      0.010 [9856]  |
      0.010 [107]   |
      0.011 [9]     |
      0.012 [5]     |
      0.012 [5]     |
      0.013 [3]     |
      0.014 [1]     |
      0.015 [8]     |
      0.015 [1]     |
      0.016 [4]     |


    Latency distribution:
      10% in 0.0090 secs
      25% in 0.0090 secs
      50% in 0.0090 secs
      75% in 0.0091 secs
      90% in 0.0092 secs
      95% in 0.0093 secs
      99% in 0.0097 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0052 secs, 0.0088 secs, 0.0161 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0038 secs, 0.0037 secs, 0.0106 secs
      resp read:    0.0001 secs, 0.0001 secs, 0.0005 secs

    Status code distribution:
      [200] 10000 responses


    # Run HTTP server with PostgreSQL backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --storage-type postgresql --storage-host localhost:5432 --storage-database postgres --storage-user postgres --storage-password postgres --defaults
    ab -n 10000 -c 1 -k http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests


    Server Software:        gunicorn/19.9.0
    Server Hostname:        127.0.0.1
    Server Port:            8080

    Document Path:          /snippy/api/app/v1/snippets?limit=20
    Document Length:        31914 bytes

    Concurrency Level:      1
    Time taken for tests:   52.412 seconds
    Complete requests:      10000
    Failed requests:        0
    Keep-Alive requests:    0
    Total transferred:      320920000 bytes
    HTML transferred:       319140000 bytes
    Requests per second:    190.80 [#/sec] (mean)
    Time per request:       5.241 [ms] (mean)
    Time per request:       5.241 [ms] (mean, across all concurrent requests)
    Transfer rate:          5979.51 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     5    5   0.4      5      21
    Waiting:        5    5   0.4      5      21
    Total:          5    5   0.4      5      21

    Percentage of the requests served within a certain time (ms)
      50%      5
      66%      5
      75%      5
      80%      5
      90%      5
      95%      5
      98%      6
      99%      7
     100%     21 (longest request)

    # Run HTTP server with PostgreSQL backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --storage-type postgresql --storage-host localhost:5432 --storage-database postgres --storage-user postgres --storage-password postgres --defaults
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20

    Summary:
      Total:        52.7001 secs
      Slowest:      0.0211 secs
      Fastest:      0.0050 secs
      Average:      0.0053 secs
      Requests/sec: 189.7530

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.005 [1]     |
      0.007 [9968]  |
      0.008 [9]     |
      0.010 [6]     |
      0.011 [8]     |
      0.013 [0]     |
      0.015 [1]     |
      0.016 [1]     |
      0.018 [1]     |
      0.020 [3]     |
      0.021 [2]     |


    Latency distribution:
      10% in 0.0051 secs
      25% in 0.0052 secs
      50% in 0.0053 secs
      75% in 0.0053 secs
      90% in 0.0054 secs
      95% in 0.0054 secs
      99% in 0.0058 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0050 secs, 0.0211 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0051 secs, 0.0048 secs, 0.0209 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0003 secs

    Status code distribution:
      [200] 10000 responses

    # HTTP server with PyPy and Sqlite as storage backed (comment psycopg2 out from setup)
    sudo pypy -m pip install --editable .[devel]
    pypy runner --server-host 127.0.0.1:8080 --defaults
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    
    Summary:
      Total:        21.4936 secs
      Slowest:      0.0139 secs
      Fastest:      0.0017 secs
      Average:      0.0021 secs
      Requests/sec: 465.2553
      
      Total data:   319140000 bytes
      Size/request: 31914 bytes
    
    Response time histogram:
      0.002 [1]     |
      0.003 [9489]  |
      0.004 [204]   |
      0.005 [77]    |
      0.007 [1]     |
      0.008 [146]   |
      0.009 [77]    |
      0.010 [2]     |
      0.011 [2]     |
      0.013 [0]     |
      0.014 [1]     |
    
    
    Latency distribution:
      10% in 0.0018 secs
      25% in 0.0019 secs
      50% in 0.0020 secs
      75% in 0.0020 secs
      90% in 0.0021 secs
      95% in 0.0029 secs
      99% in 0.0071 secs
    
    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0017 secs, 0.0139 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0020 secs, 0.0016 secs, 0.0127 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0004 secs
    
    Status code distribution:
      [200] 10000 responses

    # HTTPS server with PyPy and Sqlite as storage backed (comment psycopg2 out from setup)
    pypy runner --server-host 127.0.0.1:8080 --server-ssl-cert ./server.crt --server-ssl-key ./server.key --defaults
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    /root/go/bin/hey -n 10000 -c 1 https://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=20
    
    Summary:
      Total:        108.0445 secs
      Slowest:      0.0409 secs
      Fastest:      0.0075 secs
      Average:      0.0108 secs
      Requests/sec: 92.5545
      
      Total data:   319140000 bytes
      Size/request: 31914 bytes
    
    Response time histogram:
      0.008 [1]     |
      0.011 [7368]  |
      0.014 [513]   |
      0.018 [721]   |
      0.021 [8]     |
      0.024 [1377]  |
      0.028 [9]     |
      0.031 [1]     |
      0.034 [0]     |
      0.038 [1]     |
      0.041 [1]     |
    
    
    Latency distribution:
      10% in 0.0078 secs
      25% in 0.0079 secs
      50% in 0.0081 secs
      75% in 0.0138 secs
      90% in 0.0215 secs
      95% in 0.0217 secs
      99% in 0.0226 secs
    
    Details (average, fastest, slowest):
      DNS+dialup:   0.0067 secs, 0.0075 secs, 0.0409 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0039 secs, 0.0021 secs, 0.0180 secs
      resp read:    0.0001 secs, 0.0001 secs, 0.0007 secs
    
    Status code distribution:
      [200] 10000 responses



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
