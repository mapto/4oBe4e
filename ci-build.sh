#!/bin/sh -e

export PIPENV_VERBOSITY=-1

echo '>>> Run Black'
pipenv run black src

echo '>>> Run Pylint'
pipenv run pylint -E src/*.py

echo '>>> Run Mypy'
pipenv run mypy src

echo '>>>  Run Pytest'
pipenv run pytest -v --doctest-modules src