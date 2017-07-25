Usage
=====

The basic usage contains adding a snippet with specified tags and search them.

.. code:: bash

    cuma --snippet 'docker rm $(docker ps -a -q)' --tags docker, image, cleanup

