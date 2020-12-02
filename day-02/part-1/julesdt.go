package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	total := 0
	for _, line := range strings.Split(s, "\n") {
		policySplit := strings.Split(line, ": ")
		password := policySplit[1]

		numbersSplit := strings.Split(policySplit[0], " ")
		letter := numbersSplit[1]

		numbers := strings.Split(numbersSplit[0], "-")
		low, _ := strconv.Atoi(numbers[0])
		high, _ := strconv.Atoi(numbers[1])

		count := strings.Count(password, letter)
		if count >= low && count <= high {
			total++
		}
	}
	return total
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
