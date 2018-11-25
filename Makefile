.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev
test:
	pipenv run pytest
black:
	pipenv run black .

docs:
	cd docs && make clean && make html
