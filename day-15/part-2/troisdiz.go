package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	lines := strings.Split(s, "\n")
	nbStrs := strings.Split(lines[0], ",")

	prevPositions := make(map[int]int)
	lastNb := 0
	for idx, nbStr := range nbStrs {
		nb, _ := strconv.Atoi(nbStr)
		if idx != len(nbStrs)-1 {
			prevPositions[nb] = idx
		}
		lastNb = nb
		// fmt.Printf("Pos(%d) = %d\n", idx, lastNb)
	}
	for i := len(nbStrs); i < 30000000; i++ {
		prevPos, seen := prevPositions[lastNb]
		prevPositions[lastNb] = i -1
		if seen {
			lastNb = i - prevPos -1
		} else {
			lastNb = 0
		}
		// fmt.Printf("At %d : prevPos : %v => lastNb = %d\n", i, prevPos, lastNb)
		// fmt.Printf("Pos(%d) = %d\n", i, lastNb)
	}
	return lastNb
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
