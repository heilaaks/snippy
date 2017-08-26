Usage
=====

You can add any number of command or code snippets and search them with a keyword
list. The keyword list search finds the results with any matching keyword.

Deleting the snippets works with the index of the snippet.

.. code:: bash

    python snip.py --input 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker, image, cleanup
    python snip.py --search docker
    python snip.py --job delete --role snippet --id 1
