package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strconv"
	"strings"
	"time"
)

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func run(s string) interface{} {
	currentDir := 3 // Clock directions, 1 to 12 -> 0 to 11
	currentX := 0
	currentY := 0

	for _, instr := range strings.Split(s, "\n") {
		action := instr[0]
		value, _ := strconv.Atoi(instr[1:])
		switch action {
		case 'N':
			currentY -= value
		case 'S':
			currentY += value
		case 'E':
			currentX += value
		case 'W':
			currentX -= value
		case 'L':
			currentDir += 12 - (3 * (value / 90)) // -3 % 12 = -3 in Go, here we want 9 so we first add 12
			currentDir %= 12
		case 'R':
			currentDir += (3 * (value / 90))
			currentDir %= 12
		case 'F':
			switch currentDir {
			case 0:
				currentY -= value
			case 3:
				currentX += value
			case 6:
				currentY += value
			case 9:
				currentX -= value
			}
		}
	}

	return abs(currentX) + abs(currentY)
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
