package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	groups := strings.Split(s, "\n\n")
	count := 0
	for _, group := range groups {
		answerCounts := make([]int, 26)
		for _, c := range group {
			if c == '\n' {
				continue
			}
			answerCounts[c - 97] = 1
		}
		for _, val := range answerCounts {
			count += val
		}
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
