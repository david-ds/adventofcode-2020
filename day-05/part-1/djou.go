package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	correspondances := map[rune]int{
		'F': 0,
		'B': 1,
		'L': 0,
		'R': 1,
	}

	ids := strings.Split(s, "\n")
	max := 0
	for _, id := range ids {
		curr := 0
		for i, c := range id {
			curr += correspondances[c] * int(math.Pow(2, float64(9-i)))
		}

		if curr > max {
			max = curr
		}
	}

	return max
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
