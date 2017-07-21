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

## Devel

   $ cd devel/cuma
   $ workon cuma
   $ cuma.py -s test
   $ pytest
   $ pylint --rcfile tests/pylint/pylint-cuma.rc ./cuma
   $ pylint --rcfile tests/pylint/pylint-cuma-tests.rc ./tests
   $ pytest --cov=cuma tests/
   $ pytest --cov=cuma --cov-report html tests/
   > file:///home/heilaaks/devel/cuma/htmlcov/index.html
