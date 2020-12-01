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
	numbersSet := make(map[int]int, len(lines))

	for i, raw := range lines {
		number, _ := strconv.Atoi(raw)
		numbers[i] = number
		numbersSet[number] = 1
	}

	for _, n1 := range numbers {
		for _, n2 := range numbers {
			diff := 2020 - n1 - n2
			if numbersSet[diff] == 1 {
				return n1 * n2 * diff
			}
		}
	}
	return 0
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
