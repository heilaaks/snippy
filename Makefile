# Disable default suffixes and rules to reduce spam with make --debug
# option. This is a Python project and these builtins are not needed.
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: docs

DEV_VERSION    := 0.11a0
TAG_VERSION    := 0.10.0

PIP            := pip
PYTHON         := python
PYTHON_VERSION := $(shell python -c 'import sys; print(sys.version_info[0])')
INSTALL_USER   :=
COVERAGE       := --cov=snippy --cov-branch

# Only the Python 3 implementation supports parallel tests. Sqlite database
# can be run as a in-memory database only with Python 3. An in-memory DB is
# is needed for parallel testing.
ifeq ($(PYTHON_VERSION), 3)
PYTEST_CORES   := --numprocesses auto
else
PYTEST_CORES   :=
endif

# The new pyproject.toml from PEP517 does not support --editable install.
# It is not possible to run --user install inside a virtual environment.
#
# When the Makefile is used outside of a virtual environment to intsall
# dependencies, the INSTALL_USER variable should be set to '--user' to
# avoid a global install.
#
# There is a different between 'pip' and 'python -m pip' when installing
# the project itself. The later does not work with the uninstall with an
# actitve virtual environment. Using 'pip' works inside active virtual
# environment as well as without virtual environment.
install:
	$(PIP) install . $(INSTALL_USER)

upgrade:
	$(PIP) install --upgrade . $(INSTALL_USER)

uninstall:
	$(PIP) uninstall --yes snippy .

upgrade-wheel:
	@test -x "$(shell which pip)" || $(PYTHON) -m ensurepip $(INSTALL_USER)
	$(PYTHON) -m pip install pip setuptools wheel twine --upgrade $(INSTALL_USER)

install-devel:
	$(PYTHON) -m pip install .[devel] $(INSTALL_USER)

install-tests:
	$(PYTHON) -m pip install .[test] $(INSTALL_USER)

install-server:
	$(PYTHON) -m pip install .[server] $(INSTALL_USER)

outdated:
	$(PYTHON) -m pip list --outdated

docs:
	make -C docs html

test:
	$(PYTHON) -m pytest -x ${COVERAGE} --snippy-db sqlite -m "not (docker or server)" $(PYTEST_CORES)

test-docker:
	$(PYTHON) -m pytest -x ${COVERAGE} --snippy-db sqlite -m "docker"

test-server:
	$(PYTHON) -m pytest -x ${COVERAGE} --snippy-db sqlite -m "server"

test-postgresql:
	$(PYTHON) -m pytest -x ${COVERAGE} --snippy-db postgresql -m "not (docker or server)"

test-in-memroy:
	$(PYTHON) -m pytest -x ${COVERAGE} --snippy-db in-memory -m "not (docker or server)"

test-tox:
	tox

test-all: test test-postgresql test-server test-docker test-tox

test-release: clean-all test-all lint docs test-release-wheel

test-release-wheel: clean-all
	$(PYTHON) setup.py sdist bdist_wheel
	twine check dist/*

coverage:
	$(PYTHON) -m pytest ${COVERAGE} --cov-report html -m "not (server or docker)" $(PYTEST_CORES)

lint:
	$(PYTHON) -m pylint --jobs=0 tests/
	$(PYTHON) -m pylint --jobs=0 snippy/
	$(PYTHON) -m flake8 snippy

pyflakes:
	$(PYTHON) -m pyflakes .

jsonschema:
	openapi2jsonschema snippy/data/server/openapi/swagger-2.0.yml -o snippy/data/server/openapi/schema/

docker: clean-all
	docker build --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -t heilaaks/snippy .

security-scan:
	-bandit -r snippy

clean: clean-build clean-pyc clean-test

clean-all: clean clean-db

clean-build:
	rm -drf .cache
	rm -drf build
	rm -drf dist
	rm -drf docs/build/*
	rm -drf pip-wheel-metadata
	rm -drf snippy.egg-info
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -drf .cache
	rm -drf .coverage
	rm -drf .pytest_cache
	rm -drf .tox
	rm -drf htmlcov
	rm -f .coverage.*
	rm -f coverage.xml
	rm -f pytestdebug.log
	rm -f snippy.bash-completion

clean-db:
	> snippy/data/storage/snippy.db

upgrade-tool-version: clean-all
	sed -i -r "s/${DEV_VERSION}/${TAG_VERSION}/" ./snippy/meta.py
	$(PYTHON) runner import --defaults --scat all -q
	$(PYTHON) runner export --defaults --scat all -q
	! grep -rn -e ${DEV_VERSION} --exclude=releasing.rst --exclude=Makefile ./

upgrade-tool-version-devel: clean-all
	sed -i -r "s/${TAG_VERSION}/${DEV_VERSION}/" ./snippy/meta.py
	$(PYTHON) runner import --defaults --scat all -q
	$(PYTHON) runner export --defaults --scat all -q
	! grep -rn -e ${TAG_VERSION} --exclude=CHANGELOG.rst --exclude=Makefile --exclude=releasing.rst ./
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): Updated tool version ${TAG_VERSION} to ${DEV_VERSION}"

prepare-release:
	make upgrade-wheel
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): Updated setuptools twine and wheel to latest"
	make upgrade-tool-version
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): Updated tool version ${DEV_VERSION} to ${TAG_VERSION}"
	make test-release
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): All automated tests and checks run"
