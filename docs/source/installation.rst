Installation
============

To install, run:

.. code:: text

    pip install snippy --user

    # Export user local Python package bin to PATH if needed.
    export PATH=${PATH}:~/.local/bin

To remove, run:

.. code:: text

    pip uninstall --yes snippy

To install as a server, run:

.. code:: text

    docker pull docker.io/heilaaks/snippy:latest

To install from Github, run:

.. code:: text

    git clone https://github.com/heilaaks/snippy.git
    cd snippy
    make install INSTALL_USER=--user

To install Bash completion, run:

.. code:: text

    snippy export --complete bash
    sudo cp snippy.bash-completion /etc/bash_completion.d/snippy.bash-completion

To try for the very first time, run:

.. code:: text

    snippy import --defaults
    snippy search untar
