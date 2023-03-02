#!/bin/bash
set -eu

TEST_DIRS="hoki scripts apps webapp"

black --check $TEST_DIRS
echo "black format check passed!"
flake8 $TEST_DIRS
echo "flake8 lint check passed!"
echo