#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1

function run() {
    # Your code goes here
    NUM_BIN=$(echo "$INPUT" | tr "BFRL\n" "1010;")
    NUM=$(echo "ibase=2;obase=A;$NUM_BIN" | bc | sort -n)

    N_MIN=$(echo "$NUM" | head -n 1)
    N_MAX=$(echo "$NUM" | tail -n 1)

    diff <(echo "$NUM") <(seq $N_MIN $N_MAX) | tail -n 1 | cut -d " " -f 2
}

echo $(run)
