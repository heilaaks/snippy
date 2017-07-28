init:
	pip3 install -e .[dev]

test:
	py.test tests

coverage:
	pytest --cov=snippy --cov-report html tests/
	pytest --cov=snippy tests/

docs:
	make -C docs html

lint:
	-pylint --rcfile tests/pylint/pylint-snippy.rc snippy/ | tee tests/pylint/pylint-snippy.txt
	-pylint --rcfile tests/pylint/pylint-snippy-tests.rc tests/ | tee tests/pylint/pylint-snippy-tests.txt

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -drf .cache
	rm -drf .coverage
	rm -drf snippy.egg-info
	rm -drf htmlcov
	rm -rf docs/build/*
	rm -f pytestdebug.log

.PHONY: init test coverage docs lint clean
