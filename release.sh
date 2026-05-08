#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f "$HOME/.pypirc" ]; then
    echo "error: ~/.pypirc not found. See https://packaging.python.org/en/latest/specifications/pypirc/" >&2
    echo "       Use username = __token__ and password = pypi-... (account-scoped for first publish)." >&2
    exit 1
fi

rm -rf dist/
uv build
uvx twine upload dist/*
