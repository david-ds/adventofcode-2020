package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	map_ := strings.Split(s, "\n")
	h := len(map_)
	w := len(map_[0])
	right := 3
	down := 1

	x := 0
	y := 0
	counter := 0
	for y < h {
		if map_[y][x] == '#' {
			counter += 1
		}
		x = (x + right) % w
		y = y + down
	}
	return counter
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
