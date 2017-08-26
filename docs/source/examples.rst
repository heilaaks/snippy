Examples
========

Add snippet with brief description and tags.

.. code:: bash

    python snip.py --input 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker, image, cleanup

Find snippet with keyword list.

.. code:: bash

    python snip.py --search docker,containers

Delete snippet with index.

.. code:: bash

    python snip.py --job delete --role snippet --id 1
