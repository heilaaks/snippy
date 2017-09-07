Examples
========

Add snippet with brief description and tags.

.. code:: bash

    python snip.py create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup

Find snippet with keyword list.

.. code:: bash

    python snip.py search --sall docker,containers

Delete snippet with index.

.. code:: bash

    python snip.py delete --digest 5feded9ec5945d6a
