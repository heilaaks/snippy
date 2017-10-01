Workflows
=========

Searching
---------

Printing all examples on terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to print all snippets on screen by using dot in the search
query. The search is a regexp query but the only special character passed
to the query is dot which matches to to any character.

.. code:: bash

    snippy search --sall .
    OK

Filtering with grep
~~~~~~~~~~~~~~~~~~~

With Linux grep it is possible to filter for example only the actual
commands from the search query.

.. code:: bash

    snippy search --sall . | grep --color=never '\$'
    snippy search --sgrp docker | grep --color=never '\$'

Filtering out solution content to list only the metadata.

.. code:: bash

    snippy search --solution --sall . | grep -Ev '[^\s]+:'


Updating duplicated content
---------------------------

There is an unique constraint defined for the content. This means that two
examples with the same content cannot be stored. There are two supported
work flows.

Updating duplicated content with message digest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tool will prompt failure log with a message digest for content that is
already existing. User can change the create operation to update and define
the message digest. This will launch a vi editor that contain the values
that were previously stored. User may change the values in editor and save
the content which will get then updated.

.. code:: bash

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest f6062e09e2c11b47
    snippy update --digest f6062e09e2c11b47
    OK

Updating duplicated content by defining content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tool will prompt failure log with a message digest for content that is
already existing. User can change the create operation to uddate and use
the same command. This will launch a vi editor with the content defined
in command line. If some of the values are not defined in command line,
they are shown as previously stored. User may change the values in editor
and save the content which will get then updated.

.. code:: bash

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest 5feded9ec5945d6a
    snippy update --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    OK

