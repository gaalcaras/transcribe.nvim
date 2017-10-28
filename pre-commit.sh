#!/bin/sh

# Stash unstaged changes before running tests
# to avoid testing code that isn't part of the
# prospective commit.
git stash save -q --keep-index

# Run tests
make test
RESULT=$?

# Restore stash
git stash pop -q

# Act on test results
[ $RESULT -ne 0 ] && exit 1
exit 0
