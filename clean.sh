#!/bin/bash -e

cd "$(git rev-parse --show-toplevel)"

echo Removing .pyc files
find . -type f -name "*.pyc" -print0 | xargs -0 rm -vf
