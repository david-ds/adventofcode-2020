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
	lines := strings.Split(s, "\n")
	inputs := make([]int, len(lines))
	i := 0
	for {
		inputs[i], _ = strconv.Atoi(lines[i])
		for j := 0; j < i; j++ {
			if inputs[i] + inputs[j] == 2020 {
				return inputs[i] * inputs[j]
			}
		}
		i++
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
