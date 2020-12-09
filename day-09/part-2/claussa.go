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
	start, end := findSet(invalid, &numbers)
	return sumMaxAndMin(&numbers, start, end)
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

func findSet(invalid int, numbers *[]int) (int, int) {
	start, end := 0, 1
	sum := (*numbers)[start] + (*numbers)[end]
	for {
		if sum == invalid {
			return start, end
		}
		if sum < invalid {
			end += 1
			sum += (*numbers)[end]
		}
		if sum > invalid {
			sum -= (*numbers)[start]
			start += 1
		}
	}
}

func sumMaxAndMin(numbers *[]int, start int, end int) int {
	min, max := (*numbers)[start], (*numbers)[start]
	for _, v := range (*numbers)[start+1:end+1] {
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}
	return min + max
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
