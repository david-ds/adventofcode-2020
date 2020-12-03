package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strings"
	"time"
)

func parseData(input string) [][]bool {
    var result [][]bool
    for _, line := range strings.Split(input, "\n") {
        symbols := make([]bool, len(line))
        for idx, letter := range line {
            symbols[idx] = (letter == '#')
        }
        result = append(result, symbols)
    }
    /*
    for _, line := range result {
        for _, cell := range line {
            if cell {
                fmt.Print("#")
            } else {
                fmt.Print(".")
            }
        }
        fmt.Print("\n")
    }
    */
    return result
}

func puzzleTest(input [][]bool, height int, width int, right int, down int) int {
    var currentHeight, currentRight int
    var treeCount int
    for currentHeight <= height {
        currentHeight += down
        currentRight = (currentRight + right) % width

        if currentHeight < height && input[currentHeight][currentRight] {
            treeCount += 1
        }
    }
    return treeCount

}


func puzzle(input [][]bool) int {
    height := len(input)
    width := len(input[0])

    fmt.Printf("Height : %d, width : %d\n", height, width)
    t1 := puzzleTest(input, height, width, 1, 1)
    t2 := puzzleTest(input, height, width, 3, 1)
    t3 := puzzleTest(input, height, width, 5, 1)
    t4 := puzzleTest(input, height, width, 7, 1)
    t5 := puzzleTest(input, height, width, 1, 2)

    return t1 * t2 * t3 * t4 * t5
}

func run(s string) interface{} {
	// Your code goes here
    grid := parseData(s)
    return puzzle(grid)
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
