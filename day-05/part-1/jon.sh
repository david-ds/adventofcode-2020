#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1

function run() {
    # Your code goes here
    NUMBERS=$(echo "$INPUT" | tr "BFRL\n" "1010;")
    echo "ibase=2;obase=A;$NUMBERS" | bc | sort -nr | head -n 1
}

echo $(run)
