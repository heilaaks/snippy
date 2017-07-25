# cuma

## Installation

   ```
   # Installing with Python virtual environment wrapper.
   $ mkdir -p ${HOME}/devel/python-virtualenvs
   $ sudo pip3 install virtualenvwrapper
   $ virtualenv --version
   $ export WORKON_HOME=${HOME}/devel/python-virtualenvs # Add to ~/.bashrc
   $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3    # Add to ~/.bashrc
   $ source /usr/bin/virtualenvwrapper.sh                # Add to ~/.bashrc
   $ mkvirtualenv cuma
   ```

   ```
   # Installing
   $ mkvirtualenv cuma
   $ pip install .
   $ pip install -e .[dev] # Development packages.
   ```

   ```
   # Example commands for the Python virtualenvwrapper.
   $ lssitepackages
   $ lsvirtualenv
   $ deactivate
   $ workon cuma
   $ rmvirtualenv cuma
   ```

   ```
   # Using Pylint for the first time.
   #    - Modified test line from 100 to 125 characters.
   $ pylint --generate-rcfile > tests/pylint/pylint-cuma.rc
   ```

   ```
   # Running Pylint.
   $ pylint --rcfile tests/pylint/pylint-cuma.rc ./cuma
   $ pylint --rcfile tests/pylint/pylint-cuma.rc ./cuma > tests/pylint/pylint-cuma.txt
   ```

   ```
   # Running pytests tests
   $ pytest
   ```

   ```
   # Freezing project for tag (check this one)
   $ pip freeze > requirements.txt
   ```

   ```
   # Test if Pyflame will have problems with SELinux or settings. The first
   # value needs to be 'off' and second value zero.
   $ getsebool deny_ptrace
     deny_ptrace --> off
   $ sysctl kernel.yama.ptrace_scope
     kernel.yama.ptrace_scope = 0
   ```
   
   ```
   # Install pyflame dependencies
   $ sudo dnf install autoconf automake gcc-c++ python-devel python3-devel libtool
   $ git clone https://github.com/uber/pyflame.git
   $ cd pyflame
   $ git checkout v1.4.4
   $ ./autogen.sh
   $ ./configure
   $ make
   ```

## Devel

cd devel/cuma
workon cuma
cuma.py -s test
pytest
pylint --rcfile tests/pylint/pylint-cuma.rc ./cuma
pylint --rcfile tests/pylint/pylint-cuma-tests.rc ./tests
pytest --cov=cuma tests/
pytest --cov=cuma --cov-report html tests/
make -C docs html

   > file:///home/heilaaks/devel/cuma/htmlcov/index.html
   > file:///home/heilaaks/devel/cuma/docs/build/html/index.html
