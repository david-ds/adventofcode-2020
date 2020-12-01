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

	numbers := make([]int, len(lines))
	for i, raw := range lines {
		numbers[i], _ = strconv.Atoi(raw)
	}

	for _, n1 := range numbers {
		for _, n2 := range numbers {
			if n1+n2 == 2020 {
				return n1 * n2
			}
		}
	}

	return "deso"
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
