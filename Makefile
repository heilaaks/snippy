python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
python_version_major := $(word 1,${python_version_full})

install:
	pip install .

upgrade:
	pip install --upgrade .

uninstall:
	pip uninstall --yes snippy

server:
	pip install -e .[server]

dev:
	pip install -e .[dev]

test:
	python -m pytest -x ./tests/test_*.py --cov snippy

test-fast:
ifeq ($(python_version_major), 3)
	python -m pytest -n auto -x ./tests/test_*.py --cov snippy -m "not serial"
else
	@echo "##########################################################################"
	@echo "Parallel tests are supported only with Python 3. Executing tests serially."
	@echo "##########################################################################"
	make test
endif

coverage:
	pytest --cov=snippy --cov-branch --cov-report html tests/
	pytest --cov=snippy tests/

outdated:
	pip list --outdated

docs:
	make -C docs html

lint:
	-pylint --rcfile tests/pylint/pylint-snippy-tests.rc tests/ | tee tests/pylint/pylint-snippy-tests.txt
	-pylint --rcfile tests/pylint/pylint-snippy.rc snippy/ | tee tests/pylint/pylint-snippy.txt
	-flake8 --config tests/flake8/flake8.ini snippy

pyflakes:
	-python -m pyflakes .

schema:
	openapi2jsonschema snippy/data/server/openapi/swagger-2.0.yml -o snippy/data/server/openapi/schema/

docker: clean clean-db
	docker build --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -t heilaaks/snippy .

security-scan:
	-bandit -r snippy | tee tests/bandit/bandit.txt

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -drf .cache
	rm -drf .coverage
	rm -drf .tox
	rm -dfr build
	rm -dfr dist
	rm -drf docs/build/*
	rm -drf htmlcov
	rm -drf .pytest_cache
	rm -drf snippy.egg-info
	rm -f .coverage.*
	rm -f coverage.xml
	rm -f pytestdebug.log
	rm -f snippets.json
	rm -f snippets.yaml
	rm -f snippet*.text
	rm -f snippets.txt
	rm -f snippet-template.txt
	rm -f solutions.json
	rm -f solutions.yaml
	rm -f solution*.text
	rm -f solutions.txt
	rm -f solution-template.txt
	rm -f references.json
	rm -f references.yaml
	rm -f references.text
	rm -f references.txt
	rm -f content.yaml
	rm -f content.text

clean-db:
	> snippy/data/storage/snippy.db

.PHONY: install upgrade uninstall server dev test test-fast coverage outdated docs lint pyflakes docker security-scan clean clean-db
