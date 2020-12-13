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
	lines := strings.Split(s, "\n")
	earliest, _ := strconv.Atoi(lines[0])

	bestBusID := 0
	bestWaitTime := earliest

	for _, id := range strings.Split(lines[1], ",") {
		if id == "x" {
			continue
		}

		bus, _ := strconv.Atoi(id)
		earliestDeparture := -earliest + (int(earliest/bus)+1)*bus
		if earliestDeparture < bestWaitTime {
			bestWaitTime = earliestDeparture
			bestBusID = bus
		}
	}

	return bestWaitTime * bestBusID
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
