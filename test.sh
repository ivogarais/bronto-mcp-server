#!/usr/bin/env bash
set -e

PROJECT_ROOT_DIR="${PWD}"
PYPROJECT_FILE="${PROJECT_ROOT_DIR}/pyproject.toml"

if [ ! -f "${PYPROJECT_FILE}" ]
then
  echo "${PYPROJECT_FILE} is missing. Cannot run uv-based tests."
  exit 0
fi

uv sync --dev

cd "${PROJECT_ROOT_DIR}/src/test" || exit 1

echo "Running Ruff"
uv run ruff format . || true
echo "Running Tests"
uv run coverage run -m pytest -v -s
echo "Reporting Test Coverage"
uv run coverage report -m
