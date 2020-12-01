# Advent of code 2020 solutions <!-- omit in toc --> <!-- do not remove comment + use Markdown All in One in VSCode -->

⁣    🌟
    🎄
   🎄🎄
  🎄🎄🎄
 🎄🎄🎄🎄
🎄🎄🎄🎄🎄
  🎁🎁🎁

These are proposed solutions for the [Advent of Code 2020](http://adventofcode.com/2020).

The solutions are automatically tested with github-actions.

[![Build Status](https://github.com/david-ds/adventofcode-2020/workflows/CI/badge.svg)](https://github.com/david-ds/adventofcode-2020/actions?query=branch%3Amaster)

- [Usage](#usage)
  - [Installation](#installation)
  - [Examples](#examples)
    - [Run last problem](#run-last-problem)
    - [Run specific problems from specific users](#run-specific-problems-from-specific-users)
- [Contribute](#contribute)
  - [New submission with aoc](#new-submission-with-aoc)
  - [New submission without aoc](#new-submission-without-aoc)
- [Installing runners to try out other people code](#installing-runners-to-try-out-other-people-code)
  - [Go](#go)
  - [Rust](#rust)
  - [Node](#node)
  - [Deno](#deno)
  - [Nim](#nim)
- [History](#history)

## Usage

use `./aoc` script

```
usage: aoc <command> [<args>]

aoc commands are:
   run      Runs submissions
   create   Creates a new submission
   config   Configures user's parameters
```

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# And now aoc can work
./aoc run
```

### Examples

#### Run last problem

```
./aoc run
```

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running submissions for day 04:

* part 2:
---------------------------------------------------
Avg over all inputs
---------------------------------------------------
----------  ----------  -----------  ---
silvestre      78452        1.99 ms  py
degemer        43695        2.39 ms  py
jules          23037        2.49 ms  py
david          36371        2.94 ms  py
thomas          9763        2.97 ms  py
ayoub         136461        5.85 ms  cpp
evqna          49137        6.65 ms  cpp
badouralix     51232        7.26 ms  go
tpxp           41668      133.63 ms  rb
----------  ----------  -----------  ---
```

#### Run specific problems from specific users

```
./aoc run -d 1 -d 2 -p 1 -a ayoub -a david
```

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running submissions for day 01:

* part 1:
---------------------------------------------------
Avg over all inputs
---------------------------------------------------
-----  -------  -----------  ---
david    543        0.46 ms  py
ayoub    445        4.94 ms  cpp
-----  -------  -----------  ---
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running submissions for day 02:

* part 1:
---------------------------------------------------
Avg over all inputs
---------------------------------------------------
-----  --------  -----------  ---
david    5658        1.22 ms  py
ayoub    6448        4.84 ms  cpp
-----  --------  -----------  ---
```

You can use `-r` to run each submission on it's own input, or `-e` to print non-aggregated results.
see `./aoc run -h` for full arguments description.

## Contribute

To participate, you'll have to create your own files. For instance, if you want to code in `go` and participate the the day 3, you'll have to create those 3 files:

```
day-03/input/yourname.txt (input provided by advent of code)
day-03/part-1/yourname.go
day-03/part-2/yourname.go
```

You can add other functions & modules if you need to. Any external dependency should be added to the appropriate files (`requirements.txt`, `package.json`, and so on).

Once you tested your solution you can submit it by making a PR and a GitHub action will check that your code generates the same outputs as others' code.

For now we support `c`, `c++`, `java`, `javascript` (with node and deno), `typescript` (with deno) , `go`, `python 3` (+ `cython`), `ruby`, `rust (stable)`, `julia`, `bash`, and `nim` scripts.

### New submission with aoc

You can use `./aoc create` tool to create a new empty submission:

```
usage: aoc create [-h] [-a AUTHOR] [-d DAY] [-p PART]
                  [-l {c,cpp,go,intcode,java,js,deno.js,deno.ts,nim,py,pyx,rb,sh}]

Create a new submission

optional arguments:
  -a AUTHOR, --author AUTHOR
                        submission author
  -d DAY, --day DAY     problem day
  -p PART, --part PART  problem part
  -l {c,cpp,go,intcode,java,js,deno.js,deno.ts,nim,py,pyx,rb,sh}, --language {c,cpp,go,intcode,java,js,deno.js,deno.ts,nim,py,pyx,rb,sh}
                        submission language
```

you can also use `./aoc config` to setup your local profile

```
usage: aoc config [-h] username {c,cpp,go,intcode,java,js,deno.js,deno.ts,nim,py,pyx,rb,sh}

Configures user parameters

positional arguments:
  username              prefered username
  {c,cpp,go,intcode,java,js,deno.js,deno.ts,nim,py,pyx,rb,sh}
                        prefered programming language
```

### New submission without aoc

If you don't use `./aoc create` tool you should follow this convention:

```
day-[number]/part-[number]/[username].py    # your submission code
day-[number]/input/[username].txt           # your input file
```

Your submission code should follow templates written in the `tool/templates/` folder (there is one for each language).

## Installing runners to try out other people code

### Go

`brew install go`

### Rust

Follow: https://www.rust-lang.org/tools/install

### Node

`brew install node`

### Deno

`brew install deno`

or

`curl -fsSL https://deno.land/x/install/install.sh | sh`

### Nim

`brew install nim`

## History

- [Advent of Code 2019](https://github.com/lypnol/adventofcode-2019)
- [Advent of Code 2018](https://github.com/badouralix/advent-of-code-2018)
- [Advent of Code 2017](https://github.com/lypnol/adventofcode-2017)
- [Advent of Code 2016](https://github.com/lypnol/adventofcode-2016)
