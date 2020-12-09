package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const RANGE = 25


func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	numbers := make([]int, len(lines))
	i := 0
	for {
		value, _ := strconv.Atoi(lines[i])
		numbers[i] = value
		i += 1
		if i == RANGE {
			break
		}
	}

	for {
		value, _ := strconv.Atoi(lines[i])
		if !isSumOfPrevious(value, &numbers, i) {
			return value
		}
		numbers[i] = value
		i += 1
	}
}

func isSumOfPrevious(value int, numbers *[]int, i int) bool {
	for index, v1 := range (*numbers)[i-RANGE:i] {
		for _, v2 := range (*numbers)[i-RANGE+index+1:i] {
			if v1 + v2 == value {
				return true
			}
		}
	}
	return false
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
