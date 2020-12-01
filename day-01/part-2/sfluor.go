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
	hashmap := make([]int, 2021)
	for i, raw := range lines {
		numbers[i], _ = strconv.Atoi(raw)
		hashmap[numbers[i]] = 1
	}

	for _, n1 := range numbers {
		for _, n2 := range numbers {
			rem := 2020 - n1 - n2
			if rem > 0 && hashmap[rem] == 1 {
				return n1 * n2 * rem
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
