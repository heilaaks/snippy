# Disable default suffixes and rules to reduce spam with make --debug
# option. This is a Python project and these are not needed.
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

# Run all commands in one shell.
.ONESHELL:

PKG_MANAGER    := $(shell command -v dnf)
PKG_COMMAND    := list installed
PIP            := pip
PYPY           := pypy3
PYPY2_LIBS     := pypy pypy-devel postgresql-devel
PYPY3_LIBS     := pypy3 pypy3-devel postgresql-devel
PYTHON         := python
PYTHON_VERSION := $(shell python -c 'import sys; print(sys.version_info[0])')

.PHONY: clean
clean: clean-build clean-pyc clean-test

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

clean-db:
	> snippy/data/storage/snippy.db

install:
	$(PIP) install .

upgrade:
	$(PIP) install --upgrade .

uninstall:
	$(PIP) uninstall --yes snippy

.PHONY: devel
devel:
	$(PIP) install --editable .[devel]

.PHONY: docs
docs:
	make -C docs html

server:
	$(PIP) install --editable .[server]

server-pypy:
	@echo "##########################################################################"
	@echo "Requires on Fedora:"
	@echo "    dnf install pypy3 -y"
	@echo "    dnf install pypy3-devel -y"
	@echo "    dnf install postgresql-devel -y"
	@echo "##########################################################################"
	$(PYPY) -m pip install --editable .[serverpypy]

devel-pypy:
	@echo "##########################################################################"
	@echo "Requires on Fedora:"
	@echo "    dnf install pypy3 -y"
	@echo "    dnf install pypy3-devel -y"
	@echo "    dnf install postgresql-devel -y"
	@echo "##########################################################################"
	$(PYPY) -m pip install --editable .[develpypy]

.PHONY: test
test: test-sqlite

test-all: test-sqlite test-postgresql test-docker

test-fast:
ifeq ($(PYTHON_VERSION), 3)
	$(PYTHON) -m pytest -n auto -x ./tests/test_*.py --cov snippy -m "not (server or docker)"
else
	@echo "##########################################################################"
	@echo "Parallel tests are supported only with Python 3. Executing tests serially."
	@echo "##########################################################################"
	make test
endif

test-docker:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite

test-docker-only:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite -m "docker"

test-postgresql:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db postgresql -m "not docker"

test-postgresql-pypy:
	$(PYPY) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db postgresql -m "not docker"

test-sqlite:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite -m "not docker"

test-sqlite-pypy:
	$(PYPY) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite -m "not docker"

coverage:
	$(PYTHON) -m pytest --cov=snippy --cov-branch --cov-report html tests/ -m "not docker"
	$(PYTHON) -m pytest --cov=snippy tests/

lint:
	-$(PYTHON) -m pylint --jobs=0 --rcfile tests/pylint/pylint-snippy-tests.rc tests/ | tee tests/pylint/pylint-snippy-tests.txt
	-$(PYTHON) -m pylint --jobs=0 --rcfile tests/pylint/pylint-snippy.rc snippy/ | tee tests/pylint/pylint-snippy.txt
	-$(PYTHON) -m flake8 --config tests/flake8/flake8.ini snippy

pyflakes:
	-$(PYTHON) -m pyflakes .

outdated:
	$(PIP) list --outdated

.PHONY: schema
schema:
	openapi2jsonschema snippy/data/server/openapi/swagger-2.0.yml -o snippy/data/server/openapi/schema/

.PHONY: docker
docker: clean clean-db
	docker build --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -t heilaaks/snippy .

security-scan:
	-bandit -r snippy | tee tests/bandit/bandit.txt

# $(call test-pypy-libs, pkg-manager, pkg-COMMAND, required-libs)
#
# Test if given array of pacakges is installed with given package
# manager. Backslashes are aligned for 8 space tabs.
define test-installed-libs
	$$(										\
		set -x;									\
		MISSING=();								\
		i=0;									\
		if [ ! -z "${1}" ]; then						\
			for PACKAGE in ${3}; do						\
				if [ -z "$$(${1} ${2} | grep $${PACKAGE})" ]; then	\
					MISSING+=$$PACKAGE;				\
				fi							\
			done;								\
		else									\
			false;								\
		fi;									\
		if [ $${#MISSING[@]} -eq 0 ]; then					\
			true;								\
		else									\
			echo "$${MISSING[*]}";						\
		fi									\
	)
endef
