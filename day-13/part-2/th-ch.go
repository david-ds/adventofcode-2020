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
	// Parsing
	lines := strings.Split(s, "\n")
	busLines := strings.Split(lines[1], ",")
	busWithOffset := make([][2]int, 0, len(busLines))

	for offset, id := range busLines {
		if id == "x" {
			continue
		}

		bus, _ := strconv.Atoi(id)
		busWithOffset = append(busWithOffset, [2]int{bus, offset})
	}

	// Processing
	step := 1
	t := 0
	currentBus := 0
	for {
		t += step
		for (t+busWithOffset[currentBus][1])%busWithOffset[currentBus][0] == 0 {
			step *= busWithOffset[currentBus][0]
			currentBus++
			if currentBus >= len(busWithOffset) {
				return t
			}
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
