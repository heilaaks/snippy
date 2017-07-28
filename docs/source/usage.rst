Usage
=====

The basic usage contains adding a snippet with specified tags and search them.

.. code:: bash

    snippy --snippet 'docker rm $(docker ps -a -q)' --tags docker, image, cleanup

