#!/usr/bin/env bash

if ! [ -x "$(command -v git)" ]; then
  echo 'Error: git is not installed.' >&2
  exit 1
fi

REPO_URL="https://github.com/interledger/open-payments"
REPO_PATH=$(mktemp -d)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

git clone $REPO_URL "$REPO_PATH"
cp -r "$REPO_PATH"/openapi/* "$SCRIPT_DIR/../spec"