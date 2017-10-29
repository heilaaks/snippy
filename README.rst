|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-docs| |badge-health|

Features
========

Manage command snippets and solution examples directly from console. The tool is designed
to support software development and troubleshooting workflows by collecting frequently
used command examples and troubleshooting solutions into one manager.

Content is divided to two categories called snippets and solutions. Snippets are short
command examples and solutions longer solution descriptions. You can combine for example
links and tags with the content in order to help searching and tracking the content.

You can operate snippet or solution content with six basic operations: create, search,
update, delete, import and export. These operations manage the content in persistent
storage installed into the same location as the tool.

.. raw:: html

<a href="https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO"><img src="https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO.png"/></a>

Installation
============

Installaltion from PyPI.

.. code-block:: none

    pip install snippy

Installing from Docker Hub.

.. code-block:: none

    docker run heilaaks/snippy

Installing from repository

.. code-block:: none

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make install
   snippy --help
   make uninstall

Usage
=====

Snippy commands always include content operation and category. The content operation is
one of the six basic operations and the category is either snippet or solution. The
content category is snippet by default. Metadata attached to the content allows adding
brief description of the content, single group to which the content belongs, list of
tags to assist search operations and a list of links for more information about the
content.

The search output allows identifying snippets ($), solutions (:), groups (@), tags (#)
and links (>). This allows easier post processing the content with Linux command line
tools.

Snippy tool outputs always OK after a successful operation and NOK with a failure
string in case of failure. You can use ``--debug`` option with the command to help
investigating problems. For more detailed troubleshooting instructions, please refer
to contributing_ instructions.

The workflow section below contains the basic use cases. Please see more detailed
documentation from `Read the Docs`_.

.. note::

    The tool is used by the author in Linux environment. There is an edit functionality
    with editor that always assumes vi editor. This limitation can be circumvented by
    using text based templates to import content or command line options in case of
    snippets.

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

    snippy export --digest 4b7ef784a57fcc72
    snippy import --digest 4b7ef784a57fcc72 --file howto-debug-elastic-beats.txt

Migrating content
-----------------

Exporting content
~~~~~~~~~~~~~~~~~

Following commands allow exporting all snippets and solutions to YAML file that you use to
back-up your data. The commands below will create snippets.yaml and solutions.yaml files into
same directory where the command was executed. You can define the file name and path with the
``-f|--file`` option.

.. code-block:: none

    snippy export --solution
    snippy export --snippet

Importing content
~~~~~~~~~~~~~~~~~

Following commands allow importing snippets and solutions from default YAML files named
snippets.yaml and solutions.yaml that must be located in the same directory where the command
is executed. You can define the file name and path with the ``-f|--file`` option.

.. code-block:: none

    snippy import --solution
    snippy import --snippet

Contributing
============

Bug Reports and Feature Requests
--------------------------------

Run the failing command with --debug option to get a better idea what is failing. Please
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

.. |badge-health| image:: https://landscape.io/github/heilaaks/snippy/master/landscape.svg?style=flat
   :target: https://landscape.io/github/heilaaks/snippy/master

.. _Read the Docs: http://snippy.readthedocs.io/en/latest/

.. _contributing: https://github.com/heilaaks/snippy/blob/master/CONTRIBUTING.rst

.. _asciinema: https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO
