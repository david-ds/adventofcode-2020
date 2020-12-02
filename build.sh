#!/bin/bash

set -ev

# source $HOME/.cargo/env
export PATH=$PATH:~/.cargo/bin:$GOROOT/bin
export PYENV_VERSION=3.7

run() {
    echo $1 | grep "day-" | cut -d "/" -f1 | cut -d "-" -f2 | sort | uniq | xargs -I{} ./aoc run -fd {}
}

if [ "$(git branch --show-current)" = "master" ];
then
    run "$(git --no-pager diff --name-only HEAD HEAD^ --)"
else
    run "$(git --no-pager diff --name-only origin/master --)"
fi


