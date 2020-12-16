#!/bin/bash

set -ev

# source $HOME/.cargo/env
export PATH=$PATH:~/.cargo/bin:$GOROOT/bin
export PYENV_VERSION=3.8

run() {
    echo "$1" | grep "day-" | cut -d "/" -f1 | cut -d "-" -f2 | sort | uniq | xargs -I{} ./aoc run -fntd {}
}


# In PRs, GITHUB_HEAD_REF is set the the name of the branch
# This variable isn't set on regular commits and as we only allowed the CI to run on pushs only in master
# checking if the variable is the empty string is the same as checking if the branch is master
# Note: we cannot use "git branch --show-current" as GitHub rewrites the history in actions
if [ "$GITHUB_HEAD_REF" == "" ];
then
    # if on master, check the diff of the last commit
    run "$(git --no-pager diff --name-only HEAD HEAD^ --)"
else
    # otherwise, check the diff with master
    run "$(git --no-pager diff --name-only origin/master --)"
fi


