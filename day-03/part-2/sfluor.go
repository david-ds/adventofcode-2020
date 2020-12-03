package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func count(theMap []string, dx, dy int) int {
	rows := len(theMap)
	cols := len(theMap[0])

	x := 0
	y := 0

	count := 0
	for y < rows {
		if theMap[y][x] == '#' {
			count += 1
		}

		x = (x + dx) % cols
		y += dy
	}

	return count
}

func run(s string) interface{} {
	// Your code goes here
	theMap := strings.Split(s, "\n")

	return count(theMap, 1, 1) * count(theMap, 3, 1) * count(theMap, 5, 1) * count(theMap, 7, 1) * count(theMap, 1, 2)
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
