package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func encountered(s string, n int, down, right int) int {
	j := 0
	i := 0
	index := 0
	res := 0
	for index < len(s) {
		if s[index] == '#' {
			res++
		}
		i += down
		j = (j+right)%n
		index = i*(n+1) + j
	}
	return res
}

func run(s string) interface{} {
	var lineSize int
	for lineSize = 0; ; lineSize++ {
		if s[lineSize] == uint8('\n') {
			break
		}
	}

	return encountered(s, lineSize, 1, 1) *
		encountered(s, lineSize, 1, 3) *
		encountered(s, lineSize, 1, 5) *
		encountered(s, lineSize, 1, 7) *
		encountered(s, lineSize, 2, 1)
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
