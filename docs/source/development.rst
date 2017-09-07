Development
===========

Quick Start
-----------

For the development, you can clone the repository and run the setup
for Python virtual environment like below:

.. code:: bash

    git clone https://github.com/heilaaks/snippy.git
    mkvirtualenv snippy
    make dev

The basic commands to run and test are:

.. code:: bash

    python3 snip.py create -c 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -t docker,container,cleanup
    make test
    make lint
    make coverage
    make doc
    make clean

Python Virtual Environment
--------------------------

You can install the Python virtual environment wrapper like below:

.. code:: bash

    mkdir -p ${HOME}/devel/python-virtualenvs
    sudo pip3 install virtualenvwrapper
    virtualenv --version
    export WORKON_HOME=${HOME}/devel/python-virtualenvs # Add to ~/.bashrc
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3    # Add to ~/.bashrc
    source /usr/bin/virtualenvwrapper.sh                # Add to ~/.bashrc
    mkvirtualenv snippy

Example commands to operate the virtual environment are below. More
information can be found from the Python virtualenvwrapper_ command
reference documentation.

.. code:: bash

    lssitepackages
    lsvirtualenv
    deactivate
    workon snippy
    rmvirtualenv snippy

Pylint
------

The Pylint rc file can be generated for the very first time like:

.. code:: bash

    pylint --generate-rcfile > tests/pylint/pylint-snippy.rc

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html
