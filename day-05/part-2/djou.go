package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"sort"
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
	seats := make([]int, 2048)
	for i, id := range ids {
		curr := 0
		for j, c := range id {
			curr += correspondances[c] * int(math.Pow(2, float64(9-j)))
		}
		seats[i] = curr
	}

	sort.Ints(seats)

	for i := 0; i < len(seats) - 1; i++ {
		if seats[i + 1] - seats[i] == 2 {
			return seats[i] + 1
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
