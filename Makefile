install:
	pip3 install .

dev:
	pip3 install -e .[dev]

test:
	python3 -m pytest ./tests/test_*.py --cov snippy -vv

coverage:
	pytest --cov=snippy --cov-report html tests/
	pytest --cov=snippy tests/

doc:
	make -C docs html

lint:
	-pylint --rcfile tests/pylint/pylint-snippy-tests.rc tests/ | tee tests/pylint/pylint-snippy-tests.txt
	-pylint --rcfile tests/pylint/pylint-snippy.rc snippy/ | tee tests/pylint/pylint-snippy.txt

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -drf .cache
	rm -drf .coverage
	rm -drf snippy.egg-info
	rm -drf htmlcov
	rm -rf docs/build/*
	rm -f pytestdebug.log

.PHONY: install dev test coverage doc lint clean
