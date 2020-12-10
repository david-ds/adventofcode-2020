package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"sort"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Parse/sort input
	input := strings.Split(s, "\n")
	joltageRatings := make(sort.IntSlice, len(input)+1)
	joltageRatings[0] = 0
	for i := range input {
		joltageRatings[i+1], _ = strconv.Atoi(input[i])
	}
	sort.Sort(joltageRatings)

	cache := make([]int, len(joltageRatings)) // More efficient than a map with make(map[int]int)
	cache[len(joltageRatings)-1] = 1
	for i := len(joltageRatings) - 2; i >= 0; i-- {
		for j := i + 1; j < len(joltageRatings) && joltageRatings[j]-joltageRatings[i] <= 3; j++ {
			cache[i] += cache[j]
		}
	}
	return cache[0]
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
