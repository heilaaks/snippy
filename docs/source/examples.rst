Examples
========

Add snippet with brief description and tags.

.. code:: bash

    python snip.py --snippet 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker, image, cleanup

Find snippet with keyword list

.. code:: bash

    python snip.py --find docker,containers
