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
		answerMap := map[rune]int{}
		grpSize := 1
		for _, c := range group {
			if c == '\n' {
				grpSize += 1
				continue
			}
			answerMap[c] += 1
		}
		for _, val := range answerMap {
			if val == grpSize {
				count += 1
			}
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
