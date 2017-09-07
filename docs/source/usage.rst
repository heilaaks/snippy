Usage
=====

You can add any number of command examples and search them with a keyword
list. You can update the examples afterwards with a vi editor. Exporting
and importing the data is supported.

Deleting the snippets works with a message digest of the snippet or
solution.

Editing
-------

.. code:: bash

    python snip.py create -c 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -g docker -t docker,image,cleanup
    python snip.py create --editor
    python snip.py update --digest cc3aecd819eed9f4
    python snip.py delete --digest cc3aecd819eed9f4


Searching
---------

.. code:: bash

    python snip.py search --sall docker,containers


Importing and Exporting
-----------------------

.. code:: bash

    python snip.py export --file snippets.yaml
    python snip.py export --file snippets.json
    python snip.py export --file snippets.txt
    python snip.py import --file snippets.yaml
    python snip.py import --file snippets.json

Support
-------

.. code:: bash

    python snip.py --help
    python snip.py --version
    python snip.py -vv
    python snip.py --debug
    python snip.py --profile
