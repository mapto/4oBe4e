#!/bin/sh -e

# Only difference from pre-commit is that black performs formatting

export PIPENV_VERBOSITY=-1 

cd $(git rev-parse --show-toplevel)

echo '>>> Run Pylint'
pipenv run pylint -E src/

echo '>>> Run Mypy'
pipenv run mypy src

echo '>>>  Run Pytest'
pipenv run pytest -v --doctest-modules -s src

echo '>>> Run Black'
pipenv run black src

