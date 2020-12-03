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
	multiplyTrees := 1
	rights := [5]int{1, 3, 5, 7, 1}
	downs := [5]int{1, 1, 1, 1, 2}
	for i := 0; i < 5; i++ {
		multiplyTrees *= countTrees(strings.Split(s, "\n"), downs[i], rights[i])
	}
	return multiplyTrees
}

func countTrees(lines []string, down int, right int) int {
	i, j := 0, 0
	trees := 0
	mapLines, mapColumns := len(lines), len(lines[0])
	for {
		i += down
		if i >= mapLines {
			break
		}
		j += right
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
