install:
	pip install -e .[dev]

test:
	py.test tests

coverage:
	pytest --cov=cuma --cov-report html tests/
	pytest --cov=cuma tests/

docs:
	make -C docs html

lint:
	-pylint --rcfile tests/pylint/pylint-cuma.rc cuma/ | tee tests/pylint/pylint-cuma.txt
	-pylint --rcfile tests/pylint/pylint-cuma-tests.rc tests/ | tee tests/pylint/pylint-cuma-tests.txt

.PHONY: init test coverage docs lint
