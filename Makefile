.PHONY : test-local test-local-file serve build-docs check-readme install-local lint format dev-setup

check-readme:
	rm -rf dist build brazil_monthly_deaths.egg-info
	python setup.py sdist bdist_wheel
	python -m twine check dist/*

test:
	tox -e py37 -- --cov-report term-missing --cov-report html

format:
	black brazil_monthly_deaths setup.py tests --check

lint:
	flake8 brazil_monthly_deaths

dev-setup:
	pip install -e ".[dev]"
