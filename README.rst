|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-docs| |badge-health|

Features
========

Manage command snippets and solution examples directly from console. The tool is designed
to support software development and troubleshooting workflows by collecting frequently used
command examples and troubleshooting solutions into one manager.

Content is divided to two categories called snippets and solutions. Snippets are short
command examples and solutions longer solution descriptions. You can combine links and
metadata with the content in order to help searching specific content.

You can operate snippet or solution content with six basic operations: create, search,
update, delete, import and export.

Installation
============

Installaltion from PyPI.

.. code:: bash

    pip install snippy

Installing from Docker Hub.

.. code:: bash

    docker run heilaaks/snippy

Installing from repository

.. code:: bash

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make install
   snippy --help
   make uninstall

Usage
=====

Commands always include content operation and category. The content operation is one of
the six basic operation and the category is either snippet or solution. The content category
is snippet by default.

Symbols used in the tool ouput allow separating snippets ($), solutions (:), groups (@),
tags (#) and links (>).

The tool outputs always OK after successfull operation and NOK with failure string in case
of failure.

The tool is used by the author in Linux environment. There is an edit functionality with
editor that always assumes vi editor. This limitation can be circumvented by using text
based templates to import content or command line options in case of snippets.

The workflow section below contains the basic use cases. Please see more detailed
documentation from `Read the Docs`_.

Workflows
=========

Printing help and examples
--------------------------

Use help option with keyword examples to read about basic usage.

.. code:: bash

    snippy --help
    snippy --help examples

Importing default content
-------------------------

Snippy instals by default without content. Following examples allow importing default
content for snippets and solutions.

.. code:: bash

    snippy import --snippet --defaults
    snippy import --solution --defaults


Searching content
-----------------

Printing all content to console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to print all snippets and solutions to console by using a dot in the search
query. The only special character passed to the query is dot which matches to to any character.

.. code:: bash

    snippy search --sall .
    snippy search --solution --sall .

Filtering with grep
~~~~~~~~~~~~~~~~~~~

With Linux grep it is possible to filter for example only the actual commands from the search query.

.. code:: bash

    snippy search --sall . --no-ansi | grep '\$'
    snippy search --sgrp docker --no-ansi | grep '\$'

Filtering out solution content to list only the metadata.

.. code:: bash

    snippy search --solution --sall . | grep -Ev '[^\s]+:'

Creating content
----------------

Create snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command uses vi editor to create new content. The command opens an input template where
you can define the mandatory snippet and optional brief description, group, tags and links related
to the snippet.

.. code:: bash

    snippy create --snippet --editor

Create snippet from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new snippet.

.. code:: bash

    snippy export --snippet --template
    snippy import --snippet -f snippet-template.txt

Create solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new solution.

.. code:: bash

    snippy export --solution --template
    snippy import --snippet -f solution-template.txt

Updating content
----------------

Update solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows updating existing solution by exporting the content to text file and
importing it again.

.. code:: bash

    snippy search --solution --sall beats
    snippy export --digest 4b7ef784a57fcc72
    snippy import --digest 4b7ef784a57fcc72 --file howto-debug-elastic-beats.txt

Migrating content
-----------------

Exporting content
~~~~~~~~~~~~~~~~~

Following commands allows exporting all snippets and solutions to YAML file that you use to back-up
your data. The commands will create snippets.yaml and solutions.yaml file into same directory. You
can define the filename and path with --file option.

.. code:: bash

    snippy export --solution
    snippy export --snippet

Importing content
~~~~~~~~~~~~~~~~~

Following commands allow importing snippets and solutions from default YAML files named snippets.yaml
and solutions.yaml that must be located in the same directory where the command is given. You can
define the filename and path with --file option.

Contributing
============

Bug Reports and Feature Requests
--------------------------------

Run the failing command with --debug option to get a better idea what is failing. Bug reports are
wellcomed. Please fill bug report based on contributing_ guidelines.


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

.. |badge-health| image:: https://landscape.io/github/heilaaks/snippy/master/landscape.svg?style=flat
   :target: https://landscape.io/github/heilaaks/snippy/master

.. _Read the Docs: http://snippy.readthedocs.io/en/latest/

.. _contributing: https://github.com/heilaaks/snippy/blob/master/CONTRIBUTING.rst
