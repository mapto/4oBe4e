#!/bin/sh -e

export PIPENV_VERBOSITY=-1

echo '>>> Run Black'
pipenv run black --check .

echo '>>> Run Pylint'
pipenv run pylint -E *.py

echo '>>> Run Mypy'
pipenv run mypy .

echo '>>>  Run Pytest'
pipenv run pytest -v --doctest-modules .