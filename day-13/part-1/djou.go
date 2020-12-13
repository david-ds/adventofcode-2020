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
	input := strings.Split(s, "\n")
	timestamp, _ := strconv.Atoi(input[0])
	var shortest int
	var id int
	for _, busIdStr := range strings.Split(input[1], ",") {
		if busIdStr == "x" {
			continue
		}
		busId, _ := strconv.Atoi(busIdStr)
		currentWaiting := busId - (timestamp % busId)
		if shortest == 0 && id == 0 {
			shortest = currentWaiting
			id = busId
		} else if shortest > currentWaiting {
			shortest = currentWaiting
			id = busId
		}
	}

	return shortest * id
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
