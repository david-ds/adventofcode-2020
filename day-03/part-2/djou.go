package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(s string) interface{} {
	counter1 := 0
	counter2 := 0
	counter3 := 0
	counter4 := 0
	counter5 := 0
	j1 := 1
	j2 := 3
	j3 := 5
	j4 := 7
	j5 := 1
	for i := 1; i < 323; i++ {
		if s[i * 32 + j1] == '#' {
			counter1 += 1
		}
		if s[i * 32 + j2] == '#' {
			counter2 += 1
		}
		if s[i * 32 + j3] == '#' {
			counter3 += 1
		}
		if s[i * 32 + j4] == '#' {
			counter4 += 1
		}
		if (i % 2) == 0 {
			if s[i * 32 + j5] == '#' {
				counter5 += 1
			}
			j5 = (j5 + 1) % 31
		}

		j1 = (j1 + 1) % 31
		j2 = (j2 + 3) % 31
		j3 = (j3 + 5) % 31
		j4 = (j4 + 7) % 31
	}
	return counter1 * counter2 * counter3 * counter4 * counter5
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
