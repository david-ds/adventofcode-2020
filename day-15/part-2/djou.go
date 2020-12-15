package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const NUMBER = 30000001

type Memory struct {
	last int
	secondToLast int
}

func run(s string) interface{} {
	input := strings.Split(s, ",")
	memory := make(map[int]Memory)

	i := 1
	lastSpoken := 0
	for _, in := range input {
		val, _ := strconv.Atoi(in)
		if _, ok := memory[val]; !ok {
			lastSpoken = 0
			memory[val] = Memory{
				last: i,
				secondToLast: 0,
			}
		} else {
			if memory[val].secondToLast == 0 {
				lastSpoken = 0
			} else {
				lastSpoken = memory[val].last - memory[val].secondToLast
			}
			memory[lastSpoken] = Memory {
				last: i,
				secondToLast: memory[val].last,
			}
		}
		i++
	}

	for {
		if _, ok := memory[lastSpoken]; !ok {
			lastSpoken = 0
			memory[lastSpoken] = Memory{
				last: i,
				secondToLast: 0,
			}
		} else {
			if memory[lastSpoken].secondToLast == 0 {
				lastSpoken = 0
			} else {
				lastSpoken = memory[lastSpoken].last - memory[lastSpoken].secondToLast
			}
			memory[lastSpoken] = Memory {
				last: i,
				secondToLast: memory[lastSpoken].last,
			}
		}
		i++
		if i == NUMBER {
			return lastSpoken
		}
	}
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	// Read input from stdin
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
