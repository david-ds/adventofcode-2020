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
	sequence := make([]int, 2048)
	memory := make(map[int]int)
	var fault int
	var lastIndex int
	for i, n := range strings.Split(s, "\n") {
		sequence[i], _ = strconv.Atoi(n)
	}

	for i := 0; i < RANGE; i++ {
		for j := i+1; j < RANGE; j++ {
			memory[sequence[i] + sequence[j]] = i
		}
	}

	for i, val := range sequence[RANGE:] {
		index := i + RANGE
		if memory[val] < index - RANGE {
			fault = val
			lastIndex = val
			break
		}
		addLastNumber(memory, &sequence, index)
	}

	for i := 0; i < lastIndex; i++ {
		sum := sequence[i]
		max := sequence[i]
		min := sequence[i]
		for j := i + 1; j < lastIndex; j++ {
			sum += sequence[j]
			if sum > fault {
				break
			}

			if sequence[j] < min {
				min = sequence[j]
			} else if sequence[j] > max {
				max = sequence[j]
			}

			if sum == fault {
				return max + min
			}
		}
	}

	return 0
}

func addLastNumber(memory map[int]int, sequence *[]int, index int) {
	for i := index - RANGE + 1; i < index; i++ {
		sum := (*sequence)[i] + (*sequence)[index]
		if val, ok := memory[sum]; ok {
			if i > val {
				memory[sum] = i
			}
		} else {
			memory[sum] = i
		}
	}
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
