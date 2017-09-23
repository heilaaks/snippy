install:
	pip install .

upgrade:
	pip install --upgrade .

uninstall:
	pip uninstall --yes snippy

dev:
	pip install -e .[dev]

test:
	python -m pytest ./tests/test_*.py --cov snippy -vv

coverage:
	pytest --cov=snippy --cov-report html tests/
	pytest --cov=snippy tests/

docs:
	make -C docs html

lint:
	-pylint --rcfile tests/pylint/pylint-snippy-tests.rc tests/ | tee tests/pylint/pylint-snippy-tests.txt
	-pylint --rcfile tests/pylint/pylint-snippy.rc snippy/ | tee tests/pylint/pylint-snippy.txt

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -drf .cache
	rm -drf .coverage
	rm -dfr build
	rm -dfr dist
	rm -drf docs/build/*
	rm -drf htmlcov
	rm -drf snippy.egg-info
	rm -f coverage.xml
	rm -f pytestdebug.log
	rm -f snippets.json
	rm -f snippets.txt
	rm -f snippets.yaml
	rm -f solutions.json
	rm -f solutions.txt
	rm -f solutions.yaml

clean-db:
	> snippy/data/storage/snippy.db

.PHONY: install upgrade uninstall dev test coverage docs lint clean clean-db
