package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(s string) interface{} {
	counter := 0
	j := 3
	for i := 1; i < 323; i++ {
		if s[i * 32 + j] == '#' {
			counter += 1
		}
		j = (j + 3) % 31
	}

	return counter
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
