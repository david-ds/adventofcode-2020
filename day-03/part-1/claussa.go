package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	lines := strings.Split(s, "\n")
	mapLines, mapColumns := len(lines), len(lines[0])
	i, j := 0, 0
	trees := 0
	for {
		i += 1
		if i == mapLines {
			break
		}
		j += 3
		if j >= mapColumns {
			j = j - mapColumns
		}
		if lines[i][j] == '#' {
			trees++
		}
	}
	return trees
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
