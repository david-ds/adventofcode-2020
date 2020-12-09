package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const RANGE = 25

func run(s string) interface{} {
	sequence := [2048]int{0}
	for i, n := range strings.Split(s, "\n") {
		sequence[i], _ = strconv.Atoi(n)
	}

	for i, val := range sequence[RANGE:] {
		if !searchVal(&sequence, val, i) {
			return val
		}
	}

	return 0
}

func searchVal(sequence *[2048]int, val int, i int) bool {
	for j, a := range (*sequence)[i:i + RANGE - 1] {
		for _, b := range (*sequence)[j+1:i + RANGE] {
			if a + b == val {
				return true
			}
		}
	}
	return false
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
