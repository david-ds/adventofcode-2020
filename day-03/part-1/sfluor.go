package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	theMap := strings.Split(s, "\n")

	rows := len(theMap)
	cols := len(theMap[0])

	x := 0
	y := 0

	count := 0
	for y < rows {
		if theMap[y][x] == '#' {
			count += 1
		}

		x = (x + 3) % cols
		y += 1
	}

	return count
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
