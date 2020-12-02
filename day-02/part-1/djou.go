package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) int {
	passwords := strings.Split(s, "\n")
	valid := 0
	for _, input := range passwords {
		parts := strings.Split(input, " ")
		boundaries := strings.Split(parts[0], "-")
		low, _ := strconv.Atoi(boundaries[0])
		high, _ := strconv.Atoi(boundaries[1])
		refChar := string(parts[1][0])

		count := 0
		for _, char := range parts[2] {
			if string(char) == refChar {
				count += 1
			}
		}

		if count >= low && count <= high {
			valid += 1
		}
	}

	return valid
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
