Development
===========

Installation
------------

The instructions are tested with Fedora 30 and Bash shell. There are also
draft installation instructions for other Linux distributions and Windows.

.. note::

   The instructions install virtual environments with ``python3`` and add
   the Python 3 virtual environment modules to Python user script directory.
   This allows for example creating own Linux user for Snippy development
   which has an isolated virtual environment setup from global Python modules.

   In case you want different virtual environment setup, you have to modify
   the examples.

   The virtual environments are installed under ``${HOME}/.cache/snippy``.

.. note::

   The installation instructions add new software packages. Execute at your
   own risk.

.. note::

   The PostgreSQL adapters used with the server are installed by compiling
   them with the help of pip. This require working GCC toolchain. The GCC
   setup and configuration is not part of the Snippy documentation.

.. note::

   Install docker-ce to be able to run test with read container. Make sure
   that the user who runs the Snippy tests is able to run docker commands.

Fedora
~~~~~~

Follow the instructions to install the project on a Fedora Linux.

.. code:: bash

    # Clone the project from the GitHub.
    mkdir -p ${HOME}/.cache/snippy
    mkdir -p ${HOME}/.local/share/snippy
    mkdir -p ${HOME}/devel/snippy && cd $_
    git clone https://github.com/heilaaks/snippy.git .

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

    # Upgrade CPython versions.
    sudo dnf upgrade -y \
        python27 \
        python34 \
        python35 \
        python36 \
        python37 \
        python38 \
        python3-devel \
        python2-devel

    # Install PyPy versions.
    sudo dnf install -y \
        pypy2 \
        pypy3 \
        pypy2-devel \
        pypy3-devel \
        postgresql-devel

    # Upgrade PyPy versions.
    sudo dnf upgrade -y \
        pypy2 \
        pypy3 \
        pypy2-devel \
        pypy3-devel \
        postgresql-devel

    # Below are 'generic instructions' that can be used also with other
    # Linux distributions.

    # Install Python virtual environments.
    pip3 install --user --upgrade \
        pipenv \
        virtualenv \
        virtualenvwrapper

    # Enable virtualenvwrapper and add the Python user script directory
    # to the path if needed.
    vi ~/.bashrc
        # Snippy development settings.
        [[ ":$PATH:" != *"${HOME}/.local/bin"* ]] && PATH="${PATH}:${HOME}/.local/bin"
        export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
        export VIRTUALENVWRAPPER_VIRTUALENV=${HOME}/.local/bin/virtualenv
        export WORKON_HOME=${HOME}/.cache/snippy/.virtualenvs
        source virtualenvwrapper.sh
        cd ${HOME}/devel/snippy
        workon snippy-python3.7
    source ~/.bashrc

    # Create virtual environments.
    for PYTHON in python2.7 \
                  python3.4 \
                  python3.5 \
                  python3.6 \
                  python3.7 \
                  python3.8 \
                  pypy \
                  pypy3
    do
        if which ${PYTHON} > /dev/null 2>&1; then
            printf "create snippy venv for ${PYTHON}\033[37G: "
            mkvirtualenv --python $(which ${PYTHON}) snippy-${PYTHON} > /dev/null 2>&1
            if [[ -n "${VIRTUAL_ENV}" ]]; then
                printf "\033[32mOK\033[0m\n"
            else
                printf "\e[31mNOK\033[0m\n"
            fi
            deactivate > /dev/null 2>&1
        fi
    done

    # Install virtual environments.
    for VENV in $(lsvirtualenv -b | grep snippy-py)
    do
        workon ${VENV}
        printf "deploy snippy venv ${VENV}\033[37G: "
        if [ $(echo ${VENV} | cut -d"-" -f2) == $(readlink $(which python)) ]; then
            make upgrade-wheel
            make install-devel
            printf "\033[32mOK\033[0m\n"
        else
            printf "\e[31mNOK\033[0m\n"
        fi
        deactivate > /dev/null 2>&1
    done

    # Example how to delete Snippy virtual environments.
    deactivate > /dev/null 2>&1
    for VENV in $(lsvirtualenv -b | grep snippy-py)
    do
        printf "delete snippy venv ${VENV}\033[37G: "
        rmvirtualenv ${VENV} > /dev/null 2>&1
        printf "\033[32mOK\033[0m\n"
    done

Ubuntu
~~~~~~

Follow the instructions to install the project on a Ubuntu Linux.

.. code:: bash

    # Clone the project from the GitHub.
    mkdir -p ~/devel/snippy && cd $_
    git clone https://github.com/heilaaks/snippy.git .

    # Install CPython versions.
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo add-apt-repository ppa:pypy/ppa -y
    sudo apt-get install -y \
        python2.7  \
        python3.4 \
        python3.5 \
        python3.6 \
        python3.7 \
        python2.7-dev \
        python3.4-dev \
        python3.5-dev \
        python3.6-dev \
        python3.7-dev \
        python3.8-dev

    # Install PyPy versions.
    sudo apt-get install -y \
        pypy \
        pypy3 \
        pypy-dev \
        pypy3-dev \
        libpq-dev \

    # Install required Python packages.
    sudo apt-get install python3-pip -y
    sudo apt-get install python3-distutils -y

    # Follow the 'generic instructions' for the Snippy virtual environment
    # installation from the Fedora chapter.

Debian
~~~~~~

Follow the instructions to install the project on a Debian Linux.

.. code:: bash

    # Clone the project from the GitHub.
    mkdir -p ~/devel/snippy && cd $_
    git clone https://github.com/heilaaks/snippy.git .

    # Install Python virtual environments.
    sudo apt-get install python3-pip -y
    sudo apt-get install python3-distutils -y
    pip3 install --user \
        pipenv \
        virtualenv \
        virtualenvwrapper
    export PATH=${PATH}:~/.local/bin

    # Follow the 'generic instructions' for the Snippy virtual environment
    # installation from the Fedora chapter.

    # Install CPython versions.
    mkdir -p ~/devel/compile && cd $_
    apt-get install sudo -y
    sudo apt-get install -y \
        zlib1g-dev
    wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
    tar xvf Python-3.6.8.tgz
    /configure --enable-optimizations
    make -j8
    sudo make altinstall

RHEL
~~~~

Follow the instructions to install the project on a RHEL Linux.

.. code:: bash

    # Clone the project from the GitHub.
    mkdir -p ~/devel/snippy && cd $_
    git clone https://github.com/heilaaks/snippy.git .

    # Install Python virtual environments.
    yum install python-pip -y
    pip install --user \
        pipenv \
        virtualenv \
        virtualenvwrapper
    export PATH=${PATH}:~/.local/bin

    # Follow the 'generic instructions' for the Snippy virtual environment
    # installation from the Fedora chapter.

Windows
~~~~~~~

Follow the instructions to install the project on a Windows.

.. code:: bash

   # Install make and Python.
   choco install make python

   # Clone and install manually.
   git config --global http.proxy http://<proxy>:8080
   git clone https://github.com/heilaaks/snippy.git .
   python -m pip install pip setuptools wheel twine --upgrade --proxy <proxy>:8080
   python -m pip install .[devel] --proxy <proxy>:8080
   python -m pip install pipenv --proxy <proxy>:8080
   pipenv shell
   pipenv lock -r --dev > requirements-dev.txt
   pip install setuptools-scm --proxy <proxy>:8080
   pip install -r requirements-dev.txt --proxy <proxy>:8080

Workflows
---------

Testing
~~~~~~~

After virtual environments and the Docker CE have been installed succesfully,
build the Snippy container image and run the PostgreSQL database container.
The PostgreSQL database is one of the supported databases and tests are run
with it.

The local PostgreSQL username and passwords are synchronized with the Travis
CI PostgreSQL service. The default user is ``postgres`` and the password is
an empty string.

.. code:: bash

    # Compile Docker image for the 'test-docker' make target.
    make docker

    # Start PostgreSQL in a container.
    sudo docker run -d --name postgres -e POSTGRES_PASSWORD= -p 5432:5432 -d postgres

For the Snippy development, prefer a virtual environment with the latest
Python release and Python 2.7. The continuous integration will run all
the tests against all supported Python versions. Most of the problems can
be captured before committing by running the tests with the latest Python 3
release and with the Python 2.7.

.. code:: bash

    # Work in a Python virtual environment.
    workon snippy-python3.7

The Snippy continuous integration will run all tests with the default SQLite,
PostgreSQL and in-memory databases with the exception of the tests with a real
server or with a docker container. It is recomended to run ``make test-server``
and ``make test-docker`` manually until these tests are included also into the
continuous integration tests.

.. code:: bash

    # Run the default development tests. This does not include real server, real
    # docker container or tests with other than SQLite database.
    make test

    # Run all tests against PostgreSQL.
    make test-postgresql

    # Run all tests against in-memory database.
    make test-in-memory

    # Run all tests with a real server started on the same host.
    make test-server

    # Run all tests with a Docker container.
    make test-docker

    # Run tests against all supported Python versions.
    make test-tox

    # Run all tests.
    make test-all

    # Run test coverage.
    make coverage

    # Open coverage report in a web browser.
    file:///<home>/devel/snippy/htmlcov/index.html

    # Run lint.
    make lint

    # Clean all generated files with the exception of SQLite database file.
    make clean

    # Clean only the SQLite database file.
    make clean-db

    # Clean all generated files including the SQLite database file.
    make clean-all

    # Run a test with debug logs enabled.
    pytest tests/test_api_create_snippet.py -k 001 -s --snippy-logs

    # Run a test with PostgreSQL database.
    pytest tests/test_api_create_snippet.py -k 001 -s --snippy-db postgresql

    # Run a test with in-memory database.
    pytest tests/test_api_create_snippet.py -k 001 -s --snippy-db in-memory

Documentation
~~~~~~~~~~~~~

The documentation includes manual and automated documentation. Automated
documentation is extracted from source code docstrings and from the Swagger
definitions in the ``swagger-2.0.yml`` file.

.. code:: bash

    # Create documents.
    make docs

    # Open the document in a web brower.
    file:///<home>/devel/snippy/docs/build/html/development.html#documentation

Shell completions
~~~~~~~~~~~~~~~~~

Shell completion testing is done by manually testing the commands. Install
the Snippy tool and Bash completion scripts with the below examples.

.. code:: bash

    # Install and upgrade Snippy.
    make install

    # Install the Bash completion.
    python runner export --complete bash
    sudo cp snippy.bash-completion /etc/bash_completion.d/snippy.bash-completion
    exec bash

API design
~~~~~~~~~~

The Swagger editor is used to update the Snippy REST API design. Run the
Swagger editor in a container and update the ``swagger-2.0.yml`` design.
The Swagger version 2 is the baseline for the design because it still has
wider support in open source tools than version 3. The ``swagger-3.0.yml``
file is always generated with the Swagger editor from the ``swagger-2.0.yml``.

Snippy uses JSON schemas generated from the ``swagger-2.0.yml``. The generated
JSON schemas are used in Snippy server to validate HTTP requests and in tests
to validate the Snippy server HTTP responses.

If the JSON schema filenames are changed or new files are generated, the code
and tests using the JSON schema files must be updated. Note that only some of
the generated files are used in the JSON schema validation. The Snippy server
needs only the JSON schema files that define the HTTP methods received by the
server and tests need only JSON schema files that are used to define the HTTP
responses.

.. code:: bash

    # Start the Swagger editor.
    docker run -d -p 9000:8080 --name swagger-editor swaggerapi/swagger-editor

    # Edit the swagger-2.0.yml with the Swagger editor GUI in a web browser.
    http://localhost:9000

    # Convert the API design to OpenAPI version 3 with the Swagger editor
    # and save the changes to the swagger-3.0.yml.
    Edit - Convert to OpenAPI 3

    # Create JSON API schema.
    make jsonschema

    # Run tests with the updated JSON schema.
    make test

Terms
-----

==================  ============================================================================================
Term                Decscription
==================  ============================================================================================
*attribute*         |  Content attribute like ``brief``, ``links`` or ``tags``.

*category*          |  Content category that is one of ``snippet``, ``solution`` or ``reference``. This can also
                    |  refer to a field category ``groups`` or ``tags``.

*collection*        |  Collection is a set of resources objects.

*content*           |  Content is a software development note from one of the categories. A content is
                    |  stored into a resource object. In a broader view content, resource and a note can
                    |  be interpreted to have a same meaning.

*field*             |  Same as attribute. It is recommended to use the term ``attribute`` because it
                    |  refers to a commonly used term in REST API design.

*operation*         |  Command line operation like ``create`` or ``delete``. This term refers also to a HTTP
                    |  request in case of the REST API server. This term also refers to processing of
                    |  operation from start to an end.

*operation ID*      |  Unique operation identifier (OID) allocated for all log messages generation from a
                    |  single operation.

*resource*          |  Resource is an object that can store a single content from any of the categories.

*parameter*         |  An URL parameter that defines for example a search criteria like ``sall`` or ``scat`` for a
                    |  HTTP request.
==================  ============================================================================================

Guidelines
----------

Commit logs
~~~~~~~~~~~

Git commit logs must follow rules from `Chris Beams`_ with explicit change
types listed below. The change types are derived from a `keep a changelog`_
and a post in `Writing for Developers`_

1. `Add` new external features.
2. `Change` external behavior in existing functionality.
3. `Fix` bugs. Use 'Edit' for typo and layout corrections.
4. `Remove` external feature.
5. `Deprecat` a soon-to-be removed features.
6. `Security` in case of vulnerabilities.
7. `Refactor` code without external changes.
8. `Edit` small fixes like typo and layout fixes.
9. `Test` new test cases.

The rule must be applied so that the logs are written for humans. This
means that the commit log must tell the reasons and design decisions
behind the change.

This rule tries also encourage a common look and feel for commit logs.

.. _Chris Beams: https://chris.beams.io/posts/git-commit/
.. _keep a changelog: http://keepachangelog.com/en/1.0.0/
.. _Writing for Developers : https://writingfordevelopers.substack.com/p/how-to-write-commit-messages

Design
------

REST API
~~~~~~~~

The rest API follows `JSON API specification`_ version 1.1. The PATCH method
works as defined in the `RFC 7386 - JSON Merge Patch`_.

.. _JSON API specification: https://jsonapi.org/format/1.1/
.. _RFC 7386 - JSON Merge Patch: https://tools.ietf.org/html/rfc7386

Resource attributes
~~~~~~~~~~~~~~~~~~~

*Category*

The ``category`` is defined when the resource is created. After this, it cannot
be changed by updating it. The only way to change this attribute is to delete
and create the resource again.

*Data*

The ``data`` attribute contains the actual content. This is a mandatory field
for the ``snippets`` and ``solutions`` contents. Because the ``references`` are
links, they do not store the information into the  ``data`` attribute but into
the ``links`` attribute.

*Brief*

The ``brief`` is an optional attribute. It is a one-liner that describes the
content very briefly.

*Description*

The ``description`` is an optional attribute. This is a longer explanation that
provides more details than the ``brief`` attribute.

*Name*

The ``name`` is an optional attribute. This field is intended to work as a short
name for the content. The intention is that this attribute could be used to refer
and run for example a snippet content. The field does not have restrictions on
characters but it should not contain whitespaces to allow to use it as a target
or a name for an action.

*Groups*

The ``groups`` is an optional attribute. This field can store multiple values.
The desing and usage is left to user how the groups are defined. The field does
not have restrictions on characters but it is recommended that a group does not
contain whitespaces.

*Tags*

The ``tags`` is an optional attribute. This field can store multiple values.
The desing and usage is left to user how the tags are defined. The field does
not have restrictions on characters but it is recommended that a group does not
contain whitespaces.

*Links*

The ``links`` is a mandatory attribute for ``references`` content. For ``snippets``
and ``solutions`` the field is optional. This field can store multiple values.
The desing and usage is left to user how the fields are defined. The field is
intended to store HTTP links. There is nothing that prevents storing for example
file URI references.

*Source*

The ``source`` is an optional attribute. This field can store one value. The
field is designed to contain a link to a source where the content was imported.
For example the default content in snippet can set the ``source`` field to
value ``https://github.com/heilaaks/snippy``.

*Versions*

The ``versions`` is an optional attribute. This field can store multiple values.
This field is designed to contain information related to software versions used
in the content. For example commands may change between software versions. This
fields tries to track version information of the content. The field accepts only
key-value pairs with mathematical operators ``>=``, ``<=``, ``!=``, ``==``, '>``,
'<`` or ``~``. For example ``python>=3.7`` is a valid value for the field.

*Languages*

The ``languages`` is an optional attribute. This field can store multiple values.
The field is intended to store programming languages related to the content.

*Filename*

The ``filename`` is an optional attribute. This field can store one values. The
field is intended to store filenames like ``how-to-debug-nging.md``. This field
can be used for example to automatically define the exported filename and format.

*Created*

The created timestamp is set when the resource is created and it cannot be
modified. The only way to change this attribute is to delete and create the
resource again.

*Updated*

The updated timestamp is set when the resource is updated and it cannot be
modified.

*Uuid*

The UUID attribute is intended to be externally visible UUID attribute that
is exposed outside the REST API server. The UUID is allocated always for the
resource and it never changes. In order to allocate one static identifier for
each resource, an UUID4 formatted ID attribute is used.

There is always a change of an `UUID4 collitions`_ if multiple servers are run
but it is considered so small that it does not matter.

.. _UUID4 collitions: https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)

*Digest*

The digest attribute is always set by the tool based on sha256 hash algorithm.
The digest is automatically updated when resource attributes are updated.

Updating
~~~~~~~~

Following attributes can be freely modified by user within the limits of
attribute definitions.

- data
- brief
- description
- name
- group
- tags
- links
- source
- versions
- languages
- filename

Attributes that cannot be changed by user are:

- category
- created
- updated
- uuid
- digest

Error handling
~~~~~~~~~~~~~~

Operations will flow from the beginning to an end. There are no intermediate
exists or shortcuts. The error handling must be made simple in order to keep
the implementation size and testing effort in control. The target is not to
try to recover all possible errors but to fail operation as soon as the first
failure is detected by setting an error cause.

For example if the search category ``--scat`` option has multiple categories
and one of them is faulty, the ``--scat`` option will be invalidated. This
will not generate any search hits and it will minimize the database queries.

The REST API must invalidate the HTTP request if any of the attributes or
parameters is incorrect. That is, the REST API must not store valid values
of for attributes and silently set faulty attributes to a default values.

Testing
-------

Security
--------

Documentation
-------------

Docstrings
~~~~~~~~~~

Use the `Google docstring`_ format. It is considered less verbose and more
readable than the NumPy formatted docstring. In this project the intention
is that a method description explains the complicated parts and the method
argument is a short explanation of the method arguments. The NumPy format
is better suited for complex algorithms and their parameters.

.. _Google docstring: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Test cases
~~~~~~~~~~

Each test cases must have a docstring that defines the purpose of the test.
The test case docstring must have a one liner brief description and empty
line after the brief. The description part of the test case docstring can
be freely formatted.

.. code-block:: python

  @staticmethod
  @pytest.mark.usefixtures('default-snippets')
  def test_cli_search_snippet_001(snippy, capsys):
     """Search snippets with ``--sall`` option.

     Search snippets from all resource attributes. A ``brief`` attribute
     of a single snippet produces a match.
     """

Heroku app
----------

Use the examples below to deploy a Heroky Application.

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
