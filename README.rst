|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-docs| |badge-build| |badge-pyup|

Features
========

Manage command snippets, solution examples and reference links from console
or REST API server. The tool is designed to support software development and
troubleshooting workflows by collecting command examples, troubleshooting
solutions and links into one content manager. The tool may be helpful for
example when working with different open source components that all have
different configuration settings and troubleshooting methods. You can share
the best examples in Markdown format or through common data serialization
languages YAML or JSON or from a REST API server.

Content is divided into three categories called snippets, solutions and
references. Snippets are short command examples. Solutions are longer
solution descriptions and references are links to important web pages and
resources. You can combine metadata like tags, group or links with the
content in order to help searching and tracking stored content.

You can operate all content directly from command line with six operations:
create, search, update, delete, import and export. These operations manage
the content in persistent file storage installed into the same location as
the tool.

You can operate all content from `RESTish JSON API`_. server. The API follows
a subset of the `JSON API V1.0`_ specification. The tool must be installed
from Docker Hub or from the github repository if server functionality is
required. The server functionality is not currently available when installed
directly from PyPI.

.. image:: https://asciinema.org/a/Mcg6d2d6R9V5cScoW6nsGtzZ7.png
    :target: https://asciinema.org/a/Mcg6d2d6R9V5cScoW6nsGtzZ7
    :alt: Snippy in action!

Installation
============

To install, run:

.. code:: text

    pip install snippy --user

To remove, run:

.. code:: text

    pip uninstall --yes snippy

To install from Docker Hub, run:

.. code:: text

    docker pull docker.io/heilaaks/snippy

To install from Github, run:

.. code-block:: text

    git clone https://github.com/heilaaks/snippy.git
    cd snippy
    make install

Usage
=====

Snippy command line commands always include content operation and category.
The content operation is one of the six basic operations and the category is
either snippet, solution or reference. The content category is snippet by
default. Metadata attached to the content allows adding brief description of
the content, single group to which the content belongs, list of tags to
assist search operations and a list of links for more information about the
content.

Snippy tool outputs always OK after successful operation and NOK with a failure
string in case of failure. You can use debug option with the command to
investigate possible problems. For more detailed troubleshooting instructions,
please refer to the `contributing instructions`_.

The workflow section below contains the basic use cases for command line
interface. You can read more detailed documentation from the documentation
hosted by the `Read the Docs`_.

.. note::

   The tool is used by the author in Linux environment. There is an edit
   functionality with editor that always assumes vi editor. This limitation
   can be circumvented by using text based templates to import content or
   command line options in case of snippets.

.. note::

   The default content is provided "as is" basis without warranties of any
   kind.

Workflows
=========

Printing help and examples
--------------------------

Use help option with keyword examples to read about basic usage.

.. code-block:: text

   snippy --help
   snippy --help examples

Importing default content
-------------------------

Snippy instals by default without content. Following examples allow importing
default content for snippets and solutions.

.. code-block:: text

   snippy import --snippets --defaults
   snippy import --solutions --defaults
   snippy import --references --defaults

It is possible to import the default content also with one command.

.. code-block:: text

   snippy import --defaults --all

Using docker container
----------------------

Snippy tool is available also from Docker container. In this case the default
content is already imported. How ever, the content cannot be changed because
the container is immuateble and the content is not mapped from any volume from
the host machine. Exactly same commands work with container version than the
command line version.

.. code-block:: text

   docker run docker.io/heilaaks/snippy --help
   docker run docker.io/heilaaks/snippy search --sall docker

Searching content
-----------------

Printing all content to console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to print all snippets and solutions to console by using a dot
in the search query. The only special character passed to the query is dot
which matches to to any character.

.. code-block:: text

   snippy search --sall .
   snippy search --solutions --sall .

Filtering with grep
~~~~~~~~~~~~~~~~~~~

With Linux grep it is possible to filter for example only the actual commands
from the search query.

.. code-block:: text

   snippy search --sall . --no-ansi | grep '\$'
   snippy search --sgrp docker --no-ansi | grep '\$'

Filtering out solution content to list only the metadata.

.. code-block:: text

   snippy search --solutions --sall . | grep -Ev '[^\s]+:'

Creating content
----------------

Create snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command uses vi editor to create new content. The command opens an
input template where you can define the mandatory snippet and optional brief
description, group, tags and links related to the snippet.

.. code-block:: text

   snippy create --snippets --editor

Create snippet from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new snippet.

.. code-block:: text

   snippy export --snippets --template
   snippy import --snippets -f snippet-template.txt

Create solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new solution.

.. code-block:: text

   snippy export --solutions --template
   snippy import --snippets -f solution-template.txt

Updating content
----------------

Update snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command allows updating existing snippet with vi editor. The command
will launch a vi editor which allows you to modify the content. The content is
updated automatically after the file is saved and editor is exit.

.. code-block:: text

   snippy update --digest 54e41e9b52a02b63

Update solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allow updating existing solution by exporting the content
to text file and importing it again.

.. code-block:: text

   snippy export --digest 76a1a02951f6bcb4
   snippy import --digest 76a1a02951f6bcb4 --file howto-debug-elastic-beats.txt

Migrating content
-----------------

Exporting content
~~~~~~~~~~~~~~~~~

Following commands allow exporting all snippets and solutions to YAML file that
you use to back-up your data. The commands below will create snippets.yaml and
solutions.yaml files into same directory where the command was executed. You can
define the file name and path with the ``-f|--file`` option.

.. code-block:: text

   snippy export --snippets
   snippy export --snippets -f my-snippets.yaml
   snippy export --solutions
   snippy export --solutions -f my-solutions.yaml

Importing content
~~~~~~~~~~~~~~~~~

Following commands allow importing snippets and solutions from default YAML files
named snippets.yaml and solutions.yaml that must be located in the same directory
where the command is executed. You can define the file name and path with the
``-f|--file`` option.

.. code-block:: text

   snippy import --snippets
   snippy import --solutions

Server
======

The JSON REST API server is available when the tool is installed from Docker
Hub or directly from the source code. The API is experimental and changes can
be expected. The API is documented in Swagger Hub `OpenAPI definitions`_.

.. code-block:: text

   sudo docker run -d --net="host" --name snippy docker.io/heilaaks/snippy --server-host 127.0.0.1:8080 --log-json -vv
   curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=2" -H "accept: application/vnd.api+json"
   curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"

You can see the logs from the server from the default Docker log. If you do
not want to read JSON logs, remove the ``--log-json`` parameter from the
server startup optons. You can remove all the logs by removing the ``-vv``
option. Remember to remove the stopped container before starting it with new
perameters.

.. code-block:: text

   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy docker.io/heilaaks/snippy --server-host 127.0.0.1:8080 -vv
   docker logs snippy

You can remove the server with command example.

.. code-block:: text

   docker rm -f snippy

Note that Docker container is immutable and it does not share volume from the
host. If you want to run a server that allows content modification, you must
install the server from code repository.

.. code-block:: text

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make server

With a local server, you can change to location of the storage from the
default. If the default content is needed, you need to import it into the new
location before starting the server.

.. code-block:: text

   snippy import --defaults --storage-path ${HOME}/devel/temp
   snippy import --defaults --solutions --storage-path ${HOME}/devel/temp
   snippy --server-host 127.0.0.1:8080 --storage-path ${HOME}/devel/temp -vv

Contributing
============

Bug reports and feature Requests
--------------------------------

Run the failing command with ``--debug`` option to get a better idea what is failing. Please
fill a bug report based on contributing_ instructions.


.. |badge-pypiv| image:: https://img.shields.io/pypi/v/snippy.svg
   :target: https://pypi.python.org/pypi/snippy

.. |badge-pys| image:: https://img.shields.io/pypi/status/snippy.svg
   :target: https://pypi.python.org/pypi/snippy

.. |badge-pyv| image:: https://img.shields.io/pypi/pyversions/snippy.svg
   :target: https://pypi.python.org/pypi/snippy

.. |badge-cov| image:: https://codecov.io/gh/heilaaks/snippy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/heilaaks/snippy

.. |badge-docs| image:: https://readthedocs.org/projects/snippy/badge/?version=latest
   :target: http://snippy.readthedocs.io/en/latest/?badge=latest

.. |badge-build| image:: https://travis-ci.org/heilaaks/snippy.svg?branch=master
   :target: https://travis-ci.org/heilaaks/snippy

.. |badge-pyup| image:: https://pyup.io/repos/github/heilaaks/snippy/shield.svg
   :target: https://pyup.io/repos/github/heilaaks/snippy/

.. _Read the Docs: http://snippy.readthedocs.io/en/latest/

.. _contributing instructions: https://github.com/heilaaks/snippy/blob/master/CONTRIBUTING.rst

.. _RESTish JSON API: https://app.swaggerhub.com/apis/heilaaks/snippy/1.0

.. _OpenAPI definitions: `RESTish JSON API`_

.. _JSON API V1.0: http://jsonapi.org/format/
