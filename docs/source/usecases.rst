Use Cases
=========

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

    python snip.py create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest 5feded9ec5945d6a
    python snip.py update --digest 5feded9ec5945d6a
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

    python snip.py create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    NOK: content already exist with digest 5feded9ec5945d6a
    python snip.py update --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    OK

