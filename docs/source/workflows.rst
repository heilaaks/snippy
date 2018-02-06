Workflows
=========

Getting help
------------

Use help option with keyword examples to read about basic usage. Read the documentation
from `Read the Docs`_ or dive into the code in `Github`_.

.. code:: bash

    snippy --help
    snippy --help examples

Creating content
----------------

You can add new snippet directly from command line. How ever, easiest way to create new
content is to use editor.

.. code:: bash

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    snippy create --content 'docker rm --volumes $(docker ps --all --quiet)' --brief 'Remove all docker containers with volumes' --group docker --tags docker-ce,docker,moby,container,cleanup --links 'https://docs.docker.com/engine/reference/commandline/rm/'



Searching content
-----------------

Printing all examples on terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to list all snippets on screen by using dot as a search keyword.

.. code:: bash

    snippy search --sall .
    OK

Filtering with grep
~~~~~~~~~~~~~~~~~~~

With Linux grep it is possible to filter for example only the actual commands from the
search query.

.. code:: bash

    snippy search --sall . --no-ansi | grep '\$'
    snippy search --sgrp docker --no-ansi | grep '\$'

Filtering out solution content to list only the metadata.

.. code:: bash

    snippy search --solution --sall . | grep -Ev '[^\s]+:'

Updating content
----------------

Updating duplicated content with message digest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is an unique constraint defined for the content. This means that two examples
with the same content cannot be stored. There are two supported work flows.

The tool will prompt failure log with a message digest for content that is already
existing. User can change the create operation to update and define the message
digest. This will launch a vi editor that contain the values that were previously
stored. User may change the values in editor and save the content which will get
then updated.

.. code:: bash

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

.. code:: bash

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest 5feded9ec5945d6a
    snippy update --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    OK

Deleting content
---------------------------

Delete snippet with index.

.. code:: bash

    snippy delete --digest 96471dce19fe9c90


.. _Read the Docs: http://snippy.readthedocs.io/en/latest/

.. _Github: https://github.com/heilaaks/snippy
