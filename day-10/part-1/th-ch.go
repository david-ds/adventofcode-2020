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
	joltageRatings := make(sort.IntSlice, len(input))
	for i := range input {
		joltageRatings[i], _ = strconv.Atoi(input[i])
	}
	sort.Sort(joltageRatings)

	currentRating := 0
	cursor := -1
	oneDiff := 0
	threeDiff := 0
	for cursor < len(joltageRatings)-1 {
		next := cursor + 1
		diff := joltageRatings[next] - currentRating
		if diff == 1 {
			oneDiff++
		}
		if diff == 3 {
			threeDiff++
		}
		cursor = next
		currentRating = joltageRatings[cursor]
	}

	threeDiff++

	return oneDiff * threeDiff
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
