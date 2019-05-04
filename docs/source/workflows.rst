Workflows
=========

Getting help
------------

Use help option with keyword examples to read about basic usage. Read the documentation
from `Read the Docs`_ or dive into the code in `Github`_.

.. code-block:: none

    snippy --help
    snippy --help examples

Creating content
----------------

Creating snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command uses vi editor to create new content. The command opens an input
template where you can define the mandatory snippet and optional brief description,
group, tags and links related to the snippet.

.. code-block:: none

    snippy create --scat snippet --editor

Creating snippet from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allows using a text template to import new snippet.

.. code-block:: none

    snippy export --scat snippet --template
    snippy import --scat snippet -f snippet-template.txt

Creating snippet from command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add new snippet directly from command line. How ever, easiest way to create new
content is to use editor.

.. code-block:: none

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    snippy create --content 'docker rm --volumes $(docker ps --all --quiet)' --brief 'Remove all docker containers with volumes' --group docker --tags docker-ce,docker,moby,container,cleanup --links 'https://docs.docker.com/engine/reference/commandline/rm/'

Creating solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    snippy export --scat solution --template
    snippy import --scat snippet -f solution-template.txt

Searching content
-----------------

Printing all examples on terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to list all snippets on screen by using dot as a search keyword.

.. code-block:: none

    snippy search --sall .
    OK

Filtering with grep
~~~~~~~~~~~~~~~~~~~

With Linux grep it is possible to filter for example only the actual commands from the
search query.

.. code-block:: none

    snippy search --sall . --no-ansi | grep '\$'
    snippy search --sgrp docker --no-ansi | grep '\$'

Filtering out solution content to list only the metadata.

.. code-block:: none

    snippy search --scat solution --sall . | grep -Ev '[^\s]+:'

Updating content
----------------

Updating snippet with vi editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following command allows updating existing snippet with vi editor. The command will
launch a vi editor which allows you to modify the content. The content is updated
automatically after the file is saved and editor is exit.

.. code-block:: none

    snippy update --digest 54e41e9b52a02b63

Updating solution from text template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following commands allow updating existing solution by exporting the content to text
file and importing it again.

.. code-block:: none

    snippy export --digest 76a1a02951f6bcb4
    snippy import --digest 76a1a02951f6bcb4 --file howto-debug-elastic-beats.txt


Updating duplicated content with message digest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is an unique constraint defined for the content. This means that two examples
with the same content cannot be stored. There are two supported work flows.

The tool will prompt failure log with a message digest for content that is already
existing. User can change the create operation to update and define the message
digest. This will launch a vi editor that contain the values that were previously
stored. User may change the values in editor and save the content which will get
then updated.

.. code-block:: none

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest f6062e09e2c11b47
    snippy update --digest f6062e09e2c11b47
    OK

Updating duplicated content by defining content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tool will prompt failure log with a message digest for content that is already
existing. User can change the create operation to uddate and use the same command.
This will launch a vi editor with the content defined in command line. If some of
the values are not defined in command line, they are shown as previously stored.
User may change the values in editor and save the content which will get then
updated.

.. code-block:: none

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest 5feded9ec5945d6a
    snippy update --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    OK

Deleting content
----------------

Delete snippet with index.

.. code-block:: none

    snippy delete --digest 96471dce19fe9c90

Migrating content
-----------------

Exporting content
~~~~~~~~~~~~~~~~~

Following commands allow exporting all snippets and solutions to YAML file that you use
to back-up your data. The commands below will create snippets.yaml and solutions.yaml
files into same directory where the command was executed. You can define the file name
and path with the -f|--file option.

.. code-block:: none

    snippy export --scat snippet
    snippy export --scat snippet -f my-snippets.yaml
    snippy export --scat solution
    snippy export --scat solution -f my-solutions.yaml

Importing content
~~~~~~~~~~~~~~~~~

Following commands allow importing snippets and solutions from default YAML files named
snippets.yaml and solutions.yaml that must be located in the same directory where the
command is executed. You can define the file name and path with the -f|--file option.

.. code-block:: none

    snippy import --scat snippet
    snippy import --scat solution

.. _Read the Docs: http://snippy.readthedocs.io/en/latest/

.. _Github: https://github.com/heilaaks/snippy
