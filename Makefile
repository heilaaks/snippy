# Disable default suffixes and rules to reduce spam with make --debug
# option. This is a Python project and these builtins are not needed.
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

# Run all commands in one shell.
.ONESHELL:

DEV_VERSION    := 0.11a0
TAG_VERSION    := 0.10.0

PKG_MANAGER    := $(shell command -v dnf)
PKG_COMMAND    := list installed
PYPY           := pypy3
PYPY2_LIBS     := pypy pypy-devel postgresql-devel
PYPY3_LIBS     := pypy3 pypy3-devel postgresql-devel
PYTHON         := python
PYTHON_VERSION := $(shell python -c 'import sys; print(sys.version_info[0])')

# Commands assume that they are run inside virtual environment. The new
# pyproject.toml based PEP517 does not support --editable and it is not
# possible to use --user install inside a virtual environment. If these
# commands in the Makefile are run outside of a virtual environment, the
# install does global install.
install:
	$(PYTHON) -m pip install .

install-devel:
	$(PYTHON) -m pip install .[devel]

install-test:
	$(PYTHON) -m pip install .[test]

install-devel-pypy:
	@echo "##########################################################################"
	@echo "Requires on Fedora:"
	@echo "    dnf install pypy3 -y"
	@echo "    dnf install pypy3-devel -y"
	@echo "    dnf install postgresql-devel -y"
	@echo "##########################################################################"
	$(PYPY) -m pip install .[develpypy]

install-server:
	$(PYTHON) -m pip install .[server]

install-server-pypy:
	@echo "##########################################################################"
	@echo "Requires on Fedora:"
	@echo "    dnf install pypy3 -y"
	@echo "    dnf install pypy3-devel -y"
	@echo "    dnf install postgresql-devel -y"
	@echo "##########################################################################"
	$(PYPY) -m pip install .[serverpypy]

upgrade:
	$(PYTHON) -m pip install --upgrade .

upgrade-wheel:
	$(PYTHON) -m pip install pip setuptools wheel twine --upgrade --user
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): Updated setuptools twine and wheel to latest"

upgrade-tool-version: clean-all
	sed -i -r "s/${DEV_VERSION}/${TAG_VERSION}/" ./snippy/meta.py
	$(PYTHON) runner import --defaults --scat all -q
	$(PYTHON) runner export --defaults --scat all -q
	! grep -rn -e ${DEV_VERSION} --exclude=releasing.rst --exclude=Makefile ./
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): Updated tool version ${DEV_VERSION} to ${TAG_VERSION}"

upgrade-tool-version-devel: clean-all
	sed -i -r "s/${TAG_VERSION}/${DEV_VERSION}/" ./snippy/meta.py
	$(PYTHON) runner import --defaults --scat all -q
	$(PYTHON) runner export --defaults --scat all -q
	! grep -rn -e ${TAG_VERSION} --exclude=CHANGELOG.rst --exclude=Makefile --exclude=releasing.rst ./
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): Updated tool version ${TAG_VERSION} to ${DEV_VERSION}"

prepare-release:
	make upgrade-wheel
	make upgrade-tool-version
	make test-release

uninstall:
	$(PYTHON) -m pip uninstall --yes snippy

outdated:
	$(PYTHON) -m pip list --outdated

.PHONY: docs
docs:
	make -C docs html

test: test-sqlite

test-all: test-sqlite test-postgresql test-docker

test-ci: test-sqlite

test-release: clean-all test-sqlite test-postgresql test-docker test-tox lint docs test-release-wheel
	@echo "$$(date +'%Y-%m-%dT%H:%M:%S'): All automated tests and checks run"

test-release-wheel: clean-all
	$(PYTHON) setup.py sdist bdist_wheel
	twine check dist/*

test-fast:
ifeq ($(PYTHON_VERSION), 3)
	$(PYTHON) -m pytest -n auto -x ./tests/test_*.py --cov snippy -m "not (server or docker)"
else
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy -m "not (server or docker)"
endif

test-docker:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite -m "docker"

test-postgresql:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db postgresql -m "not docker"

test-postgresql-pypy:
	$(PYPY) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db postgresql -m "not docker"

test-sqlite:
	$(PYTHON) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite -m "not docker"

test-sqlite-pypy:
	$(PYPY) -m pytest -x ./tests/test_*.py --cov snippy --snippy-db sqlite -m "not docker"

test-tox:
	tox

coverage:
	$(PYTHON) -m pytest --cov=snippy --cov-branch --cov-report html tests/ -m "not (server or docker)"
	$(PYTHON) -m pytest --cov=snippy tests/

lint:
	$(PYTHON) -m pylint --jobs=0 --rcfile tests/pylint/pylint-snippy-tests.rc tests/ | tee tests/pylint/pylint-snippy-tests.txt
	$(PYTHON) -m pylint --jobs=0 --rcfile tests/pylint/pylint-snippy.rc snippy/ | tee tests/pylint/pylint-snippy.txt
	$(PYTHON) -m flake8 --config tests/flake8/flake8.ini snippy

pyflakes:
	$(PYTHON) -m pyflakes .

schema:
	openapi2jsonschema snippy/data/server/openapi/swagger-2.0.yml -o snippy/data/server/openapi/schema/

docker: clean-all
	docker build --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -t heilaaks/snippy .

security-scan:
	-bandit -r snippy | tee tests/bandit/bandit.txt

.PHONY: clean
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
