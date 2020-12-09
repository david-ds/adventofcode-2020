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
	invalid := 0
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
			invalid = value
			break
		}
		numbers[i] = value
		i += 1
	}
	return findSet(invalid, i, &numbers)
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

func findSet(invalid int, indexOfInvalid int, numbers *[]int) int {
	var sum int
	var min, max int
	for index, v1 := range (*numbers)[0:indexOfInvalid] {
		sum = v1
		min, max = v1, v1
		for i := index+1; i < indexOfInvalid; i++ {
			number := (*numbers)[i]
			sum += number
			if number > max {
				max = number
			}
			if number < min {
				min = number
			}
			if sum == invalid {
				return min + max
			}
			if sum > invalid {
				break
			}
		}
	}
	return -1
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
