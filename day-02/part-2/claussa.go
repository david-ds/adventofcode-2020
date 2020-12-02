package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	totalValid := 0

	for _, line := range strings.Split(s, "\n") {
		if validate(line) {
			totalValid++
		}
	}
	return totalValid
}

func validate(line string) bool {
	low, high := 0, 0
	var letter rune
	pos, index := 0, 0
	var isLowValid, isHighValid bool
	for _, r := range line {
		if r == '-' || r == ' ' || r == ':' {
			pos ++
			index = 0
			continue
		}
		if pos == 0 {
			low = (int(r) - '0') + low * int(math.Pow10(index))
		}
		if pos == 1 {
			high = (int(r) - '0') + high * int(math.Pow10(index))
		}
		if pos == 2 {
			letter = r
		}
		if pos == 4 {
			if index == (low - 1) {
				isLowValid = r == letter
			}
			if index == (high - 1) {
				isHighValid = r == letter
				break
			}
		}
		index++
	}
	return isLowValid != isHighValid
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
