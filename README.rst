|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-health| |badge-codacy| |badge-docs| |badge-build|

Features
========

Manage command snippets and solution examples directly from console. The tool
is designed to support software development and troubleshooting workflows by
collecting command examples and troubleshooting solutions into one manager.
The tool may be helpful for example when working with different open source
components that all have different configuration settings and troubleshooting
methods. You can share the best examples through common data serialization
languages YAML or JSON.

Content is divided into two categories called snippets and solutions. Snippets
are short command examples and solutions are longer solution descriptions. You
can combine metadata like links and tags with the content in order to help
searching and tracking the content.

You can operate snippet or solution content with six basic operations: create,
search, update, delete, import and export. These operations manage the content
in persistent file storage installed into the same location as the tool.

There is also experimental `RESTish JSON API`_. The API follows
subset of `JSON API V1.0`_. Please note that the server must be installed from
the source code or run as a Docker continer from Docker Hub. The server is not
installed by default from PyPI.


.. raw:: html

   <a href="https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO"><img src="https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO.png"/></a>

Installation
============

Installing from PyPI.

.. code-block:: none

   pip install snippy

Installing from Docker Hub.

.. code-block:: none

   docker pull heilaaks/snippy

Installing from repository.

.. code-block:: none

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make install

Installing server from repository.

.. code-block:: none

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make server

Usage
=====

Snippy commands always include content operation and category. The content operation
is one of the six basic operations and the category is either snippet or solution.
The content category is snippet by default. Metadata attached to the content allows
adding brief description of the content, single group to which the content belongs,
list of tags to assist search operations and a list of links for more information
about the content.

Snippy tool outputs always OK after successful operation and NOK with a failure
string in case of failure. You can use debug option with the command to investigate
possible problems. For more detailed troubleshooting instructions, please refer
to the contributing_ instructions.

The workflow section below contains the basic use cases. Please see more detailed
documentation from `Read the Docs`_.

.. note::

   The tool is used by the author in Linux environment. There is an edit functionality
   with editor that always assumes vi editor. This limitation can be circumvented by
   using text based templates to import content or command line options in case of
   snippets.

.. note::

   The default content is provided "as is" basis without warranties of any kind.

Workflows
=========

Printing help and examples
--------------------------

Use help option with keyword examples to read about basic usage.

.. code-block:: none

   snippy --help
   snippy --help examples

Importing default content
-------------------------

Snippy instals by default without content. Following examples allow importing default
content for snippets and solutions.

.. code-block:: none

   snippy import --snippet --defaults
   snippy import --solution --defaults

Using docker container
----------------------

Snippy tool is available also from Docker container. In this case the default content
is already imported. How ever, the content cannot be changed because the container is
immuateble and the content is not mapped from any volume from the host machine. Exactly
same commands work with container version than the command line version.

.. code-block:: none

   docker run heilaaks/snippy --help
   docker run heilaaks/snippy search --sall docker

Searching content
-----------------

Printing all content to console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to print all snippets and solutions to console by using a dot in the
search query. The only special character passed to the query is dot which matches to
to any character.

.. code-block:: none

   snippy search --sall .
   snippy search --solution --sall .

Filtering with grep
~~~~~~~~~~~~~~~~~~~

With Linux grep it is possible to filter for example only the actual commands from the
search query.

.. code-block:: none

   snippy search --sall . --no-ansi | grep '\$'
   snippy search --sgrp docker --no-ansi | grep '\$'

Filtering out solution content to list only the metadata.

.. code-block:: none

   snippy search --solution --sall . | grep -Ev '[^\s]+:'

Creating content
----------------

Create snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command uses vi editor to create new content. The command opens an input template
where you can define the mandatory snippet and optional brief description, group, tags and
links related to the snippet.

.. code-block:: none

   snippy create --snippet --editor

Create snippet from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new snippet.

.. code-block:: none

   snippy export --snippet --template
   snippy import --snippet -f snippet-template.txt

Create solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new solution.

.. code-block:: none

   snippy export --solution --template
   snippy import --snippet -f solution-template.txt

Updating content
----------------

Update snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command allows updating existing snippet with vi editor. The command will
launch a vi editor which allows you to modify the content. The content is updated
automatically after the file is saved and editor is exit.

.. code-block:: none

   snippy update --digest 54e41e9b52a02b63

Update solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allow updating existing solution by exporting the content to text
file and importing it again.

.. code-block:: none

   snippy export --digest 76a1a02951f6bcb4
   snippy import --digest 76a1a02951f6bcb4 --file howto-debug-elastic-beats.txt

Migrating content
-----------------

Exporting content
~~~~~~~~~~~~~~~~~

Following commands allow exporting all snippets and solutions to YAML file that you use to
back-up your data. The commands below will create snippets.yaml and solutions.yaml files into
same directory where the command was executed. You can define the file name and path with the
``-f|--file`` option.

.. code-block:: none

   snippy export --snippet
   snippy export --snippet -f my-snippets.yaml
   snippy export --solution
   snippy export --solution -f my-solutions.yaml

Importing content
~~~~~~~~~~~~~~~~~

Following commands allow importing snippets and solutions from default YAML files named
snippets.yaml and solutions.yaml that must be located in the same directory where the command
is executed. You can define the file name and path with the ``-f|--file`` option.

.. code-block:: none

   snippy import --snippet
   snippy import --solution

Running as server
=================

The server can be installed currently from git repository or from Docker Hub. The experimental
API is defined as `OpenAPI definition`_.

.. code-block:: none

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make server

   snippy import --defaults
   snippy import --defaults --solution
   snippy --server -vv
   snippy --server --port 8080 --ip 127.0.0.1 -vv
   curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker&limit=2" -H "accept: application/json" | python -m json.tool

.. code-block:: none

   sudo docker run -d --net="host" heilaaks/snippy --server
   curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker&limit=2" -H "accept: application/json" | python -m json.tool

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

.. |badge-health| image:: https://landscape.io/github/heilaaks/snippy/master/landscape.svg?style=flat
   :target: https://landscape.io/github/heilaaks/snippy/master

.. |badge-codacy| image:: https://api.codacy.com/project/badge/Grade/170f2ea74ead4f23b574478000ef578a
   :target: https://www.codacy.com/app/heilaaks/snippy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=heilaaks/snippy&amp;utm_campaign=Badge_Grade

.. |badge-docs| image:: https://readthedocs.org/projects/snippy/badge/?version=latest
   :target: http://snippy.readthedocs.io/en/latest/?badge=latest

.. |badge-build| image:: https://travis-ci.org/heilaaks/snippy.svg?branch=master
   :target: https://travis-ci.org/heilaaks/snippy

.. _Read the Docs: http://snippy.readthedocs.io/en/latest/

.. _contributing: https://github.com/heilaaks/snippy/blob/master/CONTRIBUTING.rst

.. _asciinema: https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO

.. _RESTish JSON API: https://app.swaggerhub.com/apis/heilaaks/snippy/1.0

.. _OpenAPI definition: `RESTish JSON API`_

.. _JSON API V1.0: http://jsonapi.org/format/